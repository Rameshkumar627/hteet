#

from odoo import models, fields, api, modules
from datetime import datetime
import pdfkit
import base64

CONSUMPTION_TYPE = [("before_food", "Before Food"), ("after_food", "After Food")]
current_date = datetime.now().strftime("%Y-%m-%d")


class Prescription(models.Model):
    _name = "arc.prescription"

    date = fields.Date(string="Date", default=current_date)
    name = fields.Char(string="Name", readonly=True)
    doctor_id = fields.Many2one(comodel_name="arc.employee", string="Doctor")
    patient_id = fields.Many2one(comodel_name="arc.patient", string="Patient")
    total_days = fields.Integer(string="Total Days")
    prescription_ids = fields.One2many(comodel_name="prescription.detail", inverse_name="prescription_id")
    file_name = fields.Char(string="File Name", default="Prescription.pdf")
    report = fields.Binary(string="Prescription")
    comment = fields.Text(string="Comment")

    def get_dental_table(self):
        heading = """<tr>
                         <th>Medicine</th>
                         <th>Morning</th>
                         <th>Noon</th>
                         <th>Evening</th>
                         <th>Consumption</th>
                         <th>Quantity</th>
                     </tr>"""

        recs = self.prescription_ids

        body = ""
        record = ""
        for rec in recs:
            morning = "Y" if rec.morning else "-"
            noon = "Y" if rec.noon else "-"
            evening = "Y" if rec.evening else "-"
            consumption_type = rec.consumption_type.title().replace("_", " ")
            body_data = """<tr>            
                               <td style="text-align: left; width: 500px;">{0}</td>
                               <td style="text-align: center;">{1}</td>
                               <td style="text-align: center;">{2}</td>
                               <td style="text-align: center;">{3}</td>
                               <td style="text-align: center;">{4}</td>
                               <td style="text-align: right;">{5}</td>
                           </tr>""".format(rec.product_id.name,
                                           morning,
                                           noon,
                                           evening,
                                           consumption_type,
                                           rec.quantity)
            body = "{0}{1}".format(body, body_data)

        if recs:
            record = """<table id="customers">
                            {0}
                            {1}
                     </table>""".format(heading, body)

        return record

    def get_static_file(self):
        file_path = modules.module.get_resource_path('hteet', 'static/src/html', 'prescription.html')

        html = ""
        html = open(file_path, "r").read()

        return html

    @api.multi
    def get_repo(self):
        file_path = modules.module.get_resource_path('hteet', 'static/src/html', 'prescription.html')

        html = ""
        html = open(file_path, "r").read()

        table = self.get_dental_table()
        prescription = html.format(table)
        pdfkit.from_string(prescription, '/opt/kon/out.pdf')

        pdf_file = open('/opt/kon/out.pdf', 'rb')
        out = pdf_file.read()
        pdf_file.close()
        gentextfile = base64.b64encode(out)

        self.report = gentextfile


class PrescriptionDetail(models.Model):
    _name = "prescription.detail"

    product_id = fields.Many2one(comodel_name="arc.product", string="Medicine")
    morning = fields.Boolean(string="Morning")
    noon = fields.Boolean(string="Noon")
    evening = fields.Boolean(string="Evening")
    consumption_type = fields.Selection(selection=CONSUMPTION_TYPE, string="Consumption")
    quantity = fields.Integer(string="Quantity", default=0)
    prescription_id = fields.Many2one(comodel_name="arc.prescription", string="Prescription")
