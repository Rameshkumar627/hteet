#

from odoo import models, fields
from datetime import datetime

Current_date = datetime.now().strftime("%Y-%m-%d")


class ClinicalNotes(models.Model):
    _name = "clinical.notes"

    date = fields.Date(string="Date", default=Current_date)
    doctor_id = fields.Many2one(comodel_name="arc.employee", string="Doctor")
    patient_id = fields.Many2one(comodel_name="arc.patient", string="Patient")
    notes = fields.Html(string="Notes")
