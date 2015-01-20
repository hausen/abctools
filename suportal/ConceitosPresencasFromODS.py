# -*- coding: utf-8 -*-

# reference
# https://github.com/marcoconti83/read-ods-with-odfpy/blob/master/odf-to-array.py
import sys,getopt,re
from ODSReader import ODSReader
from libportal import strNormalize, strDateCanonicalize

from Aula import TipoAula, Aula

class ConceitosPresencasFromODS:
  def __init__(self,inputfile):
    self.conceitos = {}
    self.faltas = {}
    self.aulas = {}

    spreadsheetdoc = ODSReader(inputfile)
    sheetConceitos = getSheetConceitos(spreadsheetdoc)
    sheetPresencas = getSheetPresencas(spreadsheetdoc)
    sheetPlanoDeAulas = getSheetPlanoDeAulas(spreadsheetdoc)
    associateSheets(conceitos=sheetConceitos, presencas=sheetPresencas,
                    plano=sheetPlanoDeAulas)

    self.conceitos, self.faltas = getConceitosFaltas(sheetConceitos)

    if sheetPresencas.planoDeAulas is not None:
      iterSheet = iter(sheetPresencas.planoDeAulas.iteritems())
      for data, aula in iterSheet:
        self.aulas[strDateCanonicalize(data)] = aula

    iterSheet = iter(sheetPresencas)
    next(iterSheet)
    rowNumber = 1
    for row in iterSheet:
      ++rowNumber
      ra = 0
      try:
        ra = int(row.get('ra', 0))
      except ValueError:
        pass
      if ra == 0:
        continue
      for data, idxData in sheetPresencas.idxData.iteritems():
        data = strDateCanonicalize(data)
        if data not in self.aulas:
          self.aulas[data] = Aula(dia = data.strip('/')[0],
                                  mes = data.strip('/')[1],
                                  ano = sheetPlanoDeAulas.ano)
        presenca = str(row.get(idxData, '')).strip().lower()
        if presenca == 'p' or presenca == '1':
          self.aulas[data].mapRAPresencas[ra] = True
        elif presenca == 'f' or presenca == '--' or \
             presenca == '-' or presenca == '0':
          self.aulas[data].mapRAPresencas[ra] = False
        else:
          #print >> sys.stderr, \
          #  "Presença não registrada para a data %s, ra %d" % (data,ra)
          self.aulas[data].mapRAPresencas[ra] = None

  def getRAFromConceitos(self):
    return self.conceitos.keys()

  def getAulas(self):
    return self.aulas

  def getAula(self, data):
    try:
      return self.aulas[strDateCanonicalize(data)]
    except IndexError:
      return None

  def getConceitoFaltas(self, ra):
    try:
      return self.conceitos[int(ra)], self.faltas[int(ra)]
    except (IndexError, ValueError):
      return None

def findSheet(doc, *names):
  tmpMap = dict( (strNormalize(k), v) for k, v in doc.SHEETS.iteritems() )
  for name in names:
    sheet = tmpMap.get(name, None)
    if sheet is not None:
      return sheet
  return None

def getSheetConceitos(spreadsheetdoc):
  sheet = findSheet(spreadsheetdoc, "conceitos", "conceito")
  if sheet is None:
    return None
  sheet.setNamedRows()

  try:
    sheet.idxRA = sheet.cols.getIndex('ra')
    sheet.idxConceito = sheet.cols.getIndex('conceito')
    sheet.idxFaltas = sheet.cols.getIndex('faltas')
  except ValueError:
    return None

  return sheet

def getSheetPresencas(spreadsheetdoc):
  sheet = findSheet(spreadsheetdoc, "presencas", "presenca")
  if sheet is None:
    return None
  sheet.setNamedRows()

  datePattern = re.compile('^[0-9]+\/[0-9]+(\/[0-9]+)?$')

  try:
    sheet.idxRA = sheet.cols.getIndex('ra')
    sheet.idxData = sheet.cols.getIndices(regex=datePattern)
  except ValueError:
    return None
  return sheet

# Faz o parse da tabela "aulas" (ou "aula," ou "plano de aulas," ou
# "diário," ou "diário de classe") que descreve o plano de aulas
# do curso.
# Esta tabela deve ter uma coluna "data" (ou "dia"), uma coluna
# "hora inicial" (ou "inicio" ou "hora") e uma coluna "horas aula"
# (ou "horas de aula" ou "horas").
# Colunas opcionais:
# - "notas de aula", uma string descrevendo a aula
# - "tipo", em { "téorica", "prática", "prova", "revisão", "exame" }
def getSheetPlanoDeAulas(spreadsheetdoc):
  sheet = findSheet(spreadsheetdoc, "aulas", "aula", "plano de aulas",
                                    "plano", "diario", "diario de classe")
  if sheet is None:
    return None
  sheet.setNamedRows()
  sheet.addAlias('data', 'dia')
  sheet.addAlias('hora inicial', 'hora inicio', 'inicio', 'hora')
  sheet.addAlias('horas aula', 'horas de aula', 'horas')
  sheet.addAlias('notas aula', 'notas de aula', 'notas da aula',
                 'notas', 'aula')
  sheet.addAlias('tipo', 'tipo de aula', 'tipo da aula')

  try:
    sheet.idxData = sheet.cols.getIndex('data')
    sheet.idxHoraInicial = sheet.cols.getOptionalIndex('hora inicial')
    sheet.idxHorasAula = sheet.cols.getOptionalIndex('horas aula')
    sheet.idxNotasAula = sheet.cols.getOptionalIndex('notas aula')
    sheet.idxTipo = sheet.cols.getOptionalIndex('tipo')
  except ValueError:
    return None
  return sheet

def matches(presencas, plano):
  for date in presencas.idxData.keys():
    if strDateCanonicalize(date) not in plano:
      return False
  return True

def associateSheets(conceitos, presencas, plano):
  plano.ano = None

  planoDeAulas = {}
  iterSheet = iter(plano)
  next(iterSheet)
  rownumber = 0
  for row in iterSheet:
    rownumber += 1

    data = row.get('data', None)
    if data is None:
      continue
    dia, mes, ano = parseData(data)
    if plano.ano is None and ano is not None:
      plano.ano = ano
    if ano is None:
      ano = plano.ano

    notasDeAula = row.get('notas de aula', default="Aula %02d" % rownumber)
    tipo = row.get('tipo', None)
    horaInicial = row.get('hora inicial', '00:00')
    horasAula = row.get('horas aula', 1)
    planoDeAulas[strDateCanonicalize(data)] = Aula(dia = dia, mes = mes,
                                                   ano = ano,
                                                   descricao = notasDeAula,
                                                   tipo = tipo,
                                                   horaInicial = horaInicial,
                                                   horasAula = horasAula)
  # end for row in iterSheet:

  if matches(presencas, planoDeAulas):
    presencas.planoDeAulas = planoDeAulas
  else:
    presencas.planoDeAulas = None
    print >> sys.stderr, "Plano de Aulas e Presenças não combinam!"
# end def associateSheets(conceitos, presencas, plano):

def parseData(data):
  dia, mes, ano = None, None, None
  d = data.split('/')
  if len(d) > 1:
    dia = int(d[0])
    mes = int(d[1])
  if len(d) > 2:
    ano = int(d[2])
  return dia, mes, ano

def getConceitosFaltas(sheet):
  conceitos = {}
  faltas = {}

  iterSheet = iter(sheet)
  next(iterSheet)
  for row in iterSheet:
    try:
      ra = int(row['ra'])
      conceito = row['conceito']
      falt = int(row['faltas'])
      conceitos[ra] = conceito
      faltas[ra] = falt
    except (IndexError, ValueError):
      pass

  return conceitos, faltas

def usage():
   sys.stderr.write("Usage: %s inputfile\n" % sys.argv[0])

if __name__ == "__main__":
  try:
    opts, args = getopt.getopt(sys.argv[1:], "o:", ["output="])
  except getopt.GetoptError:
    usage()
    sys.exit(2)
  
  if len(args) != 1:
    usage()
    sys.exit(2)

  inputfile = args[0]
  
  cp = ConceitosPresencasFromODS(inputfile)
  
  for ra in sorted(cp.getRAFromConceitos()):
    conceito, faltas = cp.getConceitoFaltas(ra)
    print "%s %s %s" % (ra, conceito, faltas)

  for aula in sorted( cp.getAulas().values() ):
    print "%s %d %s" % (repr(aula), aula.tipo, str(aula))
    x = str(aula).decode('utf-8').encode('latin-1', 'ignore')
    print x
