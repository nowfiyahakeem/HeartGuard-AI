import json
import math
from http.server import BaseHTTPRequestHandler, HTTPServer

def calculate_clinical_risk(data):
    try:
        # Extracting data from the dashboard request
        age = float(data.get('age', 45))
        bp = float(data.get('trestbps', 130))
        chol = float(data.get('chol', 200))
        mhr = float(data.get('Max_heart_rate', 150)) # New data point added
        cp = data.get('cp', 'Typical angina')

        # CLINICAL LOGIC CALCULATION
        score = 15.0
        
        # 1. Blood Pressure Risk
        if bp >= 140: 
            score += 30.0 + (bp - 140) * 0.5
            
        # 2. Cholesterol Risk
        if chol >= 240: 
            score += 20.0 + (chol - 240) * 0.1
            
        # 3. Age Risk
        if age > 50: 
            score += (age - 50) * 0.8
        
        # 4. Heart Rate Risk (New Logic)
        # Lower maximum heart rates can indicate a weaker heart or higher stress
        if mhr < 100: 
            score += 25.0 
        elif mhr < 130:
            score += 10.0
        
        # 5. Symptom Risk
        if cp == "Asymptomatic" or cp == "Atypical angina": 
            score += 15.0

        # Constraints (Keep risk between 5% and 98.8%)
        final_risk = min(max(score, 5.0), 98.8)
        return round(final_risk, 2)
    except Exception as e:
        print(f"Error calculating risk: {e}")
        return 45.0

class HeartGuardServer(BaseHTTPRequestHandler):
    def do_OPTIONS(self):
        # Handles the "pre-flight" request from your browser
        self.send_response(200)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        self.end_headers()

    def do_POST(self):
        # Handles the actual data analysis request
        content_length = int(self.headers['Content-Length'])
        post_data = self.rfile.read(content_length)
        
        # Load the data sent from HTML
        data = json.loads(post_data.decode('utf-8'))
        
        # Calculate the risk
        risk = calculate_clinical_risk(data)
        
        # Send response back to dashboard
        self.send_response(200)
        self.send_header('Content-Type', 'application/json')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.end_headers()
        
        response = {"risk_score": risk}
        self.wfile.write(json.dumps(response).encode('utf-8'))

if __name__ == "__main__":
    print("------------------------------------------")
    print("🚀 HEARTGUARD AI: CLINICAL BRAIN ACTIVE")
    print("📍 URL: https://heartguard-ai-9rel.onrender.com")
    print("------------------------------------------")
    # Change '127.0.0.1' to '0.0.0.0' so Render can host it
    # Change 8000 to 10000 (Render's preferred port, though 8000 often works)
    HTTPServer(('0.0.0.0', 8000), HeartGuardServer).serve_forever()