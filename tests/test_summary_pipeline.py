import copy
import json
import os
import unittest
from pathlib import Path
from types import SimpleNamespace
from unittest import mock

from aidb.render import render_summary
from aidb.summarizers.base import analyze_document
from aidb.summarizers.codex_exec import CodexExecProvider
from aidb.summarizers.openai_responses import OpenAIResponsesProvider
from aidb.validation import SummaryValidationError, labels_for_language


ROOT = Path(__file__).resolve().parents[1]
SCHEMA = ROOT / "schemas" / "paper-summary-v1.json"

BLOCKS = [
    {
        "id": "b-method",
        "kind": "paragraph",
        "section_path": ["Method"],
        "text": "We train a compact retrieval model using paired paper and query examples.",
    },
    {
        "id": "b-results",
        "kind": "paragraph",
        "section_path": ["Results"],
        "text": "Accuracy improved from 71.2% to 78.4% on TestSet.",
    },
    {
        "id": "b-limit",
        "kind": "paragraph",
        "section_path": ["Limitations"],
        "text": "The evaluation covers English papers only and code is not released.",
    },
]


def valid_model_output():
    return {
        "language": {"code": "en", "name": "English"},
        "labels": labels_for_language("en", {}),
        "title": "Compact retrieval for scientific papers",
        "executive_summary": (
            "The paper trains a compact retrieval model and reports a clear "
            "TestSet accuracy gain, while evaluation scope and reproducibility remain limited."
        ),
        "problem": {
            "statement": "Improve retrieval of scientific papers.",
            "importance": "Better retrieval reduces literature-review effort.",
            "scope": "Paired paper-query training and one reported TestSet evaluation.",
        },
        "method": {
            "overview": "A compact retrieval model is trained on paired examples.",
            "key_components": ["Compact retriever", "Paired paper-query examples"],
            "assumptions": ["The supplied TestSet represents the target workload"],
        },
        "claims": [
            {
                "claim": "The model is trained from paired paper and query examples.",
                "evidence": [
                    {
                        "block_id": "b-method",
                        "quote": "using paired paper and query examples",
                    }
                ],
            }
        ],
        "results": [
            {
                "result": "Accuracy increased from 71.2% to 78.4%.",
                "context": "Reported on TestSet.",
                "evidence": [
                    {
                        "block_id": "b-results",
                        "quote": "Accuracy improved from 71.2% to 78.4% on TestSet.",
                    }
                ],
            }
        ],
        "evaluation": {
            "datasets": [
                {
                    "text": "TestSet",
                    "evidence": [
                        {
                            "block_id": "b-results",
                            "quote": "on TestSet",
                        }
                    ],
                }
            ],
            "baselines": [],
            "metrics": [
                {
                    "text": "Accuracy",
                    "evidence": [
                        {
                            "block_id": "b-results",
                            "quote": "Accuracy improved",
                        }
                    ],
                }
            ],
            "ablations": [],
            "negative_results": [],
        },
        "limitations": [
            {
                "limitation": "Evaluation includes English papers only.",
                "evidence": [
                    {
                        "block_id": "b-limit",
                        "quote": "The evaluation covers English papers only",
                    }
                ],
            }
        ],
        "reproducibility": {
            "status": "weak",
            "artifacts": [],
            "missing": ["Released code"],
            "assessment": "The paper says that code is not released.",
        },
        "aidb_assessment": {
            "novelty": "Potentially useful compact retrieval setup.",
            "usefulness": "Relevant to automated literature discovery.",
            "confidence": "medium",
            "recommended_action": "read",
            "rationale": "The reported gain merits review, but evidence is narrow.",
        },
        "uncertainties": [
            {
                "uncertainty": "Generalization beyond English papers is unknown.",
                "why_it_matters": "AIDB discovers papers across languages.",
                "evidence": [
                    {
                        "block_id": "b-limit",
                        "quote": "evaluation covers English papers only",
                    }
                ],
            }
        ],
        "open_questions": ["Does the method transfer beyond English papers?"],
        "proposed_experiments": [
            {
                "hypothesis": "The compact retriever improves AIDB paper recall.",
                "baseline": "Current keyword discovery",
                "primary_metric": "Recall@20 on a labeled query set",
                "stop_condition": "Stop if Recall@20 does not improve after one fixed evaluation run",
            }
        ],
    }


RU_BLOCKS = [
    {
        "id": "ru-method",
        "text": (
            "Мы обучаем компактную модель поиска на парах из научных статей и "
            "пользовательских запросов, сохраняя одинаковую процедуру обучения."
        ),
    },
    {
        "id": "ru-results",
        "text": "Точность на тестовой выборке выросла с 71,2% до 78,4%.",
    },
    {
        "id": "ru-limit",
        "text": (
            "Оценка проведена только на русскоязычных статьях, а исходный код "
            "и веса модели не опубликованы."
        ),
    },
]


def valid_russian_output():
    return {
        "language": {"code": "ru", "name": "Русский"},
        # The pipeline must replace even incorrect known-locale labels with its
        # deterministic Russian label set before validation and rendering.
        "labels": {"wrong": "English"},
        "title": "Компактный поиск научных статей",
        "executive_summary": (
            "Работа обучает компактную модель поиска и показывает рост точности "
            "на тестовой выборке, но не публикует код и веса модели."
        ),
        "problem": {
            "statement": "Улучшить поиск научных статей.",
            "importance": "Более точный поиск ускоряет обзор литературы.",
            "scope": "Обучение на парах и одна тестовая выборка.",
        },
        "method": {
            "overview": "Компактная модель обучается на парах статей и запросов.",
            "key_components": ["Компактная модель", "Парные примеры"],
            "assumptions": ["Тестовая выборка соответствует целевой задаче"],
        },
        "claims": [
            {
                "claim": "Для обучения используются пары статей и запросов.",
                "evidence": [
                    {
                        "block_id": "ru-method",
                        "quote": "на парах из научных статей и пользовательских запросов",
                    }
                ],
            }
        ],
        "results": [
            {
                "result": "Точность выросла с 71,2% до 78,4%.",
                "context": "Результат получен на тестовой выборке.",
                "evidence": [
                    {
                        "block_id": "ru-results",
                        "quote": "Точность на тестовой выборке выросла с 71,2% до 78,4%.",
                    }
                ],
            }
        ],
        "evaluation": {
            "datasets": [
                {
                    "text": "Тестовая выборка",
                    "evidence": [
                        {
                            "block_id": "ru-results",
                            "quote": "на тестовой выборке",
                        }
                    ],
                }
            ],
            "baselines": [],
            "metrics": [
                {
                    "text": "Точность",
                    "evidence": [
                        {"block_id": "ru-results", "quote": "Точность"}
                    ],
                }
            ],
            "ablations": [],
            "negative_results": [],
        },
        "limitations": [
            {
                "limitation": "Оценка ограничена русскоязычными статьями.",
                "evidence": [
                    {
                        "block_id": "ru-limit",
                        "quote": "только на русскоязычных статьях",
                    }
                ],
            }
        ],
        "reproducibility": {
            "status": "weak",
            "artifacts": [],
            "missing": ["Исходный код", "Веса модели"],
            "assessment": "Код и веса модели не опубликованы.",
        },
        "aidb_assessment": {
            "novelty": "Компактная схема поиска может быть полезной.",
            "usefulness": "Подход релевантен автоматическому поиску статей.",
            "confidence": "medium",
            "recommended_action": "read",
            "rationale": "Рост точности требует проверки на других выборках.",
        },
        "uncertainties": [
            {
                "uncertainty": "Переносимость на другие языки неизвестна.",
                "why_it_matters": "AIDB собирает статьи на разных языках.",
                "evidence": [
                    {
                        "block_id": "ru-limit",
                        "quote": "Оценка проведена только на русскоязычных статьях",
                    }
                ],
            }
        ],
        "open_questions": ["Работает ли метод на статьях других языков?"],
        "proposed_experiments": [
            {
                "hypothesis": "Модель повышает полноту поиска AIDB.",
                "baseline": "Текущий поиск по ключевым словам",
                "primary_metric": "Полнота первых двадцати результатов",
                "stop_condition": "Остановиться, если полнота не вырастет",
            }
        ],
    }


class FakeProvider:
    name = "fake:test"

    def __init__(self, output=None):
        self.output = output if output is not None else valid_model_output()
        self.prompt = None
        self.schema = None

    def generate(self, prompt, schema):
        self.prompt = prompt
        self.schema = schema
        return copy.deepcopy(self.output)


class RepairingProvider(FakeProvider):
    def __init__(self, first, second):
        super().__init__(first)
        self.outputs = [first, second]
        self.calls = 0

    def generate(self, prompt, schema):
        self.prompt = prompt
        self.schema = schema
        output = self.outputs[self.calls]
        self.calls += 1
        return copy.deepcopy(output)


class SummaryPipelineTest(unittest.TestCase):
    def test_analyze_adds_code_owned_provenance_and_grounded_output(self):
        provider = FakeProvider()
        result = analyze_document(
            BLOCKS,
            {"arxiv_id": "2608.16889v1", "title": "Compact retrieval"},
            provider,
            SCHEMA,
        )

        self.assertEqual(result["provenance"]["provider"], "fake:test")
        self.assertEqual(result["provenance"]["schema_version"], "paper-summary-v1")
        self.assertEqual(result["provenance"]["block_count"], 3)
        self.assertEqual(result["provenance"]["repair_count"], 0)
        self.assertEqual(len(result["provenance"]["document_sha256"]), 64)
        self.assertNotIn("provenance", provider.schema["properties"])
        self.assertNotIn("provenance", provider.schema["required"])
        self.assertNotIn("$schema", provider.schema)
        self.assertNotIn("$id", provider.schema)
        self.assertIn('"id": "b-results"', provider.prompt)
        self.assertIn("Do not browse, call tools", provider.prompt)
        self.assertIn("every human-readable generated value", provider.prompt)
        self.assertIn("never translate, paraphrase", provider.prompt)

    def test_rejects_quote_not_found_in_referenced_block(self):
        output = valid_model_output()
        output["claims"][0]["evidence"][0]["quote"] = "invented evidence"
        with self.assertRaisesRegex(SummaryValidationError, "exact normalized"):
            analyze_document(BLOCKS, {}, FakeProvider(output), SCHEMA)

    def test_one_bounded_repair_can_fix_an_exact_quote(self):
        invalid = valid_model_output()
        invalid["claims"][0]["evidence"][0]["quote"] = "invented evidence"
        provider = RepairingProvider(invalid, valid_model_output())

        result = analyze_document(BLOCKS, {}, provider, SCHEMA)

        self.assertEqual(provider.calls, 2)
        self.assertEqual(result["provenance"]["repair_count"], 1)
        self.assertIn("Validator error", provider.prompt)

    def test_rejects_unknown_evidence_block(self):
        output = valid_model_output()
        output["claims"][0]["evidence"][0]["block_id"] = "does-not-exist"
        with self.assertRaisesRegex(SummaryValidationError, "unknown block id"):
            analyze_document(BLOCKS, {}, FakeProvider(output), SCHEMA)

    def test_rejects_numeric_result_not_present_in_quote(self):
        output = valid_model_output()
        output["results"][0]["result"] = "Accuracy increased from 71.2% to 99.9%."
        with self.assertRaisesRegex(SummaryValidationError, "99.9%"):
            analyze_document(BLOCKS, {}, FakeProvider(output), SCHEMA)

    def test_numeric_grounding_accepts_percent_marker_from_table_context(self):
        output = valid_model_output()
        output["results"][0]["result"] = "Accuracy increased from 71.2 to 78.4%."

        result = analyze_document(BLOCKS, {}, FakeProvider(output), SCHEMA)

        self.assertEqual(result["results"][0]["result"], output["results"][0]["result"])

    def test_rejects_missing_required_deep_section(self):
        output = valid_model_output()
        del output["limitations"]
        with self.assertRaisesRegex(SummaryValidationError, "limitations"):
            analyze_document(BLOCKS, {}, FakeProvider(output), SCHEMA)

    def test_render_is_deterministic_and_keeps_block_citations(self):
        result = analyze_document(BLOCKS, {}, FakeProvider(), SCHEMA)
        first = render_summary(result)
        second = render_summary(result)
        self.assertEqual(first, second)
        self.assertIn("## Main claims", first)
        self.assertIn("## Experimental evaluation", first)
        self.assertIn("## Proposed AIDB experiments", first)
        self.assertIn("[b-results]", first)
        self.assertIn("Accuracy improved from 71.2% to 78.4%", first)
        self.assertTrue(first.endswith("\n"))

    def test_russian_article_keeps_russian_prose_headings_and_enum_labels(self):
        result = analyze_document(
            RU_BLOCKS, {"title": "Компактный поиск"}, FakeProvider(valid_russian_output()), SCHEMA
        )
        rendered = render_summary(result)

        self.assertEqual(result["language"], {"code": "ru", "name": "Русский"})
        self.assertNotIn("wrong", result["labels"])
        self.assertEqual(result["labels"]["evidence"], "Доказательства")
        self.assertIn("## Краткое резюме", rendered)
        self.assertIn("## Основные утверждения", rendered)
        self.assertIn("## Экспериментальная оценка", rendered)
        self.assertIn("**Статус:** низкая", rendered)
        self.assertIn("- Рекомендация: прочитать", rendered)
        self.assertIn(
            "Точность на тестовой выборке выросла с 71,2% до 78,4%", rendered
        )
        self.assertNotIn("Evidence:", rendered)
        self.assertNotIn("## Provenance", rendered)

    def test_rejects_clear_language_mismatch_with_source(self):
        output = valid_model_output()
        output["language"] = {"code": "ru", "name": "Русский"}
        with self.assertRaisesRegex(
            SummaryValidationError, "predominantly Latin source text"
        ):
            analyze_document(BLOCKS, {}, FakeProvider(output), SCHEMA)

    def test_unknown_language_uses_authored_render_labels(self):
        result = analyze_document(BLOCKS, {}, FakeProvider(), SCHEMA)
        result["language"] = {"code": "es", "name": "Español"}
        result["labels"] = labels_for_language("en", {})
        result["labels"].update(
            {
                "executive_summary": "Resumen ejecutivo",
                "claims": "Afirmaciones principales",
                "evidence": "Evidencia",
                "status_weak": "débil",
                "action_read": "leer",
                "provenance": "Procedencia",
            }
        )

        rendered = render_summary(result)

        self.assertIn("## Resumen ejecutivo", rendered)
        self.assertIn("## Afirmaciones principales", rendered)
        self.assertIn("Evidencia:", rendered)
        self.assertIn("## Procedencia", rendered)


class CodexExecProviderTest(unittest.TestCase):
    def test_runs_in_isolated_read_only_ephemeral_directory(self):
        observed = {}

        def fake_run(command, **kwargs):
            observed["command"] = command
            observed.update(kwargs)
            output_path = Path(command[command.index("--output-last-message") + 1])
            output_path.write_text(json.dumps({"ok": True}), encoding="utf-8")
            return SimpleNamespace(returncode=0, stdout="", stderr="")

        with mock.patch(
            "aidb.summarizers.codex_exec.subprocess.run", side_effect=fake_run
        ):
            result = CodexExecProvider(timeout_seconds=7).generate(
                "Return JSON only", {"type": "object"}
            )

        command = observed["command"]
        self.assertEqual(result, {"ok": True})
        self.assertEqual(command[:2], ["codex", "exec"])
        self.assertIn("--ephemeral", command)
        self.assertIn("--ignore-user-config", command)
        self.assertEqual(command[command.index("--sandbox") + 1], "read-only")
        self.assertIn("--output-schema", command)
        self.assertIn("--output-last-message", command)
        self.assertEqual(command[-1], "-")
        self.assertNotIn("--yolo", command)
        self.assertNotEqual(Path(observed["cwd"]).resolve(), ROOT.resolve())
        self.assertEqual(observed["input"], "Return JSON only")
        self.assertEqual(observed["timeout"], 7)


class OpenAIResponsesProviderTest(unittest.TestCase):
    def test_posts_strict_schema_without_tools_or_storage(self):
        observed = {}
        model_output = {"ok": True}
        api_response = {
            "output": [
                {
                    "type": "message",
                    "content": [
                        {"type": "output_text", "text": json.dumps(model_output)}
                    ],
                }
            ]
        }

        class FakeResponse:
            def __enter__(self):
                return self

            def __exit__(self, *args):
                return False

            def read(self):
                return json.dumps(api_response).encode("utf-8")

        def fake_urlopen(request, timeout):
            observed["request"] = request
            observed["timeout"] = timeout
            return FakeResponse()

        with mock.patch.dict(os.environ, {"OPENAI_API_KEY": "test-secret"}, clear=False):
            with mock.patch(
                "aidb.summarizers.openai_responses.urllib.request.urlopen",
                side_effect=fake_urlopen,
            ):
                result = OpenAIResponsesProvider(
                    model="test-model", timeout_seconds=11
                ).generate("Analyze", {"type": "object"})

        request = observed["request"]
        payload = json.loads(request.data.decode("utf-8"))
        self.assertEqual(result, model_output)
        self.assertEqual(request.full_url, "https://api.openai.com/v1/responses")
        self.assertEqual(payload["model"], "test-model")
        self.assertFalse(payload["store"])
        self.assertNotIn("tools", payload)
        self.assertEqual(payload["text"]["format"]["type"], "json_schema")
        self.assertTrue(payload["text"]["format"]["strict"])
        self.assertEqual(observed["timeout"], 11)


if __name__ == "__main__":
    unittest.main()
