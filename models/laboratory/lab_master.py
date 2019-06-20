#

from odoo import models, fields


class LabMaster(models.Model):
    _name = "lab.master"

    name = fields.Char(string="Name")
    code = fields.Char(string="Code")
    price = fields.Float(string="Price")
    template = fields.Html(string="Template")
    paramsi = fields.Integer(string="Parameter")
    value_ids = fields.One2many(comodel_name="lab.master.detail.value", inverse_name="lab_id")
    image_ids = fields.One2many(comodel_name="lab.master.detail.image", inverse_name="lab_id")


class LabMasterDetailValue(models.Model):
    _name = "lab.master.detail.value"

    sequence = fields.Integer(string="S.No")
    name = fields.Char(string="Name")
    lab_id = fields.Many2one(comodel_name="lab.master", string="Lab")


class LabMasterDetailImage(models.Model):
    _name = "lab.master.detail.image"

    sequence = fields.Integer(string="S.No")
    name = fields.Char(string="Name")
    lab_id = fields.Many2one(comodel_name="lab.master", string="Lab")
