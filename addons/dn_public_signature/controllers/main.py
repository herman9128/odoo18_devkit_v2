import base64
from odoo import http, fields
from odoo.http import request

class DeliveryNoteController(http.Controller):

    @http.route('/dn/confirm/<string:token>', type='http', auth='public', website=True)
    def dn_public_view(self, token, **kwargs):
        picking = request.env['stock.picking'].sudo().search([('access_token', '=', token)], limit=1)
        if not picking:
            return request.render('website.404')

        return request.render('dn_public_signature.dn_confirmation_page', {
            'picking': picking,
        })

    @http.route('/dn/confirm/<string:token>/submit', type='http', auth='public', methods=['POST'], website=True, csrf=True)
    def dn_public_submit(self, token, **post):
        picking = request.env['stock.picking'].sudo().search([('access_token', '=', token)], limit=1)
        if not picking:
            return request.render('website.404')

        signer_name = post.get('signer_name')
        signature_data = post.get('signature_data')

        if signature_data and signer_name:
            if ',' in signature_data:
                signature_data = signature_data.split(',')[1]

            # Write signature and update signature_state to 'signed' automatically
            picking.write({
                'signature': signature_data,
                'signed_by': signer_name,
                'signed_on': fields.Datetime.now(),
                'signature_state': 'signed',  # <--- Updates status automatically
            })

            picking.message_post(
                body=f"Delivery Note electronically confirmed & signed by <b>{signer_name}</b>.",
                attachment_ids=[]
            )

        return request.render('dn_public_signature.dn_thank_you_page', {'picking': picking})