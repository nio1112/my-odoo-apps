from odoo import models, fields, api
from odoo.exceptions import ValidationError

class Ask(models.Model):
    _name = 'ask.ask'
    _description = 'Ask Order'
    _inherit = ['mail.thread']

    name = fields.Char(string='Ask Number', required=True, copy=False, readonly=True, default=lambda self: self.env['ir.sequence'].next_by_code('ask.ask'))
    partner_id = fields.Many2one('res.partner', string='Customer', required=True)
    date_target = fields.Date(string='Target Delivery Date', required=True)
    recurrence_days = fields.Selection([
        ('0', 'One-time'),
        ('7', '7 Days'),
        ('14', '14 Days'),
        ('21', '21 Days'),
        ('28', '28 Days'),
    ], string='Recurrence', default='0')
    state = fields.Selection([
        ('draft', 'Draft'),
        ('submitted', 'Submitted'),
        ('locked', 'Locked'),
        ('aggregated', 'Aggregated'),
        ('closed', 'Closed'),
    ], string='Status', default='draft', tracking=True)
    created_by = fields.Many2one('res.users', string='Created By', default=lambda self: self.env.user)
    source_type = fields.Selection([
        ('phone', 'Phone'),
        ('email', 'Email'),
        ('portal', 'Portal'),
        ('manual', 'Manual'),
    ], string='Source Type', default='manual')
    note = fields.Text(string='Note')
    line_ids = fields.One2many('ask.line', 'ask_id', string='Ask Lines')
    vkgrp = fields.Char(string='Sales Group (VKGRP)')

    def action_submit(self):
        """提交问货单"""
        for record in self:
            if not record.line_ids:
                raise ValidationError("请至少添加一个产品明细")
            record.state = 'submitted'
        return True

    def action_lock(self):
        """锁定问货单"""
        for record in self:
            record.state = 'locked'
        return True

    def action_close(self):
        """关闭问货单"""
        for record in self:
            record.state = 'closed'
        return True


class AskLine(models.Model):
    _name = 'ask.line'
    _description = 'Ask Order Line'

    ask_id = fields.Many2one('ask.ask', string='Ask Order', required=True, ondelete='cascade')
    product_id = fields.Many2one('product.product', string='Product', required=True)
    ask_qty = fields.Float(string='Ask Quantity')
    valid_ask_qty = fields.Float(string='Valid Ask Quantity', readonly=True)
    uom_id = fields.Many2one('uom.uom', string='Unit of Measure', related='product_id.uom_id')
    sales_suggested_qty = fields.Float(string='Suggested Quantity', compute='_compute_sales_suggested_qty', store=True)
    client_confirmed_qty = fields.Float(string='Client Confirmed Quantity')
    reserved_qty = fields.Float(string='Reserved Quantity', compute='_compute_reserved_qty')
    reservation_ids = fields.One2many('ask.reservation', 'ask_line_id', string='Reservations', readonly=True)

    # Fields from tb_010_ask mapping
    week_qty = fields.Integer('WeekQty')
    week_days = fields.Integer('WeekDays')
    nweek_qty = fields.Integer('NWeekQty')
    nweek_qty_s = fields.Integer('NWeekQty_S')
    over_reference = fields.Integer('OverReference')
    today_qty = fields.Integer('todayQty')
    ask_days = fields.Integer('Ask Days', default=7)
    comments = fields.Text('Comments')
    ai_trained_quantity = fields.Integer('AI Trained Quantity')
    ask_reference = fields.Integer('Ask Reference')
    last_update = fields.Datetime('Last Update')
    read_time = fields.Datetime('Read Time')
    rtype = fields.Char('Customer Type (rtype)')
    werks = fields.Char('Warehouse/Plant (WERKS)')
    buyer_id = fields.Many2one('res.users', string='Buyer')
    update_by = fields.Char('Updated By (AI/Manual)')
    inquiring_ai_adjust_time = fields.Datetime('AI Adjust Time')
    cutoff_log = fields.Text(string="Cutoff Log", readonly=True)

    @api.depends('reservation_ids.qty')
    def _compute_reserved_qty(self):
        """计算已分货数量"""
        for line in self:
            line.reserved_qty = sum(line.reservation_ids.mapped('qty'))

    @api.depends('product_id', 'ask_id.partner_id', 'ask_id.date_target')
    def _compute_sales_suggested_qty(self):
        """基于历史数据计算建议数量"""
        for line in self:
            if not line.product_id or not line.ask_id.partner_id:
                line.sales_suggested_qty = 0.0
                continue
            
            # 获取过去7/14/21/28天的历史数据
            days_back = int(line.ask_id.recurrence_days) if line.ask_id.recurrence_days != '0' else 7
            start_date = fields.Date.subtract(line.ask_id.date_target, days=days_back)
            
            # 查询历史销售数据（这里简化处理，实际应该查询sale.order.line）
            # 暂时返回0，后续可以接入真实的销售历史数据
            line.sales_suggested_qty = 0.0

    @api.constrains('ask_qty')
    def _check_ask_qty(self):
        """验证问货数量"""
        for line in self:
            if line.ask_qty < 0:
                raise ValidationError("问货数量不能为负数")

    @api.constrains('ask_id', 'product_id', 'werks')
    def _check_unique_product_per_warehouse(self):
        """确保同一仓库中每个产品只能被问货一次"""
        for line in self:
            if line.ask_id and line.product_id and line.werks:
                existing = self.search([
                    ('ask_id', '=', line.ask_id.id),
                    ('product_id', '=', line.product_id.id),
                    ('werks', '=', line.werks),
                    ('id', '!=', line.id)
                ])
                if existing:
                    raise ValidationError(f"产品 {line.product_id.name} 在仓库 {line.werks} 中已经被问货过了")