from sqlmodel import Session, SQLModel, create_engine
from sqlalchemy import text

engine = create_engine("postgresql+psycopg2://postgres:postgres1@localhost:5432/model")



SQLModel.metadata.create_all(engine)

# Use a session to insert data
with Session(engine) as session:
    session.exec(text("""
        INSERT INTO menu_list (category,quantity, name, description, image_url, price, is_archive) VALUES
        ('MAIN_COURSE', 5,'Cheeseburger', 'Juicy beef patty with melted cheese', 'images/menu/cheeseburger.jpg', 50,False),
        ('PASTA',  5,'Spaghetti Carbonara', 'Creamy pasta with bacon and parmesan', 'images/menu/carbonara.jpg', 150,False),
        ('BEVERAGES',  5,'Mango Shake', 'Fresh mango blended with ice and milk', 'images/menu/mango_shake.jpg', 90,False),
        ('SEAFOOD',  5,'Grilled Salmon', 'Perfectly grilled salmon with lemon butter sauce', 'images/menu/grilled_salmon.jpg', 250,False),
        ('DESSERT',  5,'Chocolate Lava Cake', 'Warm chocolate cake with a gooey center', 'images/menu/lava_cake.jpg', 130,False),
        ('MAIN_COURSE',  5,'BBQ Ribs', 'Tender ribs glazed with smoky barbecue sauce', 'images/menu/bbq_ribs.jpg', 180,False),
        ('SALAD',  5,'Caesar Salad', 'Crisp romaine lettuce with parmesan and croutons', 'images/menu/caesar_salad.jpg', 100,False),
        ('PIZZA',  5,'Margherita Pizza', 'Classic pizza with fresh tomatoes and basil', 'images/menu/margherita_pizza.jpg', 160,False),
        ('BEVERAGES',  5,'Strawberry Milkshake', 'Creamy milkshake with real strawberries', 'images/menu/strawberry_milkshake.jpg', 90,False),
        ('MAIN_COURSE',  5,'Teriyaki Chicken', 'Juicy chicken glazed with teriyaki sauce', 'images/menu/teriyaki_chicken.jpg', 200,False),
        ('PASTA',  5,'Shrimp Alfredo', 'Delicious pasta with creamy alfredo and shrimp', 'images/menu/shrimp_alfredo.jpg', 150,False),
        ('BEVERAGES',  5,'Iced Caramel Latte', 'Refreshing iced coffee with caramel syrup', 'images/menu/iced_caramel_latte.jpg', 110,False);
    """
                      ))
    
with Session(engine) as session:
    session.exec(text("""
        INSERT INTO kitchen_stock (
            id, quantity, price, category, batch_code, name, unit, delivery_date, spoilage_date, is_archive
        ) VALUES
        (1, 0, 50.0, 'DAIRY', 'D001', 'Milk', 'L', '2025-05-20', '2025-04-01',False),
        (2, 5, 200.0, 'DAIRY', 'D002', 'Cheddar Cheese', 'KG', '2025-05-18', '2025-06-15',False),
        (3, 444, 50.0, 'DAIRY', 'D003', 'Butter', 'KG', '2025-05-19', '2025-06-25',False),
        (4, 12, 75.0, 'DAIRY', 'D004', 'Yogurt', 'L', '2025-05-20', '2025-06-10',False),
        (5, 10, 500.0, 'SEAFOOD', 'S001', 'Salmon Fillet', 'KG', '2025-05-21', '2025-05-30',False),
        (6, 15, 350.0, 'SEAFOOD', 'S002', 'Shrimp', 'KG', '2025-05-22', '2025-05-28',False),
        (7, 20, 600.0, 'SEAFOOD', 'S003', 'Crab Meat', 'KG', '2025-05-23', '2025-05-30',False),
        (8, 25, 450.0, 'SEAFOOD', 'S004', 'Squid Rings', 'KG', '2025-05-24', '2025-06-02',False),
        (9, 30, 80.0, 'SPICES', 'SP001', 'Black Pepper', 'G', '2025-05-10', '2025-12-10',False),
        (10, 40, 90.0, 'SPICES', 'SP002', 'Paprika', 'G', '2025-05-12', '2025-12-12',False),
        (11, 2222, 70.0, 'SPICES', 'SP003', 'Garlic Powder', 'G', '2025-05-14', '2025-12-14',False),
        (12, 50, 100.0, 'SPICES', 'SP004', 'Turmeric', 'G', '2025-05-16', '2025-12-16',False),
        (13, 10, 300.0, 'MEAT', 'M001', 'Chicken Breast', 'KG', '2025-05-20', '2025-05-27',False),
        (14, 15, 450.0, 'MEAT', 'M002', 'Pork Chops', 'KG', '2025-05-21', '2025-05-11',False),
        (15, 12, 600.0, 'MEAT', 'M003', 'Beef Sirloin', 'KG', '2025-05-22', '2025-05-29',False),
        (16, 18, 350.0, 'MEAT', 'M004', 'Ground Turkey', 'KG', '2025-05-23', '2025-05-30',False),
        (17, 20, 75.0, 'BEVERAGES', 'B001', 'Orange Juice', 'L', '2025-05-24', '2025-06-10',False),
        (18, 25, 50.0, 'BEVERAGES', 'B002', 'Green Tea', 'L', '2025-05-25', '2025-06-20',False),
        (19, 31, 322.0, 'SPICES', '33sdas', 'Garlic Powder 2', 'PCS', '2025-01-01', '2027-01-01',False),
        (20, 3, 3.0, 'SPICES', '23AAS2', 'Milk3', 'PCS', '2025-01-01', '2026-01-02',False);
    """))


#https://bcrypt-generator.com/ we use this to encrypt our password

with Session(engine) as session:
    session.exec(text("""
        INSERT INTO "user" (
            id, username, password, role, image_url
        ) VALUES
        (1, 'admin', '$2a$12$MgVGJkCyxAjM1/nZQGQ8zOveUxBg5Qy.RDbYKSm9QXpubRuZRkTe2', 'ADMIN', 'none'),
        (2, 'employee', '$2a$12$ABReuXCjUyXKhofv5OgujOApkjBHbUNTQu5ZlnuBuVq3VATvOTB62', 'EMPLOYEE', 'none'),
        (3, 'viewer', '$2a$12$f3p9cmvPbPNfBvN2qTGNSujZdxYaERzfTsHxtfH58ZRIoH22lKiF6', 'VIEWER', 'none');
    """))


    session.commit()



print("Data inserted successfully!")

