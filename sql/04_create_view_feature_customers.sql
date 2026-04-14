-- CREATE VIEW feature_customers AS

CREATE OR REPLACE VIEW feature_customers AS
SELECT
    customerID,
    tenure,
    MonthlyCharges,
    TotalCharges,
    SeniorCitizen,

    CASE WHEN gender = 'Male' THEN 1 ELSE 0 END AS gender_male,
    CASE WHEN Partner = 'Yes' THEN 1 ELSE 0 END AS has_partner,
    CASE WHEN Dependents = 'Yes' THEN 1 ELSE 0 END AS has_dependents,
    CASE WHEN PhoneService = 'Yes' THEN 1 ELSE 0 END AS phone_service,
    CASE WHEN PaperlessBilling = 'Yes' THEN 1 ELSE 0 END AS paperless_billing,

    CASE WHEN Contract = 'Month-to-month' THEN 1 ELSE 0 END AS contract_monthly,
    CASE WHEN Contract = 'One year' THEN 1 ELSE 0 END AS contract_one_year,
    CASE WHEN Contract = 'Two year' THEN 1 ELSE 0 END AS contract_two_year,

    CASE 
        WHEN INSTR(LOWER(Churn), 'yes') > 0 THEN 1
        ELSE 0
    END AS churn

FROM cleaned_customers;