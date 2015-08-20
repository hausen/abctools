Suportal - Suporte ao Portal do Professor
====

As planilhas a serem usadas devem ser criadas com o
OpenOffice/LibreOffice/BrOffice e devem ser gravadas
no formato ODS. Planilhas criadas em outros editores
(como, por exemplo, no Google Documents) devem ser
abertas e regravadas no OpenOffice antes de serem
usadas.

Para cada turma, deve-se usar uma planilha diferente.

Para lançamento de notas, o arquivo deve deve ter uma
planilha com o nome "Conceitos." A primeira linha dessa
planilha deve ter os rótulos das colunas, e deve ter no
mínimo as colunas "ra", "conceito" e "faltas."
As faltas devem ser listadas em horas, assim como
no lançamento de conceitos no portal.

Para lançamento de presenças e faltas, o arquivo deve
ter as planilhas "Presenças" e "Plano de Aulas."
A planilha de presenças deve ter os rótulos de colunas
"ra" e "dd/mm" (onde dd/mm são os dias de aulas).
A planilha plano de aulas deve ter as colunas "dia"
(no formato dd/mm/aaaa), "aula" (descrição da aula),
"inicio" (horário de inicio da aula) e "horas"
(quantidade de horas de aula).

Scripts
----

    lanca_conceitos.py -u usuario CodigoTurma Planilha.ods

Faz login no portal com o usuário especificado, lê a planilha
e lança os conceitos.

    lanca_presencas.py -u usuario CodigoTurma planilha.ods

Faz login no portal com o usuário especificado, lê a planilha
e preenche o diário de classe com as aulas e presenças de
alunos.

    lista_de_alunos.py -u usuario CodigoTurma > arquivo.csv

Obtém a lista de alunos, no formato CSV separado por tabulação,
com o RA na primeira coluna e o nome na segunda coluna.

    lista_de_presenca.py -l "Descrição da turma" -p {a4,a3} -o lista.pdf \
                         [-d "data"] < arquivo.csv

Gera uma lista de presença, no formato PDF, para os alunos
assinarem a partir do arquivo CSV. Se o parâmetro data não
for fornecido, será impressa a data atual.

Instalação
----

    pip install mechanize beautifulsoup reportlab odfpy
