#

from odoo import models, fields, api

PROGRESS_INFO = [("draft", "Draft"), ("confirm", "Confirm")]


class Laboratory(models.Model):
    _name = "arc.lab"

    date = fields.Date(string="Date", reauired=True)
    name = fields.Char(string="Name", readonly=True)
    patient_id = fields.Many2one(comodel_name="arc.patient", string="Patient", reauired=True)
    test_ids = fields.One2many(comodel_name="lab.test", inverse_name="laboratory_id", string="Tests")
    invoice_id = fields.Many2one(comodel_name="arc.invoice", string="Invoice")
    progress = fields.Selection(selection=PROGRESS_INFO, string="Progress")
    report = fields.Html(string="Report")
    attachment_ids = fields.Many2many(comodel_name="ir.attachment", string="Attachment")
    comment = fields.Text(string="Comment")
    report_pdf = fields.Binary(string="Report")
    file_name = fields.Char(string="File Name", default="report.pdf")

    @api.multi
    def trigger_confirm(self):
        self.write({"progress": "confirm"})

    @api.multi
    def trigger_report(self):
        recs = self.test_ids

