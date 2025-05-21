from sqlmodel import Field,Session,SQLModel,create_engine,select,Field, Relationship
from enum import Enum
import datetime

from typing import Optional



from datetime import date

#user
#-------------------------------------------------------------------------------------------------------------------------------|


class RoleEnum(str,Enum):

    admin =     'admin'     #Enter new item,update,archive
    employee =  'employee'    #Edit
    viewer =    'viewer'    #read-only
    
    def __self__(self):
        return self.value



class User(SQLModel,table=True):
    #Name           #Type 
    id:             int                  = Field(default=None,primary_key=True)
    username:       str                  = Field(index=True,unique=True)

    #bcrypt hash  for password
    password:        str                 = Field()
    role:            RoleEnum            = Field(default=RoleEnum.admin)


    image_url:       str                 = Field(default=None, max_length=512)

#-----------------------------------------------------------------------------------------------------------------------------------------#



#Menu
#-------------------------------------------------------------------------------------------------------------------------------|
class CategoryMenuEnum(str,Enum):

    Main_Course = 'Main_Course'
    Seafood = 'Seafood'
    Pasta = 'Pasta'
    Beverages = 'Beverages'
    Salad   = 'Salad'
    Pizza   = 'Pizza'
    Dessert = 'Dessert'
    
    def __str__(self):
        return self.value

    
class Menu_List(SQLModel,table=True):
    #Name           #Type                   # field                                          #Admin      #Employee     #Viewer
    id:             int                     = Field(default=None,primary_key=True)           #Visible    #Visible      #Hide    
    quantity:       int                     = Field(nullable=False)                          #Visible    #Visible      #Hide
    price:          float                   = Field(nullable=False,)                         #Visible    #Visible      #Visible

    category:      CategoryMenuEnum         = Field()    

    name:           str                     = Field(nullable=False,max_length=56)            #Visible    #Visible      #Visible
    description:    str                     = Field(nullable=False,max_length=56)            #Visible    #Visible      #Visible


    image_url:      str                     = Field(default=None, max_length=512)           #Visible     #Visible      #Visible

    orders:         list['Order_list']      = Relationship(back_populates='menu')           #Visible     #Visible      #Hide

    is_archive:     bool                    = Field(default=False)                           #Visible     #Hide        #Hide
   
    def __str__(self):
        return self.name
#-------------------------------------------------------------------------------------------------------------------------------|




#Order
#-------------------------------------------------------------------------------------------------------------------------------|

class TableEnum(str, Enum): 

    table1 = 'table1'
    table2 = 'table2'
    table3 = 'table3'
    table4 = 'table4'
    table5 = 'table5'

class Order_list(SQLModel, table=True):
    
    id:             int                     = Field(default=None, primary_key=True)
    menu_id:        int                     = Field(foreign_key='menu_list.id')
    quantity:       int                     = Field(nullable=False)
    total:          float                   = Field(nullable=False)
    table:          TableEnum               = Field(nullable=False)

    #order_date:     datetime.date           = Field(default_factory=datetime.date.today)
    # relationship to Menu_List
    menu: Optional["Menu_List"] = Relationship(back_populates="orders")
    income: Optional["Income_table"] = Relationship(back_populates="order")
#------------------------------------------------------------------------------------------------------

class PaymentEnum(str,Enum):
    Cash =   'Cash'
    Online = 'Online'

    # force  it  value when seeing the front end
    def __str__(self):
        return self.value


class Income_table(SQLModel, table=True):

    id:             int                     = Field(default=None, primary_key=True)
    order_id:       int                     = Field(foreign_key='order_list.id')
    order_date:     datetime.date           = Field(default_factory=datetime.date.today)
    income:         float                   = Field(nullable=False)
    payment_type:   PaymentEnum             = Field()
    image_url:       str                    = Field(default='/static/payment/')
    order_list_item: str                    = Field()
    # relationship to Menu_List
    order: Optional[Order_list] = Relationship(back_populates="income")
    
#kitchen
#------------------------------------------------------------------------------------------------------
class UnitEnum(str,Enum):
    kg = 'kg'
    g = 'g'
    pcs = 'pcs'
    L = 'L'

    # force  it  value when seeing the front end
    def __str__(self):
        return self.value


class CategoryEnum(str,Enum):
    Dairy = 'Dairy'
    Seafood = 'Seafood'
    Spices = 'Spices'
    Meat = 'Meat'
    Beverages = 'Beverages'
    
    def __str__(self):
        return self.value


class Kitchen_Stock(SQLModel,table=True):

    #Name           #Type                # field                                          #Admin      #Employee     #Viewer
    id:             int                  = Field(default=None,primary_key=True)           #Visible    #Visible      #HIDE
    quantity:       int                  = Field()                                        #Visible    #Visible      #Visible
    price:          float                = Field()                                        #Visible    #Visible      #Visible

    category:       CategoryEnum         = Field()                                        #Visible    #Visible      #Visible

    batch_code:     str                  = Field(nullable=False,max_length=6,unique=True) #Visible    #Visible      #HIDE
    name:           str                  = Field(nullable=False, max_length=56)           #Visible    #Visible      #Visible

    unit:           UnitEnum             = Field()                                        #Visible    #Visible      #Visible

    delivery_date:  datetime.date        = Field(default=date.today())                    #Visible    #Visible      #HIDE
    spoilage_date:  datetime.date        = Field()                                        #Visible    #Visible      #HIDE

    # i add this so we could hide the item 
    is_archive:     bool                 = Field(default=False)                           #Visible     #Hide        #Hide




engine = create_engine('sqlite:///model.db')
SQLModel.metadata.create_all(engine)



