#

from odoo import models, fields


class Symptoms(models.Model):
    _name = "arc.symptoms"

    name = fields.Char(string="Symptoms")
    code = fields.Char(string="Code")
