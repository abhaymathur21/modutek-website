from flask import Flask, render_template, request, jsonify,redirect, url_for
from flask_sqlalchemy import SQLAlchemy
import csv

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.db'  # Use SQLite for simplicity
db = SQLAlchemy()

csv_file_path = 'database.csv'

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    email = db.Column(db.String(255), nullable=False)
    query = db.Column(db.Text, nullable=True)
    
db.init_app(app)
with app.app_context():
    db.create_all()
    
@app.route('/')
def index():
    return render_template('main.html')

@app.route('/submit', methods=['POST'])
def submit():
    name = request.form.get('name')
    email = request.form.get('email')
    query = request.form.get('message')
    
    new_user = User(name=name, email=email, query=query)
    db.session.add(new_user)
    db.session.commit()

    # For demonstration, log the data to the console
    print('Received data:', {'name': name, 'email': email, 'query': query})

    update_csv_file(name, email, query)

    # Send a response to the client
    # return jsonify({'message': 'Data received successfully!'})
    return redirect(url_for('index'))

def update_csv_file(name, email, query):
    # Open the CSV file in append mode
    with open(csv_file_path, mode='a', newline='') as csv_file:
        fieldnames = ['name', 'email', 'query']
        writer = csv.DictWriter(csv_file, fieldnames=fieldnames)

        # Write a new row to the CSV file
        writer.writerow({'name': name, 'email': email, 'query': query})

if __name__ == '__main__':
    app.run(debug=True)
