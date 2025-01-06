from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///firms.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class Firm(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    vkn = db.Column(db.String(10), unique=True, nullable=False)
    establishment_date = db.Column(db.String(10), nullable=False)
    firm_type = db.Column(db.String(50), nullable=False)
    address = db.Column(db.String(200), nullable=True)

db.create_all()

@app.route('/api/firms', methods=['POST'])
def add_firm():
    data = request.get_json()
    new_firm = Firm(
        name=data['name'],
        vkn=data['vkn'],
        establishment_date=data['establishment_date'],
        firm_type=data['firm_type'],
        address=data.get('address', '')
    )
    db.session.add(new_firm)
    db.session.commit()
    return jsonify({'message': 'Firm added successfully'}), 201

@app.route('/api/firms', methods=['GET'])
def get_firms():
    firms = Firm.query.all()
    firms_list = [
        {
            'id': firm.id,
            'name': firm.name,
            'vkn': firm.vkn,
            'establishment_date': firm.establishment_date,
            'firm_type': firm.firm_type,
            'address': firm.address,
        }
        for firm in firms
    ]
    return jsonify(firms_list)

@app.route('/api/firms/<int:id>', methods=['PUT'])
def update_firm(id):
    data = request.get_json()
    firm = Firm.query.get_or_404(id)
    firm.name = data['name']
    firm.vkn = data['vkn']
    firm.establishment_date = data['establishment_date']
    firm.firm_type = data['firm_type']
    firm.address = data.get('address', '')
    db.session.commit()
    return jsonify({'message': 'Firm updated successfully'})

@app.route('/api/firms/<int:id>', methods=['DELETE'])
def delete_firm(id):
    firm = Firm.query.get_or_404(id)
    db.session.delete(firm)
    db.session.commit()
    return jsonify({'message': 'Firm deleted successfully'})

if __name__ == '__main__':
    app.run(debug=True)
