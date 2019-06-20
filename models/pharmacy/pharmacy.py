#

from odoo import models, fields, api
from datetime import datetime

current_date = datetime.now().strftime("%Y-%m-%d")
PROGRESS = [("draft", "Draft"), ("confirmed", "Confirmed")]
PAYMENT_PROGRESS = [("un_paid", "Un-Paid"), ("paid", "Paid")]


class Pharmacy(models.Model):
    _name = "arc.pharmacy"
    _inherit = "mail.thread"

    date = fields.Date(string="Date", default=current_date, required=True)
    name = fields.Char(string="Name", readonly=True)
    patient_id = fields.Many2one(comodel_name="arc.patient", string="Patient", required=True)
    progress = fields.Selection(selection=PROGRESS, string="Progress", default="draft")
    payment_progress = fields.Selection(selection=PAYMENT_PROGRESS, string="Payment Progress", default="un_paid")
    detail_ids = fields.One2many(comodel_name="pharmacy.detail", inverse_name="pharmacy_id")
    comment = fields.Text(string="Comment")

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

    @api.multi
    def generate_payment(self):
        self.env["arc.payment"].create({"date": current_date,
                                        "patient_id": self.patient_id.id,
                                        "amount": self.grand_amount})

    @api.multi
    def trigger_update_total(self):
        recs = self.detail_ids

        sub_total_amount = cgst = sgst = igst = tax_amount = discount_amount = 0
        for rec in recs:
            rec.update_total()
            cgst = cgst + rec.cgst
            sgst = sgst + rec.sgst
            igst = igst + rec.igst
            sub_total_amount = sub_total_amount + rec.total
            tax_amount = tax_amount + rec.tax_amount
            discount_amount = discount_amount + rec.discount_amount

        total = sub_total_amount
        self.grand_amount = round(total)
        self.round_off = round(total) - total
        self.cgst = cgst
        self.sgst = sgst
        self.igst = igst
        self.sub_total_amount = sub_total_amount
        self.tax_amount = tax_amount
        self.discount_amount = discount_amount

    @api.multi
    def trigger_paid(self):
        self.trigger_update_total()
        source_id = self.env["arc.location"].search([("location_uid", "=", "PHARMACY")])
        destination_id = self.env["arc.location"].search([("location_uid", "=", "VIRTUAL OUT")])

        # Check Batch
        for rec in self.detail_ids:
            self.env["arc.move"].create({"date": self.date,
                                         "product_id": rec.product_id.id,
                                         "batch_id": rec.batch_id.id,
                                         "quantity": rec.quantity,
                                         "source_id": source_id.id,
                                         "destination_id": destination_id.id,
                                         "progress": "moved",
                                         "ref": self.name})

        self.generate_payment()
        self.write({"payment_progress": "paid"})

    @api.model
    def create(self, vals):
        vals["name"] = self.env["ir.sequence"].next_by_code(self._name)
        return super(Pharmacy, self).create(vals)


class PharmacyDetails(models.Model):
    _name = "pharmacy.detail"

    product_id = fields.Many2one(comodel_name="arc.product", string="Product")
    batch_id = fields.Many2one(comodel_name="arc.batch", string="Batch")
    manufacturing_date = fields.Date(string="Manufacturing Date", related="batch_id.manufacturing_date")
    expiry_date = fields.Date(string="Expiry Date", related="batch_id.expiry_date")
    unit_price = fields.Float(string="Unit Price", related="batch_id.unit_price")
    mrp = fields.Float(string="MRP", related="batch_id.mrp")
    quantity = fields.Float(string="Quantity")
    discount = fields.Float(string="Discount in INR", default=0.0)
    tax_id = fields.Many2one(comodel_name="product.tax", string="Tax")
    total = fields.Float(string="Total in INR", default=0.0)
    pharmacy_id = fields.Many2one(comodel_name="arc.pharmacy", string="Pharmacy")

    cgst = fields.Float(string="CGST", required=True, readonly=True, default=0.0)
    sgst = fields.Float(string="SGST", required=True, readonly=True, default=0.0)
    igst = fields.Float(string="IGST", required=True, readonly=True, default=0.0)
    discount_amount = fields.Float(string="", required=True, readonly=True, default=0.0)
    after_discount = fields.Float(string="", required=True, readonly=True, default=0.0)
    tax_amount = fields.Float(string="", required=True, default=0.0)

    def update_total(self):
        state_type = "inter"

        vals = self.env["arc.calculation"].get_item_val(self.mrp,
                                                        self.quantity,
                                                        self.discount,
                                                        self.tax_id.rate,
                                                        state_type)

        self.write(vals)

