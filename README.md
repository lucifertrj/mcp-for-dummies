# mcp-for-dummies

PyCon AU - MCP for Dummies

Providing the right context to large language models is challenging. Every integration—whether accessing local files, connecting to Google Calendar, or querying internal databases—requires custom work. Each tool connection becomes a separate, manual effort. This is where MCP comes in. Model Context Protocol (MCP), in simple terms, is a universal adapter for AI models that need external context. It standardizes how context is passed to models, making it easier to build and manage these connections.

Talk: [MCP for dummies - Tarun Jain](https://2025.pycon.org.au/program/D8DNXQ/)

## Quick Setup

### System Requirements

- Mac or Windows computer
- Latest Python version installed
- The latest version of [uv](https://docs.astral.sh/uv/getting-started/installation/) installed

1. **Install uv** (if not already installed):
   ```bash
   # On macOS and Linux
   curl -LsSf https://astral.sh/uv/install.sh | sh

   # On Windows
   powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"
   ```

2. **Create secrets configuration**:
   ```bash
   cp .streamlit/secrets.toml.example .streamlit/secrets.toml
   ```
   Then edit `.streamlit/secrets.toml` with your API keys and configuration.

3. API Keys and Configuration:
   - Qdrant URL and API Key: Create a free cluster on the [Qdrant Cloud](https://cloud.qdrant.io/) and get the URL and API key from the dashboard.
   - Google API Key: Get your Gemini API key from the [Google AI Studio](https://aistudio.google.com/).

4. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

5. **Run the application**:
   ```bash
   streamlit run app.py
   ```

The application will open in your browser at `http://localhost:8501`.
