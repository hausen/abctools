#!/usr/bin/python
# -*- coding: utf-8 -*-
from PortalDoProfessor import PortalDoProfessor, \
                              PasswordException
from getpass import getpass, getuser
import sys
import getopt

reload(sys)
sys.setdefaultencoding("utf-8")

usuario = getuser()

def parseOpts(opts):
  global usuario

  for opt, arg in opts:
    if opt in ("-u", "--user"):
      usuario = arg

try:
  opts, args = getopt.getopt(sys.argv[1:], "u:", ["user="])
  parseOpts(opts)
  codigoTurma = args[0]
except (IndexError, getopt.GetoptError):
  sys.stderr.write("Uso: %s [-u usuario] CodigoTurma\n" % sys.argv[0])
  sys.stderr.write("     CodigoTurma deve ser o código como aparece no portal.\n");
  sys.stderr.write("     Ex. NBBC1499SA.\n");
  exit(1)

try:
  portal = PortalDoProfessor(usuario, getpass("senha: "))
  turma = portal.getTurma(codigoTurma)
  if turma is not None:
    for aluno in sorted(turma.alunos.values(), key=lambda al:al.nome):
      print aluno.ra + "\t" + aluno.nome
  else:
    sys.stderr.write("Turma %s inexistente.\n" % codigoTurma)
    exit(1)
except PasswordException:
  sys.stderr.write("Senha incorreta ou usuário %s inexistente.\n" %
                   usuario)
  exit(2)
except:
  sys.stderr.write("Não pude fazer login no portal.\n")
  exit(3)


