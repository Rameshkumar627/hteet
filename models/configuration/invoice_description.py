#

from odoo import models, fields


class InvoiceDescription(models.Model):
    _name = "invoice.description"

    name = fields.Char(string="Description")
    code = fields.Char(string="Code")
