import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.tree import DecisionTreeRegressor
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import mean_absolute_error, r2_score
import joblib
import os

def create_synthetic_data():
    """Create a synthetic AQI dataset for demonstration"""
    np.random.seed(42)
    n_samples = 1500
    
    # Generate synthetic features with realistic ranges
    pm25 = np.random.normal(50, 30, n_samples)
    pm10 = pm25 + np.random.normal(20, 15, n_samples)
    no2 = np.random.normal(40, 20, n_samples)
    so2 = np.random.normal(20, 10, n_samples)
    co = np.random.normal(1.2, 0.8, n_samples)
    o3 = np.random.normal(45, 25, n_samples)
    temperature = np.random.normal(25, 10, n_samples)
    humidity = np.random.normal(65, 20, n_samples)
    
    # Ensure non-negative values for pollutants
    pm25 = np.clip(pm25, 0, None)
    pm10 = np.clip(pm10, 0, None)
    no2 = np.clip(no2, 0, None)
    so2 = np.clip(so2, 0, None)
    co = np.clip(co, 0, None)
    o3 = np.clip(o3, 0, None)
    humidity = np.clip(humidity, 0, 100)
    
    # Create AQI based on a complex formula that considers all factors
    aqi = (
        0.4 * pm25 + 
        0.3 * pm10 + 
        0.1 * no2 + 
        0.05 * so2 + 
        0.1 * co * 100 +  # CO is multiplied by 100 to make it significant
        0.05 * o3 +
        0.05 * np.abs(temperature - 25) +  # Temperature effect
        0.05 * humidity  # Humidity effect
    )
    
    # Add some random noise
    aqi += np.random.normal(0, 20, n_samples)
    aqi = np.clip(aqi, 0, 500)  # AQI is typically 0-500
    
    # Create DataFrame
    data = pd.DataFrame({
        'pm25': pm25,
        'pm10': pm10,
        'no2': no2,
        'so2': so2,
        'co': co,
        'o3': o3,
        'temperature': temperature,
        'humidity': humidity,
        'aqi': aqi
    })
    
    return data

def train_models():
    """Train Linear Regression and Decision Tree models"""
    # Load or create dataset
    data_path = 'ml_models/data/aqi_dataset.csv'
    if os.path.exists(data_path):
        df = pd.read_csv(data_path)
    else:
        print("Dataset not found. Creating synthetic data...")
        df = create_synthetic_data()
        # Ensure the directory exists
        os.makedirs('ml_models/data', exist_ok=True)
        df.to_csv(data_path, index=False)
        print(f"Synthetic dataset saved to {data_path}")
    
    # Prepare features and target
    X = df[['pm25', 'pm10', 'no2', 'so2', 'co', 'o3', 'temperature', 'humidity']]
    y = df['aqi']
    
    # Split the data
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    
    # Feature scaling
    scaler = StandardScaler()
    X_train_scaled = scaler.fit_transform(X_train)
    X_test_scaled = scaler.transform(X_test)
    
    # Train Linear Regression model
    lr_model = LinearRegression()
    lr_model.fit(X_train_scaled, y_train)
    
    # Train Decision Tree model
    dt_model = DecisionTreeRegressor(max_depth=10, random_state=42)
    dt_model.fit(X_train, y_train)  # Decision Tree doesn't need scaling
    
    # Evaluate models
    # Linear Regression
    lr_pred = lr_model.predict(X_test_scaled)
    lr_mae = mean_absolute_error(y_test, lr_pred)
    lr_r2 = r2_score(y_test, lr_pred)
    
    # Decision Tree
    dt_pred = dt_model.predict(X_test)
    dt_mae = mean_absolute_error(y_test, dt_pred)
    dt_r2 = r2_score(y_test, dt_pred)
    
    # Print model performance
    print("Model Performance:")
    print(f"Linear Regression - MAE: {lr_mae:.2f}, R²: {lr_r2:.2f}")
    print(f"Decision Tree - MAE: {dt_mae:.2f}, R²: {dt_r2:.2f}")
    
    # Create models directory if it doesn't exist
    os.makedirs('ml_models/models', exist_ok=True)
    
    # Save models and scaler
    joblib.dump(lr_model, 'ml_models/models/linear_regression.pkl')
    joblib.dump(dt_model, 'ml_models/models/decision_tree.pkl')
    joblib.dump(scaler, 'ml_models/models/scaler.pkl')
    
    print("\nModels and scaler saved successfully!")
    print("- Linear Regression model: ml_models/models/linear_regression.pkl")
    print("- Decision Tree model: ml_models/models/decision_tree.pkl")
    print("- Scaler: ml_models/models/scaler.pkl")

if __name__ == "__main__":
    train_models()