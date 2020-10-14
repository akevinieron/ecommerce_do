/*
# @ 2020 Kevin Jiménez <kevin@katanalabs.do>
*/

odoo.define('l10n_do_ecommerce.rnc_autocomplete', function (require) {
    'use strict';

    require('web.dom_ready');

    var $tax_payer_type = $("#tax_payer_type");
    if (!$tax_payer_type.length) {
        return;
    }

    var self = this,
        $rnc_input = $(".div_vat").find("input"),
        $company_name = $("input[name='company_name']"),
        $tax_type = $("#tax_payer_type");

    $rnc_input.on('keyup', function (ev) {
        var rnc = $rnc_input.val();
        
        if (rnc.length !== 9 && rnc.length !== 11) {
            return;
        }

        $.ajax({
            url: "/dgii_ws?term=" + rnc,
            dataType: 'json',
            success: function (data) {
                if(data.length > 0) {
                    fillTaxInputs(data[0]);
                }
            },
        });
    });

    function fillTaxInputs(data) {
        $company_name.val(data.name);
        $tax_type.val("fiscal");
    }

});