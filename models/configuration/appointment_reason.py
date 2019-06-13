#

from odoo import models, fields


class AppointmentReason(models.Model):
    _name = "appointment.reason"

    name = fields.Char(string="Reason")
