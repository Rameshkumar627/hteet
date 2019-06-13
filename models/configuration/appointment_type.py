#

from odoo import models, fields


class AppointmentType(models.Model):
    _name = "appointment.type"

    name = fields.Char(string="Type")
