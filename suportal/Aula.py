# -*- coding: utf-8 -*-
from libportal import strNormalize 
import datetime

class TipoAula:
  TEORICA=1
  PRATICA=2
  PROVA=3
  REVISAO=4
  EXAME=5

# mapRAPresenca must be a mapping ra -> {True,False}
class Aula:
  def __init__(self, dia, mes, ano=None, horaInicial=None, horasAula=None,
               descricao="", tipo=TipoAula.TEORICA, idaula=None):
    self.dia = int(dia)
    self.mes = int(mes)
    self.ano = Aula._parseAno(ano)
    self.horaInicial = Aula._parseHoraInicial(horaInicial)
    self.horasAula = Aula._parseHorasAula(horasAula)
    self.descricao = descricao
    if isinstance(tipo, int):
      self.tipo = tipo
    else:
      self.tipo = Aula._parseTipo(tipo)
    self.idaula = idaula
    self.mapRAPresencas = dict()

  def presente(self,ra):
    if not isinstance(ra,int):
      ra = int(ra)
    return self.mapRAPresencas.get(ra, None)

  def data(self):
    return "%02d/%02d/%04d" % (self.dia, self.mes, self.ano)

  def hora(self):
    return self.horaInicial if self.horaInicial else "00:00"

  def __repr__(self):
    return "%s %s" % (self.data(), self.hora())

  def __str__(self):
    return self.descricao.encode('utf-8')

  def sortableTimeRepr(self):
    hora = self.horaInicial if self.horaInicial else "00:00"
    return "%04d/%02d/%02d %s" % (self.ano, self.mes, self.dia, hora)

  def __cmp__(self, other):
    s = self.sortableTimeRepr()
    o = other.sortableTimeRepr()
    return cmp(s,o)

  @staticmethod
  def _parseAno(ano):
    if ano is None:
      return datetime.date.today().year
    else:
      return int(ano)

  @staticmethod
  def _parseHoraInicial(hora):
    if hora is not None:
      arr = hora.split(":")
      if len(arr) > 1:
        hora = "%02d:%02d" % (int(arr[0]), int(arr[1]))
      else:
        hora = "%02d:00" % int(arr[0])
    return hora

  @staticmethod
  def _parseHorasAula(qtd):
    if qtd is None:
      return None
    else:
      return int(qtd)

  @staticmethod
  def _parseTipo(tipo):
    if tipo is None:
      return TipoAula.TEORICA
    tipo = strNormalize(tipo)
    return {
             'teorica': TipoAula.TEORICA,
             'pratica': TipoAula.PRATICA,
             'prova':   TipoAula.PROVA,
             'revisao': TipoAula.REVISAO,
             'exame':   TipoAula.EXAME
           }.get(tipo, TipoAula.TEORICA) # TEORICA is the default
