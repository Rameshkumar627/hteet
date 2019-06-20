#

from odoo import models, fields, api

PROGRESS_INFO = [("draft", "Draft"), ("confirm", "Confirm")]


class Laboratory(models.Model):
    _name = "arc.lab"

    date = fields.Date(string="Date")
    name = fields.Char(string="Name")
    patient_id = fields.Many2one(comodel_name="arc.patient", string="Patient")
    test_ids = fields.One2many(comodel_name="lab.test", inverse_name="laboratory_id", string="Tests")
    invoice_id = fields.Many2one(comodel_name="arc.invoice", string="Invoice")
    progress = fields.Selection(selection=PROGRESS_INFO, string="Progress")
    report = fields.Html(string="Report")
    attachment_ids = fields.Many2many(comodel_name="ir.attachment", string="Attachment")
    comment = fields.Text(string="Comment")

    @api.multi
    def trigger_confirm(self):
        pass
