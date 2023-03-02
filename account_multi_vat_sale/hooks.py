# Copyright 2023 ForgeFlow, S.L.
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).
import logging

try:
    from openupgradelib import openupgrade
except Exception:
    from odoo.tools import sql as openupgrade

_logger = logging.getLogger(__name__)


def pre_init_hook(cr):
    _logger.info("Pre-creating column customer_vat_partner_id for table account_move")
    if not openupgrade.column_exists(cr, "account_move", "customer_vat_partner_id"):
        cr.execute(
            """
            ALTER TABLE account_move
            ADD COLUMN customer_vat_partner_id int;
            COMMENT ON COLUMN account_move.customer_vat_partner_id
            IS 'Customer tax administration';
            """
        )
    _logger.info("Pre-creating column customer_vat for table sale_order")
    if not openupgrade.column_exists(cr, "sale_order", "customer_vat"):
        cr.execute(
            """
            ALTER TABLE sale_order
            ADD COLUMN customer_vat text;
            COMMENT ON COLUMN sale_order.customer_vat
            IS 'Customer VAT';
            """
        )
        openupgrade.logged_query(
            cr,
            """
        UPDATE sale_order so
        SET customer_vat = rp.vat
        FROM res_partner rp
        WHERE so.partner_id = rp.id and so.partner_id is not null""",
        )
    if not openupgrade.column_exists(cr, "sale_order", "customer_vat_partner_id"):
        cr.execute(
            """
            ALTER TABLE sale_order
            ADD COLUMN customer_vat_partner_id int;
            COMMENT ON COLUMN sale_order.customer_vat_partner_id
            IS 'Customer tax administration';
            """
        )
