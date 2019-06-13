#

from odoo import models, fields


class Diagnosis(models.Model):
    _name = "arc.diagnosis"

    name = fields.Char(string="Diagnosis")
    code = fields.Char(string="Code")
