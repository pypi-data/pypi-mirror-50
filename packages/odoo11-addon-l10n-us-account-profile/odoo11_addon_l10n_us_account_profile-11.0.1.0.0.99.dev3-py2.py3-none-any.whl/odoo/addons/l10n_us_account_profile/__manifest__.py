# Copyright (C) 2019 Open Source Integrators
# <https://www.opensourceintegrators.com>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
{
    "name": "US Accounting",
    "summary": "Additional features to manage US accounting in Odoo",
    "version": "11.0.1.0.0",
    "category": "Accounting",
    "website": "https://github.com/OCA/l10n-usa",
    "author": "Open Source Integrators, Odoo Community Association (OCA)",
    "license": "AGPL-3",
    "depends": [
        "account_banking_reconciliation",
        "account_due_list",
        "account_payment_batch_process",
        "account_payment_credit_card",
        "account_reversal",
        "l10n_us",
        "l10n_us_check_writing_address",
        "l10n_us_form_1099",
        "partner_aging",
        "partner_time_to_pay",
    ],
    "application": True,
    "installable": True,
}
