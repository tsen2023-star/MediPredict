from django import forms

# --- PARAMETER EXPLANATIONS & CHOICES ---

SEX_CHOICES = [
    (1, "Male"),
    (0, "Female"),
]

CHEST_PAIN_CHOICES = [
    (0, "0: Typical Angina (chest pain related to decreased blood supply)"),
    (1, "1: Atypical Angina (chest pain not typical of heart disease)"),
    (2, "2: Non-Anginal Pain (typically esophageal spasms or muscle pain)"),
    (3, "3: Asymptomatic (silent or no typical chest pain)"),
]

FBS_CHOICES = [
    (0, "No (<= 120 mg/dl - Normal)"),
    (1, "Yes (> 120 mg/dl - Elevated)"),
]

RESTECG_CHOICES = [
    (0, "0: Normal ECG"),
    (1, "1: ST-T Wave Abnormality (T wave inversions or ST depression)"),
    (2, "2: Left Ventricular Hypertrophy (enlargement of heart's pumping chamber)"),
]

EXANG_CHOICES = [
    (0, "No - No chest pain during exercise"),
    (1, "Yes - Chest pain induced by exertion"),
]

SLOPE_CHOICES = [
    (0, "0: Upsloping (normal response to exercise)"),
    (1, "1: Flat (suggestive of myocardial ischemia)"),
    (2, "2: Downsloping (unhealthy heart indicator)"),
]

CA_CHOICES = [
    (0, "0 major vessels colored"),
    (1, "1 major vessel colored"),
    (2, "2 major vessels colored"),
    (3, "3 major vessels colored"),
    (4, "4 major vessels colored"),
]

THAL_CHOICES = [
    (0, "0: Normal blood flow"),
    (1, "1: Fixed Defect (no blood flow in some part)"),
    (2, "2: Reversible Defect (blood flow observed but abnormal)"),
    (3, "3: Unknown / Other"),
]

GENDER_CHOICES = [
    (1, "Male"),
    (0, "Female"),
]


class HeartForm(forms.Form):
    age = forms.FloatField(
        label="Age (Years)",
        min_value=1,
        max_value=120,
        widget=forms.NumberInput(attrs={"class": "form-control", "placeholder": "e.g. 54"}),
        help_text="Patient age between 1 and 120 years."
    )
    sex = forms.TypedChoiceField(
        label="Biological Sex",
        choices=SEX_CHOICES,
        coerce=int,
        widget=forms.Select(attrs={"class": "form-select"}),
        help_text="Biological sex at birth."
    )
    cp = forms.TypedChoiceField(
        label="Chest Pain Type (cp)",
        choices=CHEST_PAIN_CHOICES,
        coerce=int,
        widget=forms.Select(attrs={"class": "form-select"}),
        help_text="Type of chest discomfort experienced."
    )
    trestbps = forms.FloatField(
        label="Resting Blood Pressure (mm Hg)",
        min_value=50,
        max_value=250,
        widget=forms.NumberInput(attrs={"class": "form-control", "placeholder": "e.g. 130"}),
        help_text="Resting arterial blood pressure in mm Hg upon hospital admission (typical normal is 90-120)."
    )
    chol = forms.FloatField(
        label="Serum Cholesterol (mg/dl)",
        min_value=80,
        max_value=700,
        widget=forms.NumberInput(attrs={"class": "form-control", "placeholder": "e.g. 240"}),
        help_text="Total serum cholesterol level (desirable is under 200 mg/dl)."
    )
    fbs = forms.TypedChoiceField(
        label="Fasting Blood Sugar > 120 mg/dl",
        choices=FBS_CHOICES,
        coerce=int,
        widget=forms.Select(attrs={"class": "form-select"}),
        help_text="Blood sugar measured after overnight fasting (greater than 120 mg/dl suggests pre-diabetes or diabetes)."
    )
    restecg = forms.TypedChoiceField(
        label="Resting Electrocardiographic Results",
        choices=RESTECG_CHOICES,
        coerce=int,
        widget=forms.Select(attrs={"class": "form-select"}),
        help_text="Resting ECG findings."
    )
    thalach = forms.FloatField(
        label="Maximum Heart Rate Achieved (bpm)",
        min_value=50,
        max_value=250,
        widget=forms.NumberInput(attrs={"class": "form-control", "placeholder": "e.g. 150"}),
        help_text="Peak heart rate reached during treadmill stress testing."
    )
    exang = forms.TypedChoiceField(
        label="Exercise-Induced Angina",
        choices=EXANG_CHOICES,
        coerce=int,
        widget=forms.Select(attrs={"class": "form-select"}),
        help_text="Whether chest pain is triggered by physical exercise."
    )
    oldpeak = forms.FloatField(
        label="ST Depression Induced by Exercise (oldpeak)",
        min_value=0.0,
        max_value=10.0,
        widget=forms.NumberInput(attrs={"class": "form-control", "step": "0.1", "placeholder": "e.g. 1.5"}),
        help_text="ST depression measured in mm relative to rest on ECG during stress test."
    )
    slope = forms.TypedChoiceField(
        label="Slope of Peak Exercise ST Segment",
        choices=SLOPE_CHOICES,
        coerce=int,
        widget=forms.Select(attrs={"class": "form-select"}),
        help_text="The slope of the peak exercise ST segment."
    )
    ca = forms.TypedChoiceField(
        label="Major Vessels Colored by Fluoroscopy (0-4)",
        choices=CA_CHOICES,
        coerce=int,
        widget=forms.Select(attrs={"class": "form-select"}),
        help_text="Number of major vessels (0 to 4) visualized through fluoroscopy."
    )
    thal = forms.TypedChoiceField(
        label="Thallium Stress Result (thal)",
        choices=THAL_CHOICES,
        coerce=int,
        widget=forms.Select(attrs={"class": "form-select"}),
        help_text="Nuclear stress test result assessing blood perfusion."
    )


class LiverForm(forms.Form):
    age = forms.FloatField(
        label="Age (Years)",
        min_value=1,
        max_value=120,
        widget=forms.NumberInput(attrs={"class": "form-control", "placeholder": "e.g. 45"}),
        help_text="Patient age in years."
    )
    gender = forms.TypedChoiceField(
        label="Gender",
        choices=GENDER_CHOICES,
        coerce=int,
        widget=forms.Select(attrs={"class": "form-select"}),
        help_text="Patient gender."
    )
    total_bilirubin = forms.FloatField(
        label="Total Bilirubin (mg/dL)",
        min_value=0.1,
        max_value=100.0,
        widget=forms.NumberInput(attrs={"class": "form-control", "step": "0.1", "placeholder": "e.g. 1.2"}),
        help_text="Total bilirubin level (normal adult range is 0.1 to 1.2 mg/dL)."
    )
    direct_bilirubin = forms.FloatField(
        label="Direct Bilirubin (mg/dL)",
        min_value=0.0,
        max_value=50.0,
        widget=forms.NumberInput(attrs={"class": "form-control", "step": "0.1", "placeholder": "e.g. 0.4"}),
        help_text="Conjugated bilirubin level (normal range is 0.0 to 0.3 mg/dL)."
    )
    alkaline_phosphotase = forms.FloatField(
        label="Alkaline Phosphatase - ALP (IU/L)",
        min_value=10.0,
        max_value=3000.0,
        widget=forms.NumberInput(attrs={"class": "form-control", "placeholder": "e.g. 210"}),
        help_text="Enzyme related to bile ducts; normal adult range is 44 to 147 IU/L."
    )
    alamine_aminotransferase = forms.FloatField(
        label="Alamine Aminotransferase - ALT / SGPT (IU/L)",
        min_value=1.0,
        max_value=3000.0,
        widget=forms.NumberInput(attrs={"class": "form-control", "placeholder": "e.g. 35"}),
        help_text="Key liver enzyme; normal range is typically 7 to 56 IU/L."
    )
    aspartate_aminotransferase = forms.FloatField(
        label="Aspartate Aminotransferase - AST / SGOT (IU/L)",
        min_value=1.0,
        max_value=3000.0,
        widget=forms.NumberInput(attrs={"class": "form-control", "placeholder": "e.g. 40"}),
        help_text="Enzyme found in liver and muscles; normal range is typically 10 to 40 IU/L."
    )
    total_proteins = forms.FloatField(
        label="Total Proteins (g/dL)",
        min_value=1.0,
        max_value=20.0,
        widget=forms.NumberInput(attrs={"class": "form-control", "step": "0.1", "placeholder": "e.g. 6.8"}),
        help_text="Total serum protein; normal range is 6.0 to 8.3 g/dL."
    )
    albumin = forms.FloatField(
        label="Albumin (g/dL)",
        min_value=0.5,
        max_value=10.0,
        widget=forms.NumberInput(attrs={"class": "form-control", "step": "0.1", "placeholder": "e.g. 3.4"}),
        help_text="Protein synthesized exclusively by the liver; normal range is 3.5 to 5.0 g/dL."
    )
    albumin_and_globulin_ratio = forms.FloatField(
        label="Albumin / Globulin Ratio (A/G Ratio)",
        min_value=0.1,
        max_value=10.0,
        widget=forms.NumberInput(attrs={"class": "form-control", "step": "0.01", "placeholder": "e.g. 1.0"}),
        help_text="Ratio of albumin to globulins; normal range is generally 1.0 to 2.2."
    )


class DiabetesForm(forms.Form):
    pregnancies = forms.FloatField(
        label="Number of Pregnancies",
        min_value=0,
        max_value=25,
        widget=forms.NumberInput(attrs={"class": "form-control", "placeholder": "e.g. 2"}),
        help_text="Total number of times pregnant (enter 0 for males or no pregnancies)."
    )
    glucose = forms.FloatField(
        label="Plasma Glucose Concentration (mg/dL)",
        min_value=40.0,
        max_value=400.0,
        widget=forms.NumberInput(attrs={"class": "form-control", "placeholder": "e.g. 120"}),
        help_text="2-hour oral glucose tolerance test concentration (normal fasting is 70-99 mg/dL; post-meal < 140 mg/dL)."
    )
    blood_pressure = forms.FloatField(
        label="Diastolic Blood Pressure (mm Hg)",
        min_value=30.0,
        max_value=200.0,
        widget=forms.NumberInput(attrs={"class": "form-control", "placeholder": "e.g. 75"}),
        help_text="Diastolic arterial pressure in mm Hg (healthy resting is typically 60-80 mm Hg)."
    )
    skin_thickness = forms.FloatField(
        label="Triceps Skinfold Thickness (mm)",
        min_value=0.0,
        max_value=120.0,
        widget=forms.NumberInput(attrs={"class": "form-control", "placeholder": "e.g. 23"}),
        help_text="Measurement used to estimate subcutaneous body fat (average is 15-25 mm)."
    )
    insulin = forms.FloatField(
        label="2-Hour Serum Insulin (mu U/ml)",
        min_value=0.0,
        max_value=900.0,
        widget=forms.NumberInput(attrs={"class": "form-control", "placeholder": "e.g. 85"}),
        help_text="Insulin level 2 hours after glucose administration (normal fasting is 2-25 mu U/ml)."
    )
    bmi = forms.FloatField(
        label="Body Mass Index - BMI (kg/m²)",
        min_value=10.0,
        max_value=70.0,
        widget=forms.NumberInput(attrs={"class": "form-control", "step": "0.1", "placeholder": "e.g. 26.5"}),
        help_text="Weight in kilograms divided by the square of height in meters (18.5-24.9 is normal range)."
    )
    diabetes_pedigree_function = forms.FloatField(
        label="Diabetes Pedigree Function",
        min_value=0.05,
        max_value=3.0,
        widget=forms.NumberInput(attrs={"class": "form-control", "step": "0.01", "placeholder": "e.g. 0.45"}),
        help_text="Genetic score calculating family history risk of diabetes (higher scores mean higher familial predisposition)."
    )
    age = forms.FloatField(
        label="Age (Years)",
        min_value=1,
        max_value=120,
        widget=forms.NumberInput(attrs={"class": "form-control", "placeholder": "e.g. 38"}),
        help_text="Patient age in years."
    )


SG_CHOICES = [
    (1.005, "1.005"),
    (1.010, "1.010"),
    (1.015, "1.015"),
    (1.020, "1.020"),
    (1.025, "1.025"),
]

ALBUMIN_CHOICES = [
    (0, "0: None / Normal"),
    (1, "1: Trace (Mild)"),
    (2, "2: Moderate"),
    (3, "3: Heavy"),
    (4, "4: Very Heavy"),
    (5, "5: Severe"),
]

SUGAR_CHOICES = [
    (0, "0: None / Normal"),
    (1, "1: Trace (Mild)"),
    (2, "2: Moderate"),
    (3, "3: High"),
    (4, "4: Very High"),
    (5, "5: Severe"),
]


class KidneyForm(forms.Form):
    age = forms.FloatField(
        label="Age (Years)",
        min_value=1,
        max_value=120,
        widget=forms.NumberInput(attrs={"class": "form-control", "placeholder": "e.g. 48"}),
        help_text="Patient age in years."
    )
    bp = forms.FloatField(
        label="Blood Pressure (mm/Hg)",
        min_value=40.0,
        max_value=220.0,
        widget=forms.NumberInput(attrs={"class": "form-control", "placeholder": "e.g. 80"}),
        help_text="Diastolic blood pressure reading (normal is 60-80 mm/Hg)."
    )
    sg = forms.TypedChoiceField(
        label="Specific Gravity (sg)",
        choices=SG_CHOICES,
        coerce=float,
        widget=forms.Select(attrs={"class": "form-select"}),
        help_text="Urine specific gravity measurement."
    )
    al = forms.TypedChoiceField(
        label="Albumin in Urine (al)",
        choices=ALBUMIN_CHOICES,
        coerce=int,
        widget=forms.Select(attrs={"class": "form-select"}),
        help_text="Protein levels detected in routine urinalysis."
    )
    su = forms.TypedChoiceField(
        label="Sugar in Urine (su)",
        choices=SUGAR_CHOICES,
        coerce=int,
        widget=forms.Select(attrs={"class": "form-select"}),
        help_text="Glucose detected in urine sample."
    )
    bgr = forms.FloatField(
        label="Random Blood Glucose (mg/dL)",
        min_value=40.0,
        max_value=500.0,
        widget=forms.NumberInput(attrs={"class": "form-control", "placeholder": "e.g. 120"}),
        help_text="Random plasma glucose reading (normal non-fasting is typically < 140 mg/dL)."
    )
    bu = forms.FloatField(
        label="Blood Urea (mg/dL)",
        min_value=1.0,
        max_value=400.0,
        widget=forms.NumberInput(attrs={"class": "form-control", "placeholder": "e.g. 36"}),
        help_text="Waste product filtered by kidneys; normal range is 7 to 20 mg/dL."
    )
    sc = forms.FloatField(
        label="Serum Creatinine (mg/dL)",
        min_value=0.1,
        max_value=25.0,
        widget=forms.NumberInput(attrs={"class": "form-control", "step": "0.1", "placeholder": "e.g. 1.2"}),
        help_text="Key kidney filtration marker (normal adult range is 0.6 to 1.3 mg/dL)."
    )
    sod = forms.FloatField(
        label="Serum Sodium (mEq/L)",
        min_value=80.0,
        max_value=180.0,
        widget=forms.NumberInput(attrs={"class": "form-control", "placeholder": "e.g. 138"}),
        help_text="Blood sodium electrolyte level; normal range is 135 to 145 mEq/L."
    )
    pot = forms.FloatField(
        label="Serum Potassium (mEq/L)",
        min_value=1.5,
        max_value=15.0,
        widget=forms.NumberInput(attrs={"class": "form-control", "step": "0.1", "placeholder": "e.g. 4.4"}),
        help_text="Potassium electrolyte level; normal range is 3.5 to 5.0 mEq/L."
    )
    hemo = forms.FloatField(
        label="Hemoglobin (g/dL)",
        min_value=3.0,
        max_value=25.0,
        widget=forms.NumberInput(attrs={"class": "form-control", "step": "0.1", "placeholder": "e.g. 14.5"}),
        help_text="Hemoglobin level in blood; normal range is 12 to 17 g/dL."
    )


class BreastCancerForm(forms.Form):
    radius_mean = forms.FloatField(
        label="Mean Radius (mm)",
        min_value=5.0,
        max_value=35.0,
        widget=forms.NumberInput(attrs={"class": "form-control", "step": "0.01", "placeholder": "e.g. 14.12"}),
        help_text="Mean of distances from cell nucleus center to points on perimeter."
    )
    texture_mean = forms.FloatField(
        label="Mean Texture",
        min_value=8.0,
        max_value=45.0,
        widget=forms.NumberInput(attrs={"class": "form-control", "step": "0.01", "placeholder": "e.g. 19.28"}),
        help_text="Standard deviation of gray-scale values in the cell nucleus image."
    )
    perimeter_mean = forms.FloatField(
        label="Mean Perimeter (mm)",
        min_value=40.0,
        max_value=250.0,
        widget=forms.NumberInput(attrs={"class": "form-control", "step": "0.1", "placeholder": "e.g. 91.96"}),
        help_text="Mean perimeter length of the core cell nucleus."
    )
    area_mean = forms.FloatField(
        label="Mean Area (mm²)",
        min_value=100.0,
        max_value=3000.0,
        widget=forms.NumberInput(attrs={"class": "form-control", "step": "0.1", "placeholder": "e.g. 654.8"}),
        help_text="Mean area of the cell nucleus."
    )
    smoothness_mean = forms.FloatField(
        label="Mean Smoothness",
        min_value=0.04,
        max_value=0.25,
        widget=forms.NumberInput(attrs={"class": "form-control", "step": "0.001", "placeholder": "e.g. 0.096"}),
        help_text="Local variation in radius lengths."
    )
    compactness_mean = forms.FloatField(
        label="Mean Compactness",
        min_value=0.01,
        max_value=0.50,
        widget=forms.NumberInput(attrs={"class": "form-control", "step": "0.001", "placeholder": "e.g. 0.104"}),
        help_text="Computed as (perimeter^2 / area - 1.0)."
    )
    concavity_mean = forms.FloatField(
        label="Mean Concavity",
        min_value=0.0,
        max_value=0.60,
        widget=forms.NumberInput(attrs={"class": "form-control", "step": "0.001", "placeholder": "e.g. 0.088"}),
        help_text="Severity of concave portions of the nucleus contour."
    )
    concave_points_mean = forms.FloatField(
        label="Mean Concave Points",
        min_value=0.0,
        max_value=0.30,
        widget=forms.NumberInput(attrs={"class": "form-control", "step": "0.001", "placeholder": "e.g. 0.048"}),
        help_text="Number of concave portions of the contour."
    )
    symmetry_mean = forms.FloatField(
        label="Mean Symmetry",
        min_value=0.08,
        max_value=0.40,
        widget=forms.NumberInput(attrs={"class": "form-control", "step": "0.001", "placeholder": "e.g. 0.181"}),
        help_text="Symmetry measurement of the nucleus."
    )
    fractal_dimension_mean = forms.FloatField(
        label="Mean Fractal Dimension",
        min_value=0.03,
        max_value=0.15,
        widget=forms.NumberInput(attrs={"class": "form-control", "step": "0.001", "placeholder": "e.g. 0.062"}),
        help_text="Coastline approximation measurement - 1."
    )

