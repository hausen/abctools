# -*- coding: utf-8 -*-

class Aluno:
  def __init__(self, ra, nome=None, idaluno=None, turma=None, curso=None):
    self.idaluno = idaluno
    self.ra = ra
    self.nome = nome
    self.turma = turma
    self.curso = curso
    self.conceito = None
    self.horas_falta = None
