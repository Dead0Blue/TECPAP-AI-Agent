"""
Agent IA de Décision pour l'Amélioration de l'OEE - TECPAP
Application principale Flask
"""

from flask import Flask, render_template, jsonify, request
from datetime import datetime, timedelta
import os
import pandas as pd
from models.predictor import OEEPredictor
from models.recommender import LineRecommender
from models.anomaly_expert import AnomalyExpert
from models.speed_optimizer import SpeedOptimizer
from models.agent_brain import AgentBrain
from data.data_loader import DataLoader
from data.products_catalog import get_all_products

app = Flask(__name__)
app.config['SECRET_KEY'] = 'tecpap-innovation-oee-2026'

# Initialisation des composants
data_loader = DataLoader()
oee_predictor = OEEPredictor()
line_recommender = LineRecommender()
anomaly_expert = AnomalyExpert()
speed_optimizer = SpeedOptimizer()
agent_brain = AgentBrain(oee_predictor, line_recommender, anomaly_expert, speed_optimizer)

def initialize_system():
    print("Initialisation de l'Agent IA TECPAP...")
    if data_loader.load_data():
        if not oee_predictor._load_model():
            oee_predictor.train()
        line_recommender.initialize()
        anomaly_expert.load_knowledge_base()
        speed_optimizer.train(data_loader.get_data_for_training())
        print("Système opérationnel!")
        return True
    return False

initialize_system()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/dashboard')
def get_dashboard_data():
    return jsonify({
        'current': data_loader.get_current_metrics(),
        'predictions': oee_predictor.predict_next_days(days=7),
        'recommendation': line_recommender.get_best_line(),
        'alerts': anomaly_expert.active_alerts,
        'timestamp': datetime.now().isoformat()
    })

@app.route('/api/recommend')
def recommend_line():
    product_type = request.args.get('product_type', 'Fond_Plat')
    quantity = int(request.args.get('quantity', 1000))
    return jsonify(line_recommender.recommend(product_type, quantity))

@app.route('/api/anomalies')
def get_anomalies():
    period = int(request.args.get('period', 30))
    return jsonify({'anomalies': anomaly_expert.get_recent_anomalies(period)})

@app.route('/api/anomaly/similar', methods=['POST'])
def find_similar():
    data = request.json
    return jsonify({'similar_cases': anomaly_expert.find_similar(data.get('description', ''))})

@app.route('/api/speed/optimize', methods=['POST'])
def optimize_speed():
    data = request.json
    return jsonify(speed_optimizer.find_optimal_speed(data.get('line_id', 'L1'), data.get('product_type', 'Fond_Plat')))

@app.route('/api/products')
def get_products():
    return jsonify({'products': get_all_products()})

@app.route('/api/chat', methods=['POST'])
def chat():
    data = request.json
    query = data.get('query', '')
    if not query:
        return jsonify({'error': 'No query provided'}), 400
    response = agent_brain.process_query(query)
    return jsonify(response)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
