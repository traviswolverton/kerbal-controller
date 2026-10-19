"""Offline tests for dk.py with a fake API (no credentials or network needed)."""
import io
import os
import unittest
from contextlib import redirect_stdout
from unittest import mock

import dk

PRODUCT = {
    "ManufacturerProductNumber": "ABC-123",
    "Manufacturer": {"Name": "Acme"},
    "Description": {"ProductDescription": "SWITCH KEYLOCK SPST 2A"},
    "UnitPrice": 4.5,
    "QuantityAvailable": 120,
    "ProductStatus": {"Status": "Active"},
    "ProductUrl": "https://www.digikey.com/en/products/detail/acme/abc-123/1",
    "DatasheetUrl": "https://example.com/abc.pdf",
    "Parameters": [{"ParameterText": "Circuit", "ValueText": "SPST"}],
    "ProductVariations": [{
        "DigiKeyProductNumber": "100-ABC-ND", "PackageType": {"Name": "Bulk"},
        "StandardPricing": [{"BreakQuantity": 1, "UnitPrice": 4.5}, {"BreakQuantity": 10, "UnitPrice": 4.0},
                            {"BreakQuantity": 100, "UnitPrice": 3.2}]}],
}


class Reading(unittest.TestCase):
    def test_row_fields(self):
        r = dk.row(PRODUCT)
        self.assertEqual((r["dkpn"], r["mpn"], r["manufacturer"], r["stock"], r["status"]),
                         ("100-ABC-ND", "ABC-123", "Acme", 120, "Active"))
        self.assertEqual(r["params"], {"Circuit": "SPST"})

    def test_price_breaks(self):
        self.assertEqual(dk.price_at(PRODUCT, 1), 4.5)
        self.assertEqual(dk.price_at(PRODUCT, 12), 4.0)
        self.assertEqual(dk.price_at(PRODUCT, 500), 3.2)

    def test_missing_fields_do_not_crash(self):
        r = dk.row({"ManufacturerProductNumber": "X"})
        self.assertEqual((r["dkpn"], r["unit_price"], r["status"]), ("", None, ""))


class Commands(unittest.TestCase):
    def test_search_filters(self):
        cheap_out = dict(PRODUCT, ManufacturerProductNumber="OUT", QuantityAvailable=0)
        disc = dict(PRODUCT, ManufacturerProductNumber="OLD", ProductStatus={"Status": "Obsolete"})
        args = mock.Mock(keywords="k", limit=10, in_stock=True, active=True, max_price=None, json=True)
        with mock.patch.object(dk, "search", return_value=[PRODUCT, cheap_out, disc]):
            buf = io.StringIO()
            with redirect_stdout(buf):
                dk.cmd_search(args)
        self.assertIn("ABC-123", buf.getvalue())
        self.assertNotIn('"OUT"', buf.getvalue())
        self.assertNotIn('"OLD"', buf.getvalue())

    def test_check_flags_price_stock_status(self):
        parts = [{"role": "key switch", "dkpn": "100-ABC-ND", "qty": 200, "unit_price": 5.0}]
        discontinued = dict(PRODUCT, ProductStatus={"Status": "Obsolete"})
        rows, total = dk.check_rows(parts, fetch=lambda _: discontinued)
        flags = rows[0][-1]
        self.assertIn("status Obsolete", flags)
        self.assertIn("low stock", flags)
        self.assertIn("price was $5.00", flags)
        self.assertAlmostEqual(total, 3.2 * 200)

    def test_check_survives_api_error(self):
        def boom(_):
            raise dk.DigiKeyError("HTTP 404")
        rows, _ = dk.check_rows([{"role": "x", "dkpn": "y", "qty": 1}], fetch=boom)
        self.assertEqual(rows[0][5], "ERROR")


class Auth(unittest.TestCase):
    def test_missing_credentials_message(self):
        with mock.patch.dict(os.environ, {}, clear=True):
            with self.assertRaises(dk.DigiKeyError) as cm:
                dk.credentials()
        self.assertIn("DIGIKEY_CLIENT_ID", str(cm.exception))

    def test_sandbox_switch(self):
        with mock.patch.dict(os.environ, {"DIGIKEY_SANDBOX": "true"}):
            self.assertIn("sandbox", dk.base_url())
        with mock.patch.dict(os.environ, {"DIGIKEY_SANDBOX": ""}):
            self.assertEqual(dk.base_url(), "https://api.digikey.com")


if __name__ == "__main__":
    unittest.main()
