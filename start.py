"""
Imports
"""
import json
import os
from flask import request

from .app.app import create_app
from .app.models import (
    Address,
    Phone,
    PhoneType,
    PreferredContact,
    Country,
    Language,
    CoverageType,
    ReferralType,
    Intake,
    Image)

from .app.exceptions import EmptyEntityError

app = create_app(os.getenv('FLASK_CONFIG') or 'default')

def _extract_jotform_data():
    output = {}
    form_data = request.form.to_dict()
    if form_data.get("rawRequest"):
        print(f'form_data = {form_data.get("rawRequest")}')
        for key, value in json.loads(form_data["rawRequest"]).items():
            # Removes the "q<number>_" part from the key name
            # Instead of "q5_quantity" we want "quantity" as the key
            temp = key.split("_")
            new_key = key if len(temp) == 1 else "_".join(temp[1:])
            # Saves the item with the new key in the dictionary
            output[new_key] = value

    return output


@app.route('/', methods=['GET', 'POST'])
def index():
    """
        This is the main route
    """
    jotform = _extract_jotform_data()
    for key, value in jotform.items():
        print(f"{key}: {value}")
        if type(value) is dict:
            for subkey, subvalue in value.items():
                print(f" +------ {subkey}: {subvalue}")

    return "ok", 200

if __name__ == '__main__':
    app.run()
