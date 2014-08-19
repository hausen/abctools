provaufabc
==========

Modelo de exame para a UFABC para usuários de LaTeX.

Modo de Uso Simples
-------------------

Coloque o arquivo provaufabc.cls no mesmo diretório
do seu arquivo tex, e use

        \documentclass[addpoints]{provaufabc}

no arquivo tex.

Veja o arquivo exemplo.tex.

Use pdflatex, ou gere um DVI e converta para PS.

Se você tiver o GNU Make instalado, poderá gerar
o arquivo com um simples `make`. Neste caso, edite
o arquivo `Makefile`, substituindo

    SOURCE=example

na primeira linha por

    SOURCE=nome_do_arquivo_sem_extensão

Atenção! Nunca coloque a extensão `.tex` na linha
acima.

Modo de Uso para Provas Numeradas
---------------------------------

Se quiser colocar um número em cada prova, coloque
na primeira linha do seu arquivo tex, antes do
`\documentclass`, o comando

    \def\numprova{XYZ}

onde `XYZ` é o número que você deseja dar à prova.

Usando o GNU Make, você poderá numerar automaticamente
as suas provas, da seguinte maneira:

1. Edite o arquivo `Makefile`, substituindo a linha
   `SOURCE=example` de acordo com as instruções do
   modo de uso simples.

2. Comente a linha `\def\numprova` que você inseriu no
   arquivo.

3. Crie ou obtenha um arquivo com o mapa de assentos
   da sala de aula para a qual você dará a prova. O
   formato desse arquivo está descrito ao final deste
   documento. Suponha que ele esteja gravado em
   `/path/to/seatmap.txt` (substitua pelo caminho
   correto do arquivo). O caminho e o nome do arquivo
   não podem conter espaços.

4. Execute `make provas SEATMAP=/path/to/seatmap.txt`

5. Um diretório `out/` será criado com as provas
   numeradas automaticamente. Verifique algumas provas
   para se certificar de que os arquivos foram gerados
   corretamente.

Modo de Uso para Provas Numeradas de Dois Tipos
-----------------------------------------------

É possível gerar provas numeradas de dois tipos para
coibir a cola. É preciso criar dois arquivos tex com
os sufixos `t1` e `t2` antes da extensão.

Suponha que você criou os arquivos `provaXt1.tex` e
`provaXt2.tex` no mesmo diretório do `Makefile`, com
as provas de dois tipos para a turma. Para gerar os
PDFs com as provas numeradas:

1. Edite o arquivo `Makefile`, substituindo a linha
   `SOURCE=example` por `SOURCE=provaX`.

2. Execute `make provaXt1 provaXt2` para gerar os
   arquivos `provaXt1.pdf` e `provaXt2.pdf`.
   Verifique se os arquivos foram gerados
   corretamente.

3. Comente as linhas `\def\numprova` nos arquivos
   `provaXt1.tex` e `provaXt2.tex`

4. Crie ou obtenha um arquivo com o mapa de assentos
   da sala de aula para a qual você dará a prova, de
   acordo com o passo 3 do modo de uso anterior.

5. Execute
   `make provas2tipos SEATMAP=/path/to/seatmap.txt`

6. Um diretório `out/` será criado com as provas
   numeradas automaticamente. Verifique algumas provas
   para se certificar de que os arquivos foram gerados
   corretamente.

Modo de Uso para Provas Numeradas de Quatro Tipos
-------------------------------------------------

Similar ao modo de uso anterior, mas você tem que
criar arquivos `provaXt1.tex`, `provaXt2.tex`,
`provaXt3.tex` e `provaXt4.tex` e executar
`make provas4tipos SEATMAP=/path/to/seatmap.txt`.

Mapa de Assentos de Sala de Aula
--------------------------------

Para criar o mapa de assentos para uma sala de aula,
considere os assentos dispostos em linhas e colunas,
onde as colunas são A, B, C, ... e as linhas são
00, 01, 02, ...

Exemplo:

    A10    B10 C10    D10        F10
    A09    B09 C09    D09 E09    F09
    A08    B08 C08    D08 E08    F08
    A07    B07 C07    D07 E07    F07
    A06    B06 C06    D06 E06    F06
    A05    B05 C05    D05 E05    
    A04    B04 C04    D04 E04    
    A03    B03 C03    D03 E03    F03
    A02    B02 C02    D02 E02    F02
    A01    B01 C01    D01 E01    F01
                                 F00

É fundamental que os códigos dos assentos estejam
sempre no formato `Xnn`, onde `X` é uma letra
maiúscula e nn é um número representado _sempre_
com dois dígitos.

Como a sala geralmente tem mais assentos do que
alunos, recomenda-se eliminar do mapa de assentos
aqueles no fundo da sala que ultrapassarem o
número de alunos, para evitar que sejam geradas
provas em excesso.
