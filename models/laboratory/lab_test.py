#

from odoo import models, fields, api


class LabTest(models.Model):
    _name = "lab.test"

    master_id = fields.Many2one(comodel_name="lab.master", string="Lab-Test")
    price = fields.Float(string="Price")
    template = fields.Html(string="Template")
    report = fields.Html(string="Report")
    value_ids = fields.One2many(comodel_name="lab.test.detail.value", inverse_name="lab_id")
    image_ids = fields.One2many(comodel_name="lab.test.detail.image", inverse_name="lab_id")
    laboratory_id = fields.Many2one(comodel_name="arc.lab", string="Laboratory")

    @api.model
    def create(self, vals):
        master_rec = self.env["lab.master"].search([("id", "=", vals["master_id"])])
        value_recs = self.env["lab.master.detail.value"].search([("lab_id", "=", vals["master_id"])])
        image_recs = self.env["lab.master.detail.image"].search([("lab_id", "=", vals["master_id"])])

        vals["price"] = master_rec.price
        vals["template"] = master_rec.template
        lab_id = super(LabTest, self).create(vals)

        for rec in value_recs:
            self.env["lab.test.detail.value"].create({"sequence": rec.sequence,
                                                      "name": rec.name,
                                                      "lab_id": lab_id.id})

        for rec in image_recs:
            self.env["lab.test.detail.image"].create({"sequence": rec.sequence,
                                                      "name": rec.name,
                                                      "lab_id": lab_id.id})

        return lab_id


class LabTestDetailValue(models.Model):
    _name = "lab.test.detail.value"

    sequence = fields.Integer(string="S.No")
    name = fields.Char(string="Name")
    value = fields.Char(string="Value")
    lab_id = fields.Many2one(comodel_name="lab.test", string="Lab")


class LabTestDetailImage(models.Model):
    _name = "lab.test.detail.image"

    sequence = fields.Integer(string="S.No")
    name = fields.Char(string="Name")
    image = fields.Binary(string="Image")
    lab_id = fields.Many2one(comodel_name="lab.test", string="Lab")
