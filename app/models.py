"""
Imports
"""

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
#from app.exceptions import EmptyEntityError

Base = declarative_base()
metadata = Base.metadata

db = SQLAlchemy()
migrate = Migrate()


def setup_db(app):
    """
    Setup database
    """
    db.init_app(app)
    db.app = app
    migrate.init_app(app, db)


class Patient(Base):
    """
    Patient table
    """
    __tablename__ = 'Patients'
    patient_id = Column('Id', Integer, primary_key=True)
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
    permanent_address_id = Column('PermanentAddressId', ForeignKey('Addresses.Id'), nullable=False)
    temp_address_id = Column('TempAddressId', ForeignKey('Addresses.Id'), nullable=True)
    phone_number_1_id = Column('PhoneNumber1Id', ForeignKey('Phones.Id'), nullable=True)
    phone_number_2_id = Column('PhoneNumber2Id', ForeignKey('Phones.Id'), nullable=True)
    preferred_contact_id = Column('PreferredContactId',
        ForeignKey('PreferredContacts.Id'), nullable=False)
    language_id = Column('LanguageId', ForeignKey('Languages.Id'), nullable=True)
    coverage_type_id = Column('CoverageTypeId', ForeignKey('CoverageTypes.id'), nullable=True)
    referral_type_id = Column('ReferralTypeId', ForeignKey('ReferralTypes.Id'), nullable=True)
    insurance_card_front_id = Column('InsuranceCardFrontId', ForeignKey('Images.Id'),
        nullable=False)
    insurance_card_back_id = Column('InsuranceCardBackId', ForeignKey('Images.Id'),
        nullable=True)

    permanent_address = relationship('Addresses')
    temp_address = relationship('Addresses')
    phone_number_1 = relationship('Phones')
    phone_number_2 = relationship('Phones')
    preferred_contact = relationship('PreferredContacts')
    language = relationship('Languages')
    coverage_type = relationship('CoverageTypes')
    referral_type = relationship('ReferralTypes')
    insurance_card_front = relationship('Images')
    insurance_card_back = relationship('Images')

    def __init__(self, patient_id=0, first_name=None, last_name=None, date_of_birth=None,
            gender=None, age=None, parent_first_name=None, parent_last_name=None, email=None,
            is_us_citizen=True, need_visa=None,
            dates_available=None, need_interpretor=None, insurance_card_front_id=0,
            insurance_card_back_id=0, referral_first_name=None, referral_last_name=None,
            permanent_address_id=0, temp_address_id=0, phone_number_1_id=0,
            phone_number_2_id=0, preferred_contact_id=0, language_id=0,
            coverage_type_id=0, referral_type_id=0):
        self.patient_id = patient_id
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
        self.insurance_card_front_id = insurance_card_front_id
        self.insurance_card_back_id = insurance_card_back_id
        self.referral_first_name = referral_first_name
        self.referral_last_name = referral_last_name
        self.permanent_address_id = permanent_address_id
        self.temp_address_id = temp_address_id
        self.phone_number_1_id = phone_number_1_id
        self.phone_number_2_id = phone_number_2_id
        self.preferred_contact_id = preferred_contact_id
        self.language_id = language_id
        self.coverage_type_id = coverage_type_id
        self.referral_type_id = referral_type_id

    def __repr__(self):
        return f'Patient class = {self.patient_id}, {self.first_name}, \
            {self.last_name}, {self.date_of_birth}, \
            {self.gender}, {self.age}, \
            {self.parent_name}, {self.email}, \
            {self.is_us_citizen}, {self.need_visa}, \
            {self.dates_available}, {self.need_interpretor}, \
            {self.insurance_card_front}, {self.insurance_card_back}, \
            {self.referral_first_name}, {self.referral_last_name}, \
            {self.permanent_address_id}, {self.temp_address_id}, \
            {self.phone_number_1_id}, {self.phone_number_2_id}, \
            {self.preferred_contact_id}, {self.language_id}, \
            {self.coverage_type_id}, {self.referral_type_id}, \
            {self.image_front_id}, {self.image_back_id}'

class Address(Base):
    """
    The address of a patient.
    """
    __tablename__ = 'Addresses'
    address_id = Column('Id', Integer, primary_key=True)
    street_1 = Column('Street1', String(255), nullable=False)
    street_2 = Column('Street2', String(255), nullable=False)
    city = Column('City', String(255), nullable=False)
    state = Column('State', String(255  ), nullable=False)
    zip_code = Column('ZipCode', String(255), nullable=False)
    country_id = Column('CountryId', ForeignKey('Countries.Id'), nullable=False)

    country = relationship('Countries')

    def __init__(self, address_id=None, street_1=None, street_2=None,
        city=None, state=None, zip_code=None, country_id=0):
        self.address_id = address_id
        self.street_1 = street_1
        self.street_2 = street_2
        self.city = city
        self.state = state
        self.zip_code = zip_code
        self.country_id = country_id

    def __repr__(self):
        return f'Address class = {self.address_id}, {self.street_1}, \
            {self.street_2}, {self.city}, {self.state}, {self.zip_code}, {self.country_id})'


class Phone(Base):
    """
    The phone number of a patient.
    """
    __tablename__ = 'Phones'
    phone_id = Column('Id', String(255), primary_key=True)
    phone_number = Column('PhoneNumber', String(255), nullable=False)
    phone_type_id = Column('PhoneTypeId', ForeignKey('PhoneTypes.Id'), nullable=True)

    phone_type = relationship('PhoneTypes')


    def __init__(self, phone_id=None, phone_number=None, phone_type_id=None):
        self.phone_id = phone_id
        self.phone_number = phone_number
        self.phone_type_id = phone_type_id


    def __repr__(self):
        return f'Phone class = {self.phone_id}, {self.phone_number}, {self.phone_type_id}'


class PhoneType(Base):
    """
    The phone type of a patient.
    """
    __tablename__ = 'PhoneTypes'
    phone_type_id = Column('Id', Integer, primary_key=True)
    phone_type = Column('PhoneType', String(255), nullable=False)


    def __init__(self, phone_type_id=None, phone_type=None):
        self.phone_type_id = phone_type_id
        self.phone_type = phone_type

    def __repr__(self):
        return f'PhoneType class = {self.phone_type_id}, {self.phone_type}'


class PreferredContact(Base):
    """
    The preferred contact of a patient.
    """
    __tablename__ = 'PreferredContacts'
    preferred_contact_id = Column('Id', Integer, primary_key=True)
    preferred_contact = Column('ContactTypes', String(255), nullable=False)


    def __init__(self, preferred_contact_id=None, preferred_contact=None):
        self.preferred_contact_id = preferred_contact_id
        self.preferred_contact = preferred_contact


    def __repr__(self) -> str:
        return f'PreferredContact class = {self.preferred_contact_id}, {self.preferred_contact}'


class Country(Base):
    """
    The country of a patient.
    """
    __tablename__ = 'Countries'
    country_id = Column('Id', String(255), primary_key=True)
    country = Column('Country', String(255), nullable=False)

    def __init__(self, country_id=None, country=None):
        self.country_id = country_id
        self.country = country

    def __repr__(self):
        return f'Country class = {self.country_id}, {self.country}'


class Language(Base):
    """
    The language of a patient.
    """
    __tablename__ = 'Languages'
    language_id = Column('Id', Integer, primary_key=True)
    language = Column('Language', String(255), nullable=False)

    def __init__(self, language_id=None, language=None):
        self.language_id = language_id
        self.language = language

    def __repr__(self):
        return f'Language class = {self.language_id}, {self.language}'


class CoverageType(Base):
    """
    The coverage type of the patient insurance.
    """
    __tablename__ = 'CoverageTypes'
    coverage_type_id = Column('Id', Integer, primary_key=True)
    coverage_type = Column('CoverageType', String(255), nullable=False)

    def __init__(self, coverage_type_id=None, coverage_type=None):
        self.coverage_type_id = coverage_type_id
        self.coverage_type = coverage_type

    def __repr__(self):
        return f'CoverageType class = {self.coverage_type_id}, {self.coverage_type}'

class ReferralType(Base):
    """
    The referral type of a patient.
    """
    __tablename__ ='ReferralTypes'
    referral_type_id = Column('Id', Integer, primary_key=True)
    referral_type = Column('ReferralType', String(255), nullable=False)

    def __init__(self, referral_type_id=None, referral_type=None):
        self.referral_type_id = referral_type_id
        self.referral_type = referral_type

    def __repr__(self):
        return f'ReferralType class = {self.referral_type_id}, {self.referral_type}'


class Intake(Base):
    """
    The intake record of a patient.
    """
    __tablename__ = 'Intakes'
    intake_id = Column('Id', String(255), primary_key=True)
    intake_date = Column('IntakeDate', Date(), nullable=True)
    intake_by_first_name = Column('IntakeFirstName', String(255), nullable=True)
    intake_by_last_name = Column('IntakeLastName', String(255), nullable=True)
    liason_first_name = Column('LiasonFirstName', String(255), nullable=True)
    liason_last_name = Column('LiasonLastName', String(255), nullable=True)
    patient_id = Column('PatientId', ForeignKey('Patients.Id'), nullable=True)

    patient = relationship('Patients', backref='Intakes', cascade='all, delete, delete-orphan')

    def __init__(self, intake_id=None, intake_date=None,
        intake_by_first_name=None, intake_by_last_name=None,
        liason_first_name=None, liason_last_name=None, patient_id=0):
        self.intake_id = intake_id
        self.intake_date = intake_date
        self.intake_by_first_name = intake_by_first_name
        self.intake_by_last_name = intake_by_last_name
        self.liason_first_name = liason_first_name
        self.liason_last_name = liason_last_name
        self.patient_id = patient_id

    def __repr__(self):
        return f'Intake class = {self.intake_id}, {self.intake_date}, \
            {self.intake_by_first_name}, {self.intake_by_last_name}, \
                {self.liason_first_name}, {self.liason_last_name}, {self.patient_id}'

class Image(Base):
    """
    The image of the patient's insurance card.
    """
    __tablename__ = 'Images'
    image_id = Column('Id', String(255), primary_key=True)
    image_name = Column('ImageName', String(255), nullable=False)
    image_url = Column('ImageUrl', String(500), nullable=False)
    widget_type = Column('WidgetType', String(255), nullable=False, default='imagelinks')

    def __init__(self, image_id=None, image_name=None, image_url=None, widget_type=None):
        self.image_id = image_id
        self.image_name = image_name
        self.image_url = image_url
        self.widget_type = widget_type

    def __repr__(self):
        return f'Image class = {self.image_id}, {self.image_name}, \
            {self.image_url}, {self.widget_type}'


class ResponseObject():
    """
    This class is used to store the response from the API.
    """
    patient = None
    address = None
    phone = None
    phone_type = None
    image = None
    preferred_contact = None
    country = None
    language = None
    coverage_type = None
    referral_type = None
    intake = None

    def __init__(self, patient:Patient, address:Address, phone:Phone,
        phone_type:PhoneType, image:Image, preferred_contact:PreferredContact,
        country:Country, language:Language, coverage_type:CoverageType,
        referral_type:ReferralType, intake:Intake):
        self.patient = patient
        self.address = address
        self.phone = phone
        self.phone_type = phone_type
        self.image = image
        self.preferred_contact = preferred_contact
        self.country = country
        self.language = language
        self.coverage_type = coverage_type
        self.referral_type = referral_type
        self.intake = intake

    def __repr__(self):
        return f'response_object class = {self.patient}, {self.address}, \
            {self.phone}, {self.phone_type}, {self.image}, {self.preferred_contact}, \
                {self.country}, {self.language}, {self.coverage_type}, {self.intake}'
