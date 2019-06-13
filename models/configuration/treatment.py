#

from odoo import models, fields


class Treatment(models.Model):
    _name = "arc.treatment"

    name = fields.Char(string="Treatment")
    code = fields.Char(string="Code")

    description = fields.Html(string="Description")
