#!/usr/bin/env bash
set -o errexit

pip install -r requirements.txt

# Ensure machine learning model artifacts are trained and available
if [ ! -f "prediction/ml/heart_model.pkl" ] || [ ! -f "prediction/ml/liver_model.pkl" ] || [ ! -f "prediction/ml/diabetes_model.pkl" ] || [ ! -f "prediction/ml/kidney_model.pkl" ] || [ ! -f "prediction/ml/breast_cancer_model.pkl" ]; then
    echo "Model files missing. Training machine learning models..."
    python prediction/ml/train_models.py
fi

python manage.py collectstatic --noinput
python manage.py migrate
