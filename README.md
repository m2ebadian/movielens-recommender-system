# MovieLens Recommendation System

A full-stack movie recommendation system built using the MovieLens dataset, collaborative filtering algorithms, and cloud deployment technologies. This project compares user-based and item-based collaborative filtering approaches, evaluates recommendation quality using RMSE and MAE metrics, and deploys the system through a React frontend and Flask backend on Google Cloud Run.

---

# Live Demo

🌐 https://cse482-frontend-816507479795.us-central1.run.app/

---

# Features

- User-based Collaborative Filtering
- Item-based Collaborative Filtering
- Personalized movie recommendations
- Similar user discovery
- Rated movie history visualization
- Model performance comparison
- Full-stack cloud deployment
- Interactive recommendation dashboard

---

# Tech Stack

## Frontend
- React
- TypeScript
- Vite
- CSS

## Backend
- Flask
- Python
- Pandas
- NumPy
- Scikit-learn

## Database & Storage
- MySQL
- Google Cloud SQL

## Deployment & Infrastructure
- Docker
- Google Cloud Run
- Google Artifact Registry

---

# Dataset

This project uses the MovieLens Latest Small Dataset.

Dataset characteristics:

| Metric | Value |
|---|---|
| Ratings | 100,836 |
| Users | 610 |
| Movies | 9,700+ |
| Dataset Type | Sparse User-Item Matrix |

Main tables used:

| Table | Purpose |
|---|---|
| `ratings` | User-movie rating records |
| `movies` | Movie title and genre metadata |
| `movies_genres` | Movie metadata with one-hot encoded genres |
| `ratings_with_movies` | Merged ratings and movie metadata |

---

# Project Objectives

The main goals of this project were to:

- Predict user movie preferences using collaborative filtering
- Compare user-based vs item-based collaborative filtering
- Analyze the impact of dataset sparsity
- Evaluate model performance using RMSE and MAE
- Deploy the recommendation system as a full-stack cloud application

---

# Data Preprocessing

Several preprocessing steps were performed before training the models:

- Cleaned missing and inconsistent data
- Merged ratings and movie metadata tables
- Converted timestamps into readable formats
- One-hot encoded movie genres
- Constructed sparse user-item matrices for collaborative filtering

---

# Exploratory Data Analysis

The dataset was analyzed through multiple visualizations:

- Rating distribution analysis
- Ratings per user distribution
- Ratings per movie distribution
- Genre frequency analysis

Key findings:
- Ratings were heavily concentrated between 3 and 5
- User activity was highly skewed
- The dataset was extremely sparse (~98% missing values)
- Popular movies received significantly more ratings

---

# Collaborative Filtering Models

## User-Based Collaborative Filtering

This method predicts ratings based on similarities between users.

### Challenges
- Sparse overlap between users
- Unstable similarity calculations
- Cold-start problems

---

## Item-Based Collaborative Filtering

This method predicts ratings using similarities between movies.

### Advantages
- More stable similarity estimates
- Better performance under sparse conditions
- Lower RMSE and MAE

This model achieved the best overall performance.

---

# Model Evaluation

The models were evaluated using:

- RMSE (Root Mean Squared Error)
- MAE (Mean Absolute Error)

## Best Model Results

| Model | RMSE | MAE |
|---|---|---|
| Item-Based Collaborative Filtering | 0.9016 | 0.6801 |

---

# Key Insights

- Item-based collaborative filtering outperformed user-based filtering
- Dataset sparsity was the dominant factor affecting performance
- User similarity became unreliable due to limited overlap
- Preprocessing and feature engineering improved model stability
- Collaborative filtering can still produce meaningful recommendations despite sparse data

---

# System Architecture

## Frontend
React application providing:
- Login interface
- Recommendation dashboard
- Similar user analysis
- Rated movie display

## Backend
Flask API responsible for:
- Recommendation generation
- Model inference
- User similarity computation
- Database communication

## Deployment
- Dockerized frontend and backend
- Cloud deployment using Google Cloud Run
- Container images stored in Artifact Registry

---

# Directory Structure

```bash
CSE482_Project/
│
├── backend/
│   ├── app.py
│   ├── recommender.py
│   ├── db.py
│   ├── requirements.txt
│   └── Dockerfile
│
├── frontend/
│   ├── src/
│   ├── package.json
│   ├── vite.config.ts
│   └── Dockerfile
│
├── dataset/
│   ├── ratings.csv
│   ├── movies.csv
│   ├── tags.csv
│   └── links.csv
│
├── reports/
│   └── Final_Report.pdf
│
└── README.md
```

---

# Running Locally

## Backend

```bash
cd backend

pip install -r requirements.txt

python app.py
```

---

## Frontend

```bash
cd frontend

npm install

npm run dev
```

---

# Cloud Deployment

## Backend Deployment

```bash
gcloud run deploy cse482-backend \
--image=YOUR_BACKEND_IMAGE \
--region=us-central1 \
--platform=managed \
--allow-unauthenticated
```

## Frontend Deployment

```bash
gcloud run deploy cse482-frontend \
--image=YOUR_FRONTEND_IMAGE \
--region=us-central1 \
--platform=managed \
--allow-unauthenticated
```

---

# Challenges

- Extremely sparse dataset
- Cold-start problem for new users and movies
- Limited overlap between users
- Hyperparameter sensitivity
- Scalability of similarity computation

---

# Future Improvements

- Matrix factorization methods (SVD)
- Deep learning recommendation systems
- Hybrid recommendation approaches
- Real-time recommendation updates
- Improved cold-start handling
- Larger MovieLens datasets

---

# Author

**Mehrshad Bagherebadian**  
4th Year Computer Science Major

---

# Final Report

The full technical report for this project is included in:

```bash
reports/Final_Report.pdf
```

---

# License

This project is intended for educational and academic purposes.
