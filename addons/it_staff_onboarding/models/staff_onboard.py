from odoo import models, fields, api, _
from odoo.exceptions import UserError


class ITStaffOnboard(models.Model):
    _name = 'it.staff.onboard'
    _description = 'IT Staff Onboarding'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    # 1. Primary Fields
    sequence_number = fields.Char(string='Sequence Number', readonly=True, copy=False, default='New')
    employee_number = fields.Char(string='Employee ID', required=True, tracking=True)
    staff_name = fields.Char(string='Staff Name', required=True, tracking=True)
    alias = fields.Char(string='Alias')
    position = fields.Char(string='Position')
    work_location = fields.Char(string='Work Location')
    project_id = fields.Many2one('project.project', string='Project')
    commence_date = fields.Date(string='Commence Date')
    supervisor_email = fields.Char(string='Supervisor Email')
    is_transfer = fields.Boolean(string='Is Transfer?')
    transfer_from = fields.Char(string='Transfer From')

    # IT Assets & Accounts
    mobile_phone = fields.Char(string='Mobile Phone')
    email_login = fields.Char(string='Email Login')
    initial_password = fields.Char(string='Initial Password')
    project_email = fields.Char(string='Project Email')
    m365_license_assigned = fields.Boolean(string='M365 License Assigned')
    m365_license_type = fields.Selection([
        ('business_standard', 'M365 Business Standard'),
        ('business_premium', 'M365 Business Premium'),
        ('exchange_online', 'Exchange On-line'),
    ], string='M365 License Type')
    computer_assigned = fields.Char(string='Computer Assigned')
    remark = fields.Text(string='Remark')

    # Offboarding
    resignation_date = fields.Date(string='Resignation Date')
    assets_returned = fields.Boolean(string='Assets Returned')
    m365_revoked = fields.Boolean(string='M365 Revoked')
    offboarding_notes = fields.Text(string='Offboarding Notes')

    # Status Field
    status = fields.Selection([
        ('draft', 'Draft'),
        ('active', 'Active'),
        ('resigned', 'Resigned')
    ], string='Status', default='draft', required=True, tracking=True)

    # Computed Fields for Pivot Analysis
    count_onboard = fields.Integer(
        string="Total Onboarded", 
        compute="_compute_movement_counts", 
        store=True
    )
    count_offboard = fields.Integer(
        string="Total Offboarded", 
        compute="_compute_movement_counts", 
        store=True
    )

    @api.depends('status')
    def _compute_movement_counts(self):
        for rec in self:
            if rec.status == 'active':
                rec.count_onboard = 1
                rec.count_offboard = 0
            elif rec.status == 'resigned':
                rec.count_onboard = 0
                rec.count_offboard = 1
            else:
                rec.count_onboard = 0
                rec.count_offboard = 0

    # Sequence Generation on Create
    @api.model
    def create(self, vals):
        if vals.get('sequence_number', 'New') == 'New':
            vals['sequence_number'] = self.env['ir.sequence'].next_by_code('it.staff.onboard') or 'New'
        return super(ITStaffOnboard, self).create(vals)

    def action_activate(self):
        self.write({'status': 'active'})

    def action_resign(self):
        self.write({'status': 'resigned'})

    def action_reactivate(self):
        self.write({'status': 'active'})

    def action_send_supervisor_email(self):
        """Triggers the XML template email to the supervisor."""
        self.ensure_one()
        
        if not self.supervisor_email:
            raise UserError(_("Please specify a Supervisor Email address before sending!"))

        # Look up the mail template by its XML ID
        template = self.env.ref('it_staff_onboarding.email_template_supervisor_onboard_notice', raise_if_not_found=False)
        
        if not template:
            raise UserError(_("Email template 'email_template_supervisor_onboard_notice' could not be found."))

        # Send email immediately using the template context
        template.send_mail(self.id, force_send=True)

        # Log confirmation in Chatter
        self.message_post(
            body=_("Onboarding notification email sent to supervisor: <b>%s</b>") % self.supervisor_email,
            subject=_("Supervisor Email Dispatched")
        )

        return {
            'type': 'ir.actions.client',
            'tag': 'display_notification',
            'params': {
                'title': _("Email Sent"),
                'message': _("Notification has been sent to %s") % self.supervisor_email,
                'type': 'success',
                'sticky': False,
            }
        }