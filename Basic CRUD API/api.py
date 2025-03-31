from flask import Flask, request, jsonify
from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, scoped_session

# Database Setup
DATABASE_URL = "sqlite:///./test.db"
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = scoped_session(sessionmaker(autocommit=False, autoflush=False, bind=engine))
Base = declarative_base()

# Model
class Item(Base):
    __tablename__ = "items"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    description = Column(String, index=True)

Base.metadata.create_all(bind=engine)

# Flask App
app = Flask(__name__)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Create Item
@app.route("/items/", methods=["POST"])
def create_item():
    db = SessionLocal()
    data = request.json
    item = Item(name=data["name"], description=data["description"])
    db.add(item)
    db.commit()
    db.refresh(item)
    db.close()
    return jsonify({"id": item.id, "name": item.name, "description": item.description})

# Read All Items
@app.route("/items/", methods=["GET"])
def read_items():
    db = SessionLocal()
    items = db.query(Item).all()
    db.close()
    return jsonify([{"id": item.id, "name": item.name, "description": item.description} for item in items])

# Read Single Item
@app.route("/items/<int:item_id>", methods=["GET"])
def read_item(item_id):
    db = SessionLocal()
    item = db.query(Item).filter(Item.id == item_id).first()
    db.close()
    if item is None:
        return jsonify({"error": "Item not found"}), 404
    return jsonify({"id": item.id, "name": item.name, "description": item.description})

# Update Item
@app.route("/items/<int:item_id>", methods=["PUT"])
def update_item(item_id):
    db = SessionLocal()
    data = request.json
    item = db.query(Item).filter(Item.id == item_id).first()
    if item is None:
        db.close()
        return jsonify({"error": "Item not found"}), 404
    item.name = data["name"]
    item.description = data["description"]
    db.commit()
    db.refresh(item)
    db.close()
    return jsonify({"id": item.id, "name": item.name, "description": item.description})

# Delete Item
@app.route("/items/<int:item_id>", methods=["DELETE"])
def delete_item(item_id):
    db = SessionLocal()
    item = db.query(Item).filter(Item.id == item_id).first()
    if item is None:
        db.close()
        return jsonify({"error": "Item not found"}), 404
    db.delete(item)
    db.commit()
    db.close()
    return jsonify({"message": "Item deleted successfully"})

if __name__ == "__main__":
    app.run(debug=True)
