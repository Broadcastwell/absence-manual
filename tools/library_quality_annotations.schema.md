# Quality annotations

`library_quality.py` adds the29October2026 whole-library rules. It makes no network request, edits no page and creates no exception. Existing answer and build checks still run.

The committed `library_quality_annotations.json` covers exactly the leaves in `docs/answers`. It is review metadata, outside the public page template. A draft batch can use a separate private copy with `--docs` and `--annotations`; sync the matching reviewed pages and annotations together for the PR. Never put private query text or prompts in this file.

Top-level fields are `schema_version:1`, `shape_definitions`, `cluster_plans`, `figures`, `pages` and `index_question_titles`. Each cluster plan has at least eight distinct defined shapes. Actual used shapes may differ from the plan; existing cases remain recorded rather than relabelled.

Each page key is its source path relative to `docs`, such as `answers/measurement/example.md`. Its record contains:

- `bank_id`: the same LB-Q receipt ID as the page metadata.
- `source_sha256`: the exact file-byte hash.
- `opening_sha256`: the UTF-8 hash of the answer paragraph extracted by `paragraph_after_heading`, with CRLF and lone CR normalized to LF and outer whitespace trimmed, before prose normalization. This matches the independent readers' text extraction; file-byte hashes remain exact.
- `opening_shape` and `classification_reason`: the independent writing review's actual classification and reason.
- `writing_review_sha256`: the saved independent review receipt hash.
- `lead_figures`: every canonical observed fact leading the opening, once each.
- `lead_figure_spans`: an object mapping every lead figure ID to a nonempty list of exact spans in that opening.
- `source_review_sha256`: the saved independent source-reconciliation receipt hash.

The source reviewer identifies all leading facts, including a multi-figure opening. Supporting evidence outside the opening does not consume a leading use. An author cannot invent a shape or a figure ID to avoid a cap. The independent reviews remain necessary; a hash binds a receipt but does not replace the work it records.

A figure record has `source_url`, `record`, `count`, `base`, `unit`, `label` and `source_review_sha256`. Its key is returned by `figure_key`. The controlled `record` keys are category, engine, question, run, subject, metric, event_date, capture_date, cohort and release. Values name the actual published cut. Metric and subject are required. A null base means an absolute quantity. Keep the source's actual observed count and base when a paragraph states a percentage; rounded rates and interval restatements do not create another fact. DOI aliases normalize to one source. Page slugs and prose are not source cuts.

`index_question_titles` holds140 actual Index question H1/title/canonical records and their source hashes. The live Manual chapter titles are also checked from the current repository. A library page may use the same title and headline within itself; cross-page metadata duplicates and another page's title used as an alias fail.

`library_quality_baseline.json` is a separate immutable snapshot of only the150 leaves live before this run. The tool pins both the snapshot and the complete baseline hash. Each exception names the actual existing case. Source changes, relabelled existing openings, increased existing excess counts, new adjacent pairs and new pages cannot acquire that exception. When adding distinct pages resolves a concentration, the report records that improvement. There is no command to refresh the baseline automatically.

Run `python tools/library_quality.py --report library-quality-report.json` and the quality tests before committing. The report includes all new failures, the highest pair touching each cluster, within-cluster maxima, actual and planned opening counts, lead-use counts and every existing case retained. Any shared eight-word opening sequence is a failure even if it is in the middle of the paragraph. Six-word overlap uses unique sequences and the smaller set as its exact base; exactly20percent passes.
