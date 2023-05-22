.PHONY: all clean

all:
	# LaTex - Process files
	pdflatex Documentation

define delete_files
	find . -name ${1} -type f -exec rm -rf {} \;
endef

clean:
	$(call delete_files, "*-blx.bib")
	$(call delete_files, "*.aux")
	$(call delete_files, "*.bbl")
	$(call delete_files, "*.bcf")
	$(call delete_files, "*.blg")
	$(call delete_files, "*.fdb_latexmk")
	$(call delete_files, "*.fls")
	$(call delete_files, "*.lof")
	$(call delete_files, "*.log")
	$(call delete_files, "*.out")
	$(call delete_files, "*.pdf")
	$(call delete_files, "*.run.xml")
	$(call delete_files, "*.synctex.gz")
	$(call delete_files, "*.toc")
