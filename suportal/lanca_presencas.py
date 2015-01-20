#!/usr/bin/python
# -*- coding: utf-8 -*-
from PortalDoProfessor import PortalDoProfessor, \
                              PasswordException
from getpass import getpass, getuser
from ConceitosPresencasFromODS import ConceitosPresencasFromODS
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
  codigoTurma, nomeArq = args[0], args[1]
except (IndexError, getopt.GetoptError):
  sys.stderr.write("Uso: %s [-u usuario] CodigoTurma Planilha.ods\n" % sys.argv[0])
  sys.stderr.write("     CodigoTurma deve ser o código como aparece no portal.\n");
  sys.stderr.write("     Ex. NBBC1499SA.\n");
  exit(1)

try:
  cp = ConceitosPresencasFromODS(nomeArq)
except:
  sys.stderr.write("Erro ao ler %s.\n" % nomeArq)
  sys.stderr.write("Tem certeza de que é uma planilha do OpenOffice?\n")
  exit(1)

portal = PortalDoProfessor()
portal.debug = True
try:
  portal.login(usuario, getpass("senha: "))

  turma = portal.getTurma(codigoTurma)

  for aula in cp.aulas.values():
    print "lançando aula " + repr(aula)
    try:
      portal.lancaAula(aula, turma)
    except:
      print >> sys.stderr, "ERRO: aula " + repr(aula) + " pode não " + \
                           "ter sido lançada!"

  portal.logout()
except PasswordException:
  print >> sys.stderr, "Senha incorreta ou usuário " + usuario + \
                       " inexistente"
