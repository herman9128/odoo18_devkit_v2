import base64
from odoo import http
from odoo.http import request


class ContactSupportController(http.Controller):

    @http.route(['/contact-support'], type='http', auth='public', website=True)
    def contact_support_page(self, **kw):
        return request.render('helpdesk_website.contact_support_page_template')

    @http.route(['/contact-support/submit'], type='http', auth='public', methods=['POST'], website=True, csrf=True)
    def submit_support_ticket(self, **post):
        partner_id = False
        if not request.env.user._is_public():
            partner_id = request.env.user.partner_id.id

        ticket_vals = {
            'name': post.get('name'),
            'partner_name': post.get('partner_name'),
            'partner_email': post.get('partner_email'),
            'site_office': post.get('site_office'),
            'mobile_phone': post.get('mobile_phone'),
            'description': post.get('description'),
            'partner_id': partner_id,
        }

        # Create ticket
        ticket = request.env['helpdesk.ticket'].sudo().create(ticket_vals)

        # Process uploaded files safely
        if request.httprequest.files.getlist('attachment'):
            for file in request.httprequest.files.getlist('attachment'):
                if file.filename:
                    request.env['ir.attachment'].sudo().create({
                        'name': file.filename,
                        'datas': base64.b64encode(file.read()),
                        'res_model': 'helpdesk.ticket',
                        'res_id': ticket.id,
                    })

        # Ensure this template ID exists!
        return request.render('helpdesk_website.ticket_submitted_success', {'ticket': ticket})


