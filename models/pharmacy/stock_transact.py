#

from odoo import models, fields, api
from datetime import datetime

PROGRESS_INFO = [("draft", "Draft"), ("Confirm", "Confirmed")]
TRANSACT_TYPE = [("in", "In"), ("scrap", "Scrap"), ("block", "Block")]
current_date = datetime.now().strftime("%Y-%m-%d")


class StockTransact(models.Model):
    _name = "stock.transact"

    date = fields.Date(string="Date", default=current_date)
    name = fields.Char(string="Name", readonlt=True)
    progress = fields.Selection(selection=PROGRESS_INFO, default="draft", string="Progress")
    transact_type = fields.Selection(selection=TRANSACT_TYPE, string="Transact Type")
    comment = fields.Text(string="Comment")
    transact_ids = fields.One2many(comodel_name="transact.detail", inverse_name="transact_id")

    @api.multi
    def trigger_transact(self):
        if self.transact_type == "in":
            source_id = self.env["arc.location"].search([("location_uid", "=", "VIRTUAL IN")])
            destination_id = self.env["arc.location"].search([("location_uid", "=", "PHARMACY")])
        elif self.transact_type == "scrap":
            source_id = self.env["arc.location"].search([("location_uid", "=", "PHARMACY")])
            destination_id = self.env["arc.location"].search([("location_uid", "=", "SCRAP")])
        elif self.transact_type == "block":
            source_id = self.env["arc.location"].search([("location_uid", "=", "PHARMACY")])
            destination_id = self.env["arc.location"].search([("location_uid", "=", "BLOCK")])

        # Check Batch
        for rec in self.transact_ids:
            batch_id = self.env["arc.batch"].search([("product_id", "=", rec.product_id.id),
                                                     ("name", "=", rec.name)])

            if not batch_id:
                batch_id = self.env["arc.batch"].create({"product_id": rec.product_id.id,
                                                         "name": rec.name,
                                                         "manufacturing_date": rec.manufacturing_date,
                                                         "expiry_date": rec.expiry_date,
                                                         "unit_price": rec.unit_price,
                                                         "mrp": rec.mrp})

            if batch_id:
                self.env["arc.move"].create({"date": self.date,
                                             "product_id": rec.product_id.id,
                                             "batch_id": batch_id.id,
                                             "description": rec.description,
                                             "quantity": rec.quantity,
                                             "source_id": source_id.id,
                                             "destination_id": destination_id.id,
                                             "progress": "moved",
                                             "ref": self.name})

    @api.model
    def create(self, vals):
        sequence = "{0}.{1}".format(self._name, vals["transact_type"])
        vals["name"] = self.env["ir.sequence"].next_by_code(sequence)
        return super(StockTransact, self).create(vals)


class TransactDetail(models.Model):
    _name = "transact.detail"

    product_id = fields.Many2one(comodel_name="arc.product", string="Product", required=True)
    name = fields.Char(string="Batch", required=True)
    description = fields.Text(string="Description")
    manufacturing_date = fields.Date(string="Manufacturing Date")
    expiry_date = fields.Date(string="Expiry Date")
    unit_price = fields.Float(string="Unit Price", default=0.0, required=True)
    mrp = fields.Float(string="MRP", default=0.0, required=True)
    quantity = fields.Float(string="Quantity", default=0.0, required=True)
    transact_id = fields.Many2one(comodel_name="stock.transact", string="Transact")




