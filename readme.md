# 🤖 ReAct Agent

> A modular implementation of the **ReAct (Reasoning + Acting)** framework that enables an AI agent to reason about a task, decide when external tools are required, execute those tools, observe their results, and continue until the task is completed.

[![Python](https://img.shields.io/badge/Python-3.12+-3776AB?logo=python&logoColor=white)](https://www.python.org/)
[![LangChain](https://img.shields.io/badge/LangChain-Framework-1C3C3C)](https://www.langchain.com/)
[![ReAct](https://img.shields.io/badge/Architecture-ReAct-purple)](https://arxiv.org/abs/2210.03629)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](#license)

---

## 📌 Overview

This project demonstrates how to build an AI agent using the **ReAct (Reasoning and Acting)** pattern.

Instead of simply generating a response, the agent follows an iterative workflow:

```text
User Request
     ↓
   Reason
     ↓
 Decide Action
     ↓
  Call Tool
     ↓
 Observe Result
     ↓
   Reason Again
     ↓
 Final Answer
```

This allows the agent to dynamically decide when it needs external information instead of relying entirely on the knowledge contained within the language model.

The project is designed to be **modular and extensible**, making it easier to add new tools, modify prompts, and experiment with different agent behaviors.

---

# 🧠 What is ReAct?

ReAct stands for:

**Reasoning + Acting**

A traditional LLM application generally follows:

```text
User → LLM → Response
```

A ReAct agent follows a more dynamic process:

```text
User
 ↓
LLM reasoning
 ↓
Should I use a tool?
 ↓
Tool execution
 ↓
Tool result
 ↓
LLM reasoning
 ↓
Another action?
 ↓
Final response
```

The key idea is that the model can combine reasoning with actions instead of generating the answer in a single step.

---

# ✨ Features

- 🧠 ReAct-style reasoning and action workflow
- 🔧 External tool execution
- 🔄 Iterative agent loop
- 📝 Centralized prompt management
- 🧩 Modular agent architecture
- 🐍 Python 3.12 support
- 📦 Standard Python project structure
- 🔐 Environment-variable based API configuration
- 🚀 Interactive application entry point
- 🔌 Easy to extend with additional tools

---

# 🏗️ Architecture

```text
                    ┌─────────────────┐
                    │      User       │
                    └────────┬────────┘
                             │
                             ▼
                    ┌─────────────────┐
                    │    ReAct Agent  │
                    └────────┬────────┘
                             │
                       Reasoning
                             │
                             ▼
                  ┌─────────────────────┐
                  │ Decide Next Action  │
                  └──────────┬──────────┘
                             │
                    ┌────────┴────────┐
                    │                 │
                  Tool             No Tool
                    │                 │
                    ▼                 ▼
             ┌────────────┐    ┌────────────┐
             │ Tool Call  │    │Final Answer│
             └─────┬──────┘    └────────────┘
                   │
                   ▼
             ┌────────────┐
             │ Observation│
             └─────┬──────┘
                   │
                   └──────────────► Reason Again
```

---

# 📁 Project Structure

```text
ReAct-Agent/
│
├── Agent/
│   ├── agent.py
│   │   └── Core agent execution logic
│   │
│   ├── ReAct.py
│   │   └── ReAct reasoning/action workflow
│   │
│   ├── prompts.py
│   │   └── System prompts and ReAct templates
│   │
│   └── app.py
│       └── Application entry point
│
├── src/
│   └── react_agent/
│       └── __init__.py
│
├── .gitignore
├── .python-version
├── pyproject.toml
├── requirements.txt
└── README.md
```

---

# 🛠️ Tech Stack

| Technology | Purpose |
|---|---|
| Python | Core programming language |
| LangChain | LLM/tool integration |
| ReAct | Agent reasoning architecture |
| Python dotenv | Environment configuration |
| PyProject / pip | Dependency management |

The repository is configured for **Python 3.12**.

---

# 🚀 Getting Started

## 1. Clone the repository

```bash
git clone https://github.com/jillasrivardhan/ReAct-Agent.git
cd ReAct-Agent
```

---

## 2. Create a virtual environment

### Windows PowerShell

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

### Git Bash

```bash
python -m venv .venv
source .venv/Scripts/activate
```

---

## 3. Install dependencies

```bash
pip install -r requirements.txt
```

Or, if you want to install the package in editable mode:

```bash
pip install -e .
```

---

# 🔐 Environment Configuration

Create a local `.env` file in the project root.

Example:

```env
OPENAI_API_KEY=your_api_key_here
```

**Never commit your real `.env` file or API key to GitHub.**

Your `.gitignore` should contain:

```gitignore
.env
.venv/
__pycache__/
*.pyc
```

For security, use environment variables for credentials rather than hard-coding secrets inside Python files.

---

# ▶️ Running the Agent

The repository's application entry point is:

```text
Agent/app.py
```

So from the project root:

```bash
python Agent/app.py
```

### Important

Do **not** run:

```bash
streamlit run app.py
```

unless there is actually an `app.py` in the repository root.

The current project structure places the application inside the `Agent` directory.

---

# 💻 Programmatic Usage

The agent components can also be imported into another Python application.

Example:

```python
from Agent.agent import Agent
from Agent.ReAct import ReActEngine

agent = Agent()

response = agent.run(
    "Calculate the total revenue from the quarterly data "
    "and summarize the top product line."
)

print(response)
```

---

# 🔄 ReAct Execution Flow

A typical agent interaction follows this pattern:

### 1. User provides a task

```text
Calculate the total revenue and identify the best-performing product.
```

### 2. Agent reasons

The agent determines whether it needs additional information.

### 3. Agent chooses an action

```text
Action → Use an external tool
```

### 4. Tool executes

The selected tool performs the requested operation.

### 5. Agent receives the observation

```text
Observation → Tool result
```

### 6. Agent reasons again

The agent evaluates the new information and decides whether another action is necessary.

### 7. Final response

Once enough information has been collected:

```text
Agent → Final Answer
```

---

# 🔧 Extending the Agent

The project is designed so additional tools can be added without redesigning the entire application.

Possible future tools include:

- 🌐 Web search
- 🧮 Calculator
- 📄 Document search
- 🗃️ Database queries
- 📅 Calendar operations
- 🌦️ Weather information
- 📧 Email operations
- 🔍 Knowledge-base search
- 🧠 RAG retrieval

A possible expanded architecture is:

```text
                    ReAct Agent
                         │
          ┌──────────────┼──────────────┐
          │              │              │
          ▼              ▼              ▼
      Web Search     Calculator      RAG Search
          │              │              │
          └──────────────┼──────────────┘
                         ▼
                     Observation
                         │
                         ▼
                    Reason Again
```

---

# 🎯 Why ReAct?

A simple LLM application:

```text
Prompt → LLM → Answer
```

has limited ability to interact with external systems.

A ReAct agent can:

```text
Understand
   ↓
Reason
   ↓
Act
   ↓
Observe
   ↓
Reason
   ↓
Act again
   ↓
Answer
```

This makes the architecture useful for applications that need dynamic tool usage and multi-step problem solving.

---

# 🧪 Example Use Cases

This architecture can be extended to build:

### 🔎 Web Search Agent

```text
User Question
     ↓
ReAct Agent
     ↓
Web Search Tool
     ↓
Search Results
     ↓
Reasoning
     ↓
Answer
```

### 📊 Data Analysis Agent

```text
User Question
     ↓
Agent
     ↓
Data Tool
     ↓
Calculation
     ↓
Observation
     ↓
Answer
```

### 📚 RAG Agent

```text
Question
   ↓
Agent
   ↓
Retriever
   ↓
Documents
   ↓
Reason
   ↓
Answer
```

---

# 📚 Learning Goals

This project demonstrates practical concepts including:

- LLM application development
- AI agents
- ReAct architecture
- Tool calling
- Prompt engineering
- Agent loops
- External tool integration
- Modular Python design
- Environment configuration

---

# 🔒 Security

Never commit:

```text
.env
API keys
access tokens
credentials
private configuration
```

If a real API key has already been pushed to GitHub, treat it as compromised:

1. Revoke the key.
2. Generate a new key.
3. Remove the secret from Git history.
4. Add the secret file to `.gitignore`.

---

# 🚧 Future Improvements

Planned or possible improvements:

- [ ] Add multiple production-ready tools
- [ ] Add web-search integration
- [ ] Add structured tool outputs
- [ ] Add stronger error handling
- [ ] Add agent execution tracing
- [ ] Add conversation memory
- [ ] Add RAG integration
- [ ] Add automated tests
- [ ] Add Docker support
- [ ] Add deployment configuration
- [ ] Add a richer web interface

---

# 🤝 Contributing

Contributions are welcome.

```bash
git checkout -b feature/your-feature
git add .
git commit -m "Add your feature"
git push origin feature/your-feature
```

Then open a Pull Request.

---

# 📄 License

This project is released under the **MIT License**.

---

# 👨‍💻 Author

**Sri Vardhan Jilla**

AI / Generative AI / Agentic AI Enthusiast

GitHub:  
https://github.com/jillasrivardhan

---

⭐ If you find this project useful, consider giving the repository a star.
