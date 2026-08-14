# Software & Machine Learning Tech Stack

This document outlines the core technologies, infrastructure, and machine learning components utilized in this project.

## Dataset Sources & Environment
*   **Vehicle Classification Data:** [Infinite Dataset Hub - Vehicle Classifier](https://huggingface.co/datasets/infinite-dataset-hub/VehicleClassifier) — Utilized for categorizing visual automotive inputs and model validation.
*   **Traffic Speed & Time-Series Data:** [witgaw/METR-LA](https://huggingface.co/datasets/witgaw/METR-LA) — Sourced for spatial-temporal graph modeling and highway sensor performance tracking.
*   **NVIDIA Kaolin 3D Library Wheel Index:** [`https://nvidia-kaolin.s3.us-east-2.amazonaws.com/torch-2.0.0_cu118.html`](https://nvidia-kaolin.s3.us-east-2.amazonaws.com/torch-2.0.0_cu118.html)
    *   *Target Build:* PyTorch 2.0.0 with CUDA 11.8 support for accelerated 3D deep learning and differentiable rendering pipelines.

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
    *   **scikit-learn:** Implementation of Logistic Regression, SVMs (Support Vector Machines), and Isolation Forests for anomaly detection.
