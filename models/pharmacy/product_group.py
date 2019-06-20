#

from odoo import models, fields


class ProductGroup(models.Model):
    _name = "product.group"

    name = fields.Char(string="Name", required=True)
    group_uid = fields.Char(string="Code", required=True)
    sub_group_ids = fields.One2many(comodel_name="product.sub.group", inverse_name="group_id")
