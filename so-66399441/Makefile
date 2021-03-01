run_orig:
	echo "" > orig.pytxcode
	latex orig.tex
	pythontex3 orig.tex
	latex orig.tex

run_modif1:
	echo "" > modif1.pytxcode
	latex modif1.tex
	pythontex3 modif1.tex
	latex modif1.tex

genpatch:
	diff -u orig.tex modif1.tex > p1.patch; [ $$? -eq 1 ]

clean:
	rm -f *.pytxcode
	rm -f *.aux *.dvi *.log
	rm -rf pythontex-files-*

.PHONY: run_orig run_modif1 clean diff
