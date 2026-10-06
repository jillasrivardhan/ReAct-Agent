# ReAct Agent

A modular, extensible implementation of the **ReAct (Reasoning and Acting)** framework in Python. This repository provides an end-to-end setup for building, prompt-engineering, and deploying intelligent AI agents capable of combining step-by-step reasoning with external tool execution.

---

## 📁 Repository Structure

```text
ReAct-Agent-main/
├── Agent/
│   ├── agent.py          # Core agent loop and execution logic
│   ├── ReAct.py          # ReAct reasoning chain implementation
│   ├── prompts.py        # System prompts and ReAct templates
│   └── app.py            # User interface / REST application entrypoint
├── src/
│   └── react_agent/
│       └── __init__.py   # Package initialization
├── .env                  # Environment variables and API keys
├── .gitignore            # Git ignore patterns
├── .python-version       # Python runtime version pin (3.12)
├── pyproject.toml        # Project metadata and dependencies (uv / hatch)
└── requirements.txt      # Python dependencies list
```

---

## 🛠️ Features

* **ReAct Framework Implementation:** Combines dynamic reasoning loops (*Thought*) with actionable tool calls (*Action* / *Observation*).
* **Modular Prompt Management:** Centralized prompt templates in `Agent/prompts.py` for structured output and robust multi-step reasoning.
* **Interactive Application:** Interface/API server in `Agent/app.py` for real-time interactions with the agent.
* **Modern Packaging:** Python 3.12 support configured via `pyproject.toml` and standard package management tools.

---

## 🚀 Getting Started

### Prerequisites

* Python **3.12** or higher
* `pip` or standard package managers like `uv`

### Installation

1. **Clone the repository:**
   ```bash
   git clone https://github.com/your-username/ReAct-Agent.git
   cd ReAct-Agent-main
   ```

2. **Create and activate a virtual environment:**
   ```bash
   python -m venv .venv
   source .venv/bin/activate  # On Windows: .venv\Scripts\activate
   ```

3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```
   *Alternatively, if using editable package mode:*
   ```bash
   pip install -e .
   ```

4. **Set up Environment Variables:**
   Create or edit the `.env` file in the project root to include your API credentials:
   ```env
   OPENAI_API_KEY=your_openai_api_key_here
   ```

---

## 💡 Usage

### Running the Agent Application
To launch the interactive agent interface or backend application:

```bash
python Agent/app.py
```

### Programmatic Usage
You can import and initialize the ReAct agent within your custom scripts:

```python
from Agent.agent import Agent
from Agent.ReAct import ReActEngine

# Initialize the agent
agent = Agent()

# Run a task requiring reasoning and action
response = agent.run("Calculate the total revenue from the quarterly data and summarize the top product line.")
print(response)
```

---

## 🤝 Contributing

Contributions are welcome! Please follow these steps:
1. Fork the repository.
2. Create a feature branch (`git checkout -b feature/NewFeature`).
3. Commit your changes (`git commit -m 'Add new feature'`).
4. Push to the branch (`git push origin feature/NewFeature`).
5. Open a Pull Request.

---

## 📜 License

This project is open-source under the terms of the MIT License.