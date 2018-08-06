from WebDriver import Driver
import selenium.common.exceptions as exceptions
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from CSVHelper import CSVHelper
import re
import zipfile 
import os
from io import BytesIO
import time




class RosReestrPage():

    keyfield = "(//input[@type = 'text' and @class = 'v-textfield'])"
    keyfieldSelected = "(//input[@type = 'text' and @class = 'v-textfield v-textfield-focus'])"
    kadastrRegion = "(//input[@class = 'v-filterselect-input'])[1]"
    kadastrNums = "(//input[@type = 'text' and @class = 'v-textfield v-textfield-prompt'])[1]"
    title = "//p[@class = 'portlet-title']"
    genericElement = "//*[text() = '{}']"
    queryText = "//div[@class = 'v-label v-label-tipFont tipFont v-label-undef-w']"
    qString = "//span[text() = '{}' and text() = '{}' and text() = '{}' and '{}']"
    queryNumField = "(//div[.//*[text() = 'Номер запроса'] and .//input[@class = 'v-textfield']])[last()]//input[@class = 'v-textfield']"
    queryField = "//table[.//div[@class = 'v-table-cell-wrapper' and text() = '{}']]"
    queryFieldDownloadIcon = queryField + "//img"
    sentKNums = {}
    qButton = "//span[./label[text() = 'Запросить сведения о переходе прав на объект']]/input[@value = 'on']"
            
    def __init__(self, driver):
        self.page = driver
        self.seleniumdriver = driver.driver
        self.wait = self.page.wait
        
    
    def open_starting_page(self):
        self.seleniumdriver.get('https://rosreestr.ru/wps/portal/p/cc_present/ir_egrn')
        self.page.confirmVisibility(self.keyfield)

    def enter_key(self, key):
        self.checkKey(key)
        self.page.pasteText(self.keyfieldSelected, key)
        self.page.simpleClick(self.genericElement.format('Войти'))
        self.page.confirmInvisibility(self.keyfield)
        self.page.confirmVisibility(self.genericElement.format('Поиск объектов недвижимости'))

    def find_knums(self, filename, region):
        source_csv = CSVHelper(filename)
        self.page.simpleClick(self.genericElement.format('Поиск объектов недвижимости'))
        self.page.confirmVisibility(self.kadastrNums, timeout = 25)
        self.page.pasteText(self.kadastrNums, source_csv.get_requested_knums_string())
        self.page.simpleClick(self.title)
        self.page.pasteText(self.kadastrRegion, region)
        self.page.simpleClick(self.genericElement.format(region))
        self.page.simpleClick(self.genericElement.format('Найти'))
        self.page.confirmVisibility(self.genericElement.format('Найдено объектов: '), timeout = 25)

    def regAll(self):
        self.page.waitTime(3)
        try:
            for i in self.seleniumdriver.find_elements_by_xpath("//div[@class = 'v-label' and ./span]/span"):
                self.regKNum(i)
        finally:
            print(self.sentKNums)
            CSVHelper('ParsedQueries.csv').writeQueriesToCSV(self.sentKNums)
    
    def regKNum(self, i):
        i.click()
        try:
            a = self.genericElement.format('Запросить сведения о переходе прав на объект')
            b = self.genericElement.format('Отправить запрос')
            for t in [a, b]: self.page.confirmVisibility(t)
            self.page.simpleClick(a)
            self.page.confirmVisibility(self.qButton)
            self.page.simpleClick(b)
            self.page.simpleClick(b)
        except exceptions.StaleElementReferenceException:
            self.page.simpleClick(b)
        self.page.confirmVisibility(self.queryText)
        text = re.search(
            r'(?<=Номер запроса ).*(?<!\.)', 
            self.seleniumdriver.find_element_by_xpath(self.queryText).text).group(0)
        self.sentKNums[i.text] = text
        print("Отправлено кадастровых номеров: {}".format(len(self.sentKNums)))
        self.page.simpleClick(self.genericElement.format('Продолжить работу'))
        self.page.confirmInvisibility(self.genericElement.format('Продолжить работу'))

    def find_queries(self, filename):
        self.page.simpleClick(self.genericElement.format('Мои заявки'))
        self.page.confirmVisibility(self.genericElement.format('Номер запроса'))
        self.page.confirmVisibility(self.queryNumField)
        num_a = CSVHelper('ParsedQueries.csv').get_requested_queries()
        for num in num_a:
            self.page.pasteText(self.queryNumField, num, clearField = True)
            self.page.simpleClick(self.genericElement.format('Обновить'))
            self.page.confirmVisibility(self.queryField.format(num))
            self.page.simpleClick(self.queryFieldDownloadIcon.format(num))
            self.page.simpleClick(self.genericElement.format('Очистить фильтр'))
        

    def checkKey(self, key):
        keyCheck = [
            len(key.replace('-', '')) == 32,
            key.count('-') == 4,
            len(key.split('-')[0]) == 8,
            len(key.split('-')[1]) == 4,
            len(key.split('-')[2]) == 4,
            len(key.split('-')[3]) == 4,
            len(key.split('-')[4]) == 12,
        ]
        if not all(keyCheck): raise ValueError('''
            Неверный формат ключа. Длина ключа: 32 символа. 
            Ожидаемый формат ключа: 16200ead-6f35-426b-8329-2b6863b4c54a''')

class DocCheck():
    
    URI = "https://rosreestr.ru/wps/portal/cc_vizualisation"
    inputElement = "//input[@name= 'xml_file' and @type = 'file']"
    genericElement = "//*[text() =  '{}']"
    #saveButton = "//input[@type = 'button' and @value = 'Сохранить']"

    def __init__(self, driver):
        self.page = driver
        self.seleniumdriver = driver.driver
        self.wait = self.page.wait
        self.seleniumdriver.get(self.URI)
        #self.page.confirmInvisibility(self.inputElement)

    def getReadableFile(self, path2XML):
        print(path2XML)
        print()
        self.seleniumdriver.find_element_by_xpath(self.inputElement).send_keys(path2XML)
        self.page.simpleClick(self.genericElement.format('Проверить '))
        self.page.simpleClick(self.genericElement.format('Показать в человекочитаемом формате'))
        while len(self.seleniumdriver.window_handles) == 1: time.sleep(0.2)
        window_before = self.seleniumdriver.window_handles[0]
        window_after = self.seleniumdriver.window_handles[1]
        self.seleniumdriver.switch_to_window(window_after)
        #self.page.simpleClick(self.saveButton)
        page = self.seleniumdriver.page_source
        
        fName = os.getcwd() +  os.path.join(r"\readableHTML", '{}.html'.format(os.path.splitext(os.path.basename(path2XML))[0]))
        with open(fName, 'w', encoding = 'utf-8-sig', newline='') as f:
            f.write(page)
        self.seleniumdriver.close()
        while len(self.seleniumdriver.window_handles) != 1: time.sleep(0.2)
        self.seleniumdriver.switch_to_window(window_before)

    def extractXmlFromZip(self, zipname):
        zipname = (os.getcwd() +  os.path.join(r"\archives", zipname))
        with zipfile.ZipFile(zipname, "r") as zip_ref:
            innerZipFileName = [f for f in  zip_ref.namelist() if f[-4:] == '.zip'][0]
            with zip_ref.open(innerZipFileName) as nested:
                nested_filedata = BytesIO(nested.read())
                with zipfile.ZipFile(nested_filedata) as n:
                    n.extractall(os.getcwd() +  os.path.join(r"\xml"))
        
    



    