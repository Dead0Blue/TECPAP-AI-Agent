"""
Orchestrateur Intelligence Artificielle - Agent de Décision TECPAP
Simule un cerveau d'agent (LLM-style) avec appels de fonctions locaux
"""

import re
from datetime import datetime

class AgentBrain:
    def __init__(self, predictor, recommender, anomaly_expert, speed_optimizer):
        self.predictor = predictor
        self.recommender = recommender
        self.expert = anomaly_expert
        self.optimizer = speed_optimizer
        self.memory = []
        
    def process_query(self, query):
        """Traite une requête utilisateur et décide des outils à appeler"""
        query_lower = query.lower()
        self.memory.append({"role": "user", "content": query})
        
        # 1. Analyse de l'intention et construction de la "pensée"
        thought = self._generate_thought(query_lower)
        
        # 2. Exécution des outils basés sur la pensée
        observations = []
        for action in thought['actions']:
            obs = self._execute_tool(action['tool'], action['params'])
            observations.append(obs)
            
        # 3. Synthèse de la réponse finale
        response = self._synthesize_response(query, thought, observations)
        self.memory.append({"role": "assistant", "content": response})
        
        return {
            "thought": thought['description'],
            "actions": thought['actions'],
            "observations": observations,
            "response": response
        }

    def _generate_thought(self, q):
        """Simulation du raisonnement de l'agent"""
        actions = []
        description = "Je dois analyser la demande pour choisir le bon outil."
        
        if any(w in q for w in ["prévoir", "prediction", "futur", "oee", "semaine"]):
            line = "L1" # Default
            if "l2" in q: line = "L2"
            elif "l3" in q: line = "L3"
            actions.append({"tool": "oee_forecast", "params": {"line": line, "days": 7}})
            description = f"L'utilisateur s'interroge sur les performances futures. Je vais consulter le modèle de prédiction pour la {line}."
            
        elif any(w in q for w in ["recommander", "choisir", "quelle ligne", "meilleure"]):
            prod = "Fond_Plat"
            if "carre" in q: prod = "Fond_Carre_Sans_Poignees"
            actions.append({"tool": "line_recommendation", "params": {"product": prod, "qty": 1000}})
            description = "Une décision de production est requise. Je vais évaluer la meilleure ligne pour ce produit."
            
        elif any(w in q for w in ["problème", "panne", "erreur", "anomalie", "solution"]):
            desc = q.replace("problème", "").replace("anomalie", "").strip()
            actions.append({"tool": "solve_anomaly", "params": {"description": desc or "problème général"}})
            description = "Une anomalie industrielle est signalée. Je vais chercher des solutions dans la base de connaissances."
            
        elif any(w in q for w in ["vitesse", "optimiser", "sweet spot", "rapide"]):
            line = "L1"
            if "l2" in q: line = "L2"
            elif "l3" in q: line = "L3"
            actions.append({"tool": "optimize_speed", "params": {"line": line, "product": "Fond_Plat"}})
            description = "Optimisation de la productivité demandée. Je vais calculer le Sweet Spot de vitesse."
            
        else:
            description = "Demande générale reçue. Je vais fournir une vue d'ensemble de l'état du système."
            actions.append({"tool": "system_status", "params": {}})
            
        return {"description": description, "actions": actions}

    def _execute_tool(self, tool, params):
        """Appel dynamique des modèles analytiques"""
        try:
            if tool == "oee_forecast":
                res = self.predictor.predict_line(params['line'], params['days'])
                return f"Prédiction OEE pour {params['line']}: {res[0]['oee_predicted']}% en moyenne."
            
            elif tool == "line_recommendation":
                res = self.recommender.recommend(params['product'], params['qty'])
                return f"Recommandation: {res['line_id']} (Score: {res['score']}) avec un OEE prédit de {res['predicted_oee']}%."
            
            elif tool == "solve_anomaly":
                res = self.expert.find_similar(params['description'])
                if res:
                    return f"Trouvé un cas similaire (Sim: {res[0]['similarity']}%). Cause: {res[0]['cause']}. Solution: {res[0]['solution']}."
                return "Aucun cas similaire trouvé."
            
            elif tool == "optimize_speed":
                res = self.optimizer.find_optimal_speed(params['line'], params['product'])
                return f"Vitesse optimale pour {params['line']}: {res['optimal_speed']} pcs/h pour un rendement max de {res['max_output']}."
            
            elif tool == "system_status":
                return "Toutes les lignes sont opérationnelles. L1: 75%, L2: 72%, L3: 68% OEE."
                
        except Exception as e:
            return f"Erreur lors de l'utilisation de l'outil {tool}: {str(e)}"

    def _synthesize_response(self, q, thought, obs):
        """Construction de la réponse en langage naturel"""
        if not obs:
            return "Je suis l'assistant TECPAP. Je peux vous aider à prévoir l'OEE, recommander des lignes ou résoudre des anomalies. Que souhaitez-vous savoir ?"
        
        main_obs = " ".join(obs)
        return f"D'après mes analyses de production : {main_obs} Est-ce que cela répond à votre question ou souhaitez-vous approfondir un point ?"
