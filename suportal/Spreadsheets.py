from libportal import strNormalize

###########################################################
class ColumnMap:
  def __init__(self, row):
    self._cols = row
    self._map = {}
    for idx, name in enumerate(row):
      name = strNormalize(name)
      self._map[name] = idx

  def addAlias(self, name, *aliases):
    name = strNormalize(name)
    idx = self._map.get(name, None)
    if idx is None:
      for alias in aliases:
        alias = strNormalize(alias)
        idx = self._map.get(alias, None)
        if idx is not None:
          self._map[name] = idx
          break
    if idx is not None:
      for alias in aliases:
        alias = strNormalize(alias)
        self._map[alias] = idx
      return True
    else:
      return False

  def getOptionalIndex(self, name):
    return self._map.get(strNormalize(name), None)

  def getIndex(self, name):
    index = self.getOptionalIndex(name)
    if index is None:
      raise IndexError()
    return index

  def getOptionalIndices(self, regex):
    indices = {}
    for idx, col in enumerate(self._cols):
      if regex.match(col):
        indices[col] = idx
    return indices

  def getIndices(self, regex):
    indices = self.getOptionalIndices(regex)
    if not indices:
      raise IndexError()
    return indices

###########################################################
class Row:
  def __init__(self, row, columnMap = None):
    self.row = row
    self.columnMap = columnMap

  def get(self, index, default=None):
    if not isinstance(index, int):
      index = self.columnMap.getOptionalIndex(index)
      if index is None:
        return default
    if index < len(self.row):
      return self.row[index]
    else:
      return default

  def __getitem__(self, index):
    if not isinstance(index, int):
      index = self.columnMap.getIndex(index)
    return self.row[index]

  def __str__(self):
    return str(self.row)

  def __len__(self):
    return len(self.row)

###########################################################
class RowIterator:
  def __init__(self, rows, columnMap = None):
    self.rows = rows
    self.columnMap = columnMap
    self.it = iter(self.rows)

  def __iter__(self):
    return self

  def next(self):
    return Row(next(self.it), self.columnMap)

###########################################################
class Sheet:
  def __init__(self, name, rows, namedRows=False):
    self.name = name
    self.rows = rows
    self.cols = None
    if namedRows:
      self.setNamedRows()

  def setNamedRows(self):
    self.cols = ColumnMap(self.rows[0])

  def addAlias(self, name, *aliases):
    self.cols.addAlias(name, *aliases)

  def __getitem__(self, index):
    return self.rows[index]

  def __iter__(self):
    return RowIterator(self.rows, self.cols)

###########################################################
# test
if __name__ == "__main__":
  rows = [ ['X', 'y', 'z' ],
           [  1,   2,   3 ],
           [  4 ],
           [  7,   8,   9 ] ]
  sheet = Sheet('test', rows)
  sheet.setNamedRows()
  sheet.addAlias('x', 'ex')
  sheet.addAlias('Yes', 'y', 'bla')
  for row in sheet:
    print row.get('Yes', None)
