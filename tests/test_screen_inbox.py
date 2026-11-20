import unittest

from scripts.screen_inbox import normalize_quotes, valid_records, validate_records


class ScreeningTest(unittest.TestCase):
    def setUp(self):
        self.inputs = [
            {"id": "paper:a", "title": "Paper A", "abstract": "We compare memory with raw history."},
            {"id": "paper:b", "title": "A release with no description", "abstract": ""},
        ]
        self.records = [
            {"id": "paper:a", "priority": "read", "topic": "memory", "assessment": "Авторы сравнивают память с исходной историей.", "evidence": "compare memory with raw history"},
            {"id": "paper:b", "priority": "reference", "topic": "runtime", "assessment": "Нет описания; по заголовку нельзя оценить результат.", "evidence": "A release with no description"},
        ]

    def test_exact_coverage_and_title_fallback(self):
        validate_records(self.records, self.inputs)
        for records in [self.records[:1], self.records[::-1], [self.records[0]] * 2]:
            with self.assertRaises(ValueError):
                validate_records(records, self.inputs)

    def test_quote_must_belong_to_its_own_source(self):
        self.records[0]["evidence"] = self.records[1]["evidence"]
        with self.assertRaises(ValueError):
            validate_records(self.records, self.inputs)

    def test_only_exact_wrapped_quote_is_normalized(self):
        self.records[0]["evidence"] = "“compare memory with raw history”"
        normalize_quotes(self.records, self.inputs)
        validate_records(self.records, self.inputs)
        self.records[0]["evidence"] = "“compare memory with rewritten history”"
        normalize_quotes(self.records, self.inputs)
        with self.assertRaises(ValueError):
            validate_records(self.records, self.inputs)

    def test_one_bad_quote_does_not_discard_other_analyses(self):
        self.records[1]["evidence"] = "invented source text"
        self.assertEqual(set(valid_records(self.records, self.inputs)), {"paper:a"})
        self.assertEqual(valid_records([self.records[0], self.records[0], None], self.inputs), {})


if __name__ == "__main__":
    unittest.main()
