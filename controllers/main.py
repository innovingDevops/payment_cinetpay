# -*- coding: utf-8 -*-
import logging
import pprint
import werkzeug

from odoo import http
from odoo.http import request
from odoo.addons.payment.controllers.portal import PaymentProcessing

_logger = logging.getLogger(__name__)


class CinetpayController(http.Controller):

    @http.route(['/cinetpay/payment/process'], type='http', auth='public')
    def cinetpay_payment_process(self, **post):
        PaymentProcessing.add_payment_transaction()
        return werkzeug.utils.redirect('/payment/process')

