from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///bakeries.db'  # SQLite database

db = SQLAlchemy(app)

# Define the BakedGood model
class BakedGood(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    price = db.Column(db.Float)
    bakery_id = db.Column(db.Integer, db.ForeignKey('bakery.id'))

# Define the Bakery model
class Bakery(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    
    # Establish the relationship between Bakery and BakedGood
    baked_goods = db.relationship('BakedGood', backref='bakery', lazy=True)

# Create database tables
db.create_all()

# Route for creating a new baked good
@app.route('/baked_goods', methods=['POST'])
def create_baked_good():
    data = request.get_json()
    name = data.get('name')
    price = data.get('price')
    bakery_id = data.get('bakery_id')

    # Validate data (e.g., check for required fields)
    if not name or price is None or bakery_id is None:
        return jsonify({"error": "Incomplete data"}), 400  # Return 400 Bad Request

    # Create a new baked good
    baked_good = BakedGood(name=name, price=price, bakery_id=bakery_id)
    db.session.add(baked_good)
    db.session.commit()

    return jsonify({"message": "Baked good created"}), 201  # Return 201 Created

# Route for updating a bakery
@app.route('/bakeries/<int:id>', methods=['PATCH'])
def update_bakery(id):
    data = request.get_json()
    new_name = data.get('name')

    # Find the bakery by ID
    bakery = Bakery.query.get(id)
    if not bakery:
        return jsonify({"error": "Bakery not found"}), 404  # Return 404 Not Found

    # Update the bakery's name
    bakery.name = new_name
    db.session.commit()

    return jsonify({"message": "Bakery updated"}), 200  # Return 200 OK

# Route for deleting a baked good
@app.route('/baked_goods/<int:id>', methods=['DELETE'])
def delete_baked_good(id):
    # Find the baked good by ID
    baked_good = BakedGood.query.get(id)
    if not baked_good:
        return jsonify({"error": "Baked good not found"}), 404  # Return 404 Not Found

    # Delete the baked good
    db.session.delete(baked_good)
    db.session.commit()

    return jsonify({"message": "Baked good deleted"}), 200  # Return 200 OK

if __name__ == '__main__':
    app.run(port=5555, debug=True)
