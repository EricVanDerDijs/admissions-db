import sqlite3
import hashlib, binascii, os
from .init_script import init_db

class Database:
  def __init__(self, db_file, *, initialize = False):
    self.connection = sqlite3.connect(db_file)
    self.connection.row_factory = sqlite3.Row
    with self.connection:
      self.connection.execute("PRAGMA foreign_keys = 1")
    if initialize == 'True':
      init_db(self.connection)
    

  async def handleGenericQuery(self, reqHeader, reqBody):
    query = reqBody.get('query')
    values = reqBody.get('values')
    body = {}
    header = {}

    if isinstance(query, str):
      try:
        with self.connection:
          cursor = self.connection.cursor()

          if isinstance(values, list):
            cursor.execute(query, tuple(values))
          else:
            cursor.execute(query)
          
          rows = cursor.fetchall()
          columns = []
          if len(rows) > 0:
            columns = rows[0].keys()
          results = self.formatListOfResults(columns, rows)
          body = { 'results': results }
          header = { **reqHeader, 'code': 200 }
      except Exception as e:
        body = { 'error_code': 'database-error', 'error': repr(e) }
        header = { **reqHeader, 'code': 500 }

    else:
      body = { 'error_code': 'no-query' }
      header = { **reqHeader, 'code': 400 }
    
    return header, body

  async def handleFetchOneQuery(self, reqHeader, reqBody):
    query = reqBody.get('query')
    values = reqBody.get('values')
    body = {}
    header = {}

    if isinstance(query, str):
      try:
        with self.connection:
          cursor = self.connection.cursor()

          if isinstance(values, list):
            cursor.execute(query, tuple(values))
          else:
            cursor.execute(query)
          
          row = cursor.fetchone()
          if row:
            columns = row.keys()
            body = { 'results': [ self.formatResult(columns, row) ] }
            header = { **reqHeader, 'code': 200 }
          else:
            body = { 'results': [] }
            header = { **reqHeader, 'code': 200 }
      except Exception as e:
        body = { 'error_code': 'database-error', 'error': repr(e) }
        header = { **reqHeader, 'code': 500 }

    else:
      body = { 'error_code': 'no-query' }
      header = { **reqHeader, 'code': 400 }
    
    return header, body

  async def handleFetchManyQuery(self, reqHeader, reqBody):
    query = reqBody.get('query')
    numOfRows = reqBody.get('numOfRows')
    values = reqBody.get('values')
    body = {}
    header = {}

    if isinstance(query, str) and isinstance(numOfRows, str):
      try:
        with self.connection:
          cursor = self.connection.cursor()

          if isinstance(values, list):
            cursor.execute(query, tuple(values))
          else:
            cursor.execute(query)
          
          rows = cursor.fetchall()
          columns = []
          if len(rows) > 0:
            columns = rows[0].keys()
          results = self.formatListOfResults(columns, rows)
          body = { 'results': results }
          header = { **reqHeader, 'code': 200 }
      except Exception as e:
        body = { 'error_code': 'database-error', 'error': repr(e) }
        header = { **reqHeader, 'code': 500 }

    else:
      if query is None:
        body = { 'error_code': 'no-query' }
      elif numOfRows is None:
        body = { 'error_code': 'no-specific-num-of-rows' }
      
      header = { **reqHeader, 'code': 400 }
    
    return header, body
  
  def formatListOfResults(self, columns, rows):
    list_of_results = [self.formatResult(columns, row) for row in rows]
    return list_of_results

  def formatResult(self, columns, row):
    result = {}
    for column_index, column_name in enumerate(columns):
      result[column_name] = row[column_index]
    return result


      


