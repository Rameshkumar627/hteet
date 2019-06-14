#

from odoo import models, fields, api
from datetime import datetime
import pdfkit
import base64

current_date = datetime.now().strftime("%Y-%m-%d")
TEETH_TYPE = [("canine", "Canine"),
              ("incisor", "Incisor"),
              ("premolar", "Premolar"),
              ("molar", "Molar")]


class Dental(models.Model):
    _name = "dental.treatment"

    date = fields.Date(string="Date")
    name = fields.Char(string="Name", readonly=True)
    patient_id = fields.Many2one(comodel_name="arc.patient", string="Patient")
    doctor_id = fields.Many2one(comodel_name="arc.employee", string="Doctor")
    patient_uid = fields.Char(string="Patient ID", related="patient_id.patient_uid")
    symptoms_ids = fields.Many2many(comodel_name="arc.symptoms", string="Symptoms")
    diagnosis_ids = fields.Many2many(comodel_name="arc.diagnosis", string="Diagnosis")
    diagnosis_comment = fields.Text(string="Treatment Comment")
    treatment_ids = fields.Many2many(comodel_name="arc.treatment", string="Treatment")
    treatment_comment = fields.Text(string="Treatment Comment")
    teeth_ids = fields.One2many(comodel_name="treatment.teeth", inverse_name="dental_id")
    prescription_id = fields.Many2one(comodel_name="arc.prescription", string="Prescription")
    invoice_id = fields.Many2one(comodel_name="arc.invoice", string="Invoice")
    report = fields.Html(string="Report")
    attachment_ids = fields.Many2many(comodel_name="ir.attachment", string="Attachment")
    file_name = fields.Char(string="File Name", default="treatment.pdf")
    report_pdf = fields.Binary(string="Report")
    next_appointment = fields.Date(string="Next Appointment")

    teeth_1 = fields.Boolean()
    teeth_2 = fields.Boolean()
    teeth_3 = fields.Boolean()
    teeth_4 = fields.Boolean()
    teeth_5 = fields.Boolean()
    teeth_6 = fields.Boolean()
    teeth_7 = fields.Boolean()
    teeth_8 = fields.Boolean()
    teeth_9 = fields.Boolean()
    teeth_10 = fields.Boolean()
    teeth_11 = fields.Boolean()
    teeth_12 = fields.Boolean()
    teeth_13 = fields.Boolean()
    teeth_14 = fields.Boolean()
    teeth_15 = fields.Boolean()
    teeth_16 = fields.Boolean()
    teeth_17 = fields.Boolean()
    teeth_18 = fields.Boolean()
    teeth_19 = fields.Boolean()
    teeth_20 = fields.Boolean()
    teeth_21 = fields.Boolean()
    teeth_22 = fields.Boolean()
    teeth_23 = fields.Boolean()
    teeth_24 = fields.Boolean()
    teeth_25 = fields.Boolean()
    teeth_26 = fields.Boolean()
    teeth_27 = fields.Boolean()
    teeth_28 = fields.Boolean()
    teeth_29 = fields.Boolean()
    teeth_30 = fields.Boolean()
    teeth_31 = fields.Boolean()
    teeth_32 = fields.Boolean()

    def get_comma(self, recs):
        record = ""
        for rec in recs:
            if record == "":
                record = "{1}({2})".format(record, rec.name, rec.code)
            else:
                record = "{0}, {1}({2})".format(record, rec.name, rec.code)

        return record

    def get_dental_table(self):
        heading = """<tr>
                         <th>Teeth</th>
                         <th>Teeth Type</th>
                         <th>Treatment</th>
                         <th>Comment</th>
                     </tr>"""

        recs = self.teeth_ids

        body = ""
        record = ""
        for rec in recs:
            body_data = """<tr>            
                               <td>{0}</td>
                               <td>{1}</td>
                               <td>{2}</td>
                               <td>{3}</td>
                           </tr>""".format(rec.teeth_id.name,
                                           rec.teeth_type,
                                           self.get_comma(rec.treatment_ids),
                                           rec.comment)
            body = "{0}{1}".format(body, body_data)

        if recs:
            record = """<table class="o_list_view table table-condensed table-striped">
                            {0}
                            {1}
                     </table>""".format(heading, body)

        return record

    @api.multi
    def generate_report(self):
        symptoms = self.get_comma(self.symptoms_ids)
        diagnosis = self.get_comma(self.diagnosis_ids)
        treatment = self.get_comma(self.treatment_ids)
        diagnosis_comment = self.diagnosis_comment or ""
        treatment_comment = self.treatment_comment or ""

        header = """<table>
                        <tr><td>{0}</td></tr>
                        <tr><td>{1}</td></tr>
                        <tr><td>{2}</td></tr>
                        <tr><td>{3}</td></tr>
                    </table>""".format(self.date, self.name, self.doctor_id.name, self.patient_id.name)

        body = """<table>
                        <tr><td style="width: 100px;">Symptoms</td><td>{0}</td></tr>
                        <tr><td>Diagnosis</td><td>{1}</td></tr>
                        <tr><td></td><td>{2}</td></tr>
                        <tr><td>Treatment</td><td>{3}</td></tr>
                        <tr><td></td><td>{4}</td></tr>
                  </table>""".format(symptoms, diagnosis, diagnosis_comment, treatment, treatment_comment)

        treatment_detail = self.get_dental_table()

        prescription = self.prescription_id.get_dental_table()

        html = self.prescription_id.get_static_file()

        report = "{0}{1}{2}{3}".format(header, body, treatment_detail, prescription)
        new_report = html.format(report)

        self.report = new_report

        pdfkit.from_string(new_report, '/opt/kon/out.pdf')

        pdf_file = open('/opt/kon/out.pdf', 'rb')
        out = pdf_file.read()
        pdf_file.close()
        gentextfile = base64.b64encode(out)

        self.report_pdf = gentextfile


class TreatmentTeeth(models.Model):
    _name = "treatment.teeth"

    teeth_id = fields.Many2one(comodel_name="teeth.teeth", string="Teeth")
    image = fields.Binary(string="Image", related="teeth_id.image")
    teeth_type = fields.Selection(selection=TEETH_TYPE, string="Teeth Type", related="teeth_id.teeth_type")
    treatment_ids = fields.Many2many(comodel_name="arc.treatment", string="Treatment")
    comment = fields.Text(string="Comment")
    dental_id = fields.Many2one(comodel_name="dental.treatment", string="Treatment")
