# -*- coding: utf-8 -*-
import logging
import pprint
import werkzeug

from odoo import http
from odoo.http import request
from odoo.addons.payment.controllers.portal import PaymentProcessing

_logger = logging.getLogger(__name__)


class StripeController(http.Controller):



    @http.route(['/payment/stripe/create_charge'], type='json', auth='public')
    def stripe_create_charge(self, **post):
        """ Create a payment transaction

        Expects the result from the user input from checkout.js popup"""
        TX = request.env['payment.transaction']
        tx = None
        if post.get('tx_ref'):
            tx = TX.sudo().search([('reference', '=', post['tx_ref'])])
        if not tx:
            tx_id = (post.get('tx_id') or request.session.get('sale_transaction_id') or
                     request.session.get('website_payment_tx_id'))
            tx = TX.sudo().browse(int(tx_id))
        if not tx:
            raise werkzeug.exceptions.NotFound()

        stripe_token = post['token']
        response = None
        if tx.type == 'form_save' and tx.partner_id:
            payment_token_id = request.env['payment.token'].sudo().create({
                'acquirer_id': tx.acquirer_id.id,
                'partner_id': tx.partner_id.id,
                'stripe_token': stripe_token
            })
            tx.payment_token_id = payment_token_id
            response = tx._create_stripe_charge(acquirer_ref=payment_token_id.acquirer_ref, email=stripe_token['email'])
        else:
            response = tx._create_stripe_charge(tokenid=stripe_token['id'], email=stripe_token['email'])
        _logger.info('Stripe: entering form_feedback with post data %s', pprint.pformat(response))
        if response:
            request.env['payment.transaction'].sudo().with_context(lang=None).form_feedback(response, 'stripe')
        # add the payment transaction into the session to let the page /payment/process to handle it
        PaymentProcessing.add_payment_transaction(tx)
        return "/payment/process"
