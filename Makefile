.PHONY: check figures check-figures chapter book-docx book-pdf book-html qa
check:
	python3 publishing/scripts/check_publishing_identity.py
	python3 publishing/scripts/check_part4_capstone.py
	python3 publishing/scripts/check_backmatter_integrity.py
	python3 publishing/scripts/check_backmatter_publication.py
	python3 publishing/scripts/check.py
	python3 publishing/scripts/check_figures.py
	python3 publishing/scripts/check_ch04_figure_semantics.py
	python3 publishing/scripts/check_ch05_acceptance.py
	python3 publishing/scripts/check_ch06_acceptance.py
	python3 publishing/scripts/check_ch07_acceptance.py
	python3 publishing/scripts/check_ch08_acceptance.py
	python3 publishing/scripts/check_part2_reference_architecture.py
	python3 publishing/scripts/check_ch09_acceptance.py
	python3 publishing/scripts/check_ch10_acceptance.py
	python3 publishing/scripts/check_ch11_acceptance.py
	python3 publishing/scripts/check_ch12_acceptance.py
	python3 publishing/scripts/check_ch13_acceptance.py
	python3 publishing/scripts/check_ch14_acceptance.py
	python3 publishing/scripts/check_ch15_acceptance.py
	python3 publishing/scripts/check_ch16_acceptance.py
	python3 publishing/scripts/check_ch17_acceptance.py
	python3 publishing/scripts/check_ch18_acceptance.py
	python3 publishing/scripts/check_ch18_v2_traceability.py
	python3 publishing/scripts/check_conceptual_continuity.py
	python3 publishing/scripts/check_c04_identity_semantics.py
	python3 publishing/scripts/check_ch19_acceptance.py
	python3 publishing/scripts/check_ch20_acceptance.py
	python3 publishing/scripts/check_ch21_acceptance.py
	python3 publishing/scripts/check_ch22_acceptance.py
	python3 publishing/scripts/check_ch23_acceptance.py
	python3 publishing/scripts/check_ch24_acceptance.py
	python3 publishing/scripts/check_ch25_acceptance.py
	python3 publishing/scripts/check_ch25_figure_geometry.py
	python3 publishing/scripts/check_ch26_acceptance.py
	python3 publishing/scripts/check_ch26_figure_geometry.py
	python3 publishing/scripts/check_ch27_acceptance.py
	python3 publishing/scripts/check_ch28_acceptance.py
	python3 publishing/scripts/check_ch28_figure_geometry.py
	python3 publishing/scripts/check_ch29_acceptance.py
	python3 publishing/scripts/check_ch30_acceptance.py
	python3 publishing/scripts/check_ch31_acceptance.py
	python3 publishing/scripts/check_ch32_acceptance.py
	python3 publishing/scripts/check_ch33_acceptance.py
	python3 publishing/scripts/check_ch34_acceptance.py
	python3 publishing/scripts/check_ch35_acceptance.py
	python3 publishing/scripts/check_ch36_acceptance.py
	python3 publishing/scripts/check_ch27_figure_geometry.py
	python3 publishing/scripts/check_ch23_ch24_arrow_geometry.py
	python3 publishing/scripts/check_code_listing_layout.py
	python3 publishing/scripts/check_chapter_first_references.py
	python3 publishing/scripts/check_reader_editorial_ch01_ch30.py
	python3 publishing/scripts/check_professional_review_perspectives.py
	python3 publishing/scripts/check_companion_architecture_docs.py
	python3 publishing/scripts/check_assurance_handoff.py
	python3 publishing/scripts/check_deep_wargame_code_contract.py
	python3 publishing/scripts/check_reader_companion_access.py
	python3 publishing/scripts/check_reader_evidence_freshness.py
	python3 publishing/scripts/check_companion_code_quality.py
	python3 -m unittest discover -s examples/refund-reference-system/build0 -p "test_*.py" -v
	python3 -m unittest discover -s examples/refund-reference-system/build1 -p "test_*.py" -v
	python3 -m unittest discover -s examples/refund-reference-system/build2 -p "test_*.py" -v
	python3 -m unittest discover -s examples/refund-reference-system/build3 -p "test_*.py" -v
	python3 -m unittest discover -s examples/refund-reference-system/build4 -p "test_*.py" -v
	python3 -m unittest discover -s examples/refund-reference-system/build5 -p "test_*.py" -v
	python3 -m unittest discover -s examples/refund-reference-system/reliability -p "test_*.py" -v
	python3 -m unittest discover -s examples/refund-reference-system/security -p "test_*.py" -v
	python3 -m unittest discover -s examples/refund-reference-system/operations -p "test_*.py" -v
	python3 -m unittest discover -s examples/refund-reference-system/assurance -p "test_*.py" -v
	python3 publishing/scripts/check_parts12_citations.py
	python3 publishing/scripts/check_parts13_reader_paths.py
	python3 publishing/scripts/check_parts13_integration.py
	python3 publishing/scripts/check_mac_word_ch01_ch17.py
	python3 publishing/scripts/check_single_volume.py
	python3 publishing/scripts/check_finished_page_ledger.py
	python3 publishing/scripts/check_pre_part_vii_audit.py
	python3 publishing/scripts/check_publication_pass04.py
figures:
	python3 publishing/scripts/figures.py
check-figures:
	python3 publishing/scripts/check_figures.py --built
chapter:
	python3 publishing/scripts/build.py --chapter $(CH) --format $(FORMAT)
book-docx:
	python3 publishing/scripts/build.py --format docx
	python3 publishing/scripts/check_figures.py --built
book-pdf:
	python3 publishing/scripts/build.py --format pdf
book-html:
	python3 publishing/scripts/build.py --format html
qa: check
	@echo "Manual figure, technical, citation, and print QA still required."

# Publication pass is a separate release gate, not a substitute for make check.
.PHONY: check-publication
check-publication: book-docx
	python3 publishing/scripts/check_publication_certification_pass.py

# Publication pass 02 validates source and Word structural readiness.
# After exporting the final Word-for-Mac PDF, populate cached PAGEREF
# values so opening the review DOCX does not display draft dashes.
.PHONY: check-publication-pass02 resolve-print-locators
check-publication-pass02: book-docx
	python3 publishing/scripts/check_publication_certification_pass_02.py
resolve-print-locators:
	python3 publishing/scripts/resolve_print_locators.py dist/etis-agentic-ai-book.docx "$(PDF)" --strict

# Publication pass 3: extended reference index, biography, and live page fields.
.PHONY: check-publication-pass03
check-publication-pass03: book-docx
	python3 publishing/scripts/check_publication_certification_pass_03.py

# Pass 4: agent-engineering depth, protocol and source/code traceability.
.PHONY: check-publication-pass04
check-publication-pass04:
	python3 publishing/scripts/check_publication_pass04.py
