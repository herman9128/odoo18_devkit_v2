from odoo import models, fields

class HelpdeskTicket(models.Model):
    _inherit = 'helpdesk.ticket'

    site_office = fields.Char(string="Site Office")
    mobile_phone = fields.Char(string="Mobile Phone")

    action_type = fields.Selection([
        ('investigate', 'Investigate Issue'),
        ('site_visit', 'Site Visit Required'),
        ('hardware_replacement', 'Hardware Replacement'),
        ('software_update', 'Software Update / Patch'),
        ('other', 'Other Action'),
    ], string="Action Required", default='investigate')

    # Custom Status field
    ticket_status = fields.Selection([
        ('pending', 'Pending Review'),
        ('in_progress', 'In Progress'),
        ('waiting_part', 'Waiting for Parts'),
        ('resolved', 'Resolved'),
        ('escalated', 'Escalated'),
        ('cancelled', 'Cancelled'),
    ], string="Status", default='pending')

    # Action Taken description field
    action_taken = fields.Text(string="Action Taken")
    # Supervision field added below Action Taken
    supervision = fields.Text(string="Supervision")

    def _default_user_id(self):
        # Search for Susann Choi's user ID via email
        user = self.env['res.users'].sudo().search([
            ('login', '=', 'Susanna Choi')
        ], limit=1)
        if not user:
            user = self.env['res.users'].sudo().search([
                ('email', '=', 'susannchoi@lanon.hk')
            ], limit=1)
        return user.id if user else False

    # Set default value for assigned user / support specialist
    user_id = fields.Many2one(
        'res.users',
        string="Support Specialist",
        default=_default_user_id
    )
