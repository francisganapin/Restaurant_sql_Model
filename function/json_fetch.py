from flask import Flask, jsonify
from sqlmodel import Session, select
from model import Kitchen_Stock,Menu_List,engine
from sqlalchemy.exc import SQLAlchemyError


app = Flask(__name__)

@app.route('/json/stock/list')
def json_menu_list():
    try:
        with Session(engine) as session:
            data = session.exec(select(Kitchen_Stock)).all()
            result = [item.model_dump() for item in data]
        return jsonify(result)
    
    except SQLAlchemyError as e:
        return jsonify({"error": "Session invalid id was not exist", "details": str(e)}), 500

@app.route('/json/stock/list/<int:id>', methods=['GET'])
def json_stock_list_id(id):
    try:
        with Session(engine) as session:
            query = select(Kitchen_Stock).where(Kitchen_Stock.id == id)
            data = session.exec(query).all()
            #if item was not found
            if not data:
                return jsonify({'message':f'No item found with ID {id}'})

            result = [item.model_dump() for item in data]
        return jsonify(result)
    except SQLAlchemyError as e:
        return jsonify({"error": "Session invalid id was not exist", "details": str(e)}), 500
    

@app.route('/json/menu/list')
def json_stock_list():
    try:
        with Session(engine) as session:
            data = session.exec(select(Menu_List)).all()
            result = [item.model_dump() for item in data]
        return jsonify(result)
    except ValueError as e:
        return jsonify({"error": "Session invalid or database issue", "details": str(e)}), 500

