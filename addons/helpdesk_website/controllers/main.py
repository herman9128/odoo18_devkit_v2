import base64
from odoo import http
from odoo.http import request


class WebsiteHelpdeskController(http.Controller):

    @http.route('/contact-support', type='http', auth='public', website=True)
    def contact_support_page(self, **kwargs):
        """Renders the frontend support ticket form page."""
        return request.render('helpdesk_website.contact_support_page_template', {})

    @http.route('/contact-support/submit', type='http', auth='public', methods=['POST'], website=True, csrf=True)
    def submit_support_ticket(self, **post):
        """Handles ticket creation, customer matching, and chatter attachments."""
        email = post.get('partner_email', '').strip()
        name = post.get('name', '').strip()
        description = post.get('description', '').strip()
        mobile = post.get('mobile_phone', '').strip()

        if not name or not email:
            return request.redirect('/contact-support?error=missing_fields')

        # 1. Match existing partner by email or logged-in portal user
        partner = request.env.user.partner_id if not request.env.user._is_public() else False
        if not partner and email:
            partner = request.env['res.partner'].sudo().search([('email', '=ilike', email)], limit=1)

        # Append phone number to description if provided
        if mobile:
            description = f"Contact Phone: {mobile}\n\n{description}"

        # 2. Construct ticket values matching OCA helpdesk.ticket schema
        ticket_val = {
            'name': name,
            'partner_email': email,
            'description': description,
        }
        if partner:
            ticket_val['partner_id'] = partner.id

        # 3. Create ticket as superuser
        ticket = request.env['helpdesk.ticket'].sudo().create(ticket_val)

        # 4. Process file attachment and post to Chatter
        file_input = post.get('attachment')
        if file_input and hasattr(file_input, 'filename') and file_input.filename:
            file_content = file_input.read()
            if file_content:
                attachment = request.env['ir.attachment'].sudo().create({
                    'name': file_input.filename,
                    'datas': base64.b64encode(file_content),
                    'res_model': 'helpdesk.ticket',
                    'res_id': ticket.id,
                    'type': 'binary',
                })
                ticket.message_post(
                    body="Attachment uploaded via website form.",
                    attachment_ids=[attachment.id]
                )

        return request.redirect('/contactus-thank-you')