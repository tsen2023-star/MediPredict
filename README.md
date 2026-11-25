# Multiple Disease Prediction System (website)

## Important medical and technical note
This is an educational starter application for preliminary model-output awareness. It is not a medical device, diagnostic service, or substitute for professional care. The displayed score is the model's positive-class probability, not a validated individual clinical probability. Do not use it to delay care or make treatment decisions. A real deployment requires clinical validation, privacy/security review, and qualified medical oversight.

## 1. Create environment and install
Windows PowerShell:
```powershell
py -m venv venv
.\venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
pip install -r requirements.txt
```
If PowerShell blocks activation, run `Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass` for that terminal, then activate again.

## 2. Configure datasets and train
Download the relevant Kaggle CSV datasets yourself and place them in `datasets/` using:
- `heart.csv` (target column default: `target`)
- `liver.csv` (target column default: `Dataset`)
- `diabetes.csv` (target column default: `Outcome`)

Check the exact column names, target labels, class meaning, and feature units in the versions you downloaded. Edit `FILES` and the column mapping in `prediction/ml/train_models.py` if needed. The HTML forms and trained model must use identical feature definitions and order. Run from the project root:
```powershell
python prediction/ml/train_models.py
```
This saves the three `.pkl` model bundles beside the script. The training script evaluates Random Forest, KNN and XGBoost (if installed) and selects the best ROC-AUC model.

## 3. Database and admin
```powershell
python manage.py makemigrations accounts prediction hospitals feedback
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
```
Open `http://127.0.0.1:8000/` and the admin at `http://127.0.0.1:8000/admin/`. Add hospital records in admin.

## 4. Pages
- `/` home
- `/accounts/register/`, `/accounts/login/`, `/accounts/logout/`
- `/dashboard/`
- `/predict/heart/`, `/predict/liver/`, `/predict/diabetes/`
- `/hospitals/`, `/chatbot/`, `/feedback/`

## 5. Before any real use
The three datasets often differ in feature names, coding, missing-value conventions, and target semantics. The included training loader is a baseline and may need dataset-specific cleaning (notably liver gender and class labels, and zero-as-missing conventions in diabetes). Verify each dataset carefully. Do not present model scores as a diagnosis. Add automated tests, rate limiting, secure production settings, HTTPS, a privacy notice, retention policy, and professional validation before deployment. SQLite is configured for local development; Django can be configured for MSSQL later with a compatible backend.
