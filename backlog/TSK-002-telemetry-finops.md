# Task: Inyección de Telemetría FinOps y Etiquetas en LangSmith

**ID:** `TSK-002`
**Status:** `Done`
**Gitflow Branch:** `feature/TSK-002-telemetry-finops`
**Dependencies:** `None`

---

## Context
Para el control de costos y observabilidad corporativa, el SDD requiere inyectar `ls_provider`, `ls_model_name`, `backend_version` y etiquetas granulares (`tool:X`, `env:production`) en cada traza. Actualmente `src/api/routes/tickets.py` inyecta solo datos básicos de `tenant_id` y `user_id`. Esta tarea actualizará la configuración de la ejecución del grafo para incluir estos metadatos inmutables y añadirá soporte para etiquetas específicas.

---

## Acceptance Criteria
- [x] `src/api/routes/tickets.py` incluye `ls_provider`, `ls_model_name` y `backend_version` en la sección de `metadata` del objeto `RunnableConfig`.
- [x] Se inyectan etiquetas (`tags`) de entorno (`env:X`) y dominio en las configuraciones de los runs.
- [x] Los metadatos de versión y proveedor se derivan de la configuración del sistema `src/core/config.py`.

---

## Definition of Done (DoD)
- [x] Code meets acceptance criteria.
- [x] All code and artifacts are written in English (per `language-policy.md`).
- [x] Walkthrough artifact generated (if applicable).
- [x] Backend QA or Tests passed (if applicable).
