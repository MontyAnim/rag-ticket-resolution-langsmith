# Task: Alineación de Modelos (GPT-4o y Claude 3.5 Sonnet)

**ID:** `TSK-001`
**Status:** `Todo`
**Gitflow Branch:** `feature/TSK-001-model-alignment`
**Dependencies:** `None`

---

## Context
El documento SDD exige el uso de GPT-4o como agente principal y Claude 3.5 Sonnet exclusivamente para evaluación a fin de evitar el sesgo de auto-mejora. Actualmente el código usa `ChatGroq` (`openai/gpt-oss-120b`) o `ChatOpenAI` (`gpt-4o-mini`). Esta tarea consiste en actualizar la instanciación de LLMs en `src/agent/llm.py` y `src/evals/llm_judge.py` para integrar Claude mediante `langchain-anthropic` y ajustar los fallbacks a los modelos estipulados en el SDD, manejando las llaves correspondientes.

---

## Acceptance Criteria
- [ ] `src/agent/llm.py` inicializa `GPT-4o` (o se deja configurado para usar un equivalente de alta capacidad) como modelo principal.
- [ ] `src/evals/llm_judge.py` inicializa `Claude 3.5 Sonnet` (`ChatAnthropic`) de forma predeterminada para todos los evaluadores (precisión, fidelidad, tono).
- [ ] Las variables de entorno `ANTHROPIC_API_KEY` se soportan en `src/core/config.py`.

---

## Definition of Done (DoD)
- [ ] Code meets acceptance criteria.
- [ ] All code and artifacts are written in English (per `language-policy.md`).
- [ ] Walkthrough artifact generated (if applicable).
- [ ] Backend QA or Tests passed (if applicable).
