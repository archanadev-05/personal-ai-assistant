# Personal AI Assistant

A multi-agent personal AI assistant that routes user queries to specialized agents — **news summarization**, **scam/fraud detection**, and **general Q&A** — built with LangGraph, LangChain, and OpenAI, with a Gradio chat UI and an input guardrail layer for basic content safety.

## How it works

1. **Input Guardrail** — every message first passes through a keyword-based guardrail node. If it matches a blocked term, the graph short-circuits and returns a rejection reason without calling the LLM.
2. **Router Agent** — an LLM call classifies the query into `news`, `scam`, or `general`.
3. **Specialized Agents**:
   - **News Agent** — a tool-using agent (via `langchain.agents.create_agent`) that calls Tavily web search and summarizes results neutrally.
   - **Scam Detection Agent** — analyzes a message and returns a risk level (LOW/MEDIUM/HIGH).
   - **General Agent** — handles everyday Q&A, coding help, writing, and brainstorming.
4. The whole flow is orchestrated as a **LangGraph** state graph with conditional edges, and exposed through a **Gradio** textbox interface.

```
User Input
    │
    ▼
Input Guardrail ──(blocked)──► End (return reason)
    │ (allowed)
    ▼
Router Agent
    │
    ├── news  ──► News Agent (Tavily search) ──► End
    ├── scam  ──► Scam Detection Agent        ──► End
    └── general ─► General Agent               ──► End
```

## Tech Stack

| Category | Technology |
|---|---|
| Orchestration | [LangGraph](https://github.com/langchain-ai/langgraph) |
| LLM Framework | [LangChain](https://github.com/langchain-ai/langchain) |
| LLM Provider | OpenAI (via `langchain-openai`) |
| Web Search Tool | [Tavily](https://tavily.com/) (via `langchain-tavily`) |
| UI | [Gradio](https://www.gradio.app/) |
| Observability (optional) | [LangSmith](https://smith.langchain.com/) |
| Config | `python-dotenv` |
| Language | Python 3.10+ |

## Project Structure

```
.
├── agents.py          # Router, news, scam, and general agent implementations
├── system_prompts.py  # System prompts for each agent
├── guardrails.py       # Input guardrail node (blocked keyword filter)
├── graph.py            # LangGraph StateGraph wiring all nodes/edges together
├── app.py              # CLI entry point
├── ui.py                # Gradio web UI entry point
├── requirements.txt
├── .env.example
└── .gitignore
```

## Setup

1. Clone the repo and install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
2. Copy `.env.example` to `.env` and fill in your API keys:
   ```bash
   cp .env.example .env
   ```
3. Run the CLI version:
   ```bash
   python app.py
   ```
   Or launch the Gradio web UI:
   ```bash
   python ui.py
   ```

## Notes / Known Limitations

- The guardrail is a simple keyword filter, not a robust safety system — it's meant as a first line of defense, not a complete solution.
- The router agent returns free-form text from the LLM (e.g. `"news"`); for stricter reliability, consider constraining it with structured output.
- Update the model name in `agents.py` to a valid OpenAI model available to your account.

## License

MIT
