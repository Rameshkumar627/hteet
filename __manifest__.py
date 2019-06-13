# -*- coding: utf-8 -GPK*-

{
    "name": "Sivappu",
    "version": "1.0",
    "author": "La Mars",
    "website": "http://",
    "category": "Sivappu",
    "sequence": 1,
    "summary": "Hospital Management System",
    "description": """

    Hospital Management System

    Patient Management
    Employee Management
    Purchase Management
    Pharmacy Management
    Assert Management
    Accounts Management

    """,
    "depends": ["base", "mail"],
    "data": [

        "views/assert_backend.xml",
        
        "views/contact/contact.xml",
        "views/contact/patient.xml",
        "views/contact/staff.xml",
        "views/contact/supplier.xml",
        "views/contact/service.xml",
        
        "views/emr/patient.xml",
        "views/emr/appointment.xml",
        "views/emr/dental_treatment.xml",
        "views/emr/prescription.xml",
        "views/emr/clinical_notes.xml",

        "views/billing/invoice.xml",
        "views/billing/payment.xml",
        
        "views/configuration/symptoms.xml",
        "views/configuration/diagnosis.xml",
        "views/configuration/treatment.xml",
        "views/configuration/appointment_type.xml",
        "views/configuration/appointment_reason.xml",
        "views/configuration/invoice_description.xml",
        "views/configuration/product.xml",
        "views/configuration/teeth.xml",

        "views/staff/doctor_availability.xml",
        "views/staff/doctor_timings.xml",
        "views/staff/notes.xml",
        "views/staff/reminder.xml",
        "views/staff/staff.xml",

        "views/others/person.xml",
        "views/others/others.xml",
        "views/others/supplier.xml",
        "views/others/service.xml",

        # Menu
        "views/menu/menu.xml",

    ],
    "demo": [

    ],
    "qweb": [

    ],
    "installable": True,
    "auto_install": False,
    "application": True,
}