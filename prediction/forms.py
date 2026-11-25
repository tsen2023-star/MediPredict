from django import forms

HEART = [
 ("age","Age",1,120),("sex","Sex (1=male, 0=female)",0,1),
 ("cp","Chest pain type (0-3)",0,3),("trestbps","Resting blood pressure",50,250),
 ("chol","Cholesterol",80,700),("fbs","Fasting blood sugar >120 (1=yes)",0,1),
 ("restecg","Resting ECG (0-2)",0,2),("thalach","Maximum heart rate",50,250),
 ("exang","Exercise-induced angina (1=yes)",0,1),("oldpeak","Oldpeak",0,10),
 ("slope","Slope (0-2)",0,2),("ca","Major vessels (0-4)",0,4),("thal","Thalassemia (0-3)",0,3)
]
LIVER = [
 ("age","Age",1,120),("gender","Gender (1=male, 0=female)",0,1),
 ("total_bilirubin","Total bilirubin",0,100),("direct_bilirubin","Direct bilirubin",0,100),
 ("alkaline_phosphotase","Alkaline phosphatase",0,3000),("alamine_aminotransferase","SGPT",0,3000),
 ("aspartate_aminotransferase","SGOT",0,3000),("total_proteins","Total proteins",0,20),
 ("albumin","Albumin",0,20),("albumin_and_globulin_ratio","Albumin/globulin ratio",0,10)
]
DIABETES = [
 ("pregnancies","Pregnancies",0,30),("glucose","Glucose",0,500),("blood_pressure","Blood pressure",0,300),
 ("skin_thickness","Skin thickness",0,150),("insulin","Insulin",0,3000),("bmi","BMI",0,100),
 ("diabetes_pedigree_function","Diabetes pedigree function",0,5),("age","Age",1,120)
]

def make_form(fields):
    attrs = {}
    for key, label, low, high in fields:
        attrs[key] = forms.FloatField(label=label, min_value=low, max_value=high,
                                      widget=forms.NumberInput(attrs={"class":"form-control", "step":"any"}))
    return type("DiseaseInputForm", (forms.Form,), attrs)

HeartForm = make_form(HEART)
LiverForm = make_form(LIVER)
DiabetesForm = make_form(DIABETES)
