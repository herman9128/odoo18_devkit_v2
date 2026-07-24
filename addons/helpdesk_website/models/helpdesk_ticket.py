from odoo import models, fields

class HelpdeskTicket(models.Model):
    _inherit = 'helpdesk.ticket'

    site_office = fields.Char(string="Site Office")
    mobile_phone = fields.Char(string="Mobile Phone")

