from fastapi import FastAPI
from pydantic import BaseModel as PydanticBaseModel
import joblib
import pandas as pd
from cleaning import clean 
from sklearn.preprocessing import FunctionTransformer

app = FastAPI()

cleaner = FunctionTransformer(clean, validate=False)

trained_model = joblib.load('model.pkl')

class ObesityFeat(PydanticBaseModel):
    gender: str
    age: int
    height: float
    weight: float
    family_history_overweight: str
    high_calorie_food: str
    vegetable_freq: float
    main_meals_per_day: float
    snack_freq: str
    smoke: str
    water_intake: float
    calorie_monitoring: str
    physical_activity: float
    tech_time: float
    alcohol_freq: str
    transport_mode: str

@app.get("/")
def read_root():
    return {"message": "Welcome to the Obesity Level Prediction API"}

@app.post('/predict')
def predict_obesity(data: ObesityFeat):
    try : 
        input_df = pd.DataFrame([data.dict()])

        for col in input_df.select_dtypes(include='object').columns:
            input_df[col] = input_df[col].str.lower()
                
        prediction = trained_model.predict(input_df)
        return {"prediction": prediction[0]}

    except Exception as e:
        return {"error": str(e)}
        
    


