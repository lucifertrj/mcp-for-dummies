import os
import asyncio
import streamlit as st
from agno.agent import Agent
from agno.models.google import Gemini
from agno.tools.mcp import MCPTools
from constants import INSTRUCTIONS

st.set_page_config(page_title="MCP Agent Interface", layout="wide")
st.title("MCP Agent Interface")

QDRANT_URL = st.secrets['QDRANT_URL']
QDRANT_API_KEY = st.secrets['QDRANT_API_KEY']
COLLECTION_NAME = "vibe-code"
EMBEDDING_MODEL = "sentence-transformers/all-MiniLM-L6-v2"
os.environ['GOOGLE_API_KEY'] = st.secrets['GOOGLE_API_KEY']

async def run_agent(message: str):
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
            instructions=INSTRUCTIONS,
            markdown=True,
        )

        response = await mcp_agent.arun(message, stream=False)
        return response

def format_metrics(metrics):
    return {
        "Input Tokens": metrics.input_tokens,
        "Output Tokens": metrics.output_tokens,
        "Total Tokens": metrics.total_tokens,
        "Duration": f"{metrics.duration:.2f}s" if metrics.duration else "N/A"
    }

with st.sidebar:
    st.header("Tool Call Details")
    
    if 'response_data' in st.session_state and st.session_state.response_data:
        response = st.session_state.response_data
        
        with st.expander("Tool Usage"):
            if response.tools:
                for tool in response.tools:
                    st.write(f"**Tool:** {tool.tool_name}")
                    st.write(f"**Success:** {not tool.tool_call_error}")
                    st.write(f"**Duration:** {tool.metrics.duration:.2f}s" if tool.metrics.duration else "N/A")
                    st.write(f"**Result:** {tool.result}")
                    st.divider()
        
        with st.expander("Metrics"):
            metrics_data = format_metrics(response.metrics)
            for key, value in metrics_data.items():
                st.metric(key, value)
        
        with st.expander("Agent"):
            st.write(f"**Model:** {response.model}")
            st.write(f"**Status:** {response.status}")
    else:
        st.info("Execute a query to see tool call details")

user_input = st.text_area("Enter your message:", height=100)

col1, col2, col3 = st.columns([1, 1, 1])
with col2:
    if st.button("Execute Query", type="primary", use_container_width=True):
        if user_input.strip():
            with st.spinner("Processing your request..."):
                try:
                    response = asyncio.run(run_agent(user_input))
                    st.session_state.response_data = response
                    st.rerun()
                except Exception as e:
                    st.error(f"Error: {str(e)}")
        else:
            st.warning("Please enter a message")

if 'response_data' in st.session_state and st.session_state.response_data:
    st.header("Agent Response")
    response = st.session_state.response_data
    st.markdown(response.content)