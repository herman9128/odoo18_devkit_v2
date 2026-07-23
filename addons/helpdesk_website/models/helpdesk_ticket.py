from odoo import models, fields

class HelpdeskTicket(models.Model):
    _inherit = 'helpdesk.ticket' # Targets the exact OCA model name

    # The OCA model already has 'name' (subject), 'description', and 'partner_email'.
    # If you want to add a unique field just for your web form, define it here:
    mobile_phone = fields.Char(string="Customer Mobile")