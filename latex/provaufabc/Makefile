SOURCE=exemplo

all: $(SOURCE).pdf

%.pdf: %.tex provaufabc.cls
	pdflatex $<
	@grep -q -i '^latex warning:.*rerun' $*.log && pdflatex $< || true
	@grep -q -i '^latex warning:.*rerun' $*.log && pdflatex $< || true

clean:
	rm -f _tmp* $(SOURCE).aux $(SOURCE).log $(SOURCE).pdf $(SOURCE).dvi $(SOURCE).ps
	rm -rf out/

provas:
	@if [ ! -f "$(SEATINGMAP)" ]; \
	then \
		echo "Define SEATINGMAP environment variable correctly!"; \
		false; \
	fi
	@make out
	@for num in `sed -e 's/  */\n/g' "$(SEATINGMAP)"|sort|grep ^[A-Z]`; \
	do \
		echo "\\def\\\numprova{$$num}" > _tmpprova.tex; \
		cat $(SOURCE).tex >> _tmpprova.tex; \
		make _tmpprova.pdf; \
		mv _tmpprova.pdf out/$(SOURCE)-$$num.pdf; \
	done

help:
	@echo SEATINGMAP=/path/to/file make provas
	@echo As provas serão geradas no diretório out

out:
	mkdir out
