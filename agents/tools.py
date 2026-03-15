from langchain.tools import tool
from tavily import TavilyClient
from config import config
from langchain_openai import OpenAIEmbeddings
from langchain_community.vectorstores import LanceDB
import lancedb


class PlantCareVectorStore:
    """Singleton class to manage vector store connection."""

    _instance = None
    _vectorstore = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def get_vectorstore(self, db_path="./lancedb"):
        """Get or create vector store connection."""
        if self._vectorstore is None:
            try:
                embeddings = OpenAIEmbeddings(api_key=config.OPENAI_API_KEY)
                db = lancedb.connect(db_path)

                self._vectorstore = LanceDB(
                    connection=db,
                    embedding=embeddings,
                    table_name="plant_care_guides"
                )
                print("Vector store loaded")
            except Exception as e:
                print(f"Vector store not available: {e}")
                self._vectorstore = None

        return self._vectorstore


# Global instance
vector_store_manager = PlantCareVectorStore()


@tool
def query_plant_care_database(plant_name: str) -> str:
    """
    Query the vector database for plant care information.
    Use this first before web search for plants in the database.

    Args:
        plant_name: Name of the plant to get care information for

    Returns:
        str: Relevant care information from the database
    """
    try:
        vectorstore = vector_store_manager.get_vectorstore()

        if vectorstore is None:
            return "Vector database not available. Use web search instead."

        query = f"How to grow and care for {plant_name}? What are the watering, soil, light, temperature, and fertilizer requirements?"

        plant_filter = plant_name.lower().replace(" ", "")

        # Search with metadata filter
        results = vectorstore.similarity_search(
            query,
            k=4,
            filter=f"metadata.plant_name = '{plant_filter}'"
        )

        if not results:
            # Try without filter if no exact match
            results = vectorstore.similarity_search(query, k=4)

        if results:
            # Combine results
            combined_info = "\n\n---\n\n".join([doc.page_content for doc in results])
            sources = list(set([doc.metadata.get("source_url", "Unknown") for doc in results]))

            return f"Care information for {plant_name} from database:\n\n{combined_info}\n\nSources: {', '.join(sources)}"
        else:
            return f"No information found in database for {plant_name}. Try web search."

    except Exception as e:
        return f"Error querying database: {str(e)}. Try web search instead."


@tool
def search_plant_info(query: str) -> str:
    """Search the web for plant care information.

    Args:
        query: Search query about plant care, growing conditions, or problems

    Returns:
        str: Relevant information from web search
    """
    if not config.TAVILY_API_KEY:
        return "Web search not available - Tavily API key not configured"

    try:
        client = TavilyClient(api_key=config.TAVILY_API_KEY)
        response = client.search(query, max_results=3)

        results = []
        for result in response.get('results', []):
            source = result.get('url', 'Unknown source')
            content = result.get('content', '')
            results.append(f"Source: {source}\n{content}\n")

        return "\n".join(results) if results else "No relevant information found"

    except Exception as e:
        return f"Search error: {str(e)}"