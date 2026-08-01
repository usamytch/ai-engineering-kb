# 07. Safety, security и governance

**Обновлено:** 2026-08-01

## Базовая модель риска

Agentic system расширяет attack surface четырьмя слоями:

1. **Model:** ошибочное reasoning, goal misinterpretation, jailbreak.
2. **Harness:** слабые policies, бесконечные loops, отсутствие approval.
3. **Tools/data:** prompt injection, malicious output, overbroad permissions, supply chain.
4. **Environment:** secrets, filesystem, browser, network, shared state и другие agents.

Security нельзя поручить system prompt. Enforcement должен находиться в коде, identity layer, sandbox и external policy checks.

## Главные threat classes

- direct и indirect prompt injection;
- excessive agency / tool misuse;
- data exfiltration и sensitive information disclosure;
- confused deputy и privilege escalation;
- insecure output handling и code execution;
- memory/context poisoning;
- malicious MCP/tool/agent supply chain;
- denial of wallet/resource exhaustion;
- inter-agent impersonation/message poisoning;
- unsafe autonomy и failure to escalate.

Текущие ориентиры: [OWASP Top 10 for Agentic Applications](https://genai.owasp.org/2025/12/09/owasp-top-10-for-agentic-applications-the-benchmark-for-agentic-security-in-the-age-of-autonomous-ai/), [OWASP Top 10 for LLM Applications](https://owasp.org/www-project-top-10-for-large-language-model-applications/), [MITRE ATLAS](https://atlas.mitre.org/) и [NIST AI RMF](https://www.nist.gov/itl/ai-risk-management-framework).

## Trust boundaries

Явно отметить:

- user input;
- retrieved documents/web/email;
- tool descriptions и server metadata;
- tool results;
- memories и previous artifacts;
- messages от remote agents;
- model output перед execution;
- external side effects.

Всё содержимое за границей — данные, а не доверенная инструкция.

## Controls

| Риск | Controls |
| --- | --- |
| Prompt injection | source labels, instruction/data separation, allowlists, output/action validation |
| Excessive agency | least privilege, scoped tokens, action budgets, human approval |
| Tool misuse | typed schemas, authorization in tool, policy engine, idempotency |
| Data leakage | data minimization, tenant isolation, egress controls, redaction |
| Memory poisoning | provenance, write approval/rules, TTL, correction/delete, anomaly tests |
| Resource exhaustion | max turns/tokens/calls/cost/time, rate limits, no-progress detector |
| Supply chain | pinned versions, signed/verified artifacts, MCP/tool review, inventory |
| Unsafe code/browser | sandbox, isolated secrets, restricted network/filesystem, disposable environment |

## Human control

Human-in-the-loop работает только если:

- человек видит exact action, target и consequences;
- approval нельзя переиспользовать для другого действия;
- high-risk defaults — deny;
- у пользователя есть stop/cancel и audit trail;
- агент понимает, когда uncertain/ambiguous и должен спросить.

[Trustworthy agents in practice](https://www.anthropic.com/research/trustworthy-agents) подчёркивает human control, alignment with user expectations, secure interactions, transparency и privacy как отдельные design layers.

## Threat modeling session

Для каждого tool/use case ответить:

1. Что самое ценное доступно агенту?
2. Кто может управлять входом или observations?
3. Какой максимальный вред одного вызова и серии вызовов?
4. Где проверяются identity, authorization и intent?
5. Как обнаружить misuse и остановить run?
6. Что остаётся в memory/logs и как удаляется?
7. Что произойдёт при compromised tool/MCP server/remote agent?

## Governance artifacts

- system card / intended use and limitations;
- data and tool inventory;
- risk register с owner и treatment;
- eval report и critical slices;
- approval/permission matrix;
- incident response и kill switch;
- model/prompt/tool version history;
- retention/deletion policy;
- adoption decision record.

## Минимальный release gate

- [ ] Indirect prompt injection tests.
- [ ] Cross-tenant/ACL tests.
- [ ] Prohibited action tests.
- [ ] Approval binding и bypass tests.
- [ ] Secret/PII leakage tests.
- [ ] Tool/MCP failure и malicious output tests.
- [ ] Memory poisoning и delete tests.
- [ ] Budget exhaustion и infinite-loop tests.
- [ ] Incident owner, rollback и kill switch.

