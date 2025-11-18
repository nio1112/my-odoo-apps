from odoo import models, fields, api
from odoo.exceptions import ValidationError

class AskWizard(models.TransientModel):
    _name = 'ask.wizard'
    _description = 'Ask Creation Wizard'

    partner_id = fields.Many2one('res.partner', string='客户', required=True)
    date_target = fields.Date(string='目标出货日期', required=True, default=fields.Date.today)
    recurrence_days = fields.Selection([
        ('0', '一次性'),
        ('7', '7天'),
        ('14', '14天'),
        ('21', '21天'),
        ('28', '28天'),
    ], string='周期', default='7', required=True)
    source_type = fields.Selection([
        ('phone', '电话'),
        ('email', '邮件'),
        ('portal', '门户'),
        ('manual', '手工'),
    ], string='来源类型', default='phone', required=True)
    vkgrp = fields.Char(string='销售组')
    note = fields.Text(string='备注')
    
    # 产品明细
    line_ids = fields.One2many('ask.wizard.line', 'wizard_id', string='产品明细')

    @api.model
    def default_get(self, fields_list):
        """设置默认值"""
        res = super().default_get(fields_list)
        # 设置默认的目标日期为明天
        res['date_target'] = fields.Date.add(fields.Date.today(), days=1)
        return res

    def action_create_ask(self):
        """创建问货单"""
        if not self.line_ids:
            raise ValidationError("请至少添加一个产品明细")
        
        # 创建问货单头
        ask_vals = {
            'partner_id': self.partner_id.id,
            'date_target': self.date_target,
            'recurrence_days': self.recurrence_days,
            'source_type': self.source_type,
            'vkgrp': self.vkgrp,
            'note': self.note,
            'state': 'draft',
        }
        ask = self.env['ask.ask'].create(ask_vals)
        
        # 创建明细行
        for line in self.line_ids:
            line_vals = {
                'ask_id': ask.id,
                'product_id': line.product_id.id,
                'ask_qty': line.ask_qty,
                'werks': line.werks,
                'comments': line.comments,
            }
            self.env['ask.line'].create(line_vals)
        
        # 返回创建的问货单
        return {
            'type': 'ir.actions.act_window',
            'name': '问货单',
            'res_model': 'ask.ask',
            'res_id': ask.id,
            'view_mode': 'form',
            'target': 'current',
        }

class AskWizardLine(models.TransientModel):
    _name = 'ask.wizard.line'
    _description = 'Ask Wizard Line'

    wizard_id = fields.Many2one('ask.wizard', string='向导', required=True, ondelete='cascade')
    product_id = fields.Many2one('product.product', string='产品', required=True)
    ask_qty = fields.Float(string='问货数量', required=True)
    werks = fields.Char(string='仓库')
    comments = fields.Text(string='备注')

