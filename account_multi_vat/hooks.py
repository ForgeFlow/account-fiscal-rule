# Copyright 2023 ForgeFlow, S.L.
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).
import logging

try:
    from openupgradelib import openupgrade
except Exception:
    from odoo.tools import sql as openupgrade

_logger = logging.getLogger(__name__)


def pre_init_hook(cr):
    _logger.info("Pre-creating column customer_vat for table account_move")
    if not openupgrade.column_exists(cr, "account_move", "customer_vat"):
        cr.execute(
            """
            ALTER TABLE account_move
            ADD COLUMN customer_vat text;
            COMMENT ON COLUMN account_move.customer_vat
            IS 'Customer VAT';
            """
        )
        openupgrade.logged_query(
            cr,
            """
        UPDATE account_move am
        SET customer_vat = rp.vat
        FROM res_partner rp
        WHERE am.partner_id = rp.id and am.partner_id is not null""",
        )
