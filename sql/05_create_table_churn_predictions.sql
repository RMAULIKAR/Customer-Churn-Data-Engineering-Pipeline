-- CREATE TABLE churn_predictions 

CREATE TABLE IF NOT EXISTS churn_predictions(
    customerID VARCHAR(50) PRIMARY KEY,
    churn_prediction INT,
    churn_probability FLOAT,
    prediction_timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
