from __future__ import annotations

import unittest

from aidb.domain import ArxivRef, try_parse_arxiv_ref


class ArxivRefTest(unittest.TestCase):
    def test_parses_modern_id_with_and_without_version(self) -> None:
        current = ArxivRef.parse("2608.16889v12")
        older = ArxivRef.parse("0704.0001")

        self.assertEqual(current, ArxivRef(base_id="2608.16889", version=12))
        self.assertEqual(current.version_id, "2608.16889v12")
        self.assertEqual(current.version_tag, "v12")
        self.assertEqual(current.path_key, "2608.16889")
        self.assertEqual(older.version_id, "0704.0001")
        self.assertIsNone(older.version_tag)

    def test_parses_case_insensitive_arxiv_prefix_and_outer_whitespace(self) -> None:
        self.assertEqual(
            ArxivRef.parse("  ArXiV:  hep-th/9901001v2  "),
            ArxivRef(base_id="hep-th/9901001", version=2),
        )

    def test_parses_supported_arxiv_urls(self) -> None:
        expected = ArxivRef(base_id="2608.16889", version=1)
        urls = [
            "https://arxiv.org/abs/2608.16889v1",
            "https://www.arxiv.org/pdf/2608.16889v1.pdf",
            "http://export.arxiv.org/html/2608.16889v1?download=1#paper",
            "https://arxiv.org/src/2608.16889v1",
        ]

        for url in urls:
            with self.subTest(url=url):
                self.assertEqual(ArxivRef.parse(url), expected)

    def test_parses_legacy_url_and_creates_filesystem_safe_key(self) -> None:
        ref = ArxivRef.parse("https://arxiv.org/pdf/hep-th/9901001v2.pdf?x=1")

        self.assertEqual(ref.base_id, "hep-th/9901001")
        self.assertEqual(ref.version, 2)
        self.assertEqual(ref.path_key, "hep-th--9901001")
        self.assertEqual(
            ref.canonical_abs_url,
            "https://arxiv.org/abs/hep-th/9901001v2",
        )

    def test_normalizes_legacy_archive_case(self) -> None:
        self.assertEqual(
            ArxivRef.parse("HEP-TH/9901001"),
            ArxivRef(base_id="hep-th/9901001"),
        )

    def test_query_and_fragment_are_not_part_of_url_identity(self) -> None:
        ref = ArxivRef.parse(
            "https://arxiv.org/abs/2608.16889v3?context=cs#references"
        )
        self.assertEqual(ref.version_id, "2608.16889v3")

    def test_rejects_invalid_or_unsafe_references(self) -> None:
        invalid = [
            "",
            "not-an-id",
            "2600.16889",
            "2613.16889",
            "2608.123",
            "2608.123456",
            "2608.16889v0",
            "2608.16889v01",
            "hep-th/9913001",
            "hep-th/9901001v0",
            "https://example.com/abs/2608.16889",
            "https://arxiv.org.evil/abs/2608.16889",
            "https://user@arxiv.org/abs/2608.16889",
            "https://arxiv.org:443/abs/2608.16889",
            "ftp://arxiv.org/abs/2608.16889",
            "https://arxiv.org/list/cs.AI/recent",
            "https://arxiv.org/abs/2608.16889/extra",
            "https://arxiv.org/pdf/2608.16889.pdf/extra",
        ]

        for value in invalid:
            with self.subTest(value=value):
                with self.assertRaisesRegex(ValueError, "arXiv|month|version"):
                    ArxivRef.parse(value)

    def test_constructor_enforces_canonical_base_and_version(self) -> None:
        invalid_arguments = [
            ("HEP-TH/9901001", None),
            ("hep-th/9901001v2", None),
            ("2608.16889", 0),
            ("2608.16889", -1),
            ("2608.16889", True),
        ]

        for base_id, version in invalid_arguments:
            with self.subTest(base_id=base_id, version=version):
                with self.assertRaises(ValueError):
                    ArxivRef(base_id=base_id, version=version)

    def test_try_parse_returns_none_instead_of_raising(self) -> None:
        self.assertEqual(
            try_parse_arxiv_ref("arXiv:2608.16889v1"),
            ArxivRef(base_id="2608.16889", version=1),
        )
        self.assertIsNone(try_parse_arxiv_ref("https://example.com/paper"))
        self.assertIsNone(try_parse_arxiv_ref(None))  # type: ignore[arg-type]


if __name__ == "__main__":
    unittest.main()
