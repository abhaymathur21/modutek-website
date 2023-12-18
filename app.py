from flask import Flask, render_template, request, jsonify,redirect, url_for
from flask_sqlalchemy import SQLAlchemy
import csv
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.db'  # Use SQLite for simplicity
db = SQLAlchemy()

csv_file_path = 'database.csv'

# Email configuration for Gmail
email_host = 'smtp.gmail.com'
email_port = 587  # TLS port for Gmail
my_email = 'a21.mathur21@gmail.com'
my_email_password = 'uuot lkpb viwp nacm'

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

    # Send an email to the provided email address
    send_email(name, email, query)
   
    return redirect(url_for('index'))

def update_csv_file(name, email, query):
    # Open the CSV file in append mode
    with open(csv_file_path, mode='a', newline='') as csv_file:
        fieldnames = ['name', 'email', 'query']
        writer = csv.DictWriter(csv_file, fieldnames=fieldnames)

        # Write a new row to the CSV file
        writer.writerow({'name': name, 'email': email, 'query': query})
        
def send_email(name, email, query):
    # Email content
    subject = 'Thank you for your submission'
    body = f'Hello {name},\n\nThank you for submitting your query. We will get back to you soon.\n\nBest regards,\nmodutek'

    # Create a message
    message = MIMEMultipart()
    message['From'] = my_email
    message['To'] = email
    message['Subject'] = subject
    message.attach(MIMEText(body, 'plain'))

    # Connect to the SMTP server and send the email
    with smtplib.SMTP(email_host, email_port) as server:
        server.starttls()
        server.login(my_email, my_email_password)
        server.sendmail(my_email, email, message.as_string())


if __name__ == '__main__':
    app.run(debug=True)
