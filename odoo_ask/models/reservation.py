from odoo import models, fields, api
from odoo.exceptions import ValidationError

class AskReservation(models.Model):
    _name = 'ask.reservation'
    _description = 'Ask Reservation'

    name = fields.Char(string='Reservation Number', required=True, copy=False, readonly=True, default=lambda self: self.env['ir.sequence'].next_by_code('ask.reservation'))
    ask_line_id = fields.Many2one('ask.line', string='Ask Line', required=True)
    product_id = fields.Many2one('product.product', string='Product', related='ask_line_id.product_id', store=True)
    qty = fields.Float(string='Reserved Quantity')
    uom_id = fields.Many2one('uom.uom', string='Unit of Measure', related='ask_line_id.uom_id')
    reserved_to_sales_id = fields.Many2one('res.users', string='Reserved for Salesperson')
    reserved_at = fields.Datetime(string='Reserved At', default=fields.Datetime.now)
    obligation_end_date = fields.Datetime(string='Obligation End Date', compute='_compute_obligation_end_date', store=True)
    status = fields.Selection([
        ('reserved', 'Reserved'),
        ('partially_released', 'Partially Released'),
        ('released', 'Released'),
        ('overdue', 'Overdue'),
    ], string='Status', default='reserved')
    related_po_id = fields.Many2one('purchase.order', string='Related Purchase Order')
    storage_fee_estimate = fields.Monetary(string='Storage Fee Estimate', currency_field='currency_id')
    storage_fee_invoiced = fields.Monetary(string='Storage Fee Invoiced', currency_field='currency_id')
    currency_id = fields.Many2one('res.currency', related='ask_line_id.ask_id.partner_id.currency_id')

    @api.depends('reserved_at')
    def _compute_obligation_end_date(self):
        for record in self:
            # Default to 14 days, can be made configurable
            if record.reserved_at:
                record.obligation_end_date = fields.Datetime.add(record.reserved_at, days=14)
            else:
                record.obligation_end_date = False

    @api.constrains('qty', 'ask_line_id')
    def _check_qty(self):
        for record in self:
            if record.qty <= 0:
                raise ValidationError("Reserved quantity must be positive.")
            total_reserved = sum(record.ask_line_id.reservation_ids.mapped('qty'))
            if total_reserved > record.ask_line_id.valid_ask_qty:
                raise ValidationError("Total reserved quantity cannot exceed the valid ask quantity.")

class AskStorageFee(models.Model):
    _name = 'ask.storage_fee'
    _description = 'Ask Storage Fee'

    reservation_id = fields.Many2one('ask.reservation', string='Reservation', required=True)
    days_overdue = fields.Integer(string='Days Overdue')
    daily_rate = fields.Float(string='Daily Rate')
    total_fee = fields.Monetary(string='Total Fee', compute='_compute_total_fee', store=True, currency_field='currency_id')
    accounted_move_id = fields.Many2one('account.move', string='Accounted Journal Entry')
    currency_id = fields.Many2one('res.currency', related='reservation_id.currency_id')

    @api.depends('days_overdue', 'daily_rate')
    def _compute_total_fee(self):
        for record in self:
            record.total_fee = record.days_overdue * record.daily_rate