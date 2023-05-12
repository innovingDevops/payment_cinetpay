# -*- coding: utf-8 -*-
import logging
import pprint
import werkzeug
import datetime

from odoo import http
from odoo.http import request
from odoo.addons.payment.controllers.portal import PaymentProcessing
from odoo import api, fields, models, _
from datetime import date, datetime, timedelta
import time
_logger = logging.getLogger(__name__)


class CinetpayController(http.Controller):

    @http.route(['/cinetpay/payment/process'], type='http', auth='public')
    def cinetpay_payment_process(self, **post):

        #ligne payement transaction
        transaction = request.env['payment.transaction'].sudo().search([('reference', '=', post['invoice_num'])])
        #recuperation de le reference
        invoice_num = post['invoice_num'].split("-")[0]
        sale_order = request.env['sale.order'].sudo().search([('name', '=', invoice_num)])

        # confirm le bon de commande
        if sale_order.state == "draft":
            if float(sale_order.amount_total) == float(post['amount']):
                sale_order.sudo().action_confirm()

                #création de la facture
                if sale_order.state == "sale":
                    account_invoice = sale_order.sudo().action_invoice_create()
                    invoice = request.env['account.invoice'].sudo().browse(account_invoice[0])
                    invoice.action_invoice_open()

                    payment = request.env['account.payment'].sudo().create({
                        'payment_type': 'inbound',  # Type de paiement entrant
                        'partner_type': 'customer',  # Type de partenaire (client)
                        'partner_id': invoice.partner_id.id,  # Identifiant du partenaire (client)
                        'amount': invoice.residual,  # Montant du paiement (solde de la facture)
                        'currency_id': invoice.currency_id.id,  # Identifiant de la devise de la facture
                        'payment_date': invoice.date,  # Date du paiement (aujourd'hui)
                        'payment_method_id' : 3,
                        'journal_id' :transaction.acquirer_id.journal_id.id,
                        'communication': invoice.number,  # Référence du paiement (numéro de facture)
                        'invoice_ids': [(4, invoice.id)],  # Liste des identifiants de facture associés au paiement
                    })


                    payment.action_validate_invoice_payment()
                    transaction.payment_id = payment.id
                    transaction.state = "done"
                    transaction.acquirer_reference = post['transaction_id']

                return werkzeug.utils.redirect('/shop/confirmation')
            else:
                return "Montant incorect"
        else:
            return "Aucun bon de commande"

