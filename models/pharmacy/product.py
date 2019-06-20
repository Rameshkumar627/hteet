#

from odoo import models, fields, api

PROGRESS_INFO = [("draft", "Draft"), ("confirmed", "Confirmed")]


class Product(models.Model):
    _name = "arc.product"

    name = fields.Char(string="Name", required=True)
    product_uid = fields.Char(string="Code", readonly=True)
    group_id = fields.Many2one(comodel_name="product.group", string="Group", required=True)
    sub_group_id = fields.Many2one(comodel_name="product.sub.group", string="Sub Group", required=True)
    image = fields.Binary(string="Image")
    description = fields.Text(string="Description")
    comment = fields.Text(string="Comment")
    batch_ids = fields.One2many(comodel_name="arc.batch", inverse_name="product_id")
    hsn_code = fields.Char(string="HSN Code")
    progress = fields.Selection(selection=PROGRESS_INFO, string="Progress", default="draft")
    quantity = fields.Float(string="Quantity", compute="get_quantity")

    @api.multi
    def get_quantity(self):
        for rec in self:
            batch_ids = rec.batch_ids

            rec.quantity = sum(batch_ids.mapped("quantity"))

    @api.multi
    def name_get(self):
        result = []
        for record in self:
            name = "[{0}] {1}".format(record.product_uid, record.name)
            result.append((record.id, name))
        return result

    @api.multi
    def trigger_confirm(self):
        # Generate Code on confirmation
        group_uid = self.group_id.group_uid
        sub_group_uid = self.sub_group_id.sub_group_uid
        sequence = self.env["ir.sequence"].next_by_code(self._name)

        product_uid = "{0}/{1}/{2}".format(group_uid, sub_group_uid, sequence)

        self.write({"progress": "confirmed", "product_uid": product_uid})


