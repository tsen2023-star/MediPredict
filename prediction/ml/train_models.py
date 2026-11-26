"""
Place the three CSV files in datasets/ before running this script.
Expected default filenames and target columns:
  heart.csv: target
  liver.csv: Dataset (change TARGETS below if your Kaggle file differs)
  diabetes.csv: Outcome

Check the Kaggle dataset's actual column names and target encoding before training.
The script reports metrics; it does not guarantee clinical validity.
"""
from pathlib import Path
import warnings
import joblib
import numpy as np
import pandas as pd
from sklearn.compose import ColumnTransformer
from sklearn.impute import SimpleImputer
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score, roc_auc_score, confusion_matrix
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.ensemble import RandomForestClassifier
from sklearn.neighbors import KNeighborsClassifier

try:
    from xgboost import XGBClassifier
except ImportError:
    XGBClassifier = None

ROOT = Path(__file__).resolve().parents[2]
DATA = ROOT / "datasets"
OUT = Path(__file__).resolve().parent
FILES = {"heart": ("heart.csv", "target"), "liver": ("liver.csv", "Dataset"), "diabetes": ("diabetes.csv", "Outcome")}

ALIASES = {
    "heart": {
        "age":"age", "sex":"sex", "cp":"cp", "chestpaintype":"cp",
        "trestbps":"trestbps", "restingbloodpressure":"trestbps",
        "chol":"chol", "cholesterol":"chol", "fbs":"fbs",
        "fastingbloodsugar":"fbs", "restecg":"restecg", "thalach":"thalach",
        "maxheartrate":"thalach", "exang":"exang", "exerciseinducedangina":"exang",
        "oldpeak":"oldpeak", "slope":"slope", "ca":"ca",
        "numberofmajorvessels":"ca", "thal":"thal", "thalassemia":"thal"
    },
    "liver": {
        "age":"age", "gender":"gender", "sex":"gender",
        "totalbilirubin":"total_bilirubin", "directbilirubin":"direct_bilirubin",
        "alkalinephosphotase":"alkaline_phosphotase", "alkalinephosphatase":"alkaline_phosphotase",
        "sgpt":"alamine_aminotransferase", "alanineaminotransferase":"alamine_aminotransferase",
        "alamineaminotransferase":"alamine_aminotransferase",
        "sgot":"aspartate_aminotransferase", "aspartateaminotransferase":"aspartate_aminotransferase",
        "totalproteins":"total_proteins", "albumin":"albumin",
        "albuminandglobulinratio":"albumin_and_globulin_ratio",
        "agratio":"albumin_and_globulin_ratio"
    },
    "diabetes": {
        "pregnancies":"pregnancies", "glucose":"glucose",
        "bloodpressure":"blood_pressure", "blood_pressure":"blood_pressure",
        "skinthickness":"skin_thickness", "insulin":"insulin", "bmi":"bmi",
        "diabetespedigreefunction":"diabetes_pedigree_function",
        "age":"age"
    }
}

def canonical(name):
    return "".join(ch for ch in str(name).lower() if ch.isalnum() or ch == "_").replace("_", "")

def load_data(disease, filename, target):
    path = DATA / filename
    if not path.exists():
        raise FileNotFoundError(f"Missing {path}. Download the matching Kaggle CSV and place it in datasets/.")
    df = pd.read_csv(path)
    # Resolve target case-insensitively and normalize common Kaggle feature headers
    target_col = next((c for c in df.columns if canonical(c) == canonical(target)), None)
    if target_col is None:
        raise ValueError(f"{filename}: target column '{target}' not found. Available columns: {list(df.columns)}")
    y = df.pop(target_col)
    y = y.replace({1: 1, 2: 0, "1": 1, "2": 0, "yes": 1, "no": 0, "Yes": 1, "No": 0,
                   "Male": 1, "Female": 0, "Liver": 1, "No Liver": 0})
    y = pd.to_numeric(y, errors="coerce")
    valid = y.notna()
    X, y = df.loc[valid].copy(), y.loc[valid].astype(int)
    rename = {}
    aliases = ALIASES[disease]
    for col in X.columns:
        key = canonical(col)
        if key in aliases:
            rename[col] = aliases[key]
    X = X.rename(columns=rename)
    # Convert gender/sex labels into the numeric form expected by the forms.
    for col in X.columns:
        if X[col].dtype == object or str(X[col].dtype).startswith("str"):
            X[col] = X[col].replace({"Male": 1, "Female": 0, "male": 1, "female": 0})
    X = X.apply(pd.to_numeric, errors="coerce")
    expected = {
        "heart": ["age","sex","cp","trestbps","chol","fbs","restecg","thalach","exang","oldpeak","slope","ca","thal"],
        "liver": ["age","gender","total_bilirubin","direct_bilirubin","alkaline_phosphotase","alamine_aminotransferase","aspartate_aminotransferase","total_proteins","albumin","albumin_and_globulin_ratio"],
        "diabetes": ["pregnancies","glucose","blood_pressure","skin_thickness","insulin","bmi","diabetes_pedigree_function","age"]
    }[disease]
    missing = [c for c in expected if c not in X.columns]
    if missing:
        raise ValueError(f"{filename}: could not map required feature columns {missing}. Found: {list(X.columns)}")
    X = X[expected]
    if y.nunique() != 2:
        raise ValueError(f"{filename}: expected a binary target; found {sorted(y.unique())}")
    return X, y

def train_one(disease, filename, target):
    X, y = load_data(disease, filename, target)
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, stratify=y, random_state=42
    )
    numeric = X.select_dtypes(include=np.number).columns.tolist()
    prep = ColumnTransformer([("numeric", Pipeline([
        ("imputer", SimpleImputer(strategy="median")),
        ("scale", StandardScaler())
    ]), numeric)], remainder="drop")
    models = {
        "Random Forest": RandomForestClassifier(n_estimators=300, class_weight="balanced", random_state=42),
        "KNN": KNeighborsClassifier(n_neighbors=5, weights="distance")
    }
    if XGBClassifier:
        models["XGBoost"] = XGBClassifier(
            n_estimators=250, max_depth=4, learning_rate=0.05,
            subsample=0.9, colsample_bytree=0.9, eval_metric="logloss",
            random_state=42
        )
    else:
        warnings.warn("xgboost is not installed; skipping XGBoost.")
    results, best, best_auc = [], None, -1
    for name, estimator in models.items():
        pipe = Pipeline([("preprocess", prep), ("model", estimator)])
        pipe.fit(X_train, y_train)
        pred = pipe.predict(X_test)
        prob = pipe.predict_proba(X_test)[:, 1]
        try: auc = roc_auc_score(y_test, prob)
        except ValueError: auc = float("nan")
        metrics = {
            "disease": disease, "model": name,
            "accuracy": accuracy_score(y_test, pred),
            "precision": precision_score(y_test, pred, zero_division=0),
            "recall": recall_score(y_test, pred, zero_division=0),
            "f1": f1_score(y_test, pred, zero_division=0),
            "roc_auc": auc,
            "confusion_matrix": confusion_matrix(y_test, pred).tolist()
        }
        results.append(metrics)
        score = auc if np.isfinite(auc) else metrics["f1"]
        if score > best_auc:
            best_auc, best = score, (name, pipe)
    name, model = best
    joblib.dump({"model": model, "model_name": name, "features": list(X.columns)}, OUT / f"{disease}_model.pkl")
    return results

if __name__ == "__main__":
    all_results = []
    for disease, (filename, target) in FILES.items():
        all_results.extend(train_one(disease, filename, target))
    print(pd.DataFrame([{k:v for k,v in row.items() if k != "confusion_matrix"} for row in all_results]).to_string(index=False))
    print("\\nConfusion matrices:")
    for row in all_results: print(row["disease"], row["model"], row["confusion_matrix"])
    print("\\nSaved best models in", OUT)
