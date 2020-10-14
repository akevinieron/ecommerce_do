# @ 2020 Kevin Jiménez <kevin@katanalabs.do>

from odoo import http, _
from odoo.http import request
from odoo.addons.website_sale.controllers.main import WebsiteSale


class WebsiteSaleL10nDO(WebsiteSale):

    def checkout_form_validate(self, mode, all_form_values, data):
        error = dict()
        error_message = []

        if mode[1] == "billing" and data.get("tax_payer_type") in ["fiscal", "gov"]:
            vat_value = data.get("vat", None)

            if not vat_value:
                error["vat"] = 'error'
                error_message.append(_('For fiscal tax, RNC field cannot be empty.'))

            if not vat_value.isdigit() or len(vat_value) not in [9, 11]:
                error["vat"] = 'error'
                error_message.append(_('RNC looks invalid. Please check to continue.'))

            if not data.get("company_name", None):
                error["company_name"] = 'error'
                error_message.append(_('For fiscal tax, Company Name field cannot be empty.'))

            if error:
                return error, error_message

        return super(WebsiteSaleL10nDO, self).checkout_form_validate(mode, all_form_values, data)

    @http.route(['/shop/address'], type='http', methods=['GET', 'POST'], auth="public", website=True, sitemap=False)
    def address(self, **kw):
        res = super(WebsiteSaleL10nDO, self).address(**kw)

        sale_fiscal_types = request.env['account.invoice']._fields.get('sale_fiscal_type').selection
        res.qcontext['fiscal_types'] = {name: label for name, label in sale_fiscal_types}

        return res
