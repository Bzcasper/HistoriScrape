from pydantic import BaseModel, Field
from typing import List, Optional, Dict


class SubstituteRequest(BaseModel):
    original_ingredient: str = Field(..., example="butter")
    recipe_context: List[str] = Field(..., example=["flour", "sugar", "eggs", "milk"])
    dietary_restrictions: Optional[List[str]] = Field(None, example=["vegan"])
    available_ingredients: Optional[List[str]] = Field(
        None, example=["coconut oil", "applesauce"]
    )


class SubstituteAttributes(BaseModel):
    flavor_profile: Optional[str]
    texture: Optional[str]
    nutritional_info: Optional[Dict[str, str]]


class SubstituteOption(BaseModel):
    name: str
    reason: str
    attributes: SubstituteAttributes


class SubstituteResponse(BaseModel):
    status: str
    substitutions: List[SubstituteOption]
