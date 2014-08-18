SOURCE=exemplo
LATEX=pdflatex -interaction nonstopmode
GREP=grep ^[A-Z]
GREPT1=grep ^[ACEGIKMOQSUWY]
GREPT2=grep ^[BDFHJLNPRTVXZ]
SUFFIX=

all: $(SOURCE).pdf

%.pdf: %.tex provaufabc.cls
	$(LATEX) $<
	@grep -q -i '^latex warning:.*rerun' $*.log && $(LATEX) $< || true
	@grep -q -i '^latex warning:.*rerun' $*.log && $(LATEX) $< || true

.PHONY: clean provas provas2tipos
clean:
	rm -f _tmp* $(SOURCE).aux $(SOURCE).log $(SOURCE).pdf $(SOURCE).dvi $(SOURCE).ps texput.log
	rm -rf out/

provas:
	@if [ ! -f "$(SEATINGMAP)" ]; \
	then \
		echo "Define SEATINGMAP environment variable correctly!"; \
		false; \
	fi
	@make out
	@for num in `sed -e 's/  */\n/g' "$(SEATINGMAP)"|sort|$(GREP)`; \
	do \
		echo "\\def\\\numprova{$$num}" > _tmpprova.tex; \
		cat $(SOURCE)$(SUFFIX).tex >> _tmpprova.tex; \
		make _tmpprova.pdf; \
		mv _tmpprova.pdf out/$(SOURCE)-$$num.pdf; \
	done

provas2tipos: $(SOURCE)t1.tex $(SOURCE)t2.tex
	make provas GREP="$(GREPT1)" SUFFIX="t1"
	make provas GREP="$(GREPT2)" SUFFIX="t2"

help:
	@echo SEATINGMAP=/path/to/file make provas
	@echo As provas serão geradas no diretório out

out:
	mkdir out
