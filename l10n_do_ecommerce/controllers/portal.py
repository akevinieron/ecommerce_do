# @ 2020 Kevin Jiménez <kevin@katanalabs.do>

from odoo import _
from odoo.http import request, route
from odoo.addons.portal.controllers.portal import CustomerPortal


class Portal(CustomerPortal):

    CustomerPortal.OPTIONAL_BILLING_FIELDS.append('tax_payer_type')

    @route(['/my/account'], type='http', auth='user', website=True)
    def account(self, redirect=None, **post):
        res = super(Portal, self).account(redirect, **post)

        sale_fiscal_types = request.env['account.invoice']._fields.get('sale_fiscal_type').selection
        res.qcontext['fiscal_types'] = {name: label for name, label in sale_fiscal_types}

        return res

    def details_form_validate(self, data):
        error = dict()
        error_message = []

        if data.get("tax_payer_type") in ["fiscal", "gov"]:
            if not data.get("vat", None):
                error["vat"] = 'error'
                error_message.append(_('For fiscal tax, RNC field cannot be empty.'))

            if not data.get("company_name", None):
                error["company_name"] = 'error'
                error_message.append(_('For fiscal tax, Company Name field cannot be empty.'))

            if error:
                return error, error_message

        return super(Portal, self).details_form_validate(data)
