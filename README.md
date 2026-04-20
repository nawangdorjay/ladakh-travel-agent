# 🏔️ Ladakh Travel & Tourism AI Agent

An intelligent AI assistant that helps tourists plan trips to Ladakh by answering questions about permits, weather, altitude acclimatization, road conditions, homestays, and local cultural etiquette.

> Built by a developer **from Ladakh** (Nubra Valley, Leh) who knows the region firsthand.

---

## 🎯 Problem

Tourists visiting Ladakh face:
- Scattered information across multiple government sites
- Confusion about Inner Line Permits (ILP) requirements
- Unpredictable weather and road closures (Khardung La, Chang La)
- Lack of guidance on altitude sickness prevention
- Difficulty finding authentic homestays and local experiences

## 💡 Solution

A conversational AI agent that aggregates real-time data from weather APIs, government portals, and local knowledge into one friendly chat interface.

## ✨ Features

- **Permit Guidance** — Who needs ILPs, how to apply, costs, processing time
- **Weather Intelligence** — Real-time weather + forecasts for Leh, Nubra, Pangong, etc.
- **Altitude Safety** — Acclimatization tips, AMS symptoms, when to descend
- **Road Status** — Current conditions for key passes and routes
- **Homestay Finder** — Authentic local stays with cultural context
- **Cultural Etiquette** — Do's and don'ts, monastery visits, local customs

## 🛠️ Tech Stack

- **Python 3.10+**
- **LangChain** — Agent framework and tool orchestration
- **Groq/OpenAI API** — LLM backbone
- **Streamlit** — Chat UI
- **Requests** — API calls for weather data
- **python-dotenv** — Environment management

## 🚀 Quick Start

```bash
# Clone
git clone https://github.com/nawangdorjay/ladakh-travel-agent.git
cd ladakh-travel-agent

# Install dependencies
pip install -r requirements.txt

# Set up environment
cp .env.example .env
# Add your API keys to .env

# Run
streamlit run app.py
```

## 📁 Project Structure

```
ladakh-travel-agent/
├── app.py                  # Streamlit chat UI
├── agent/
│   ├── __init__.py
│   ├── core.py             # Main agent logic
│   └── tools.py            # Agent tools (weather, permits, etc.)
├── data/
│   ├── permits.json        # ILP data
│   ├── homestays.json      # Homestay listings
│   ├── routes.json         # Route/pass information
│   └── cultural_guide.json # Etiquette and customs
├── utils/
│   ├── __init__.py
│   └── weather.py          # Weather API wrapper
├── tests/
│   └── test_agent.py       # Basic tests
├── requirements.txt
├── .env.example
├── .gitignore
└── README.md
```

## 🧑‍💻 About the Developer

Built by **Nawang Dorjay** — a 2nd-year B.Tech CSE (Data Science) student from Nubra Valley, Leh, Ladakh. Previous projects include a Jarvis-type AI agent and an automated resume reviewer.

## 📜 License

MIT

---

## 🤖 AI-Assisted Development

This project was built with AI assistance as part of a transparent human-AI collaboration workflow. AI helped with code generation, structure, and documentation — while domain expertise, data accuracy, and architectural decisions were human-driven.

> **See [BUILDING.md](BUILDING.md) for full transparency on AI usage, roles, and workflow.**

---


