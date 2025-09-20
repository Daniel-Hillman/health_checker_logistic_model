from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
import pandas as pd
import numpy as np
from sklearn.preprocessing import OneHotEncoder, StandardScaler
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
import joblib
import os

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

# Global variables for model, scaler and encoder
model = None
scaler = None
encoder = None
feature_columns = None

def load_or_train_model():
    """Load existing model or train Daniel's exact model"""
    global model, scaler, encoder, feature_columns
    
    try:
        # Try to load existing model files (from Daniel's notebook)
        if os.path.exists('model.pkl') and os.path.exists('scaler.pkl'):
            model = joblib.load('model.pkl')
            scaler = joblib.load('scaler.pkl')
            print("✅ Loaded Daniel's trained model!")
            
            # We need to recreate the encoder and feature columns
            df = pd.read_csv('synthetic_coffee_health_10000.csv')
            categorical_cols = ['Stress_Level', 'Sleep_Quality', 'Country', 'Gender', 'Occupation']
            encoder = OneHotEncoder(handle_unknown='ignore', sparse_output=False)
            encoded_array = encoder.fit_transform(df[categorical_cols])
            encoded_cols = encoder.get_feature_names_out(categorical_cols)
            encoded_df = pd.DataFrame(encoded_array, columns=encoded_cols, index=df.index)
            df_final = df.drop(columns=categorical_cols).join(encoded_df)
            df_final['Health_Issues'] = df_final['Health_Issues'].fillna('Good')
            
            # Binary classification like Daniel's model
            df_binary = df_final.copy()
            df_binary['Health_Issues'] = df_binary['Health_Issues'].replace({
                'Mild': 'Issue',
                'Moderate': 'Issue', 
                'Severe': 'Issue',
                'Good': 'Good'
            })
            
            X = df_binary.drop(['Health_Issues', 'ID'], axis=1)
            feature_columns = X.columns.tolist()
            
            return True
    except Exception as e:
        print(f"❌ Error loading existing model: {e}")
    
    # Train Daniel's exact model if loading failed
    try:
        print("🤖 Training Daniel's model architecture...")
        
        # Load data exactly like Daniel's notebook
        df = pd.read_csv('synthetic_coffee_health_10000.csv')
        
        # One-hot encoding exactly like Daniel
        categorical_cols = ['Stress_Level', 'Sleep_Quality', 'Country', 'Gender', 'Occupation']
        encoder = OneHotEncoder(handle_unknown='ignore', sparse_output=False)
        encoded_array = encoder.fit_transform(df[categorical_cols])
        encoded_cols = encoder.get_feature_names_out(categorical_cols)
        encoded_df = pd.DataFrame(encoded_array, columns=encoded_cols, index=df.index)
        df_final = df.drop(columns=categorical_cols).join(encoded_df)
        df_final['Health_Issues'] = df_final['Health_Issues'].fillna('Good')
        
        # Binary classification exactly like Daniel
        df_binary = df_final.copy()
        df_binary['Health_Issues'] = df_binary['Health_Issues'].replace({
            'Mild': 'Issue',
            'Moderate': 'Issue',
            'Severe': 'Issue', 
            'Good': 'Good'
        })
        
        # Features and target exactly like Daniel
        X = df_binary.drop(['Health_Issues', 'ID'], axis=1)
        y = df_binary['Health_Issues']
        feature_columns = X.columns.tolist()
        
        # Train-test split exactly like Daniel
        X_train, X_val, y_train, y_val = train_test_split(
            X, y, test_size=0.2, random_state=136, stratify=y
        )
        
        # Standard scaling exactly like Daniel
        scaler = StandardScaler()
        X_train_scaled = scaler.fit_transform(X_train)
        X_val_scaled = scaler.transform(X_val)
        
        # Logistic regression exactly like Daniel
        model = LogisticRegression(max_iter=1000, class_weight="balanced")
        model.fit(X_train_scaled, y_train)
        
        # Save model and scaler like Daniel
        joblib.dump(model, "model.pkl")
        joblib.dump(scaler, "scaler.pkl")
        
        # Test accuracy
        y_pred = model.predict(X_val_scaled)
        from sklearn.metrics import accuracy_score
        accuracy = accuracy_score(y_val, y_pred)
        print(f"✅ Daniel's model trained successfully! Accuracy: {accuracy:.2%}")
        return True
        
    except Exception as e:
        print(f"❌ Error training Daniel's model: {e}")
        return False

def preprocess_input(data):
    """Preprocess user input exactly like Daniel's model expects"""
    try:
        # Create template with all features (like Daniel's template_input)
        template_input = {col: 0 for col in feature_columns}
        
        # Fill in the actual values from user input
        template_input.update({
            "Age": float(data['age']),
            "BMI": float(data['bmi']),
            "Coffee_Intake": float(data['coffee_intake']),
            "Caffeine_mg": float(data['caffeine_mg']),
            "Sleep_Hours": float(data['sleep_hours']),
            "Heart_Rate": int(data['heart_rate']),
            "Physical_Activity_Hours": float(data['physical_activity']),
            "Smoking": int(data['smoking']),
            "Alcohol_Consumption": int(data['alcohol_consumption'])
        })
        
        # Handle categorical variables with one-hot encoding
        # Gender
        if data['gender'] == 'Male':
            template_input['Gender_Male'] = 1
        elif data['gender'] == 'Female':
            template_input['Gender_Female'] = 1
        elif data['gender'] == 'Other':
            template_input['Gender_Other'] = 1
            
        # Country
        country_key = f"Country_{data['country']}"
        if country_key in template_input:
            template_input[country_key] = 1
            
        # Occupation
        occupation_key = f"Occupation_{data['occupation']}"
        if occupation_key in template_input:
            template_input[occupation_key] = 1
            
        # Sleep Quality
        sleep_quality_key = f"Sleep_Quality_{data['sleep_quality']}"
        if sleep_quality_key in template_input:
            template_input[sleep_quality_key] = 1
            
        # Stress Level
        stress_level_key = f"Stress_Level_{data['stress_level']}"
        if stress_level_key in template_input:
            template_input[stress_level_key] = 1
        
        # Convert to DataFrame and ensure correct column order
        input_df = pd.DataFrame([template_input])
        input_df = input_df[feature_columns]  # Ensure correct order
        
        return input_df
        
    except Exception as e:
        print(f"❌ Error preprocessing input: {e}")
        raise e

@app.route('/')
def index():
    """Serve the main HTML page"""
    with open('html.html', 'r', encoding='utf-8') as f:
        return f.read()

@app.route('/predict', methods=['POST'])
def predict():
    """Handle prediction requests"""
    try:
        # Get JSON data from request
        data = request.get_json()
        
        if not data:
            return jsonify({'error': 'No data provided'}), 400
        
        # Preprocess input exactly like Daniel's model
        processed_input = preprocess_input(data)
        
        # Scale the input using Daniel's scaler
        processed_input_scaled = scaler.transform(processed_input)
        
        # Make prediction using Daniel's trained model
        prediction = model.predict(processed_input_scaled)[0]
        prediction_proba = model.predict_proba(processed_input_scaled)[0]
        
        # Get confidence like Daniel's predict_health function
        if prediction == "Good":
            confidence = float(prediction_proba[0])
        else:  # prediction == "Issue"
            confidence = float(prediction_proba[1])
        
        # Create response
        response = {
            'prediction': prediction,
            'confidence': confidence,
            'probabilities': {
                class_name: float(prob) 
                for class_name, prob in zip(model.classes_, prediction_proba)
            }
        }
        
        return jsonify(response)
        
    except Exception as e:
        print(f"❌ Prediction error: {e}")
        return jsonify({'error': str(e)}), 500

@app.route('/styles.css')
def serve_css():
    """Serve CSS file"""
    return send_from_directory('.', 'styles.css', mimetype='text/css')

@app.route('/font_files/<path:filename>')
def serve_fonts(filename):
    """Serve font files"""
    return send_from_directory('font_files', filename)

@app.route('/health')
def health_check():
    """Health check endpoint"""
    return jsonify({
        'status': 'healthy',
        'model_loaded': model is not None,
        'encoder_loaded': encoder is not None
    })

if __name__ == '__main__':
    # Load or train model on startup
    if load_or_train_model():
        print("🚀 Starting Flask server...")
        # Use environment port for deployment, fallback to 5000 for local
        import os
        port = int(os.environ.get('PORT', 5000))
        app.run(debug=False, host='0.0.0.0', port=port)
    else:
        print("❌ Failed to load/train model. Exiting.")