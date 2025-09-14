from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
# Use a relative path to store the database in the same directory
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///ecommerce.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False # This is a good practice to avoid a warning

db = SQLAlchemy(app)

# All column definitions must start with a capital 'C'
class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False)
    price = db.Column(db.Float, nullable=False)
    description = db.Column(db.Text, nullable=True)

@app.route('/api/products/add', methods= ["POST"])
def add_product():
    data = request.json
    if 'name' in data and 'price'  in data:
        product = Product(name=data["name"], price = data["price"], description=data.get("description", ""))
        db.session.add(product)
        db.session.commit()
        return jsonify({"message": "Product added sucessfuly"}), 200
    return jsonify({"message": "Invalid product data"}), 400

@app.route('/api/products/delete/<int:product_id>', methods = ['DELETE'])
def delete_product(product_id):
    product= Product.query.get(product_id)
    if product:
        db.session.delete(product)
        db.session.commit()
        return jsonify({"message": "Product deleted sucessfuly"}), 200
    return jsonify({"message": "Product not found"}), 404



# Define the root route
@app.route('/')
def hello_world():
    return 'Hello World'

if __name__ == "__main__":
    # Create the database tables before running the app
    with app.app_context():
        db.create_all()
    app.run(debug=True)