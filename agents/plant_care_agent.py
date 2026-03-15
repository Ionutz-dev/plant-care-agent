from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain.agents import create_tool_calling_agent, AgentExecutor
from config import config
from schemas import PlantCareCard
from agents.tools import query_plant_care_database, search_plant_info
from prompts import PLANT_CARE_AGENT_PROMPT, PLANT_CARE_USER_INPUT, PLANT_CARE_STRUCTURED_OUTPUT


def create_plant_care_agent():
    """Create a Langchain agent for generating plant care cards."""

    # Initialize LLM
    llm = ChatOpenAI(
        model=config.LLM_MODEL,
        temperature=config.LLM_TEMPERATURE,
        api_key=config.OPENAI_API_KEY
    )

    # Create prompt template using prompt from plant_care_prompts.py
    prompt = ChatPromptTemplate.from_messages([
        ("system", PLANT_CARE_AGENT_PROMPT),
        ("human", "{input}"),
        ("placeholder", "{agent_scratchpad}")
    ])

    # Tools - RAG first, then web search
    tools = [query_plant_care_database, search_plant_info]

    # Create agent
    agent = create_tool_calling_agent(llm, tools, prompt)
    agent_executor = AgentExecutor(agent=agent, tools=tools, verbose=True)

    return agent_executor


def generate_care_card(plant_name: str) -> dict:
    """
    Generate a plant care card for the given plant name.

    Args:
        plant_name: Name of the plant

    Returns:
        dict: Plant care information as dictionary
    """
    # Create agent executor
    agent = create_plant_care_agent()

    # Get structured output from LLM
    llm = ChatOpenAI(
        model=config.LLM_MODEL,
        temperature=config.LLM_TEMPERATURE,
        api_key=config.OPENAI_API_KEY
    )

    structured_llm = llm.with_structured_output(PlantCareCard)

    # Run agent to gather information using prompt template
    print(f"Agent gathering information for {plant_name}...")
    agent_response = agent.invoke({
        "plant_name": plant_name,
        "input": PLANT_CARE_USER_INPUT.format(plant_name=plant_name)
    })

    # Generate structured output using prompt template
    print("Generating structured care card...")
    care_card = structured_llm.invoke(
        PLANT_CARE_STRUCTURED_OUTPUT.format(
            agent_output=agent_response['output'],
            plant_name=plant_name
        )
    )

    return care_card.model_dump()