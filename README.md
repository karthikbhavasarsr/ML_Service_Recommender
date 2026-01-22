# ML Service Recommender

A machine learning-based service recommendation system that suggests relevant business services to customers based on their business type, location, budget, and other factors.

## Project Structure

```
ml_service_recommender/
├── src/
│   ├── __init__.py
│   ├── data_preprocessing.py      # Data loading and cleaning
│   ├── feature_encoding.py         # Feature encoding for ML
│   ├── ranking_engine.py           # ML-based ranking algorithm
│   ├── explanation_generator.py    # Generate explanations for recommendations
│   └── main.py                     # Main orchestration logic
├── ui/
│   └── app.py                      # Web interface (Streamlit)
├── data/
│   └── service_recommendation_data.csv
├── notebooks/
├── reports/
├── test_app.py                     # Unit tests
└── readme.md
```

## Features

- **Data Preprocessing**: Load and clean service data
- **Feature Encoding**: Convert categorical features to numerical format
- **Ranking Engine**: ML-based ranking of services using similarity scores
- **Explainability**: Generate human-readable explanations for recommendations
- **Web UI**: Interactive Streamlit interface for recommendations

## Installation

```bash
pip install pandas numpy scikit-learn streamlit
```

## Usage

### Run Web UI
```bash
streamlit run ui/app.py
```

### Run Tests
```bash
python test_app.py
```

## Data Format

The CSV file contains service information with columns:
- Service_ID: Unique identifier
- Service_Name: Name of the service
- Target_Business_Type: Intended business category
- Price_Category: Service pricing level
- Language_Support: Language availability
- Location_Area: Service location
- Description: Service details
- Match_Quality: Quality indicator
#

