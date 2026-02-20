"""
Système de recommandation de ligne optimale pour la production
"""

import numpy as np
import pandas as pd
from datetime import datetime, timedelta

class LineRecommender:
    def __init__(self):
        self.lines = ['L1', 'L2', 'L3']
        self.line_characteristics = {
            'L1': {'speed': 1000, 'quality_rate': 0.97, 'flexibility': 0.85, 'maintenance_level': 'Good', 'operators_required': 3},
            'L2': {'speed': 1100, 'quality_rate': 0.94, 'flexibility': 0.90, 'maintenance_level': 'Medium', 'operators_required': 4},
            'L3': {'speed': 900, 'quality_rate': 0.92, 'flexibility': 0.75, 'maintenance_level': 'Medium', 'operators_required': 2}
        }
        self.predictor = None
    
    def initialize(self):
        from models.predictor import OEEPredictor
        self.predictor = OEEPredictor()
        self.predictor._load_model()
    
    def get_best_line(self):
        from data.data_loader import DataLoader
        loader = DataLoader()
        loader.load_data()
        recent_data = loader.oee_data[loader.oee_data['timestamp'] >= loader.oee_data['timestamp'].max() - timedelta(days=7)]
        
        scores = {}
        for line in self.lines:
            line_data = recent_data[recent_data['line_id'] == line]
            if len(line_data) > 0:
                oee = line_data['oee'].mean()
                avail = line_data['availability'].mean()
                qual = line_data['quality'].mean()
                perf = line_data['performance'].mean()
                stab = 100 - line_data['oee'].std() * 2
                
                total_score = oee * 0.4 + avail * 0.2 + qual * 0.2 + perf * 0.1 + stab * 0.1
                scores[line] = {
                    'total_score': round(total_score, 2), 'oee': round(oee, 2), 
                    'availability': round(avail, 2), 'quality': round(qual, 2),
                    'performance': round(perf, 2), 'stability': round(stab, 2)
                }
        
        best_line = max(scores.items(), key=lambda x: x[1]['total_score'])
        return {
            'recommended_line': best_line[0], 'score': best_line[1]['total_score'],
            'details': best_line[1], 'all_scores': scores,
            'reason': self._generate_reason(best_line[0], best_line[1])
        }
    
    def recommend(self, product_type='standard', quantity=1000):
        from data.data_loader import DataLoader
        loader = DataLoader()
        loader.load_data()
        predictions = self.predictor.predict_next_days(days=1) if self.predictor and self.predictor.trained else None
        
        recommendations = []
        for line in self.lines:
            chars = self.line_characteristics[line]
            predicted_oee = predictions[line][0]['oee_predicted'] if predictions and line in predictions else 70
            prod_time = quantity / chars['speed']
            
            speed_score = chars['speed'] / 1100 * 100
            total_score = predicted_oee * 0.35 + chars['quality_rate'] * 25 + speed_score * 0.25 + chars['flexibility'] * 15
            
            recommendations.append({
                'line_id': line, 'score': round(total_score, 2), 'predicted_oee': round(predicted_oee, 2),
                'production_time_hours': round(prod_time, 2), 'speed': chars['speed'],
                'operators_needed': chars['operators_required'], 'status': chars['maintenance_level']
            })
        
        recommendations.sort(key=lambda x: x['score'], reverse=True)
        return {
            'recommended_line': recommendations[0]['line_id'], 'score': recommendations[0]['score'],
            'details': recommendations[0], 'alternatives': recommendations[1:],
            'confidence': 'High' if recommendations[0]['score'] > 80 else 'Medium'
        }
    
    def _generate_reason(self, line, s):
        reasons = []
        if s['oee'] > 75: reasons.append(f"OEE excellent ({s['oee']}%)")
        if s['quality'] > 95: reasons.append(f"Qualité supérieure ({s['quality']}%)")
        if s['stability'] > 90: reasons.append("Performance très stable")
        return " - ".join(reasons) if reasons else "Meilleur équilibre performance/fiabilité"
