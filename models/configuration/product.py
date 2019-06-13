#

from odoo import models, fields


class Product(models.Model):
    _name = "arc.product"

    name = fields.Char(string="Medicine")
    code = fields.Char(string="Code")
