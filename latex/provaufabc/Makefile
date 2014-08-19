SOURCE=exemplo
LATEX=pdflatex -interaction nonstopmode
GREP=grep ^[A-Z]
GREP2T1=grep ^[ACEGIKMOQSUWY]
GREP2T2=grep ^[BDFHJLNPRTVXZ]
GREP4T1=grep ^[ACEGIKMOQSUWY][0-9][13579]
GREP4T2=grep ^[BDFHJLNPRTVXZ][0-9][13579]
GREP4T3=grep ^[ACEGIKMOQSUWY][0-9][24680]
GREP4T4=grep ^[BDFHJLNPRTVXZ][0-9][24680]
SUFFIX=

all: $(SOURCE).pdf

.PHONY: $(SOURCE)t1 $(SOURCE)t2 $(SOURCE)t3 $(SOURCE)t4
$(SOURCE)t1: $(SOURCE)t1.pdf
$(SOURCE)t2: $(SOURCE)t2.pdf
$(SOURCE)t3: $(SOURCE)t3.pdf
$(SOURCE)t4: $(SOURCE)t4.pdf
2tipos: $(SOURCE)t1 $(SOURCE)t2
4tipos: $(SOURCE)t1 $(SOURCE)t2 $(SOURCE)t3 $(SOURCE)t4

%.pdf: %.tex provaufabc.cls
	$(LATEX) $<
	@grep -q -i '^latex warning:.*rerun' $*.log && $(LATEX) $< || true
	@grep -q -i '^latex warning:.*rerun' $*.log && $(LATEX) $< || true

.PHONY: clean provas provas2tipos
clean:
	rm -f _tmp* texput.log $(SOURCE).aux $(SOURCE).log $(SOURCE).pdf $(SOURCE).dvi $(SOURCE).ps $(SOURCE)t1.aux $(SOURCE)t1.log $(SOURCE)t1.pdf $(SOURCE)t1.dvi $(SOURCE)t1.ps $(SOURCE)t2.aux $(SOURCE)t2.log $(SOURCE)t2.pdf $(SOURCE)t2.dvi $(SOURCE)t2.ps $(SOURCE)t3.aux $(SOURCE)t3.log $(SOURCE)t3.pdf $(SOURCE)t3.dvi $(SOURCE)t3.ps $(SOURCE)t4.aux $(SOURCE)t4.log $(SOURCE)t4.pdf $(SOURCE)t4.dvi $(SOURCE)t4.ps
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
	make provas GREP="$(GREP2T1)" SUFFIX="t1"
	make provas GREP="$(GREP2T2)" SUFFIX="t2"

provas4tipos: $(SOURCE)t1.tex $(SOURCE)t2.tex $(SOURCE)t3.tex $(SOURCE)t4.tex
	make provas GREP="$(GREP4T1)" SUFFIX="t1"
	make provas GREP="$(GREP4T2)" SUFFIX="t2"
	make provas GREP="$(GREP4T3)" SUFFIX="t3"
	make provas GREP="$(GREP4T4)" SUFFIX="t4"

help:
	@echo SEATINGMAP=/path/to/file make provas
	@echo As provas serão geradas no diretório out

out:
	mkdir out
