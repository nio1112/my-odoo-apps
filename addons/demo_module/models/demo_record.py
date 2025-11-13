from odoo import api, fields, models

class DemoRecord(models.Model):
    _name = "demo.record"
    _description = "Demo Record"

    name = fields.Char(string="Name", required=True)
    description = fields.Text(string="Description")
    active = fields.Boolean(string="Active", default=True)
    value = fields.Integer(string="Value", default=0)