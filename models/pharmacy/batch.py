#

from odoo import models, fields, api


class Batch(models.Model):
    _name = "arc.batch"

    name = fields.Char(string="Batch")
    product_id = fields.Many2one(comodel_name="arc.product", string="Product")
    description = fields.Text(string="Description")
    manufacturing_date = fields.Date(string="Manufacturing Date")
    expiry_date = fields.Date(string="Expiry Date")
    unit_price = fields.Float(string="Unit Price")
    mrp = fields.Float(string="MRP")
    quantity = fields.Float(string="Quantity", compute="get_quantity")

    @api.multi
    def get_quantity(self):
        pharmacy_id = self.env["arc.location"].search([("location_uid", "=", "PHARMACY")])
        for rec in self:
            rec.quantity = self.env["arc.stock"].get_current_stock(rec.product_id.id,
                                                                   pharmacy_id.id,
                                                                   rec.id)
