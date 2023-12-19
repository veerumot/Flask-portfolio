from typing import Dict, Any

from flask import Flask, request, render_template, redirect
import os
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from flask_cors import CORS
from OpenSSL import SSL

context = SSL.Context(SSL.PROTOCOL_TLSv1_2)
context.use_privatekey_file('server.key')
context.use_certificate_file('server.crt')

app = Flask(__name__)
CORS(app)


@app.route('/')
def index():
    return render_template('navbar.html')


@app.route('/about')
def about():
    return render_template('about.html')


@app.route('/skills')
def skills():
    return render_template('skills.html')


@app.route('/contact')
def contact():
    return render_template('contact.html')


@app.route('/submit', methods=['POST'])
def submit():
    if request.method == 'POST':
        # Get form data
        recipient_email = os.getenv('recipient_email')
        print(recipient_email)
        # Your email configuration
        sender_email = os.getenv('sender_email')
        print(sender_email)
        sender_password = os.getenv('sender_password')
        print(sender_password)
        subject = request.form['subject']
        form_data = {
            'name': request.form['name'],
            'email': request.form['email'],
            'mobile': request.form['mobile'],
            'message': request.form['message']
        }
        print("Form Data:", form_data)
        # Create the email message
        message = MIMEMultipart()
        message['From'] = sender_email
        message['To'] = recipient_email
        message['Subject'] = subject
        text_content = f"name: {form_data['name']}\nemail: {form_data['email']}\nmobile: {form_data['mobile']}\nmessage: {form_data['message']}"
        message.attach(MIMEText(text_content, 'plain'))

        # Connect to the SMTP server and send the email
        with smtplib.SMTP('smtp.gmail.com', 587) as server:
            server.starttls()
            server.login(sender_email, sender_password)
            server.sendmail(sender_email, recipient_email, message.as_string())
        return redirect('/contact')
    return 'Error'


if __name__ == '__main__':
    app.run(host='127.0.0.1', port='443', debug=True, ssl_context=context)
