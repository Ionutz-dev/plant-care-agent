import sys
import os

# Add project root to path
script_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.dirname(script_dir)
sys.path.insert(0, project_root)

from langchain_community.document_loaders import WebBaseLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_openai import OpenAIEmbeddings
from langchain_community.vectorstores import LanceDB
import lancedb
from config import config

# Care guide URLs for selected plants
CARE_GUIDE_URLS = {
    "aloevera": [
        "https://www.almanac.com/plant/aloe-vera",
        "https://www.gardeningknowhow.com/houseplants/aloe-vera/aloe-vera-plant-care.htm"
    ],
    "banana": [
        "https://www.gardeningknowhow.com/edible/fruits/banana/growing-banana-trees.htm",
        "https://www.epicgardening.com/grow-bananas/"
    ],
    "mango": [
        "https://www.gardeningknowhow.com/edible/fruits/mango/mango-tree-care.htm",
        "https://www.epicgardening.com/how-to-grow-mango/"
    ],
    "cucumber": [
        "https://www.almanac.com/plant/cucumbers",
        "https://www.gardeningknowhow.com/edible/vegetables/cucumber/growing-cucumbers.htm"
    ],
    "ginger": [
        "https://www.gardeningknowhow.com/edible/herbs/ginger/growing-ginger-root.htm",
        "https://www.epicgardening.com/how-to-grow-ginger/"
    ],
    "spinach": [
        "https://www.almanac.com/plant/spinach",
        "https://www.gardeningknowhow.com/edible/vegetables/spinach/growing-spinach.htm"
    ],
    "watermelon": [
        "https://www.almanac.com/plant/watermelons",
        "https://www.gardeningknowhow.com/edible/fruits/watermelon/watermelon-care.htm"
    ]
}


def load_documents_from_urls(plant_urls_dict):
    """Load and process documents from URLs."""
    all_documents = []

    for plant_name, urls in plant_urls_dict.items():
        print(f"Loading documents for {plant_name}...")

        for url in urls:
            try:
                loader = WebBaseLoader(url)
                docs = loader.load()

                # Add metadata
                for doc in docs:
                    doc.metadata["plant_name"] = plant_name
                    doc.metadata["source_url"] = url

                all_documents.extend(docs)
                print(f"Loaded {url}")

            except Exception as e:
                print(f"Failed to load {url}: {e}")

    return all_documents


def split_documents(documents):
    """Split documents into chunks."""
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000,
        chunk_overlap=200,
        length_function=len,
    )

    splits = text_splitter.split_documents(documents)
    print(f"\nCreated {len(splits)} document chunks")

    return splits


def build_vector_store(documents, db_path="./lancedb"):
    """Build and save vector store."""
    print("\nBuilding vector store...")

    # Initialize embeddings
    embeddings = OpenAIEmbeddings(api_key=config.OPENAI_API_KEY)

    # Connect to LanceDB
    db = lancedb.connect(db_path)

    # Create vector store
    vectorstore = LanceDB.from_documents(
        documents=documents,
        embedding=embeddings,
        connection=db,
        table_name="plant_care_guides"
    )

    print(f"Vector store created at {db_path}")
    return vectorstore


def main():
    """Main function to build the vector store."""
    print("=" * 70)
    print("Building Plant Care Vector Store")
    print("=" * 70)

    # Load documents
    documents = load_documents_from_urls(CARE_GUIDE_URLS)
    print(f"\nTotal documents loaded: {len(documents)}")

    # Split documents
    splits = split_documents(documents)

    # Build vector store
    vectorstore = build_vector_store(splits)

    print("\n" + "=" * 70)
    print("Vector store built successfully!")
    print("=" * 70)

    # Test query
    print("\nTesting vector store with sample query...")
    results = vectorstore.similarity_search("How to water aloe vera?", k=2)
    print(f"Found {len(results)} relevant documents")
    if results:
        print(f"Top result plant: {results[0].metadata.get('plant_name')}")

    return vectorstore


if __name__ == "__main__":
    main()