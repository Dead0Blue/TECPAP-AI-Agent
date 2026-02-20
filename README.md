# TECPAP AI Agent - OEE Decision Support System

TECPAP AI Agent is an advanced industrial intelligence system designed to optimize **Overall Equipment Effectiveness (OEE)** in manufacturing environments. It transforms descriptive data into prescriptive actions using a localized "Agent Brain" that orchestrates analytical models.

🚀 **[Live Demo on Vercel](https://tecpap-ai-agent.vercel.app)** | 📦 **[Repository on GitHub](https://github.com/Dead0Blue/TECPAP-AI-Agent)**

---

## 🚀 Key Features

- **🧠 Agentic Orchestrator**: A localized natural language reasoning engine that identifies user intent and selects the appropriate analytical tool.
- **📈 OEE Prediction**: Forecasting performance for the next 7 days using ensemble Machine Learning (Random Forest & Gradient Boosting).
- **🎯 Line Recommender**: Intelligent prioritization of production lines based on product type, quantity, and predicted OEE.
- **🛠️ Anomaly Expert**: Automated diagnostic system using TF-IDF similarity search to resolve production issues based on historical cases.
- **⚡ Speed Optimizer**: "Sweet Spot" finder that calculates the optimal machine speed to maximize net output (Production × Quality).
- **🖥️ High-Contrast Dashboard**: A professional **Black and Red dark-themed UI** optimized for industrial monitoring.

## 📂 Project Structure

```text
├── app.py              # Flask server and API endpoints
├── models/             # AI Brain & Analytical Tools
│   ├── agent_brain.py  # Orchestrator (Intent processing)
│   ├── predictor.py    # OEE Forecasting (ML)
│   ├── anomaly_expert.py# Diagnostic system
│   └── ...
├── data/               # Data ingestion & generation
├── static/             # UI Assets (CSS, JS)
├── templates/          # Dashboard (HTML)
├── research/           # Source documents & extraction scripts
├── requirements.txt    # Python dependencies
└── vercel.json         # Deployment config
```

## 🤖 How the Agent Works

The system implements a "Simulated Brain" orchestrator (`AgentBrain`) that:
1. **Analyses Intent**: Uses advanced pattern matching to understand natural language queries.
2. **Orchestrates Tools**: Selects and executes specific analytical models (Predictor, Recommender, etc.) based on the request.
3. **Synthesizes Insights**: Combines tool outputs into a human-readable response with actionable advice.
4. **Proactive Monitoring**: Periodically scans for production drops and alerts the user through the "Agent Command Center".

## 🛠️ Tech Stack

- **Backend**: Flask (Python)
- **AI/ML**: Scikit-Learn (Random Forest, GBR), Pandas, NumPy, NLP Pattern Matching
- **Frontend**: HTML5, Vanilla CSS (Custom Design System), JavaScript (ES6+), Chart.js
- **Deployment**: Vercel (Serverless Python Runtime)

## 📦 Installation & Local Run

1. **Clone the repository**:
   ```bash
   git clone https://github.com/Dead0Blue/TECPAP-AI-Agent.git
   cd TECPAP-AI-Agent
   ```

2. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Run the application**:
   ```bash
   python app.py
   ```

4. **Access the dashboard**: Open `http://localhost:5000` in your browser.

## 💬 Interacting with the Agent

Use the **Agent Command Center** at the bottom of the dashboard to ask questions like:
- *"Quelle est la prédiction OEE pour la ligne 2 ?"*
- *"Recommande-moi une ligne pour la production de sacs kraft."*
- *"J'ai une baisse de vitesse sur la ligne 1, que faire ?"*

---
Developed for the **TECPAP** Innovation Project. 🏗️
