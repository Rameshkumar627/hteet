#

from odoo import models, fields
from datetime import datetime

current_date = datetime.now().strftime("%Y-%m-%d")
TRANSACTION_TYPE = [("cash", "Cash"), ("bank", "Bank")]
TRANSACTION_CATEGORY = [("credit_debit_card", "Credit/ Debit Card"),
                        ("paytm", "Paytm"),
                        ("google_pay", "Google Pay")]


class Payment(models.Model):
    _name = "arc.payment"
    _inherit = "mail.thread"

    date = fields.Date(string="Date", default=current_date)
    name = fields.Char(string="Name", readonly=False)
    patient_id = fields.Many2one(comodel_name="arc.patient", string="Patient")
    amount = fields.Float(string="Amount", default=0.0)
    transaction_type = fields.Selection(selection=TRANSACTION_TYPE, string="Payment")
    transaction_category = fields.Selection(selection=TRANSACTION_CATEGORY, string="Payment Category")

