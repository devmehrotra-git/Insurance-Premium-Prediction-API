from pydantic import BaseModel, Field, computed_field, field_validator
from typing import Annotated, Literal
from config.city_tier import tier_1_cities,tier_2_cities


#pydantic model to validate incoming data    
class UserInput(BaseModel):
    age:Annotated[int, Field(..., description='Age of the user',gt=0,lt=120)] 
    weight:Annotated[float,Field(..., description='Weight of the user',gt=0)] 
    height:Annotated[float,Field(..., description='Height of the user',gt=0)]  
    income_lpa:Annotated[float,Field(..., description='Annual Income of the user in lpa',gt=0)]
    smoker:Annotated[bool,Field(...,description='Is the user a smoker?',examples=[False])]
    city:Annotated[str,Field(...,description='City of the User')]
    occupation:Annotated[Literal['retired', 'freelancer', 'student', 'government_job',
       'business_owner', 'unemployed', 'private_job'],Field(...,description='Occupation of the user')]
    
    @field_validator('city')
    @classmethod
    def normalize_city(cls,v:str)->str:
        return v.strip().title()
    
    @computed_field
    @property
    def bmi(self)->float:
        return self.weight/(self.height**2)
    
    @computed_field
    @property
    def lifestyle_risk(self) -> str:
        if self.smoker and self.bmi > 30:
            return "high"
        elif self.smoker or self.bmi > 27:
            return "medium"
        else:
            return "low"
        
    @computed_field
    @property
    def age_group(self)->str:
        if self.age < 25:
            return "young"
        elif self.age < 45:
            return "adult"
        elif self.age < 60:
            return "middle_aged"
        return "senior"    
    
    @computed_field
    @property
    def city_tier(self)->int:
        if self.city in tier_1_cities:
            return 1
        elif self.city in tier_2_cities:
            return 2
        else:
            return 3