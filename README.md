# Software & Machine Learning Tech Stack

This document outlines the core technologies, infrastructure, and machine learning components utilized in this project.

## Backend Engine
*   **Servers:** WSGI, Gunicorn process manager, Render Paas
*   **Infrastructure:** Multiple server processes
*   **Data Strategy:** Local MongoDB layer implementation ensuring zero data export policy.

## Databases
*   **MongoDB:** Atlas Version 8.0.29, `myAtlasClusterEDU`
*   **PostgreSQL:** Aiven PaaS Version 18.4

## Data & Machine Learning
*   **ML Frameworks:** 
    *   **PyTorch:** LSTM models utilized for time-series horizon forecasting.
    *   **scikit-learn:** Implementation of Logistic Regression, Support Vector Machines, and Isolation Forests for anomaly detection.
