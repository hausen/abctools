#!/usr/bin/env python
# -*- coding: utf-8 -*-
from reportlab.pdfgen import canvas
from reportlab.lib.units import cm, inch
from reportlab.lib.pagesizes import A3, A4
import datetime, fileinput, getopt, locale, re, sys

reload(sys)
sys.setdefaultencoding("utf-8")
locale.setlocale(locale.LC_ALL, "pt_BR.utf8")

class Margins:
  def __init__(self, left, right, top, bottom):
    self.left = left
    self.right = right
    self.top = top
    self.bottom = bottom

# fontSize in pt
def newPdfCanvas(fileName = sys.stdout, pageSize = A4,
                 fontFamily = "Helvetica", fontSize = 12,
                 marginLeft = 1.0*cm, marginRight = 1.0*cm,
                 marginTop = 1.85*cm, marginBottom = 1.85*cm):
  p = canvas.Canvas(fileName, pagesize = pageSize)
  p.pageNumber = 1
  p.totalPages = 0
  p.pageWidth = pageSize[0]
  p.pageHeight = pageSize[1]
  p.fontFamily = fontFamily
  p.fontSize = fontSize
  p.margin = Margins(marginLeft, marginRight, marginTop, marginBottom)
  return p

def drawHeader(p, left = "", center = "", right = ""):
  headerBottom = p.pageHeight - p.margin.top
  pageCenter = (p.margin.left + p.pageWidth - p.margin.right)/2
  # left example: "Turma A — Noturno"
  p.drawString(p.margin.left, headerBottom + 2*p.fontSize, left)
  # center example: "Funções de Uma Variável"
  p.drawCentredString(pageCenter, headerBottom + 2*p.fontSize, center)
  p.drawRightString(p.pageWidth - p.margin.right,
                    headerBottom + 2*p.fontSize, right)
  p.drawString(p.margin.left + .2*cm, headerBottom + p.fontSize/3, "RA")
  p.drawString(p.margin.left + 6*p.fontSize, headerBottom + p.fontSize/3,
               "Nome")
  p.drawString(pageCenter, headerBottom + p.fontSize/3, "Assinatura")

def drawFooter(p, center = ""):
  pageCenter = (p.margin.left + p.pageWidth - p.margin.right)/2
  footerTop = p.margin.bottom - 1.2*p.fontSize
  p.drawCentredString(pageCenter, footerTop, center) 
  footerTop -= 1.6*p.fontSize #aqui
  p.drawCentredString(pageCenter, footerTop, 
                      "Página %d/%d" % (p.pageNumber, p.totalPages))

def drawPage(p, students, headerLeft = "", headerCenter = "",
             date = None, footer = None, paginateOnly = False):
  p.setLineWidth(.3)
  p.setFont(p.fontFamily, p.fontSize)
  maxRowHeight = 1.5*cm
  minRowHeight = 0.74*cm

  if date is None:
    date = datetime.date.today().strftime("%d/%m/%Y")

  if footer is None:
    footer = "Se o seu nome não estiver na lista, " + \
             "não o adicione! Fale com o professor ao final da aula."

  studentsLeft = []

  diffWidth = p.pageWidth - A4[0]
  if diffWidth > 0:
    if p.pageNumber % 2 == 1:
      p.margin.right += diffWidth
    else:
      p.margin.left += diffWidth

  if len(students) > 0:
    textHeight = p.pageHeight - p.margin.top - p.margin.bottom
    rowHeight = textHeight/len(students)
    if rowHeight > maxRowHeight:
      rowHeight = maxRowHeight
    elif rowHeight < minRowHeight:
      numStudents = int(textHeight/minRowHeight)
      rowHeight = textHeight/numStudents
      if numStudents < len(students):
        studentsLeft = students[numStudents:]
        students = students[:numStudents]

    pos = textHeight + p.margin.bottom

    if not paginateOnly:
      p.line(p.margin.left, pos, p.pageWidth - p.margin.right, pos)

    raiseText = (rowHeight - 0.7*p.fontSize)/2

    if not paginateOnly:
      for student in students:
        (ra,nome) = student
        pos -= rowHeight
        p.drawString(p.margin.left + .2*cm, pos+raiseText, "%08d" % ra)
        p.drawString(p.margin.left + 6*p.fontSize, pos+raiseText, nome)
        p.line(p.margin.left, pos, p.pageWidth - p.margin.right, pos)
        p.line(p.margin.left, pos, p.margin.left, pos + rowHeight)
        p.line(p.pageWidth - p.margin.right, pos,
               p.pageWidth - p.margin.right, pos + rowHeight)

      drawHeader(p, left = headerLeft,
                    center = headerCenter,
                    right = date)
      drawFooter(p, center = footer)

  if diffWidth > 0:
    if p.pageNumber % 2 == 1:
      p.margin.right -= diffWidth
      if not paginateOnly:
        p.line(A4[0], 0, A4[0], p.pageHeight)
    else:
      p.margin.left -= diffWidth
      if not paginateOnly:
        p.line(p.pageWidth-A4[0], 0, p.pageWidth-A4[0], p.pageHeight)

  if not paginateOnly:
    p.showPage()
  p.pageNumber += 1

  return studentsLeft

def makePdf(students, headerLeft = "", headerCenter = "",
            date = None, footer = None, fileName = sys.stdout,
            fontFamily = None, pageSize = A4):
  headerLeft = headerLeft.replace(" -- ", " – ")
  headerCenter = headerCenter.replace(" -- ", " – ")

  p = newPdfCanvas(fileName, pageSize = pageSize)

  if fontFamily is not None:
    p.fontFamily = fontFamily

  studentsCopy = students
  studentsInPage = []
  
  while len(studentsCopy) > 0:
    studentsCopy2 = drawPage(p, studentsCopy, paginateOnly = True)
    studentsInPage.append(len(studentsCopy)-len(studentsCopy2))
    studentsCopy = studentsCopy2
  
  p.totalPages = p.pageNumber-1
  p.pageNumber = 1
  
  if p.totalPages == 1:
    drawPage(p,students, headerLeft = headerLeft,
             headerCenter = headerCenter, date = date, footer = footer)
  else:
    if studentsInPage[-1] < studentsInPage[0]-1:
    # distribute students more equitably
      studentsPerPage = int(len(students)/p.totalPages)
      total = studentsPerPage*p.totalPages
      for i in range(0,len(studentsInPage)):
        if total < len(students):
          studentsInPage[i] = studentsPerPage+1
          total += 1
        else:
          studentsInPage[i] = studentsPerPage

    low = 0
    for inPage in studentsInPage:
      high = min(low + inPage,len(students))
      drawPage(p, students[low:high], headerLeft = headerLeft,
               headerCenter = headerCenter, date = date, footer = footer)
      low = high
  
  p.save()

def getColumns(line):
  line = line.strip("\r\n")
  cols = line.split("\t")
  if len(cols) < 2:
    cols = line.split(",")
    if len(cols) < 2:
      cols = line.split(";")
  return cols

whiteSpaceRegex = re.compile(r"\s+")
articleRegex = re.compile(" D(a|e|i|o|as|os) ")

def readStudents(infile = sys.stdin, capitalize = True):
  students = []
  colRA = None
  colNome = None
  lineNo = 0

  for line in infile.readlines():
    lineNo += 1
    cols = getColumns(line)
    if len(cols) < 2:
      continue
    if colRA is None:
      try:
        ra = int(cols[0])
        if ra < 10000000:
          raise ValueError()
        nome = cols[1]
      except ValueError:
        for idx,val in enumerate(cols):
          if val.lower() == 'ra':
            colRA = idx
          elif val.lower() == 'nome':
            colNome = idx
        if (colRA is None) ^ (colNome is None):
          raise Exception("Erro na linha %d." % (lineNo))
        continue
    else:
      try:
        ra = int(cols[colRA])
        nome = cols[colNome]
      except ValueError:
        continue
    nome = whiteSpaceRegex.sub(" ", nome.strip())
    orig = nome
    if capitalize:
      nome = articleRegex.sub(r" d\1 ", unicode(nome).title())
    students.append((ra, nome))
  return students

def parsePaper(paper):
  if paper.lower() == 'a4':
    return A4
  elif paper.lower() == 'a3':
    return A3
  else:
    usage(2)

def usage(exitStatus = 0):
  print >> sys.stderr, "Usage: lista.py [-i inputfile] [-o outputfile]"
  print >> sys.stderr, "                [-l header-left] [-c header-center]"
  print >> sys.stderr, "                [-p paper] [-d date] [-f footer]"
  print >> sys.stderr, "                [-t type-face]"
  print >> sys.stderr, "       paper is one of A4 or A3"
  print >> sys.stderr, "       type-face is one of %s" % \
                       canvas.Canvas(sys.stdout).getAvailableFonts()

  sys.exit(exitStatus)

if __name__ == '__main__':
  ifile = sys.stdin
  ofile = sys.stdout
  headerLeft = ""
  headerCenter = ""
  paper = A4
  date = None
  footer = None
  fontFamily = None

  try:
    opts, args = getopt.getopt(sys.argv[1:], "hi:o:l:c:p:d:f:t:",
                               ["ifile=", "ofile=", "header-left=",
                                "header-center=", "paper=", "date=",
                                "footer=", "type-face="])
  except getopt.GetoptError:
    usage(exitStatus = 2)

  for opt, arg in opts:
    if opt == '-h':
      usage()
    elif opt in ("-i", "--ifile"):
      try:
        ifile = open(arg, "r")
      except Exception,e:
        print >> sys.stderr, "Erro ao abrir arquivo: %s" % e.message
        sys.exit(1)
    elif opt in ("-o", "--ofile"):
      ofile = arg
    elif opt in ("-l", "--header-left"):
      headerLeft = arg
    elif opt in ("-c", "--header-center"):
      headerCenter = arg
    elif opt in ("-p", "--paper"):
      paper = parsePaper(arg)
    elif opt in ("-d", "--date"):
      date = arg
    elif opt in ("-f", "--footer"):
      footer = arg
    elif opt in ("-t", "--type-face"):
      fontFamily = arg

  students = readStudents(ifile)
  makePdf(students, headerLeft = headerLeft,
          headerCenter = headerCenter, date = date, footer = footer,
          pageSize = paper, fileName = ofile, fontFamily = fontFamily)
