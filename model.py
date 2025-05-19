from sqlmodel import Field,Session,SQLModel,create_engine,select
from enum import Enum
import datetime

from sqlmodel import Session
from datetime import date





class User(SQLModel,table=True):



#--------Table_List----------#

class UnitEnum(str,Enum):
    kg = 'kg'
    g = 'g'
    pcs = 'pcs'
    liter = 'liters'

    # force  it  value when seeing the front end
    def __str__(self):
        return self.value
    
class CategoryEnum(str,Enum):
    Dairy = 'Dairy'
    Seafood = 'Seafood'
    Spices = 'Spices'
    Meat = 'Meat'
    Beverage = 'Beverage'
    
    def __str__(self):
        return self.value
    
class Menu_List(SQLModel,table=True):
    #Name           #Type 
    id:             int                  = Field(default=None,primary_key=True)
    quantity:       int                  = Field(nullable=False)
    price:          float                = Field(nullable=False,)

    name:           str                  = Field(nullable=False,max_length=56)
    description:    str                  = Field(nullable=False,max_length=56)

    image_url:      str                  = Field(default=None, max_length=512)

class Kitchen_Stock(SQLModel,table=True):

    #Name           #Type                
    id:             int                  = Field(default=None,primary_key=True)
    quantity:       int                  = Field()
    price:          float                = Field()

    category:       CategoryEnum         = Field()

    batch_code:     str                  = Field(nullable=False,max_length=6,unique=True)
    name:           str                  = Field(nullable=False, max_length=56)

    unit:           UnitEnum             = Field()

    delivery_date:  datetime.date        = Field(default=date.today()) 
    spoilage_date:  datetime.date        = Field() 

    # i add this so we could hide the item 
    is_archive:     bool                 = Field(default=False)





engine = create_engine('sqlite:///model.db')
SQLModel.metadata.create_all(engine)



