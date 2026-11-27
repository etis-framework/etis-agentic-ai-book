.PHONY: check figures check-figures chapter book-docx book-pdf book-html qa
check:
	python3 publishing/scripts/check_glossary_print_integrity.py
	python3 publishing/scripts/check_print_isbns.py
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
	$(MAKE) check-companion
	python3 publishing/scripts/check_parts12_citations.py
	python3 publishing/scripts/check_parts13_reader_paths.py
	python3 publishing/scripts/check_parts13_integration.py
	python3 publishing/scripts/check_mac_word_ch01_ch17.py
	python3 publishing/scripts/check_single_volume.py
	python3 publishing/scripts/check_finished_page_ledger.py
	python3 publishing/scripts/check_pre_part_vii_audit.py
	python3 publishing/scripts/check_publication_pass04.py
	python3 publishing/scripts/check_pass4_teaching_and_sources.py
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
	python3 publishing/scripts/check_pass4_teaching_and_sources.py

.PHONY: check-publication-pass04b
check-publication-pass04b:
	python3 publishing/scripts/check_publication_pass04.py
	python3 publishing/scripts/check_pass4_teaching_and_sources.py

# Focused final Pass-4 verification of MCP/A2A architecture and teaching claims.
.PHONY: check-publication-pass04-protocols
check-publication-pass04-protocols:
	python3 publishing/scripts/check_pass4_protocol_boundaries.py

# Pass 5 print-format identity: both ISBNs are checked independently.
.PHONY: check-publication-pass05-isbns
check-publication-pass05-isbns:
	python3 publishing/scripts/check_print_isbns.py

.PHONY: check-publication-pass05-glossary
check-publication-pass05-glossary: book-docx
	python3 publishing/scripts/check_glossary_print_integrity.py

# Independently reproducible companion tests: no DOCX, Graphviz, or paid services.
.PHONY: check-companion
check-companion:
	python3 containers/test_container_tools.py
	python3 -B containers/assurance/test_security_gate.py
	python3 publishing/scripts/test_companion_release.py -v
	python3 publishing/scripts/check_companion_release.py
	python3 publishing/scripts/check_active_reader_links.py

# Container execution (Docker and Compose only; host Python is not needed).
# SPDX-License-Identifier: Apache-2.0 applies to this container target block.
.PHONY: docker-build docker-build-dev docker-check docker-up docker-shell docker-down docker-clean docker-assurance docker-build0 docker-build1 docker-build2 docker-build3 docker-build4 docker-build5
DOCKER_COMPOSE ?= docker compose
docker-build:
	$(DOCKER_COMPOSE) build companion
docker-build-dev:
	ETIS_DEV_UID="$${ETIS_DEV_UID:-$$(id -u)}" ETIS_DEV_GID="$${ETIS_DEV_GID:-$$(id -g)}" $(DOCKER_COMPOSE) build dev
docker-check:
	$(DOCKER_COMPOSE) run --build --rm --no-deps -T companion
docker-up:
	ETIS_DEV_UID="$${ETIS_DEV_UID:-$$(id -u)}" ETIS_DEV_GID="$${ETIS_DEV_GID:-$$(id -g)}" $(DOCKER_COMPOSE) up -d --build --no-deps dev
docker-shell:
	$(DOCKER_COMPOSE) exec dev bash
docker-build0 docker-build1 docker-build2 docker-build3 docker-build4 docker-build5:
	$(DOCKER_COMPOSE) run --build --rm --no-deps -T companion python3 containers/demo.py --build $(subst docker-build,,$@)
docker-assurance: docker-build
	@mkdir -p .etis-local/evidence; \
	dir=$$(mktemp -d .etis-local/evidence/run-XXXXXX) || exit 1; \
	if $(DOCKER_COMPOSE) run --rm --no-deps -T companion python3 containers/export_evidence.py > "$$dir/evidence.json" && test -s "$$dir/evidence.json"; then \
	  echo "Exported bounded fixture evidence: $$dir/evidence.json"; \
	else rm -f "$$dir/evidence.json"; rmdir "$$dir"; exit 1; fi
docker-down:
	$(DOCKER_COMPOSE) down
docker-clean:
	$(DOCKER_COMPOSE) down --remove-orphans
	@echo "Project containers removed. Exercise volumes and exported evidence retained."
