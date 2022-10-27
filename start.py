"""
Imports
"""
import json
import os
from flask import render_template, request

from app.app import create_app
from app.models import (
    Patient,
    Address,
    Phone,
    Intake,
    Image)

app = create_app(os.getenv('FLASK_CONFIG') or 'default')

@app.route('/', methods=['GET', 'POST'])
def index():
    """
        This is the main route
    """
    return render_template('index.html')


@app.route('/process', methods=['GET', 'POST'])
def process_jotform():
    """
    This is the process JotForm route
    """
    form_data = json.loads(request.form)

    intake = Intake()
    patient = Patient()
    address = Address()
    phone = Phone()
    image = Image()

    if form_data["rawRequest"]:
        req = json.loads(form_data["rawRequest"])
        address.parse_address_data(req)
        phone.parse_phone_data(req)
        image.parse_Image_data(req)
        intake.parse_intake_data(form_data)
        patient.parse_patient_data(req)

    return "ok", 200

if __name__ == '__main__':
    app.run()
