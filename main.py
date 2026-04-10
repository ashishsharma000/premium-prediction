from pydantic import BaseModel,Field,computed_field
import pickle
from typing import Annotated,Literal
from fastapi import FastAPI
import pandas as pd
import uvicorn


with open('insurance_pipeline.pkl', 'rb') as f:
    loaded_pipeline = pickle.load(f)

app = FastAPI()



class insurance(BaseModel):

    age:Annotated['int',Field(...,gt=0,lt=120, description="enter the age")]
    sex:Annotated[Literal['male','female'],Field(...,description="enter the gender")]
    height: Annotated['float',Field(...,gt=0,lt=2.5,description="wright in mtr")]
    weight: Annotated['float',Field(...,gt=10,lt=150,description="weight in kgs")]
    children:Annotated['int',Field(...,lt=4,description="how many children you have")]
    smoker:Annotated[Literal['yes','no'],Field(...,description="do you smoke")]
    region:Annotated['str',Field(...,description="enter you region")]
    

    @computed_field
    @property
    def bmi(self) -> float:
        return round(self.weight/((self.height/100)**2),2)



@app.post('/predict')
def predict_premium(data:insurance):

    input_dict = data.model_dump()

    input_dict.pop('weight')
    input_dict.pop('height')

    df = pd.DataFrame([input_dict])

    prediction = loaded_pipeline.predict(df)

    return {"estimated_premium": float(prediction[0])}