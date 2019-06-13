#

from odoo import models, fields, api, modules
from datetime import datetime
import pdfkit

current_date = datetime.now().strftime("%Y-%m-%d")
PROGRESS = [("draft", "Draft"), ("confirmed", "Confirmed")]
PAYMENT_PROGRESS = [("un_paid", "Un-Paid"), ("partially_paid", "Partially Paid"), ("paid", "Paid")]


class Invoice(models.Model):
    _name = "arc.invoice"
    _inherit = "mail.thread"

    date = fields.Date(string="Date", default=current_date)
    name = fields.Char(string="Name", readonly=False)
    doctor_id = fields.Many2one(comodel_name="arc.employee", string="Doctor")
    patient_id = fields.Many2one(comodel_name="arc.patient", string="Patient")
    detail_ids = fields.One2many(comodel_name="invoice.detail", inverse_name="invoice_id", string="Invoice Detail")
    progress = fields.Selection(selection=PROGRESS, string="Progress", default="draft")
    payment_progress = fields.Selection(selection=PAYMENT_PROGRESS, string="Payment Progress", default="un_paid")
    payment_id = fields.Many2one(comodel_name="arc.payment", string="Payment")

    sub_total_amount = fields.Float(string="Sub Total", default=0.0)
    discount_amount = fields.Float(string="Discount Amount", default=0.0)
    tax_amount = fields.Float(string="Round-Off", default=0.0)
    round_off = fields.Float(string="Round-Off", default=0.0)
    grand_amount = fields.Float(string="Round-Off", default=0.0)

    cgst = fields.Float(string="CGST", default=0.0)
    sgst = fields.Float(string="SGST", default=0.0)
    igst = fields.Float(string="IGST", default=0.0)

    file_name = fields.Char(string="File Name", default="Invoice.pdf")
    report = fields.Binary(string="Report")

    def get_dental_table(self):
        heading = """<tr>
                         <th>Description</th>
                         <th>Unit Price in INR</th>
                         <th>Discount in INR</th>
                         <th>Tax in INR</th>
                         <th>Total in INR</th>                                                  
                     </tr>"""

        recs = self.detail_ids

        body = ""
        record = ""
        for rec in recs:
            body_data = """<tr>            
                               <td style="text-align: left; width: 350px;">{0}</td>
                               <td style="text-align: right;">{1}</td>
                               <td style="text-align: right;">{2}</td>
                               <td style="text-align: right;">{3}</td>
                               <td style="text-align: right;">{4}</td>                               
                           </tr>""".format(rec.description_id.name,
                                           rec.unit_price,
                                           rec.discount,
                                           rec.tax,
                                           rec.total)
            body = "{0}{1}".format(body, body_data)

        if recs:
            record = """<table id="customers">
                            {0}
                            {1}
                     </table>""".format(heading, body)

        return record

    @api.multi
    def get_repo(self):
        file_path = modules.module.get_resource_path('hteet', 'static/src/html', 'prescription.html')

        html = ""
        html = open(file_path, "r").read()

        table = self.get_dental_table()
        prescription = html.format(table)
        pdfkit.from_string(prescription, '/opt/kon/out.pdf')


class InvoiceDetail(models.Model):
    _name = "invoice.detail"

    description_id = fields.Many2one(comodel_name="invoice.description", string="Description")
    unit_price = fields.Float(string="Unit Price in INR", default=0.0)
    discount = fields.Float(string="Discount in INR", default=0.0)
    tax = fields.Float(string="Tax in INR", default=0.0)
    total = fields.Float(string="Total in INR", default=0.0)
    invoice_id = fields.Many2one(comodel_name="arc.invoice", string="Invoice")
