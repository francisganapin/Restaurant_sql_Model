from sqlmodel import Field,Session,SQLModel,create_engine,select,Field, Relationship
from enum import Enum
import datetime

from typing import Optional


<<<<<<< HEAD
from datetime import date




                                                #Restaurant System
=======

from datetime import date

#user
>>>>>>> d60a0ea3c3fb8b17f990453c660e083d67c99676
#-------------------------------------------------------------------------------------------------------------------------------|


class RoleEnum(str,Enum):

<<<<<<< HEAD
    ADMIN =     'ADMIN'     #Enter new item,update,archive
    EMPLOYEE =  'EMPLOYEE'  #Edit
    VIEWER =    'VIEWER'    #read-only
=======
    admin =     'admin'     #Enter new item,update,archive
    employee =  'employee'    #Edit
    viewer =    'viewer'    #read-only
>>>>>>> d60a0ea3c3fb8b17f990453c660e083d67c99676
    
    def __self__(self):
        return self.value



class User(SQLModel,table=True):
    #Name           #Type 
    id:             int                  = Field(default=None,primary_key=True)
    username:       str                  = Field(index=True,unique=True)

    #bcrypt hash  for password
    password:        str                 = Field()
<<<<<<< HEAD
    role:            RoleEnum            = Field(default=RoleEnum.ADMIN)

    image_url:       str                 = Field(default=None, max_length=512)


#-----------------------------------------------------------------------------------------------------------------------------------------#


#Menu
#-------------------------------------------------------------------------------------------------------------------------------|

class CategoryMenuEnum(str,Enum):

    MAIN_COURSE = 'MAIN_COURSE'
    SEAFOOD     = 'SEAFOOD'
    PASTA       = 'PASTA'
    BEVERAGES   = 'BEVERAGES' 
    SALAD       = 'SALAD'
    PIZZA       = 'PIZZA'
    DESSERT     = 'DESSERT'

=======
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
>>>>>>> d60a0ea3c3fb8b17f990453c660e083d67c99676
    
    def __str__(self):
        return self.value

    
class Menu_List(SQLModel,table=True):
<<<<<<< HEAD
    # Field Name     | Type                                               |      Visibility:   Admin   | Employee    | Viewer
    # -------------- | --------- | ----------------- | -------- | --------                                              
=======
    #Name           #Type                   # field                                          #Admin      #Employee     #Viewer
>>>>>>> d60a0ea3c3fb8b17f990453c660e083d67c99676
    id:             int                     = Field(default=None,primary_key=True)           #Visible    #Visible      #Hide    
    quantity:       int                     = Field(nullable=False)                          #Visible    #Visible      #Hide
    price:          float                   = Field(nullable=False,)                         #Visible    #Visible      #Visible

<<<<<<< HEAD
    category:       CategoryMenuEnum         = Field()    
=======
    category:      CategoryMenuEnum         = Field()    
>>>>>>> d60a0ea3c3fb8b17f990453c660e083d67c99676

    name:           str                     = Field(nullable=False,max_length=56)            #Visible    #Visible      #Visible
    description:    str                     = Field(nullable=False,max_length=56)            #Visible    #Visible      #Visible


<<<<<<< HEAD
    image_url:      str                     = Field(default=None, max_length=512)            #Visible     #Visible      #Visible

    orders:         list['Order_List']       = Relationship(back_populates='menu')           #Visible     #Visible     #Hide

    is_archive:     bool                    = Field(default=False)                           #Visible      #Hide         #Hide    When this was hide they wont see it to front end
    
    #created_at: datetime = Field(default_factory=datetime.date.today)
    #updated_at: datetime = Field(default_factory=datetime.utcnow)

    def __str__(self):
        return self.name
    

    # -------------------------------------------
    # # Pseudocode: (Permission & Access Control)
    # -------------------------------------------


    # this will Pin this to our backend  if they are not employee or admin they cant edit this
    #def menu_list_inventory(id):
        #'''update stock quantity:'''
        #if role not in ['admin', 'employee']:
        #flash('You cannot Edit this','error')
        #return redirect(url_for('restrict_access'))
        #only admin can update the price 


    # this will Pin this to our backend  if they are  admin they cant Hide it this
    #def menu_list_archve(id):
        #if role not in ['admin']:
        #flash('You cannot Archive this','error')
        #return redirect(url_for('restrict_access'))

    

#-------------------------------------------------------------------------------------------------------------------------------|

=======
    image_url:      str                     = Field(default=None, max_length=512)           #Visible     #Visible      #Visible

    orders:         list['Order_list']      = Relationship(back_populates='menu')           #Visible     #Visible      #Hide

    is_archive:     bool                    = Field(default=False)                           #Visible     #Hide        #Hide
   
    def __str__(self):
        return self.name
#-------------------------------------------------------------------------------------------------------------------------------|




>>>>>>> d60a0ea3c3fb8b17f990453c660e083d67c99676
#Order
#-------------------------------------------------------------------------------------------------------------------------------|

class TableEnum(str, Enum): 

<<<<<<< HEAD
    TABLE1 = 'TABLE1'
    TABLE2 = 'TABLE2'
    TABLE3 = 'TABLE3'
    TABLE4 = 'TABLE4'
    TABLE5 = 'TABLE5'

class Order_List(SQLModel, table=True):
=======
    table1 = 'table1'
    table2 = 'table2'
    table3 = 'table3'
    table4 = 'table4'
    table5 = 'table5'

class Order_list(SQLModel, table=True):
>>>>>>> d60a0ea3c3fb8b17f990453c660e083d67c99676
    
    id:             int                     = Field(default=None, primary_key=True)
    menu_id:        int                     = Field(foreign_key='menu_list.id')
    quantity:       int                     = Field(nullable=False)
    total:          float                   = Field(nullable=False)
    table:          TableEnum               = Field(nullable=False)

    #order_date:     datetime.date           = Field(default_factory=datetime.date.today)
    # relationship to Menu_List
    menu: Optional["Menu_List"] = Relationship(back_populates="orders")
<<<<<<< HEAD


    
    # -------------------------------------------
    # # Pseudocode: (Permission & Access Control)
    # -------------------------------------------
 
    # this will Pin this to our backend  if they are not employee or admin they cant see this
    #def view_oder_list():
        #avoid to viewer to update this
        #role = flask_session.get('role')
        #if role not in ['ADMIN', 'EMPLOYEE']:
            #flash('You cannot Edit this','error')
            #return redirect(url_for('restrict_access'))

#------------------------------------------------------------------------------------------------------


#This Holder for income
class Income_Holder(SQLModel, table=True):
    id:             int                     = Field(default=None, primary_key=True)
    order_id:       int                     = Field(foreign_key='income_table.id')
    order:          Optional["Income_table"] = Relationship(back_populates="holder")

    
class PaymentEnum(str,Enum):
    CASH =   'CASH'
    ONLINE = 'ONLINE'
=======
    income: Optional["Income_table"] = Relationship(back_populates="order")
#------------------------------------------------------------------------------------------------------

class PaymentEnum(str,Enum):
    Cash =   'Cash'
    Online = 'Online'
>>>>>>> d60a0ea3c3fb8b17f990453c660e083d67c99676

    # force  it  value when seeing the front end
    def __str__(self):
        return self.value


class Income_table(SQLModel, table=True):
<<<<<<< HEAD
    id:              int                     = Field(default=None, primary_key=True)
    order_date:      datetime.date           = Field(default_factory=datetime.date.today)
    income:          float                   = Field(nullable=False)
    payment_type:    PaymentEnum             = Field()
    image_url:       str                     = Field()
    order_list_item: str                     = Field()

    holder: Optional["Income_Holder"] = Relationship(back_populates="order")

    
    # -------------------------------------------
    # # Pseudocode: (Permission & Access Control)
    # -------------------------------------------


    # this will Pin this to our backend  if they are not employee or admin they cant see this
    #def view_income_list():
        #avoid to viewer to update this
        #role = flask_session.get('role')
        #if role not in ['ADMIN', 'EMPLOYEE']:
            #flash('You cannot Edit this','error')
            #return redirect(url_for('restrict_access'))


#kitchen
#------------------------------------------------------------------------------------------------------

class UnitEnum(str,Enum):
    KG = 'KG'
    G = 'G'
    PCS = ' PCS'
=======

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
>>>>>>> d60a0ea3c3fb8b17f990453c660e083d67c99676
    L = 'L'

    # force  it  value when seeing the front end
    def __str__(self):
        return self.value


class CategoryEnum(str,Enum):
<<<<<<< HEAD
    DAIRY = 'Dairy'
    SEAFOOD = 'Seafood'
    SPICES = 'Spices'
    MEAT = 'Meat'
    BEVERAGES = 'Beverages'
=======
    Dairy = 'Dairy'
    Seafood = 'Seafood'
    Spices = 'Spices'
    Meat = 'Meat'
    Beverages = 'Beverages'
>>>>>>> d60a0ea3c3fb8b17f990453c660e083d67c99676
    
    def __str__(self):
        return self.value


class Kitchen_Stock(SQLModel,table=True):
<<<<<<< HEAD
     # Field Name     | Type                                                | Visibility:   Admin | Employee | Viewer
    # -------------- | --------- | ----------------- | -------- | --------

=======

    #Name           #Type                # field                                          #Admin      #Employee     #Viewer
>>>>>>> d60a0ea3c3fb8b17f990453c660e083d67c99676
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

<<<<<<< HEAD
    
    # -------------------------------------------
    # # Pseudocode: (Permission & Access Control)
    # -------------------------------------------

    # this will Pin this to our backend  if they are not employee or admin they cant edit this
    #def stock_list_update(id):
        #'''update stock quantity:'''
        #if role not in ['admin', 'employee']:
        #flash('You cannot Edit this','error')
        #return redirect(url_for('restrict_access'))

    # this will Pin this to our backend  if they are  admin they cant Hide it this
    #def stock_list_archve(id):
        #if role not in ['admin']:
        #flash('You cannot Archive this','error')
        #return redirect(url_for('restrict_access'))




# for sqlite
engine = create_engine('sqlite:///model.db')

#engine = create_engine(
    
    #"postgresql+psycopg2://postgres:postgres1@localhost:5432/model"
#)

=======



engine = create_engine('sqlite:///model.db')
>>>>>>> d60a0ea3c3fb8b17f990453c660e083d67c99676
SQLModel.metadata.create_all(engine)



