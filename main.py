from WebDriver import Driver
from Pages import RosReestrPage, DocCheck
import os


class RosReestrParse():
  
  def __init__(self, key):
    self.key = key
    self.driver = Driver()
    self.web = RosReestrPage(self.driver)

  # Метод для отправки кадастровых номеров для получения выписки по ним. Берем filename,
  # первый столбец, каждая строка читается и массив из них будет отправлен. После выполнения метода
  # будет создан или перезаписан файл ParsedQueries.csv в котором будут указаны кадастровые номера
  # и их номер задачи в росреестре

  def regKNums(self, filename, region):
    try:
      self.web.open_starting_page()
      self.web.enter_key(self.key)
      self.web.find_knums(filename, region)
      self.web.regAll()
    finally: self.driver.driver.quit()
  
  # Читаем filename, пример его можно посмотреть. Второй столбец кроме первой строки и до конца -
  # массив номеров запросов в росреестре, который мы используем чтобы выгрузить архивы 
  
  def downloadZips(self, filename):
    try:
      self.web.open_starting_page()
      self.web.enter_key(self.key)
      self.web.find_queries(filename)
    finally: self.driver.driver.quit()

  # Все архивы которые есть в папке archives будут выгружены в читаемый вид в папку readableHTML
  
  def zip2Readable(self):
    try: 
      self.docCheck = DocCheck(self.driver)
      for filename in os.listdir(os.getcwd() +  os.path.join(r"\archives")):
        if (os.path.splitext(os.path.basename(filename))[1] == ".zip"): 
          self.docCheck.extractXmlFromZip(filename)
      for filename in os.listdir(os.getcwd() +  os.path.join(r"\xml")):
        self.docCheck.getReadableFile(os.getcwd() +  os.path.join(r"\xml", filename))
    finally: self.driver.driver.quit()

regQueries = RosReestrParse('16200ead-6f35-426b-8329-2b6863b4c54a')
#regQueries.regKNums('knums_2parse.csv', 'Москва')
#regQueries.downloadZips('ParsedQueries.csv')
#regQueries.zip2Readable()

