from pydantic import BaseModel
from typing import Union

class ItemCreate(BaseModel) : 
    name:str
    sell_in: int 
    quality: int 

class ItemUpdate(BaseModel) : 
    sell_in: Union[None, int]
    quality: Union[None, int]

class ItemResponse(BaseModel) : 
    id: int 
    name:str 
    sell_in:int 
    quality:int


