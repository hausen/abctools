# -*- coding: utf-8 -*-
import unicodedata,re
from string import maketrans

whitespaceRegex = re.compile(r"\s+")
otherCharsRegex = re.compile("[^a-z0-9 ]")

def stripAccents(s):
  return ''.join((c for c in unicodedata.normalize('NFD', s)
                  if unicodedata.category(c) != 'Mn'))

def strNormalize(s):
  if not isinstance(s, unicode):
    s = str(s)
    s = unicode(s.decode('utf-8'))
  s = str(stripAccents(s))
  s = s.lower().strip()
  s = otherCharsRegex.sub(" ", s)
  s = whitespaceRegex.sub(" ", s)
  return s

def strDateCanonicalize(s):
  if not isinstance(s,str):
    s = str(s)
  parts = s.split("/")
  day, month = int(parts[0]), int(parts[1])
  return str(day) + "/" + str(month)

if __name__ == "__main__":
  print strNormalize(" This ìs höw it's    done, baby!   ")
