#

from odoo import models, fields


class Demo(models.TransientModel):
    _name = "arc.demo"

    name = fields.Char(string="Name")
