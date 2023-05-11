odoo.define('payment_cinetpay.cinetpay', function(require) {
    "use strict";

    var ajax = require('web.ajax');
    var core = require('web.core');
    var _t = core._t;
    var qweb = core.qweb;
    ajax.loadXML('/payment_cinetpay/static/src/xml/cinetpay_templates.xml', qweb);



    // The following currencies are integer only, see
    // https://cinetpay.com/docs/currencies#zero-decimal
    var int_currencies = [
        'BIF', 'XAF', 'XPF', 'CLP', 'KMF', 'DJF', 'GNF', 'JPY', 'MGA', 'PYG',
        'RWF', 'KRW', 'VUV', 'VND', 'XOF'
    ];




    require('web.dom_ready');
    if (!$('.o_payment_form').length) {
        return $.Deferred().reject("DOM doesn't contain '.o_payment_form'");
    }


    function display_cinetpay_form(provider_form) {
        // Open Checkout with further options
        var payment_form = $('.o_payment_form');
        if(!payment_form.find('i').length)
            payment_form.append('<i class="fa fa-spinner fa-spin"/>');
            payment_form.attr('disabled','disabled');

        var payment_tx_url = payment_form.find('input[name="prepare_tx_url"]').val();
        var access_token = $("input[name='access_token']").val() || $("input[name='token']").val() || '';

        var get_input_value = function(name) {
            return provider_form.find('input[name="' + name + '"]').val();
        }

        var acquirer_id = parseInt(provider_form.find('#acquirer_cinetpay').val());
        var amount = parseFloat(get_input_value("amount") || '0.0');
        var currency = get_input_value("currency");
        var email = get_input_value("email");
        var invoice_num = get_input_value("invoice_num");
        var merchant = get_input_value("merchant");

        // Search if the user wants to save the credit card information
        var form_save_token = false;
        var acquirer_form = $('#o_payment_form_acq_' + acquirer_id);
        if (acquirer_form.length) {
            form_save_token = acquirer_form.find('input[name="o_payment_form_save_token"]').prop('checked');
        }


    }

    display_cinetpay_form($('form[provider="cinetpay"]'));
});
