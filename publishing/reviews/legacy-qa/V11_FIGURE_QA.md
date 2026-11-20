# V11 Figure Redesign — QA Record

Scope: Figure 2.4 and Figures 3.1–3.4 only. No manuscript text changed.

- Figure 2.4: redesigned into workflow → bounded reasoning → trusted execution with durable state and provider adapter; removed visually misleading bent return arrows. The adapter reports observations for reconciliation as described in the chapter prose; diagram deliberately does not depict all read/write paths.
- Figure 3.1: explicit accountable process and independent authority before verified effect.
- Figure 3.2: responsibility/allocation matrix, not a misleading automation sequence.
- Figure 3.3: delegation scope, independent execution gate, permit/hold paths.
- Figure 3.4: three alternative designs in a comparison matrix feeding shared execution controls.

Checks: make check PASS; make book-docx PASS; PDF conversion succeeded (107-page current draft). Figures inspected on PDF pages 42, 49, 52, 55, and 58. Figures use consistent Helvetica, palette and rounded-box grammar. The current draft is NOT a final publication QA certification; full-book pagination and editorial review remain open.

Source DOT font size is 22 pt for these figures; effective physical type varies with figure scaling. Do not treat the source font-size check as a measured print-size certification.

Install: unzip -o ~/Downloads/ETIS_V11_Figure_Redesign_Patch.zip from the repository root; make check; make book-docx; open dist/etis-agentic-ai-book.docx.
