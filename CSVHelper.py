import xml.etree.cElementTree as ET
import csv
import os
import re


class CSVHelper():
    
  def __init__(self, filename):
      self.filename = filename

  def get_requested_knums(self):
    knum_list = []
    # encoding = 'utf-8-sig',
    with open("./{}.csv".format(self.filename[:-4]), 'r', newline='') as f:
      reader = csv.reader(f)
      for row in reader: knum_list.append(row[0])
      if len(knum_list) > 200: raise ValueError
    return knum_list

  def get_requested_queries(self):
    queries = []
    # encoding = 'utf-8-sig',
    with open("./{}.csv".format(self.filename[:-4]), 'r', newline='') as f:
      reader = csv.reader(f)
      for row in reader: queries.append(row[1])
      if len(queries) > 200: raise ValueError
    return queries[1:]

  def get_requested_knums_string(self):
    return ';'.join(self.get_requested_knums())

  def writeQueriesToCSV(self, d):
    with open('ParsedQueries.csv', 'w', newline='') as f:
      fieldnames = ['Kadastrovy nomer', 'Nomer Zaprosa']
      writer = csv.DictWriter(f, fieldnames=fieldnames)
      writer.writeheader()

      for k,v in d.items(): writer.writerow({fieldnames[0]: k, fieldnames[1]: v})
            
      
      
      
    
    
       