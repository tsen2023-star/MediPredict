Place your downloaded Kaggle CSV files here:
- heart.csv
- liver.csv
- diabetes.csv

The exact target column names are configured in prediction/ml/train_models.py.
Inspect each dataset's column names, feature order, units, and target encoding.
The web form assumes the documented Cleveland / ILPD / Pima-style features. If
your CSV uses different column names or encodings, adapt the training mapping
and form-to-model mapping before relying on predictions.
