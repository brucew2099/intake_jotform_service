"""
Imports
"""

from datetime import datetime
import json
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import (
    Boolean,
    Column,
    Date,
    ForeignKey,
    Integer,
    String)
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base

# Local imports...
from app.helpers import add_entity, get_next_id, get_id_by_item

_PATIENT_ID = 0
_PERM_ADDRESS_ID = 0
_TEMP_ADDRESS_ID = 0
_INTAKE_ID = 0
_PHONE_1_ID = 0
_PHONE_2_ID = 0
_IMAGE_FRONT_ID = 0
_IMAGE_BACK_ID = 0

Base = declarative_base()
metadata = Base.metadata

database = SQLAlchemy()
migrate = Migrate()


def setup_db(app):
    """
    Setup database
    """
    database.init_app(app)
    database.app = app
    migrate.init_app(app, database)


class Patient(Base):
    """
    Patient table
    """
    __tablename__ = 'Patients'
    id = Column('Id', Integer, primary_key=True)
    prefix = Column('Prefix', String(10), nullable=True)
    first_name = Column('FirstName', String(100), nullable=False)
    last_name = Column('LastName', String(100), nullable=False)
    date_of_birth = Column('DateOfBirth', Date, nullable=False)
    gender = Column('Gender', String(255), nullable=False)
    age = Column('Age', Integer, nullable=False)
    parent_first_name = Column('ParentFirstName', String(100), nullable=True)
    parent_last_name = Column('ParentLastName', String(100), nullable=True)
    email = Column('Email', String(255), nullable=True)
    is_us_citizen = Column('IsUsCitizen', Boolean, nullable=False, default=True)
    need_visa = Column('NeedVisa', Boolean, nullable=True)
    dates_available = Column('DatesAvailable', Date, nullable=True)
    need_interpretor = Column('NeedInterpretor', Boolean, nullable=False, default=False)
    referral_first_name = Column('ReferralFirstName', String(255), nullable=True)
    referral_last_name = Column('ReferralLastName', String(255), nullable=True)
    preferred_contact_id = Column('PreferredContactId',\
        ForeignKey('PreferredContacts.Id'), nullable=False)
    language_id = Column('LanguageId', ForeignKey('Languages.Id'), nullable=True)
    coverage_type_id = Column('CoverageTypeId', ForeignKey('CoverageTypes.id'), nullable=True)
    referral_type_id = Column('ReferralTypeId', ForeignKey('ReferralTypes.Id'), nullable=True)
    permanent_address_id = Column('PermanentAddressId', ForeignKey('Address.Id'), nullable=True)
    temporary_address_id = Column('TemporaryAddressId', ForeignKey('Address.Id'), nullable=True)
    phone_1_id = Column('Phone1Id', ForeignKey('Phone.Id'), nullable=True)
    phone_2_id = Column('Phone2Id', ForeignKey('Phone.Id'), nullable=True)
    insurance_card_front_id = Column('InsuranceCardFrontId', ForeignKey('Image.Id'), nullable=True)
    insurance_card_back_id = Column('InsuranceCardBackId', ForeignKey('Image.Id'), nullable=True)

    intake = relationship('Intake', backref='patient')

    def __init__(self, patient_id=0, prefix=None, first_name=None, last_name=None, date_of_birth=None,
            gender=None, age=None, parent_first_name=None, parent_last_name=None, email=None,
            is_us_citizen=True, need_visa=None,
            dates_available=None, need_interpretor=None,
            referral_first_name=None, referral_last_name=None,
            preferred_contact_id=0, language_id=0,
            coverage_type_id=0, referral_type_id=0,
            permanent_address_id=0, temporary_address_id=0,
            phone_1_id=0, phone_2_id=0,
            insurance_card_front_id=0, insurance_card_back_id=0):
        self.id = patient_id
        self.prefix = prefix
        self.first_name = first_name
        self.last_name = last_name
        self.date_of_birth = date_of_birth
        self.gender = gender
        self.age = age
        self.parent_first_name = parent_first_name
        self.parent_last_name = parent_last_name
        self.email = email
        self.is_us_citizen = is_us_citizen
        self.need_visa = need_visa
        self.dates_available = dates_available
        self.need_interpretor = need_interpretor
        self.language_id = language_id
        self.referral_type_id = referral_type_id
        self.referral_first_name = referral_first_name
        self.referral_last_name = referral_last_name
        self.preferred_contact_id = preferred_contact_id
        self.coverage_type_id = coverage_type_id
        self.permanent_address_id = permanent_address_id
        self.temporary_address_id = temporary_address_id
        self.phone_1_id = phone_1_id
        self.phone_2_id = phone_2_id
        self.insurance_card_front_id = insurance_card_front_id
        self.insurance_card_back_id = insurance_card_back_id

    def __repr__(self):
        return f'Patient class = {self.id}, {self.prefix}, {self.first_name}, \
            {self.last_name}, {self.date_of_birth}, \
            {self.gender}, {self.age}, \
            {self.parent_name}, {self.email}, \
            {self.is_us_citizen}, {self.need_visa}, \
            {self.dates_available}, {self.need_interpretor}, \
            {self.insurance_card_front}, {self.insurance_card_back}, \
            {self.referral_first_name}, {self.referral_last_name}, \
            {self.preferred_contact_id}, {self.language_id}, \
            {self.coverage_type_id}, {self.referral_type_id}, \
            {self.permanent_address_id}, {self.temp_address_id}, \
            {self.phone_1_id}, {self.phone_2_id}, \
            {self.insurance_card_front_id}, {self.insurance_card_back_id}'


    def parse_patient_data(self, req):
        """
        Parse patient data from request
        :param req:
        :return:
        """
        _PATIENT_ID = get_next_id(database, Patient)
        self.id = _PATIENT_ID
        self.prefix = req['q18_patientName']['prefix']
        self.first_name = req['q18_patientName']['first']
        self.last_name = req['q18_patientName']['last']

        birthdate = \
            f"{req['q90_dateOf90']['month']}/{req['q90_dateOf90']['day']}/ \
            {req['q90_dateOf90']['year']}"
        self.date_of_birth = datetime.strptime(birthdate, '%m/%d/%Y')

        self.gender = req['q75_gender75']
        self.age = req['q74_age']
        self.parent_first_name = req['q64_parentName']['first']
        self.parent_last_name = req['q64_parentName']['last']
        self.email = req['q35_email']
        self.preferred_contact_id = get_id_by_item(database, PreferredContact, \
            'preferred_contact', req['q37_preferredContact'])
        self.is_us_citizen = 1 if req['q76_areYou76'] == "Yes" else 0
        self.need_visa = 1 if req['q77_doYou77'] == "Yes" else 0
        dates_available = \
            f"{req['q48_datesAvailable']['month']}/{req['q48_datesAvailable']['day']}/ \
            {req['q48_datesAvailable']['year']}"
        self.dates_available = datetime.strptime(dates_available, '%m/%d/%Y')
        self.need_interpretor = 1 if req['q78_areYou'] == "Yes" else 0
        self.language_id = get_id_by_item(database, Language, 'language', req['q70_If'])
        self.coverage_type_id = get_id_by_item(database, CoverageType, 'coverage_type', req['q50_typeA'])
        self.referral_type_id = get_id_by_item(database, ReferralType, 'referral_type', req['q53_howDid'])
        self.referral_first_name = req['q67_For67']['first']
        self.referral_last_name = req['q67_For67']['last']
        self.permanent_address_id = _PERM_ADDRESS_ID
        self.temp_address_id = _TEMP_ADDRESS_ID
        self.phone_number_1_id = _PHONE_1_ID
        self.phone_number_2_id = _PHONE_2_ID
        self.insurance_card_front_id = _IMAGE_FRONT_ID
        self.insurance_card_back_id = _IMAGE_BACK_ID

        add_entity(database, Patient)

class Address(Base):
    """
    The address of a patient.
    """
    __tablename__ = 'Addresses'
    id = Column('Id', Integer, primary_key=True)
    street_1 = Column('Street1', String(255), nullable=False)
    street_2 = Column('Street2', String(255), nullable=False)
    city = Column('City', String(255), nullable=False)
    state = Column('State', String(255  ), nullable=False)
    zip_code = Column('ZipCode', String(255), nullable=False)
    country_id = Column('CountryId', ForeignKey('Countries.Id'), nullable=False)

    patient = relationship('Patient', backref='address')

    def __init__(self, address_id=None, street_1=None, street_2=None,
        city=None, state=None, zip_code=None, country_id=0):
        self.id = address_id
        self.street_1 = street_1
        self.street_2 = street_2
        self.city = city
        self.state = state
        self.zip_code = zip_code
        self.country_id = country_id

    def __repr__(self):
        return f'Address class = {self.id}, {self.street_1}, \
            {self.street_2}, {self.city}, {self.state}, {self.zip_code}, {self.country_id})'

    def parse_address_data(self, req):
        """
        Parse address data from request
        :param req:
        :return:
        """
        # for permanent address data
        _PERM_ADDRESS_ID = get_next_id(database, Address)
        perm = req['q25_permanentStreet']
        self.id = _PERM_ADDRESS_ID
        self.street_1 = perm['addr_line1']
        self.street_2 = perm['addr_line2']
        self.city = perm['city']
        self.state = perm['state']
        self.zip_code = perm['postal']
        self.country_id = get_id_by_item(database, Country, 'country', perm['country'])
        add_entity(database, Address)

        # for temporary address data
        _TEMP_ADDRESS_ID = get_next_id(database, Address)
        temp = req['q26_temporaryStreet']
        self.id = _TEMP_ADDRESS_ID
        self.street_1 = temp['addr_line1']
        self.street_2 = temp['addr_line2']
        self.city = temp['city']
        self.state = temp['state']
        self.zip_code = temp['postal']
        self.country_id = get_id_by_item(database, Country, 'country', perm['country'])
        add_entity(database, Address)


class Phone(Base):
    """
    The phone number of a patient.
    """
    __tablename__ = 'Phones'
    id = Column('Id', String(255), primary_key=True)
    phone_number = Column('PhoneNumber', String(255), nullable=False)
    phone_type_id = Column('PhoneTypeId', ForeignKey('PhoneTypes.Id'), nullable=True)

    patient = relationship('Patient', backref='phone')

    def __init__(self, phone_id=None, phone_number=None, phone_type_id=0):
        self.id = phone_id
        self.phone_number = phone_number
        self.phone_type_id = phone_type_id


    def __repr__(self):
        return f'Phone class = {self.id}, {self.phone_number}, {self.phone_type_id}'


    def parse_phone_data(self, req):
        """
        Parse phone data from request
        :param req:
        :return:
        """
        # for phone 1 data
        _PHONE_1_ID = get_next_id(database, Phone)
        self.id = _PHONE_1_ID
        self.phone_number = req['q27_phoneNumber']['full']
        self.phone_type_id = get_id_by_item(database, PhoneType, 'phone_type', req['q33_phoneNumber33'])
        add_entity(database, Phone)

        # for phone 2 data
        _PHONE_2_ID = get_next_id(database, Phone)
        self.id = _PHONE_2_ID
        self.phone_number = req['q32_phoneNumber32']['full']
        self.phone_type_id = get_id_by_item(database, PhoneType, 'phone_type', req['q34_phoneNumber34'])
        add_entity(database, Phone)


class PhoneType(Base):
    """
    The phone type of a patient.
    """
    __tablename__ = 'PhoneTypes'
    id = Column('Id', Integer, primary_key=True)
    phone_type = Column('PhoneType', String(255), nullable=False)

    phone = relationship('Phone', backref='phone_type')


    def __init__(self, phone_type_id=None, phone_type=None):
        self.id = phone_type_id
        self.phone_type = phone_type

    def __repr__(self):
        return f'PhoneType class = {self.id}, {self.phone_type}'


class PreferredContact(Base):
    """
    The preferred contact of a patient.
    """
    __tablename__ = 'PreferredContacts'
    id = Column('Id', Integer, primary_key=True)
    preferred_contact = Column('ContactTypes', String(255), nullable=False)

    patient = relationship('Patient', backref='preferred_contact')


    def __init__(self, preferred_contact_id=None, preferred_contact=None):
        self.id = preferred_contact_id
        self.preferred_contact = preferred_contact


    def __repr__(self) -> str:
        return f'PreferredContact class = {self.id}, {self.preferred_contact}'


class Country(Base):
    """
    The country of a patient.
    """
    __tablename__ = 'Countries'
    id = Column('Id', String(255), primary_key=True)
    country = Column('Country', String(255), nullable=False)

    address = relationship('Address', backref='country')

    def __init__(self, country_id=None, country=None):
        self.id = country_id
        self.country = country

    def __repr__(self):
        return f'Country class = {self.id}, {self.country}'


class Language(Base):
    """
    The language of a patient.
    """
    __tablename__ = 'Languages'
    id = Column('Id', Integer, primary_key=True)
    language = Column('Language', String(255), nullable=False)

    patient = relationship('Patient', backref='language')

    def __init__(self, language_id=None, language=None):
        self.id = language_id
        self.language = language

    def __repr__(self):
        return f'Language class = {self.id}, {self.language}'


class CoverageType(Base):
    """
    The coverage type of the patient insurance.
    """
    __tablename__ = 'CoverageTypes'
    id = Column('Id', Integer, primary_key=True)
    coverage_type = Column('CoverageType', String(255), nullable=False)

    patient = relationship('Patient', backref='coverage_type')

    def __init__(self, coverage_type_id=None, coverage_type=None):
        self.id = coverage_type_id
        self.coverage_type = coverage_type

    def __repr__(self):
        return f'CoverageType class = {self.id}, {self.coverage_type}'

class ReferralType(Base):
    """
    The referral type of a patient.
    """
    __tablename__ ='ReferralTypes'
    id = Column('Id', Integer, primary_key=True)
    referral_type = Column('ReferralType', String(255), nullable=False)

    patient = relationship('Patient', backref='referral_type')

    def __init__(self, referral_type_id=None, referral_type=None):
        self.id = referral_type_id
        self.referral_type = referral_type

    def __repr__(self):
        return f'ReferralType class = {self.id}, {self.referral_type}'


class Intake(Base):
    """
    The intake record of a patient.
    """
    __tablename__ = 'Intakes'
    id = Column('Id', Integer, primary_key=True)
    intake_date = Column('IntakeDate', Date(), nullable=True)
    intake_by_first_name = Column('IntakeFirstName', String(255), nullable=True)
    intake_by_last_name = Column('IntakeLastName', String(255), nullable=True)
    liason_first_name = Column('LiasonFirstName', String(255), nullable=True)
    liason_last_name = Column('LiasonLastName', String(255), nullable=True)
    patient_id = Column('PatientId', ForeignKey('Patients.Id'), nullable=True)
    form_id = Column('FormId', String(255), nullable=True)
    submission_id = Column('SubmissionId', String(255), nullable=True)
    form_title = Column('FormTitle', String(255), nullable=True)

    def __init__(self, intake_id=None, intake_date=None,
        intake_by_first_name=None, intake_by_last_name=None,
        liason_first_name=None, liason_last_name=None, patient_id=0,
        form_id=0, submission_id=0, form_title=None):
        self.id = intake_id
        self.intake_date = intake_date
        self.intake_by_first_name = intake_by_first_name
        self.intake_by_last_name = intake_by_last_name
        self.liason_first_name = liason_first_name
        self.liason_last_name = liason_last_name
        self.patient_id = patient_id
        self.form_id = form_id
        self.submission_id = submission_id
        self.form_title = form_title

    def __repr__(self):
        return f'Intake class = {self.id}, {self.intake_date}, \
            {self.intake_by_first_name}, {self.intake_by_last_name}, \
            {self.liason_first_name}, {self.liason_last_name}, {self.patient_id}, \
            {self.form_id}, {self.submission_id}, {self.form_title}'


    def parse_intake_data(self, form_data):
        """
        Parse the data from the form.

        :param form_data: The data from the form.
        :type form_data: `str`
        """
        self.form_id = form_data['formId']
        self.form_title = form_data['formTitle']
        self.submission_id = form_data['submissionId']

        if form_data["rawRequest"]:
            req = json.loads(form_data["rawRequest"])
            _INTAKE_ID = get_next_id(database, Intake)
            self.id = _INTAKE_ID
            intake_date = \
                f"{req['q59_intakeDate']['month']}/{req['q59_intakeDate']['day']}/ \
                {req['q59_intakeDate']['year']}"
            self.patient_id = _PATIENT_ID
            self.intake_date = datetime.strptime(intake_date, '%m/%d/%Y')
            self.intake_by_first_name = req['q60_intakeBy']['first']
            self.intake_by_last_name = req['q60_intakeBy']['last']
            self.liason_first_name = req['q62_liason']['first']
            self.liason_last_name = req['q62_liason']['last']
            self.patient_id = _PATIENT_ID
            add_entity(database, Intake)

class Image(Base):
    """
    The image of the patient's insurance card.
    """
    __tablename__ = 'Images'
    id = Column('Id', String(255), primary_key=True)
    image_name = Column('ImageName', String(255), nullable=False)
    image_url = Column('ImageUrl', String(500), nullable=False)
    widget_type = Column('WidgetType', String(255), nullable=False, default='imagelinks')

    patient = relationship('Patient', backref='image')

    def __init__(self, image_id=None, image_name=None, image_url=None, widget_type=None):
        self.id = image_id
        self.image_name = image_name
        self.image_url = image_url
        self.widget_type = widget_type

    def __repr__(self):
        return f'Image class = {self.id}, {self.image_name}, \
            {self.image_url}, {self.widget_type}'


    def parse_Image_data(self, req):
        """
        Parse the image data from the request.
        """
        # Front image data
        _IMAGE_FRONT_ID = get_next_id(database, Image)
        self.id = _IMAGE_FRONT_ID
        if req['q83_typeA83']:
            metadata = json.loads(req['q83_typeA83']['value'])
            self.image_name = metadata['name']
            self.image_url = metadata['url']
            self.widget_type = "imagelinks"
        add_entity(database, Image)

        # Back image data
        _IMAGE_BACK_ID = get_next_id(database, Image)
        self.id = _IMAGE_BACK_ID
        if req['q84_typeA84']:
            metadata = json.loads(req['q84_typeA84']['value'])
            self.image_name = metadata['name']
            self.image_url = metadata['url']
            self.widget_type = "imagelinks"
        add_entity(database, Image)
