# -*- coding: utf-8 -*-
# to use this, you must set utf-8 encoding for your system
# add the following to the main file:
#   import sys
#   reload(sys)
#   sys.setdefaultencoding("utf-8")
 
from BeautifulSoup import BeautifulSoup
import cookielib 
import mechanize
import re
import sys, traceback 
import urllib2
from Aula import TipoAula, Aula
from Aluno import Aluno
from Turma import Turma
from libportal import strDateCanonicalize

class PortalDoProfessor:
  PORTAL_BASE_HREF="http://portal.ufabc.edu.br:8080/professor/"
  PORTAL_ENCODING="ISO-8859-1"
  CONCEITOS = {
    'A': '11',
    'a': '11',
    'B': '12',
    'b': '12',
    'C': '13',
    'c': '13',
    'D': '14',
    'd': '14',
    'F': '15',
    'f': '15',
    'O': '16',
    'o': '16',
    'I': '18',
    'i': '18'
  }

  def __init__(self, username=None, password=None):
    self.debug = False
    self.username = None
    self.br = mechanize.Browser()
    self.cookiejar = cookielib.LWPCookieJar()
    self.turmas = None

    self.setup()
    if password is not None:
      self.login(username, password)

  def setup(self):
    self.br.set_cookiejar( self.cookiejar ) 
    self.br.set_handle_equiv( True ) 
    #self.br.set_handle_gzip( True ) 
    self.br.set_handle_redirect( True ) 
    self.br.set_handle_referer( True ) 
    self.br.set_handle_robots( False )
    self.br.set_handle_refresh( mechanize._http.HTTPRefreshProcessor(),
                                max_time = 1 )
    self.br.addheaders = [ ( 'User-agent', 'Mozilla/5.0 (X11; U; '
                             'Linux i686; en-US; rv:1.9.0.1) '
                             'Gecko/2008071615 Fedora/3.0.1-1.fc9 '
                             'Firefox/3.0.1' ) ] 

  def login(self, username, password):
    self.username = username
    response = self.br.open(PortalDoProfessor.PORTAL_BASE_HREF + "index.html")
    self.br.form = list(self.br.forms())[0]
    self.br["j_username"] = username
    self.br["j_password"] = password
    if self.debug:
      print >> sys.stderr, "attempting to sign in as " + username
    response = self.br.submit()
    if response.geturl() == PortalDoProfessor.PORTAL_BASE_HREF + \
    "j_security_check":
      raise PasswordException()
    if response.geturl() != PortalDoProfessor.PORTAL_BASE_HREF + "index.html":
      raise Exception("sign-in error")

  def logout(self):
    if self.username is not None:
      self.br.open(PortalDoProfessor.PORTAL_BASE_HREF + "logout.html")
      if self.debug:
        print >> sys.stderr, self.username + " signed off"
      self.username = None

  def loadTurmas(self):
    self.br.open(PortalDoProfessor.PORTAL_BASE_HREF +
                 "diario/turmas.html?todas=1");
    self.turmas = []
    for link in self.br.links(url_regex="turma.html"):
      codigo = link.text
      idturma = link.url.split("=")[1]
      turma = Turma(codigo, idturma)
      turma.linkLancarNova = None
      turma.linksLancarAula = None
      self.turmas.append(turma)

  def getTurmas(self, codigo):
    if self.turmas is None:
      self.loadTurmas()

    turmas = []

    for turma in self.turmas:
      if codigo == turma.codigo:
        turmas.append(turma)
        if turma.alunos is None:
          self.carregaDadosTurma(turma)

    if not turmas:
      raise KeyError("Código de turma inexistente")

    return turmas

  def carregaDadosTurma(self, turma):
    response = self.br.open(PortalDoProfessor.PORTAL_BASE_HREF +
                 "diario/faltas.html?turma=" + turma.idturma)
    html = response.read()
    tree = BeautifulSoup(html, fromEncoding = 
                               PortalDoProfessor.PORTAL_ENCODING)

    lines = tree.findAll(id="Turma")[0].table('tr')
    turma.disciplina = lines[1].td.contents[0].strip()
    turma.periodo = lines[2].td.contents[0].strip()
    turma.carga = re.sub(r"\s+", " ", lines[3]('td')[1].contents[0].strip())

    alunos = tree.findAll("td", { "class":"aluno" })
    turma.alunos = {}
    for aluno in alunos:
      ra = aluno('span')[1].contents[0].strip().strip('()')
      nome = aluno('span')[0].label.contents[0].strip()
      idaluno = aluno('span')[0].label['for'].split('_')[1]
      curso = aluno('span')[2].contents[0].strip()
      novoAluno = Aluno(ra, nome=nome, idaluno=idaluno,
                        turma=turma, curso=curso)
      turma.alunos[ra] = novoAluno        

  def lancaConceito(self, idaluno, conceitos, turma, control):
    for ra, aluno in turma.alunos.iteritems():
      ra = int(ra)
      if (aluno.idaluno == idaluno):
        #print >> sys.stderr, "Aluno %s (%d) tem conceito %s" % \
        #                     (aluno.nome, ra, conceitos[ra].upper())
        control.get(PortalDoProfessor.CONCEITOS[conceitos[ra]]).selected = True
        return
    print >> sys.stderr, idaluno
    raise Exception()

  def lancaFaltas(self, idaluno, faltas, turma, control):
    for ra, aluno in turma.alunos.iteritems():
      ra = int(ra)
      if (aluno.idaluno == idaluno):
        #print >> sys.stderr, "Aluno %s (%d) faltou %d horas" % \
        #                     (aluno.nome, ra, faltas[ra])
        control.value = str(faltas[ra])
        return
    raise Exception()

  def lancaConceitosFaltas(self, conceitos, faltas, turma):
    response = self.br.open(PortalDoProfessor.PORTAL_BASE_HREF +
                            "notas/formulario.html?turma=" + turma.idturma)
    self.br.form = list(self.br.forms())[0]
    naolancou = []

    for control in self.br.form.controls:
      parts = control.name.split('.')
      if len(parts) != 3 or (parts[0] != 'nota' and parts[0] != 'faltas'):
        continue
      idaluno = parts[1]
      try:
        if parts[0] == 'nota':
          self.lancaConceito(idaluno, conceitos, turma, control)
        else:
          self.lancaFaltas(idaluno, faltas, turma, control)
      except:
        #traceback.print_exc(file=sys.stdout)
        naolancou.append(idaluno)

    if naolancou:
      print >> sys.stderr, "AVISO: %d alunos não lançados na turma %s." % \
                           (len(naolancou)/2, turma.codigo)
    response = self.br.submit()

  def lancaAula(self, aula, turma):
    if turma.linkLancarNova is None:
      self.br.open(PortalDoProfessor.PORTAL_BASE_HREF +
                   "diario/turma.html?turma=" + turma.idturma)
      self.rereadLinksDiario(turma)
    if turma.linkLancarNova is None:
      print >> sys.stderr, "Não posso lançar aula para turma " + \
                           turma.codigo
      return False
    date = strDateCanonicalize(repr(aula))
    links = turma.linksLancarAula.get(date, None)
    if links is None:
      horasAula = aula.horasAula if aula.horasAula else 1
      return self.lancaAulaComLink(aula, turma,
                                   turma.linkLancarNova,
                                   aula.hora(),
                                   horasAula)
    else:
      try:
        for link in links:
          data, horaInicio = link.text.split(" ")
          return self.lancaAulaComLink(aula, turma, link, horaInicio, 1)
      except urllib2.HTTPError:
        print >> sys.stderr, "ERRO: problema ao mudar aula " + repr(aula)
        print >> sys.stderr, "      vou tentar deletar a aula e inseri-la novamente"
        for link in links:
          print >> sys.stderr, "      deletando " + link.text
          self.deletaAulaComLink(link, turma)
        print >> sys.stderr, "      inserindo aula"
        horasAula = aula.horasAula if aula.horasAula else 1
        return self.lancaAulaComLink(aula, turma,
                                     turma.linkLancarNova,
                                     aula.hora(),
                                     horasAula)
      return True

  def lancaAulaComLink(self, aula, turma, link, horaInicio, horasAula):
    sempresenca = []
    response = self.br.open(link.url)
    self.br.form = list(self.br.forms())[0]
    self.br['data'] = aula.data()
    self.br['hora'] = horaInicio
    self.br['quantidadeHorasAula'] = [str(horasAula)]
    self.br['tipoAula'] = [str(aula.tipo)]
    obs = str(aula)
    if sys.getdefaultencoding() != PortalDoProfessor.PORTAL_ENCODING:
      obs = obs.decode(sys.getdefaultencoding())
      obs = obs.encode(PortalDoProfessor.PORTAL_ENCODING, 'ignore')
    self.br['observacoes'] = obs
    for ra, aluno in turma.alunos.iteritems():
      ra = int(ra)
      idaluno = int(aluno.idaluno)
      hora = 0
      while hora < horasAula:
        cb = self.br.find_control("presente" + str(hora)).get(str(idaluno))
        if aula.presente(ra) is True:
          cb.selected = True
        elif aula.presente(ra) is False:
          cb.selected = False
        else:
          cb.selected = True
          sempresenca.append(ra)
        hora += 1
    #log = open("/tmp/portal.log", "w")
    response = self.br.submit()
    if sempresenca:
      print >> sys.stderr, "aviso: %s alunos sem presença na aula %s." \
                           + " marcados como presentes" % \
                           (str(len(sempresenca)), str(repr(aula)))
    #log.write(response.read())
    #log.close()
    self.rereadLinksDiario(turma)

  def deletaAulaComLink(self, link, turma):
    response = self.br.open(link.url)
    self.br.form = list(self.br.forms())[0]
    response = self.br.submit(nr=1)
    self.rereadLinksDiario(turma)

  def rereadLinksDiario(self, turma):
    turma.linkLancarNova = None
    turma.linksLancarAula = {}
    regexLancarNova = re.compile(r"\?turma=[0-9]+$")
    for link in self.br.links(url_regex="formulario.html"):
      if regexLancarNova.search(link.url):
        turma.linkLancarNova = link
      else:
        date = strDateCanonicalize(link.text)
        linksLancarAula = turma.linksLancarAula.get(date, [])
        linksLancarAula.append(link)
        turma.linksLancarAula[date] = linksLancarAula 

class PasswordException(Exception):
  def __init__(self):
    super(PasswordException, self).__init__("wrong username or password")
