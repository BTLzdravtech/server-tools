# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo.tests.common import TransactionCase

from ..models.auditlog_rule import ThrowAwayCache


class TestThrowAwayCache(TransactionCase):
    def test_pending_write_survives_flush_inside_throwaway_cache(self):
        partner = self.env["res.partner"].create({"name": "Before"})
        self.env.flush_all()
        partner.name = "After"

        with ThrowAwayCache(self.env):
            self.env["res.partner"].flush_model(["name"])
            self.assertEqual(partner.name, "Before")

        self.assertEqual(partner.name, "After")
        self.env.flush_all()
        self.env.cr.execute("SELECT name FROM res_partner WHERE id = %s", [partner.id])
        self.assertEqual(self.env.cr.fetchone()[0], "After")
