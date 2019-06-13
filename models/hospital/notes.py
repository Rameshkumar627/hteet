#

from odoo import models, fields
from datetime import datetime

Current_date = datetime.now().strftime("%Y-%m-%d")


class Notes(models.Model):
    _name = "arc.notes"

    date = fields.Date(string="Date", default=Current_date)
    employee_id = fields.Many2one(comodel_name="arc.employee", string="Doctor/ Staff")
    notes = fields.Html(string="Notes")
