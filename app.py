from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///database.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)

class Data(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)

    def __repr__(self):
        return f"Data('{self.name}')"

@app.route("/create", methods=["POST"])
def create_data():
    data = request.get_json()
    new_data = Data(**data)
    db.session.add(new_data)
    db.session.commit()
    return jsonify({"message": "Data created successfully"})

@app.route("/read", methods=["GET"])
def read_data():
    data = Data.query.all()
    output = []
    for d in data:
        data_dict = {}
        data_dict["id"] = d.id
        data_dict["name"] = d.name
        output.append(data_dict)
    return jsonify({"data": output})

@app.route("/update/<int:id>", methods=["PUT"])
def update_data(id):
    data = Data.query.get(id)
    if data is None:
        return jsonify({"message": "Data not found"}), 404
    data.name = request.get_json()["name"]
    db.session.commit()
    return jsonify({"message": "Data updated successfully"})

@app.route("/delete/<int:id>", methods=["DELETE"])
def delete_data(id):
    data = Data.query.get(id)
    if data is None:
        return jsonify({"message": "Data not found"}), 404
    db.session.delete(data)
    db.session.commit()
    return jsonify({"message": "Data deleted successfully"})

if __name__ == "__main__":
    app.run(debug=True)
