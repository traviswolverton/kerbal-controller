"""Offline tests for the parts tools with fake API data (no credentials or network needed)."""
import io
import os
import unittest
from contextlib import redirect_stdout
from unittest import mock

import digikey
import mouser
import parts
from common import PartsError, is_active

DK = {
    "ManufacturerProductNumber": "ABC-123", "Manufacturer": {"Name": "Acme"},
    "Description": {"ProductDescription": "SWITCH KEYLOCK SPST 2A"}, "UnitPrice": 4.5, "QuantityAvailable": 120,
    "ProductStatus": {"Status": "Active"}, "ProductUrl": "https://www.digikey.com/x", "DatasheetUrl": "https://e.com/a.pdf",
    "Parameters": [{"ParameterText": "Circuit", "ValueText": "SPST"}],
    "ProductVariations": [{"DigiKeyProductNumber": "100-ABC-ND", "PackageType": {"Name": "Bulk"}, "MinimumOrderQuantity": 1,
                           "StandardPricing": [{"BreakQuantity": 1, "UnitPrice": 4.5}, {"BreakQuantity": 10, "UnitPrice": 4.0},
                                               {"BreakQuantity": 100, "UnitPrice": 3.2}]}],
}
MS = {   # shape taken from a live Mouser response
    "MouserPartNumber": "612-KO131A102", "ManufacturerPartNumber": "KO131A102", "Manufacturer": "E-Switch",
    "Description": "Keylock Switches", "Availability": "927 In Stock", "AvailabilityInStock": "927", "LifecycleStatus": None,
    "Min": "1", "ProductDetailUrl": "https://www.mouser.com/y", "DataSheetUrl": "",
    "PriceBreaks": [{"Quantity": 1, "Price": "$4.04", "Currency": "USD"}, {"Quantity": 10, "Price": "$3.50", "Currency": "USD"},
                    {"Quantity": 1000, "Price": "$1,234.50", "Currency": "USD"}],
    "ProductAttributes": [{"AttributeName": "Packaging", "AttributeValue": "Bulk"}],
}


class DigiKeyReading(unittest.TestCase):
    def test_row(self):
        r = digikey.row(DK)
        self.assertEqual((r["source"], r["pn"], r["mpn"], r["stock"], r["status"]), ("digikey", "100-ABC-ND", "ABC-123", 120, "Active"))

    def test_price_breaks(self):
        self.assertEqual([digikey.price_at(DK, q) for q in (1, 12, 500)], [4.5, 4.0, 3.2])

    def test_missing_fields(self):
        r = digikey.row({"ManufacturerProductNumber": "X"})
        self.assertEqual((r["pn"], r["unit_price"], r["status"]), ("", None, ""))

    def test_sandbox_switch(self):
        with mock.patch.dict(os.environ, {"DIGIKEY_SANDBOX": "true"}):
            self.assertIn("sandbox", digikey.base_url())
        with mock.patch.dict(os.environ, {"DIGIKEY_SANDBOX": ""}):
            self.assertEqual(digikey.base_url(), "https://api.digikey.com")


class MouserReading(unittest.TestCase):
    def test_row(self):
        r = mouser.row(MS)
        self.assertEqual((r["source"], r["pn"], r["stock"], r["unit_price"], r["status"]), ("mouser", "612-KO131A102", 927, 4.04, "Active"))
        self.assertEqual(r["params"], {"Packaging": "Bulk"})

    def test_price_strings_and_breaks(self):
        self.assertEqual(mouser.price_at(MS, 10), 3.5)
        self.assertEqual(mouser.price_at(MS, 5000), 1234.5)      # "$1,234.50"
        self.assertEqual(mouser._num("$0.10"), 0.10)

    def test_stock_falls_back_to_availability_text(self):
        self.assertEqual(mouser.stock_of({"Availability": "52 In Stock"}), 52)
        self.assertEqual(mouser.stock_of({}), 0)

    def test_lifecycle_status_passes_through(self):
        self.assertEqual(mouser.row(dict(MS, LifecycleStatus="End of Life"))["status"], "End of Life")

    def test_error_in_body_raises(self):
        class R:
            def __enter__(s): return s
            def __exit__(s, *a): pass
            def read(s): return b'{"Errors":[{"Message":"Invalid unique identifier."}],"SearchResults":null}'
        with mock.patch.dict(os.environ, {"MOUSER_API_KEY": "k"}), mock.patch("urllib.request.urlopen", return_value=R()), \
                mock.patch("time.sleep"), mock.patch("json.load", return_value={"Errors": [{"Message": "Invalid unique identifier."}]}):
            with self.assertRaises(PartsError) as cm:
                mouser.api("/search/keyword", {})
        self.assertIn("Invalid unique identifier", str(cm.exception))


class Tool(unittest.TestCase):
    def test_active_rule(self):
        self.assertTrue(all(is_active(s) for s in ("Active", "", None, "New Product")))
        self.assertFalse(any(is_active(s) for s in ("Obsolete", "End of Life", "Discontinued at Digi-Key")))

    def test_guess_source(self):
        self.assertEqual(parts.guess_source("100-ABC-ND", "auto"), "digikey")
        self.assertEqual(parts.guess_source("612-KO131A102", "auto"), "mouser")
        self.assertEqual(parts.guess_source("612-KO131A102", "digikey"), "digikey")

    def test_no_credentials_message(self):
        with mock.patch.dict(os.environ, {}, clear=True):
            with self.assertRaises(PartsError) as cm:
                parts.active_sources("auto")
        self.assertIn("MOUSER_API_KEY", str(cm.exception))

    def test_search_filters_and_merges_sources(self):
        rows = {"digikey": [digikey.row(DK)], "mouser": [mouser.row(MS), mouser.row(dict(MS, MouserPartNumber="OLD", LifecycleStatus="Obsolete")),
                                                           mouser.row(dict(MS, MouserPartNumber="OUT", AvailabilityInStock="0", Availability="0 In Stock"))]}
        args = mock.Mock(keywords="k", limit=10, in_stock=True, active=True, max_price=None, json=True, source="auto")
        buf = io.StringIO()
        with mock.patch.object(parts, "active_sources", return_value=["digikey", "mouser"]), \
                mock.patch.object(parts, "search_rows", side_effect=lambda s, *a: rows[s]), redirect_stdout(buf):
            parts.cmd_search(args)
        out = buf.getvalue()
        self.assertIn("100-ABC-ND", out)
        self.assertIn("612-KO131A102", out)
        self.assertNotIn('"OLD"', out)
        self.assertNotIn('"OUT"', out)

    def test_one_source_failing_does_not_hide_the_other(self):
        def fake(src, *a):
            if src == "digikey":
                raise PartsError("HTTP 503")
            return [mouser.row(MS)]
        args = mock.Mock(keywords="k", limit=10, in_stock=False, active=False, max_price=None, json=True, source="auto")
        out, err = io.StringIO(), io.StringIO()
        with mock.patch.object(parts, "active_sources", return_value=["digikey", "mouser"]), \
                mock.patch.object(parts, "search_rows", side_effect=fake), redirect_stdout(out), mock.patch("sys.stderr", err):
            parts.cmd_search(args)
        self.assertIn("612-KO131A102", out.getvalue())
        self.assertIn("HTTP 503", err.getvalue())

    def test_check_flags(self):
        shortlist = [{"role": "key", "source": "mouser", "pn": "612-KO131A102", "qty": 2000, "unit_price": 5.0}]
        rows, total = parts.check_rows(shortlist, fetch=lambda s, pn, q: mouser.row(dict(MS, LifecycleStatus="Obsolete"), pn, q))
        flags = rows[0][-1]
        self.assertIn("status Obsolete", flags)
        self.assertIn("low stock", flags)
        self.assertIn("price was $5.00", flags)
        self.assertAlmostEqual(total, 1234.5 * 2000)

    def test_check_survives_an_error(self):
        def boom(*a):
            raise PartsError("HTTP 404")
        rows, _ = parts.check_rows([{"role": "x", "source": "digikey", "pn": "y", "qty": 1}], fetch=boom)
        self.assertTrue(rows[0][-1].startswith("ERROR"))


if __name__ == "__main__":
    unittest.main()
