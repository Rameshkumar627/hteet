#

from odoo import models, fields


class Location(models.Model):
    _name = "arc.location"

    name = fields.Char(string="Name", required=True)
    location_uid = fields.Char(string="Code", required=True)
    