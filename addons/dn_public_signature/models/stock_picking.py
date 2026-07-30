import uuid
from odoo import models, fields, api

class StockPicking(models.Model):
    _inherit = 'stock.picking'

    access_token = fields.Char(string='Public Access Token', copy=False, readonly=True)
    signature = fields.Binary(string='Customer Signature', copy=False, attachment=True)
    signed_by = fields.Char(string='Signed By', copy=False)
    signed_on = fields.Datetime(string='Signed On', copy=False)
    
    # New status field
    signature_state = fields.Selection([
        ('pending', 'Pending Signature'),
        ('signed', 'Signed'),
    ], string='Signature Status', default='pending', copy=False, tracking=True)

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            if not vals.get('access_token'):
                vals['access_token'] = str(uuid.uuid4())
        return super().create(vals_list)

    def action_generate_access_token(self):
        for picking in self:
            if not picking.access_token:
                picking.access_token = str(uuid.uuid4())

    def get_public_url(self):
        self.ensure_one()
        base_url = self.env['ir.config_parameter'].sudo().get_param('web.base.url')
        return f"{base_url}/dn/confirm/{self.access_token}"

    def action_copy_public_url(self):
        self.ensure_one()
        if not self.access_token:
            self.action_generate_access_token()
            
        public_url = self.get_public_url()

        return {
            'type': 'ir.actions.client',
            'tag': 'display_notification',
            'params': {
                'title': 'Public Signature Link Generated',
                'message': f'Link: {public_url}',
                'sticky': True,
                'type': 'info',
            }
        }