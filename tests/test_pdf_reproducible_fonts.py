import datetime
import io
import os
from pathlib import Path
import unittest
from unittest.mock import patch

from fontTools.ttLib import TTFont
from fontTools.misc.timeTools import epoch_diff
from tools.build_pdf import configure_reproducible_fonts, manual_cover_date


class ReproducibleFontTests(unittest.TestCase):
    def test_cover_date_uses_reviewed_config_instead_of_the_build_clock(self):
        with patch("tools.build_pdf.datetime.date", wraps=datetime.date) as date:
            date.today.side_effect = AssertionError("The build clock is not a publication input")
            self.assertEqual("2026-11-05", manual_cover_date({
                "manual_version_date": "2026-08-18", "manual_build_date": "2026-11-05"}))
            self.assertEqual("2026-08-18", manual_cover_date({"manual_version_date": "2026-08-18"}))
            with self.assertRaises(ValueError):
                manual_cover_date({"manual_version_date": "2026-08-18", "manual_build_date": "invalid"})
            date.today.assert_not_called()

    def test_release_date_sets_a_timezone_independent_epoch(self):
        expected = str(int(datetime.datetime(2026, 8, 18, tzinfo=datetime.timezone.utc).timestamp()))
        with patch.dict(os.environ, {}, clear=True):
            self.assertEqual(expected, configure_reproducible_fonts("2026-08-18"))
            self.assertEqual(expected, os.environ["SOURCE_DATE_EPOCH"])

    def test_explicit_reproducible_build_epoch_is_preserved(self):
        with patch.dict(os.environ, {"SOURCE_DATE_EPOCH": "1234567890"}, clear=True):
            self.assertEqual("1234567890", configure_reproducible_fonts("2026-08-18"))

    def test_invalid_manual_release_date_fails_before_font_serialization(self):
        with patch.dict(os.environ, {}, clear=True):
            with self.assertRaises(ValueError):
                configure_reproducible_fonts("not-a-date")
            self.assertNotIn("SOURCE_DATE_EPOCH", os.environ)

    def test_actual_font_bytes_match_across_different_build_clocks(self):
        source = Path(__file__).resolve().parents[1] / "docs/assets/fonts/inter-regular.ttf"
        outputs = []
        with patch.dict(os.environ, {}, clear=True):
            epoch = int(configure_reproducible_fonts("2026-08-18"))
            for clock in [1793664000, 1793750400]:
                with patch("time.time", return_value=clock):
                    font = TTFont(source, recalcTimestamp=True)
                    buffer = io.BytesIO()
                    font.save(buffer)
                    outputs.append(buffer.getvalue())
                    font.close()
            self.assertEqual(outputs[0], outputs[1])
            with TTFont(io.BytesIO(outputs[0])) as font:
                self.assertEqual(epoch - epoch_diff, font["head"].modified)


if __name__ == "__main__":
    unittest.main()
