#!/usr/bin/python
# -*- coding: utf-8 -*-
from PortalDoProfessor import PortalDoProfessor, \
                              PasswordException
from getpass import getpass, getuser
from ConceitosPresencasFromODS import ConceitosPresencasFromODS
import sys, traceback
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
#  traceback.print_exc(file=sys.stdout)
  exit(1)

portal = None
try:
  portal = PortalDoProfessor(usuario, getpass("senha: "))

  turmas = portal.getTurmas(codigoTurma)

  try:
    portal.lancaConceitosFaltas(cp.conceitos, cp.faltas, turmas[0])
  except:
    print >> sys.stderr, "ERRO: conceitos da turma " + codigoTurma + \
                         " podem não ter sido lançados!"
    traceback.print_exc(file=sys.stdout)

  portal.logout()
except KeyError:
  sys.stderr.write("Turma %s inexistente.\n" % codigoTurma)
  exit(1)
except PasswordException:
  print >> sys.stderr, "Senha incorreta ou usuário %s inexistente." % usuario
finally:
  if portal is not None:
    portal.logout()
    sys.stderr.write("logged out.\n")
