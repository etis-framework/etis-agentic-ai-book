.PHONY: check figures check-figures chapter book-docx book-pdf book-html qa
check:
	python3 publishing/scripts/check.py
	python3 publishing/scripts/check_figures.py
	python3 publishing/scripts/check_ch04_figure_semantics.py
	python3 publishing/scripts/check_ch05_acceptance.py
	python3 publishing/scripts/check_ch06_acceptance.py
	python3 publishing/scripts/check_single_volume.py
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
