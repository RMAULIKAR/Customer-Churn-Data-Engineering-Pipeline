-- Create VIEW cleaned_customer
CREATE OR REPLACE VIEW cleaned_customers AS
SELECT
    customerID,
    gender,
    SeniorCitizen,
    Partner,
    Dependents,
    tenure,
    PhoneService,
    MultipleLines,
    InternetService,
    OnlineSecurity,
    OnlineBackup,
    DeviceProtection,
    TechSupport,
    StreamingTV,
    StreamingMovies,
    Contract,
    PaperlessBilling,
    PaymentMethod,
    MonthlyCharges,
    CASE 
        WHEN TRIM(TotalCharges) = '' THEN 0
        ELSE CAST(TotalCharges AS DECIMAL(10,2))
    END AS TotalCharges,
    Churn
FROM raw_customers;
