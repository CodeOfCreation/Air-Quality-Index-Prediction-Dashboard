import joblib
import os
from pathlib import Path
import numpy as np
class AQIPredictor:
    _instance = None
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(AQIPredictor, cls).__new__(cls)
            cls._instance._initialized = False
        return cls._instance
    
    def __init__(self):
        if self._initialized:
            return
        
        # Load models and scaler
        try:
            base_dir = Path(__file__).resolve().parent.parent
            model_dir = base_dir / 'ml_models' / 'models'
            
            self.lr_model = joblib.load(model_dir / 'linear_regression.pkl')
            self.dt_model = joblib.load(model_dir / 'decision_tree.pkl')
            self.scaler = joblib.load(model_dir / 'scaler.pkl')
            
        except FileNotFoundError as e:
            raise FileNotFoundError(f"Model files not found. Please train the models first. Error: {e}")
        
        self._initialized = True
    
    def predict(self, features, model_type='lr'):
        """
        Predict AQI using specified model
        :param features: List of 8 features [pm25, pm10, no2, so2, co, o3, temperature, humidity]
        :param model_type: 'lr' for Linear Regression, 'dt' for Decision Tree
        :return: Predicted AQI value
        """
        import numpy as np
        
        # Convert features to numpy array and reshape
        features_array = np.array(features).reshape(1, -1)
        
        if model_type == 'lr':
            # Scale features for Linear Regression
            features_scaled = self.scaler.transform(features_array)
            prediction = self.lr_model.predict(features_scaled)
        elif model_type == 'dt':
            # Decision Tree doesn't need scaling
            prediction = self.dt_model.predict(features_array)
        else:
            raise ValueError("model_type must be 'lr' or 'dt'")
        
        return float(prediction[0])
    
    def get_aqi_category(self, aqi_value):
        """
        Get AQI category and color based on value
        :param aqi_value: AQI value
        :return: Dictionary with category name and color
        """
        if 0 <= aqi_value <= 50:
            return {
                'name': 'Good',
                'color': '#00e400',
                'bg_color': 'bg-success',
                'text_color': 'text-success'
            }
        elif 51 <= aqi_value <= 100:
            return {
                'name': 'Moderate',
                'color': '#ffff00',
                'bg_color': 'bg-warning',
                'text_color': 'text-warning'
            }
        elif 101 <= aqi_value <= 150:
            return {
                'name': 'Unhealthy for Sensitive Groups',
                'color': '#ff7e00',
                'bg_color': 'bg-orange',
                'text_color': 'text-orange'
            }
        elif 151 <= aqi_value <= 200:
            return {
                'name': 'Unhealthy',
                'color': '#ff0000',
                'bg_color': 'bg-danger',
                'text_color': 'text-danger'
            }
        elif 201 <= aqi_value <= 300:
            return {
                'name': 'Very Unhealthy',
                'color': '#8f3f97',
                'bg_color': 'bg-purple',
                'text_color': 'text-purple'
            }
        else:
            return {
                'name': 'Hazardous',
                'color': '#7e0023',
                'bg_color': 'bg-dark',
                'text_color': 'text-dark'
            }
    def predict(self, features, model_type='lr'):
        features_array = np.array(features).reshape(1, -1)
    
        if model_type == 'lr':
           # Scale features for Linear Regression
           features_scaled = self.scaler.transform(features_array)
           prediction = self.lr_model.predict(features_scaled)
        elif model_type == 'dt':
           # Decision Tree doesn't need scaling
           prediction = self.dt_model.predict(features_array)
        else:
           raise ValueError("model_type must be 'lr' or 'dt'")
    
         # Clip prediction to valid AQI range (0-500)
        prediction = max(0, min(float(prediction[0]), 500))
    
        return prediction