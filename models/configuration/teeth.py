#

from odoo import models, fields

TEETH_TYPE = [("canine", "Canine"),
              ("incisor", "Incisor"),
              ("premolar", "Premolar"),
              ("molar", "Molar")]


class Teeth(models.Model):
    _name = "teeth.teeth"

    name = fields.Char(string="Teeth")
    image = fields.Binary(string="Image")
    teeth_type = fields.Selection(selection=TEETH_TYPE, string="Teeth Type")
