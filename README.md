# TECPAP AI Agent - OEE Decision Support System

TECPAP AI Agent is an advanced industrial intelligence system designed to optimize **Overall Equipment Effectiveness (OEE)** in manufacturing environments. It transforms descriptive data into prescriptive actions using a localized "Agent Brain" that orchestrates analytical models.

## 🚀 Key Features

- **🧠 Agentic Orchestrator**: A natural language reasoning engine that identifies user intent and selects the appropriate analytical tool.
- **📈 OEE Prediction**: Forecasting performance for the next 7 days using ensemble Machine Learning (Random Forest & Gradient Boosting).
- **🎯 Line Recommender**: Intelligent prioritization of production lines based on product type, quantity, and predicted OEE.
- **🛠️ Anomaly Expert**: Automated diagnostic system using TF-IDF similarity search to resolve production issues based on historical cases.
- **⚡ Speed Optimizer**: "Sweet Spot" finder that calculates the optimal machine speed to maximize net output (Production × Quality).
- **🖥️ Dark Dashboard**: A professional black and red dark-themed UI built with Vanilla CSS and Chart.js.

## 🛠️ Tech Stack

- **Backend**: Flask (Python)
- **AI/ML**: Scikit-Learn, Pandas, NumPy, NLTK-style pattern matching
- **Frontend**: HTML5, Vanilla CSS, JavaScript (ES6+), Chart.js

## 📦 Installation

1. Clone the repository:
   ```bash
   git clone <your-repo-url>
   cd AI-Agent-TECPAP
   ```

2. Install dependencies:
   ```bash
   pip install flask pandas numpy scikit-learn joblib
   ```

3. Run the application:
   ```bash
   python app.py
   ```

4. Open your browser at `http://localhost:5000`.

## 🤖 Interacting with the Agent

The dashboard includes an **Agent Command Center**. You can interact with the agent using natural language:
- *"Quelle est la prédiction OEE pour la ligne 2 ?"*
- *"Recommande-moi une ligne pour produire 2000 sacs fond plat."*
- *"J'ai une baisse de qualité sur la ligne 1, que faire ?"*

---
Developed for **TECPAP** Innovation Project.
