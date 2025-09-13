import os
import asyncio
from agno.agent import Agent
from agno.models.google import Gemini
from agno.tools.mcp import MCPTools

QDRANT_URL = ""
QDRANT_API_KEY = ""
COLLECTION_NAME = "vibe-code"
EMBEDDING_MODEL = "sentence-transformers/all-MiniLM-L6-v2"
os.environ['GOOGLE_API_KEY'] = ""

async def run_agent(message: str) -> None:
    async with MCPTools(
        "uvx mcp-server-qdrant",
        env={
            "QDRANT_URL": QDRANT_URL,
            "QDRANT_API_KEY": QDRANT_API_KEY,
            "COLLECTION_NAME": COLLECTION_NAME,
            "EMBEDDING_MODEL": EMBEDDING_MODEL,
        },
        timeout_seconds=50,
    ) as mcp_tools:

        mcp_agent = Agent(
            name="MCP Agent",
            model=Gemini(id="gemini-2.5-pro"),
            tools=[mcp_tools],
            instructions="""
            You are the storage agent for the Model Context Protocol (MCP) server.
            You need to save the information in the vector database or retrieve the information to answer the user's questions.
            You can use the following tools:
            - qdrant-store: Store data/output in the Qdrant vector database.
            - qdrant-find: Retrieve data/output from the Qdrant vector database.
            """,
            markdown=True,
        )

        response = await mcp_agent.arun(message, stream=False)
        return response #response.content

if __name__ == "__main__":
    query = """
    write a poem on PyCon AU and save in DB
    """
    print(asyncio.run(run_agent(query)))