"""
Optimiseur de vitesse machine (Sweet Spot Finder)
"""

import numpy as np
import pandas as pd
from sklearn.ensemble import GradientBoostingRegressor
from sklearn.preprocessing import StandardScaler
import joblib
import os

class SpeedOptimizer:
    def __init__(self):
        self.model_production = None
        self.model_quality = None
        self.scaler = StandardScaler()
        self.is_trained = False
        self.speed_ranges = {
            'L1': {'min': 700, 'max': 1300, 'optimal_estimate': 1000},
            'L2': {'min': 800, 'max': 1400, 'optimal_estimate': 1100},
            'L3': {'min': 600, 'max': 1200, 'optimal_estimate': 900}
        }
        self.product_characteristics = {
            'Fond_Plat': {'complexity': 0.7, 'speed_factor': 1.15},
            'Fond_Carre_Sans_Poignees': {'complexity': 0.8, 'speed_factor': 1.10},
            'Fond_Carre_Poignees_Plates': {'complexity': 0.9, 'speed_factor': 0.95},
            'Fond_Carre_Poignees_Torsadees': {'complexity': 1.0, 'speed_factor': 0.85}
        }
    
    def prepare_features(self, df):
        features = df.copy()
        features['line_L1'] = (features['line_id'] == 'L1').astype(int)
        features['line_L2'] = (features['line_id'] == 'L2').astype(int)
        features['line_L3'] = (features['line_id'] == 'L3').astype(int)
        for product in self.product_characteristics.keys():
            features[f'product_{product}'] = (features['product_type'] == product).astype(int)
        
        def get_speed_ratio(row):
            return row['machine_speed'] / self.speed_ranges[row['line_id']]['optimal_estimate']
        features['speed_ratio'] = features.apply(get_speed_ratio, axis=1)
        
        cols = ['machine_speed', 'speed_ratio', 'line_L1', 'line_L2', 'line_L3'] + [f'product_{p}' for p in self.product_characteristics.keys()]
        return features[cols]
    
    def train(self, data):
        data['production_rate'] = data['total_pieces']
        data['quality_rate'] = (data['good_pieces'] / data['total_pieces']) * 100
        X = self.prepare_features(data)
        X_scaled = self.scaler.fit_transform(X)
        
        self.model_production = GradientBoostingRegressor(n_estimators=100, max_depth=5, random_state=42)
        self.model_production.fit(X_scaled, data['production_rate'])
        
        self.model_quality = GradientBoostingRegressor(n_estimators=100, max_depth=5, random_state=42)
        self.model_quality.fit(X_scaled, data['quality_rate'])
        
        self.is_trained = True
        return True
    
    def find_optimal_speed(self, line_id, product_type):
        if not self.is_trained: return {}
        min_s = self.speed_ranges[line_id]['min']
        max_s = self.speed_ranges[line_id]['max']
        speeds = np.arange(min_s, max_s + 25, 25)
        
        results = []
        for s in speeds:
            X = self.prepare_features(pd.DataFrame([{'line_id': line_id, 'product_type': product_type, 'machine_speed': s}]))
            X_s = self.scaler.transform(X)
            p = self.model_production.predict(X_s)[0]
            q = self.model_quality.predict(X_s)[0]
            results.append({'speed': int(s), 'output': round(p * (q / 100), 1), 'quality': round(q, 2)})
            
        best = max(results, key=lambda x: x['output'])
        return {
            'optimal_speed': best['speed'], 'max_output': best['output'], 
            'current_speed': self.speed_ranges[line_id]['optimal_estimate'],
            'curve': results
        }
