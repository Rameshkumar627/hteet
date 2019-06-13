#

from odoo import models, fields, api
from datetime import datetime

current_date = datetime.now().strftime("%Y-%m-%d")


class InvoiceReport(models.TransientModel):
    _name = "invoice.report"

    from_date = fields.Date(string="From Date", default=current_date, required=True)
    till_date = fields.Date(string="Till Date", default=current_date, required=True)
    patient_id = fields.Many2one(comodel_name="arc.patient", string="Patient")

    @api.multi
    def trigger_report(self):
        if self.patient_id:
            recs = self.env["arc.invoice"].search([("date", ">=", self.from_date),
                                                   ("date", ">=", self.till_date),
                                                   ("patient_id", "=", self.patient_id.id)])
        else:
            recs = self.env["arc.invoice"].search([("date", ">=", self.from_date),
                                                   ("date", ">=", self.till_date)])

        report = []
        for rec in recs:
            report.append({"date": rec.date,
                           "name": rec.patient_id.name,
                           "patient_id": rec.patient_id.patient_uid,
                           "sub_total_amount": rec.sub_total_amount,
                           "discount_amount": rec.discount_amount,
                           "tax_amount": rec.tax_amount,
                           "round_off": rec.round_off,
                           "grand_amount": rec.grand_amount,
                           "payment_progress": rec.payment_progress})

        print report
