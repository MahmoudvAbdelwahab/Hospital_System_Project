from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///hospital.db'
db = SQLAlchemy(app)

class Patient(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))

@app.before_first_request
def create_tables():
    db.create_all()

@app.route('/patients', methods=['GET','POST'])
def patients():
    if request.method == 'POST':
        data = request.json
        p = Patient(name=data.get('name'))
        db.session.add(p); db.session.commit()
        return jsonify({'id': p.id, 'name': p.name})
    patients = Patient.query.all()
    return jsonify([{'id':p.id,'name':p.name} for p in patients])

if __name__ == '__main__':
    app.run(debug=True)
