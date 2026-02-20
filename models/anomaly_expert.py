"""
Système expert pour la gestion et l'analyse des anomalies
"""

import pandas as pd
import numpy as np
from datetime import datetime, timedelta
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

class AnomalyExpert:
    def __init__(self):
        self.knowledge_base = None
        self.vectorizer = TfidfVectorizer(max_features=100)
        self.symptom_vectors = None
        self.active_alerts = []
    
    def load_knowledge_base(self):
        from data.data_loader import DataLoader
        loader = DataLoader()
        loader.load_data()
        if loader.anomalies_data is not None:
            self.knowledge_base = loader.anomalies_data
            if len(self.knowledge_base) > 0:
                symptoms = self.knowledge_base['symptom'].fillna('') + ' ' + self.knowledge_base['root_cause'].fillna('')
                self.symptom_vectors = self.vectorizer.fit_transform(symptoms)
            self._generate_active_alerts(loader)
            return True
        return False
    
    def _generate_active_alerts(self, loader):
        if loader.oee_data is None: return
        recent = loader.oee_data[loader.oee_data['timestamp'] >= loader.oee_data['timestamp'].max() - timedelta(days=1)]
        self.active_alerts = []
        for line in ['L1', 'L2', 'L3']:
            line_data = recent[recent['line_id'] == line]
            if len(line_data) == 0: continue
            curr = line_data['oee'].iloc[-1]
            avg = line_data['oee'].mean()
            if curr < avg - 10:
                self.active_alerts.append({
                    'line_id': line, 'severity': 'Critical', 'type': 'Performance_Drop',
                    'message': f'Baisse critique de performance sur {line}', 'current': round(curr, 2),
                    'expected': round(avg, 2), 'timestamp': datetime.now().isoformat()
                })
            elif curr < 70:
                self.active_alerts.append({
                    'line_id': line, 'severity': 'High', 'type': 'Low_OEE',
                    'message': f'OEE en dessous du seuil sur {line}', 'current': round(curr, 2),
                    'timestamp': datetime.now().isoformat()
                })
    
    def find_similar(self, description):
        if self.knowledge_base is None or self.symptom_vectors is None: return []
        query_vector = self.vectorizer.transform([description])
        sims = cosine_similarity(query_vector, self.symptom_vectors)[0]
        top_indices = np.argsort(sims)[-5:][::-1]
        results = []
        for idx in top_indices:
            if sims[idx] > 0.1:
                row = self.knowledge_base.iloc[idx]
                results.append({
                    'similarity': round(float(sims[idx]) * 100, 1),
                    'line': row['line_id'], 'machine': row['machine_id'],
                    'symptom': row['symptom'], 'cause': row['root_cause'], 'solution': row['solution_applied']
                })
        return results
    
    def get_recent_anomalies(self, days=30):
        if self.knowledge_base is None: return []
        cutoff = datetime.now() - timedelta(days=days)
        recent = self.knowledge_base[pd.to_datetime(self.knowledge_base['timestamp']) >= cutoff]
        anomalies = []
        for _, row in recent.iterrows():
            anomalies.append({
                'id': int(row['anomaly_id']), 'date': row['timestamp'], 'line': row['line_id'],
                'machine': row['machine_id'], 'symptom': row['symptom'], 'cause': row['root_cause'],
                'solution': row['solution_applied'], 'priority': row['priority'], 'status': row['status']
            })
        return sorted(anomalies, key=lambda x: str(x['date']), reverse=True)
