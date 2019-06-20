#

from odoo import models, fields

PROGRESS_INFO = [("draft", "Draft"), ("moved", "Moved")]


class StockMove(models.Model):
    _name = "arc.move"

    date = fields.Date(string="Date")
    name = fields.Char(string="Name")
    product_id = fields.Many2one(comodel_name="arc.product", string="Product")
    batch_id = fields.Many2one(comodel_name="arc.batch", string="Batch")
    description = fields.Text(string="Description")
    quantity = fields.Float(string="Quantity", default=0.0)
    source_id = fields.Many2one(comodel_name="arc.location", string="Source")
    destination_id = fields.Many2one(comodel_name="arc.location", string="Destination")
    progress = fields.Selection(selection=PROGRESS_INFO, default="draft", string="Progress")
    comment = fields.Text(string="Comment")
    ref = fields.Char(string="Ref")
