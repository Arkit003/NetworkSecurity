# Network Security - Phishing Detection

![Python](https://img.shields.io/badge/Python-3.8%2B-blue.svg)
![Docker](https://img.shields.io/badge/Docker-Enabled-blue)
![MLflow](https://img.shields.io/badge/MLflow-Tracking-green)
![Status](https://img.shields.io/badge/Status-Active-success)

An **End-to-End Machine Learning** project designed to detect phishing attacks using network security data. This repository implements a robust MLOps pipeline covering data ingestion, validation, transformation, model training, and deployment.

---

##  Features

* **End-to-End Pipeline**: Automated workflow from data ingestion to model prediction.
* **Data Validation**: Rigorous schema checks and data drift detection.
* **Experiment Tracking**: Integrated with **MLflow** to track model performance and experiments.
* **Database Integration**: Seamless data storage and retrieval using **MongoDB**.
* **Containerization**: Fully dockerized for easy deployment across environments.
* **CI/CD Ready**: Configured with GitHub Actions for continuous integration and delivery.
* **Web Interface**: Includes a web application for real-time predictions.

---

##  Tech Stack

| Component | Technology |
| :--- | :--- |
| **Language** | Python |
| **Database** | MongoDB |
| **ML Framework** | Scikit-learn, Pandas, NumPy |
| **Tracking** | MLflow |
| **Containerization** | Docker |
| **Web Framework** | Flask / FastAPI |
| **CI/CD** | GitHub Actions |

---

##  Project Structure

```text
NetworkSecurity/
├── .github/workflows/    # CI/CD pipelines
├── data_schema/          # Schema definitions for data validation
├── final_model/          # Saved trained models
├── network_data/         # Raw dataset storage
├── networksecurity/      # Main source package
│   ├── components/       # Modules for Ingestion, Validation, Transformation, Training
│   ├── pipeline/         # Training and Prediction pipelines
│   └── utils/            # Utility functions
├── prediction_data/      # Data for batch prediction
├── templates/            # HTML templates for the web app
├── app.py                # Web application entry point
├── main.py               # Main script for pipeline execution
├── push_data.py          # Script to push data to MongoDB
├── requirements.txt      # Project dependencies
├── Dockerfile            # Docker configuration
└── setup.py              # Package installation setup
```

---

##  Installation

1. **Clone the repository**
   ```bash
   git clone [https://github.com/Arkit003/NetworkSecurity.git](https://github.com/Arkit003/NetworkSecurity.git)
   cd NetworkSecurity
   ```

2. **Create a virtual environment**
   ```bash
   python -m venv venv
   source venv/bin/activate   # On Linux/Mac
   .\venv\Scripts\activate    # On Windows
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Set up Environment Variables**
   Create a `.env` file in the root directory and add your MongoDB connection string (and AWS/Cloud keys if applicable):
   ```env
   MONGO_DB_URL="your_mongodb_connection_string"
   ```

---

##  Usage

### 1. Data Ingestion
To push the initial dataset to MongoDB:
```bash
python push_data.py
```

### 2. Training the Model
To run the full training pipeline:
```bash
python main.py
```

### 3. Running the Web App
To start the web interface for predictions:
```bash
python app.py
```
*Access the app at `http://localhost:5000` (or the port specified).*

### 4. Docker Usage
Build and run the container:
```bash
docker build -t network-security .
docker run -p 5000:5000 network-security
```

---

##  Workflow

The pipeline consists of the following stages:

1. **Data Ingestion**: Fetches data from the source (MongoDB) and splits it into train/test sets.
2. **Data Validation**: Validates data against a defined schema and checks for drift.
3. **Data Transformation**: Handles missing values, scaling, and encoding.
4. **Model Trainer**: Trains multiple models and selects the best one based on accuracy/metrics.
5. **Model Evaluation**: Evaluates the model and logs metrics to MLflow.

---

##  Contributing

Contributions are welcome! Please fork the repository and create a pull request for any feature updates or bug fixes.

---



