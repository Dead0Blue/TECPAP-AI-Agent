"""
Modèle de prédiction OEE utilisant des algorithmes de Machine Learning
"""

import numpy as np
import pandas as pd
from sklearn.ensemble import RandomForestRegressor, GradientBoostingRegressor
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import mean_absolute_error, r2_score
import joblib
import os
from datetime import datetime, timedelta

class OEEPredictor:
    def __init__(self):
        self.model = None
        self.scaler = StandardScaler()
        self.feature_columns = []
        self.models_path = os.path.join(os.path.dirname(__file__), 'saved_models')
        self.trained = False
        
        if not os.path.exists(self.models_path):
            os.makedirs(self.models_path)
    
    def prepare_features(self, df):
        features = df.copy()
        if 'timestamp' in features.columns:
            ts = pd.to_datetime(features['timestamp'])
            features['hour'] = ts.dt.hour
            features['day_of_week'] = ts.dt.dayofweek
            features['month'] = ts.dt.month
            features['day_of_year'] = ts.dt.dayofyear
            features['week_of_year'] = ts.dt.isocalendar().week
        
        features['line_L1'] = (features['line_id'] == 'L1').astype(int)
        features['line_L2'] = (features['line_id'] == 'L2').astype(int)
        features['line_L3'] = (features['line_id'] == 'L3').astype(int)
        
        numeric_features = ['hour', 'day_of_week', 'month', 'day_of_year', 'week_of_year', 'line_L1', 'line_L2', 'line_L3']
        
        for col in numeric_features:
            if col not in features.columns:
                features[col] = 0
                
        return features[numeric_features]
    
    def train(self):
        from data.data_loader import DataLoader
        print("Entraînement du modèle de prédiction OEE...")
        loader = DataLoader()
        loader.load_data()
        df = loader.get_data_for_training()
        
        if df is None or len(df) == 0:
            print("Erreur: Pas de données disponibles pour l'entraînement")
            return False
        
        X = self.prepare_features(df)
        y = df['oee']
        self.feature_columns = X.columns.tolist()
        
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
        X_train_scaled = self.scaler.fit_transform(X_train)
        X_test_scaled = self.scaler.transform(X_test)
        
        rf_model = RandomForestRegressor(n_estimators=100, max_depth=15, random_state=42, n_jobs=-1)
        rf_model.fit(X_train_scaled, y_train)
        
        gb_model = GradientBoostingRegressor(n_estimators=100, max_depth=7, random_state=42)
        gb_model.fit(X_train_scaled, y_train)
        
        rf_pred = rf_model.predict(X_test_scaled)
        gb_pred = gb_model.predict(X_test_scaled)
        y_pred = 0.6 * rf_pred + 0.4 * gb_pred
        
        mae = mean_absolute_error(y_test, y_pred)
        r2 = r2_score(y_test, y_pred)
        print(f"  - MAE: {mae:.2f}% | R²: {r2:.3f}")
        
        self.model = {'rf': rf_model, 'gb': gb_model, 'weights': [0.6, 0.4]}
        self.trained = True
        
        joblib.dump(self.model, os.path.join(self.models_path, 'oee_model.pkl'))
        joblib.dump(self.scaler, os.path.join(self.models_path, 'scaler.pkl'))
        joblib.dump(self.feature_columns, os.path.join(self.models_path, 'features.pkl'))
        return True
    
    def predict(self, features_df):
        if not self.trained and not self._load_model(): return None
        X = self.prepare_features(features_df)
        for col in self.feature_columns:
            if col not in X.columns: X[col] = 0
        X = X[self.feature_columns]
        X_scaled = self.scaler.transform(X)
        
        rf_pred = self.model['rf'].predict(X_scaled)
        gb_pred = self.model['gb'].predict(X_scaled)
        return np.clip(0.6 * rf_pred + 0.4 * gb_pred, 40, 95)
    
    def predict_next_days(self, days=7):
        from data.data_loader import DataLoader
        if not self.trained and not self._load_model(): return {}
        loader = DataLoader()
        loader.load_data()
        recent_data = loader.oee_data.tail(168)
        
        predictions = {}
        for line in ['L1', 'L2', 'L3']:
            line_data = recent_data[recent_data['line_id'] == line]
            if len(line_data) == 0: continue
            
            last_timestamp = line_data['timestamp'].max()
            future_features = []
            for d in range(days):
                date = last_timestamp + timedelta(days=d+1)
                for hour in range(8, 21):
                    future_features.append({
                        'timestamp': date + timedelta(hours=hour),
                        'line_id': line
                    })
            
            future_df = pd.DataFrame(future_features)
            preds = self.predict(future_df)
            
            if preds is not None:
                daily_preds = []
                for i in range(days):
                    day_values = preds[i*13:(i+1)*13]
                    daily_preds.append({
                        'date': (last_timestamp + timedelta(days=i+1)).strftime('%Y-%m-%d'),
                        'oee_predicted': round(float(np.mean(day_values)), 2),
                        'trend': self._calculate_trend(day_values)
                    })
                predictions[line] = daily_preds
        return predictions
    
    def _calculate_trend(self, p):
        if len(p) < 2: return 'Stable'
        slope = np.polyfit(np.arange(len(p)), p, 1)[0]
        return 'Augmentation' if slope > 0.5 else 'Diminution' if slope < -0.5 else 'Stable'
    
    def _load_model(self):
        try:
            m_path = os.path.join(self.models_path, 'oee_model.pkl')
            s_path = os.path.join(self.models_path, 'scaler.pkl')
            f_path = os.path.join(self.models_path, 'features.pkl')
            if os.path.exists(m_path):
                self.model, self.scaler, self.feature_columns = joblib.load(m_path), joblib.load(s_path), joblib.load(f_path)
                self.trained = True
                return True
        except: pass
        return False
