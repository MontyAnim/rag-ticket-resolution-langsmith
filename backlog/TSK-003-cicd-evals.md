# Task: Automatización del Pipeline de Evaluación CI/CD

**ID:** `TSK-003`
**Status:** `Todo`
**Gitflow Branch:** `feature/TSK-003-cicd-evals`
**Dependencies:** `TSK-001`

---

## Context
El código actual solo posee un script manual (`scratch_eval_test.py`) con evaluaciones LLM-as-a-judge (precisión, fidelidad, tono). El SDD especifica un framework de pruebas de regresión offline robusto que utiliza `aevaluate()` para ejecutar pruebas masivas (Golden Dataset) e incorpora evaluadores heurísticos deterministas (verificación de latencia, esquema JSON, validación de tool calling).

---

## Acceptance Criteria
- [ ] Se crea un pipeline de evaluación `src/scripts/run_evals.py` que instancia un cliente de LangSmith y usa el método `aevaluate()`.
- [ ] Se añaden evaluadores heurísticos deterministas en `src/evals/` (ej. verificador de latencia máxima de respuesta o completitud de llaves JSON).
- [ ] El pipeline es capaz de leer un dataset de LangSmith y procesarlo concurrentemente.

---

## Definition of Done (DoD)
- [ ] Code meets acceptance criteria.
- [ ] All code and artifacts are written in English (per `language-policy.md`).
- [ ] Walkthrough artifact generated (if applicable).
- [ ] Backend QA or Tests passed (if applicable).
