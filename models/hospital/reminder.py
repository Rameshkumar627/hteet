#

from odoo import models, fields
from datetime import datetime

Current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")


class Reminder(models.Model):
    _name = "arc.reminder"

    date = fields.Datetime(string="Date", default=Current_time)
    employee_id = fields.Many2one(comodel_name="arc.employee", string="Doctor/ Staff")
    reminder = fields.Text(string="Reminder")
