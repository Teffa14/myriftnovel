# Contrato de salida NDM v1.0
Usar Markdown para lectura humana o JSON/CSV equivalentes. IDs persistentes; campos desconocidos null. Los campos que no aplican se justifican; los archivos previos pueden migrarse sin cambiar ID.
 
## Ficha de unidad
work_id; unit_id; source_locator; edition; language; translator; proofreader; source_hash; access/license; date; coverage; duplicate_of; chapter_certified=false por defecto; processing_mode; metrics_executed; metric_refs; initial_state; beats[] {beat_id, source_locator, evidence_summary, fact_status, function, before, after, POV}; characters[] {id, goal, obstacle, belief, choice, result, knowledge_before, knowledge_after}; scene_structure; voice {person, tense, distance, focalization, register, dialogue, syntax, description, rhythm, humor, exposition}; technical_state {rules_version, public_information, private_information, resources, choices, results, unknowns}; threads[] {id, opened_at, state, dependency, resolution}; cross_unit_links; inconsistencies; limitations; pattern_ids; block_ids.
 
## Ficha de mecanismo
id; level (L1–L6); primary_function; name; source_refs[]; evidence_summary; fact_status; abstract_structure[]; inputs; conditions; expected_effect (hipótesis si no testado); suitable_context; unsuitable_context; original_sentence; failure_case; acceptance_checks[]; variant_of; related_ids[]; status; reviewer; test_ref; revision.
 
## Bloque original
id; functions[]; pattern_ids[]; setup; POV; knowledge_boundary; original_prose; state_change; failure_case; domain_validation; canon_status=noncanon por defecto.
 
## Ledger longitudinal
entity_id; unit_id; state_before; delta; state_after; evidence_ref; fact_status; owner/POV; time; unresolved_dependencies. Para economía añadir quantity, unit, currency, price, fee, tax, paid/receivable/projected y ownership_before/after. Para estrategia añadir rule_version, hypothesis, replay_ref y outcome. Para conocimiento: observed/reported/inferred/unknown. No calcular saldo exacto con transacciones faltantes.
 
## Registro de validación
check_id; scope; check; result (pass/fail/partial/not_run); evidence; blocker; reviewer; date. Checks mínimos: fuente y límites, duplicados, beats verificables, consistencia de conocimiento, continuidad numérica, función abstracta, originalidad de ejemplo, comparación con existentes, evidencia del estado, integridad de referencias e IDs. Chapter_certified requiere cobertura completa y revisión íntegra registrada. Estado approved requiere aprobación explícita; tested requiere resultado de evaluación.
 
## Entregables de lote
ANALYSIS.md, PATTERNS.md, opcional METRICS.json + script ejecutado, INDEX.md y STATUS.md, actualización del protocolo de uso, commit y verificación. En fase de consolidación: familias de mecanismos, mapa de variantes, evidencias, diferencias y estados; no borrar ejemplos sin autorización.
