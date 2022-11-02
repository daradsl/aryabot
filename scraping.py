from urllib.error import HTTPError, URLError
from selenium import webdriver
from bs4 import BeautifulSoup
import requests
from unidecode import unidecode
import re
from selenium.webdriver.common.by import By
import pandas as pd
from schedule import every, repeat, run_pending
import time
import datetime


urlTeachers = 'https://institucional.ufpel.edu.br/servidores'
urlListTeachers = "https://wp.ufpel.edu.br/computacao/sobre-a-computacao-ufpel/servidores/"
urlProjects = 'https://institucional.ufpel.edu.br/projetos'
urlSecretariesCoordination = "https://wp.ufpel.edu.br/computacao/sobre-a-computacao-ufpel/localizacao-e-contatos/"
urlCalendar = "https://wp.ufpel.edu.br/cra/calendario-academico/"

# Projetos de professores
# nomeProfessor: projetos
teacherTeachingProjects = {}
teacherResearchProjects = {}
teacherExtensionProjects = {}

# Resumos de projetos por tipo (pesquisa, ensino e extensão)
# nomeProjeto: resumo
researchAbstracts = {}
teachingAbstracts = {}
extensionAbstracts = {}

# Nome dos projetos
teachingProjects = []
researchProjects = []
extensionProjects = []


def secretariesAndCoordinationContacts(url):
    global navigator
    navigator.get(url)
    navigator.find_element('xpath', '//*[@id="content"]/div[2]/article/div/ul[1]/li[1]')
    infosCS = navigator.find_element('xpath', '//*[@id="content"]/div[2]/article/div/ul[1]/li[1]').text.split('\n')
    infosCE = navigator.find_element('xpath', '//*[@id="content"]/div[2]/article/div/ul[1]/li[2]').text.split('\n')
    infosPOS = navigator.find_element('xpath', '//*[@id="content"]/div[2]/article/div/ul[1]/li[3]').text.split('\n')
    coordination = navigator.find_element('xpath', '//*[@id="content"]/div[2]/article/div/ul[2]/li').text.splitlines()
    for i in range(4):
        coordination[i] = (coordination[i].split(":"))[1][1:]
    coord = [coordination[1], coordination[2], coordination[3]]
    return(infosCS, infosCE, infosPOS, coord)
      
def calendarDates(url):
        currentDateTime = datetime.datetime.now()
        date = currentDateTime.date()
        month = date.strftime("%m")
        calendarURL = url
        months = ["Janeiro", "Fevereiro", "Março", "Abril", "Maio", "Junho", "Julho", "Agosto", "Setembro", "Outrobro", "Novembro", "Dezembro"]

        pageCalendar = requests.get(calendarURL)                   
        soup = BeautifulSoup(pageCalendar.content, 'html.parser')     
        calendar = soup.find(class_='dados-cobalto cobalto-calendario cobalto-calendario-zebrado')
        calendar = calendar.find_all("div")

        for i in range(len(calendar)):
            calendar[i] = calendar[i].get_text()

        def returnMonth(string): 
            for k in range(len(months)):
                if(calendar[i].find(months[k]) != -1): 
                    return k
            return -1
        i = 0
        exit = False
        while(i<len(calendar)):
            monthRow = returnMonth(calendar[i])  
            if(monthRow > -1 and exit == False):             
                aux = -1
                while((aux == -1) and (exit == False)):       
                    calendar[i] = calendar[i] + '#' + str(monthRow)
                    if(i<len(calendar) - 1):
                        exit = False
                        i = i + 1   
                        aux = returnMonth(calendar[i])
                    else:
                        exit = True
            else:
                i = i + 1
            if(exit == True):
                break
            
        def addDayToMonth(row, k):
            returnation = ['', '']
            exit = False
            if(row[0].isdigit()==True):          
                returnation[0] = row[0] + row[1]       
                returnation[1] = row[(len(row)-2):]    
                returnation[1] = returnation[1].replace('#', "")   
            else:
                while(exit == False):              
                    k = k - 1  
                    row = calendar[k]
                    if(row[0].isdigit()==True):         
                        returnation[0] = row[0] + row[1]        
                        returnation[1] = row[-1] + row[-2]      
                        returnation[1] = returnation[1].replace('#', '')    
                        exit = True  
            date = str(returnation[0]) + " de " + months[int(returnation[1])]
            return date

        
        solicitation = ['','']
        solicitation_re = ['','']
        correction = ['','']
        correction_re = ['','']
        locking = ['','']
        locking_re = ['','']
        beginning = ['', '']
        examPeriod = ['', '', '', '']

        for i in range(len(calendar)):
            calendar[i] = calendar[i].lower()
            calendar[i] = unidecode(calendar[i])
            if("exames" in calendar[i]):     
                if(not examPeriod[0]):
                    y = 0
                else:
                    y = 2
                if("inicio" in calendar[i]):
                    examPeriod[y] = addDayToMonth(calendar[i], i)
                elif("fim" in calendar[i]):
                    examPeriod[y+1] = addDayToMonth(calendar[i], i)
            if(not beginning[0]):
                if("semestre letivo" in calendar[i]):
                    if("inicio" in calendar[i]):
                        beginning[0] = addDayToMonth(calendar[i], i)
            else:
                if("semestre letivo" in calendar[i]):
                    if("inicio" in calendar[i]):
                        beginning[1] = addDayToMonth(calendar[i], i)
            if(("solicitacao" in calendar[i]) and ("rematricula" in calendar[i]) and ("online" in calendar[i]) or ("on-line" in calendar[i])):
                if("inicio" in calendar[i]):
                    solicitation_re[0] = addDayToMonth(calendar[i], i)
                elif("fim" in calendar[i]):
                    solicitation_re[1] = addDayToMonth(calendar[i], i)
            elif(("solicitacao" in calendar[i]) and (" matricula" in calendar[i]) and ("online" in calendar[i]) or ("on-line" in calendar[i])):
                if("inicio" in calendar[i]):
                    solicitation[0] = addDayToMonth(calendar[i], i)
                elif("fim" in calendar[i]):
                    solicitation[1] = addDayToMonth(calendar[i], i)
            elif(("solicitacao" in calendar[i]) and ("correcao" in calendar[i])):
                if("rematricula" in calendar[i]):
                    if("inicio" in calendar[i]):
                        correction_re[0] = addDayToMonth(calendar[i], i)              
                    elif("fim" in calendar[i]):
                        correction_re[1] = addDayToMonth(calendar[i], i)
                elif(" matricula" in calendar[i]):
                    if("inicio" in calendar[i]):
                        correction[0] = addDayToMonth(calendar[i], i)
                    elif("fim" in calendar[i]):
                        correction[1] = addDayToMonth(calendar[i], i)
            elif(("solicitacao" in calendar[i]) and ("trancamento" in calendar[i]) and ("disciplinas" in calendar[i])):
                if("inicio" in calendar[i]):
                    locking_re[0] = addDayToMonth(calendar[i], i)
                elif("fim" in calendar[i]):
                    locking_re[1] = addDayToMonth(calendar[i], i)
            elif(("trancamento" in calendar[i]) and ("curriculares" in calendar[i])):
                if("inicio" in calendar[i]):
                    locking[0] = addDayToMonth(calendar[i], i)
                elif("fim" in calendar[i]):
                    locking[1] = addDayToMonth(calendar[i], i)

        next = False
        aux = locking_re[1].split()
        aux = (months.index(aux[2])+1)

        if(int(month) > aux):
            next = True

        def matriculationRequest(prox):
            if(prox == True):
                return (solicitation)
            else:
                return (solicitation_re)

        def matriculationCorrection(prox):
            if(prox == True):
                return(correction)
            else:
                return(correction_re)

        def lockingDisciplines(prox):
            if(prox == True):
                return(locking)
            else:
                return(locking_re)
        
        def beginningOfSemester(prox):
            if(prox == True):
                return(beginning[1])
            else:
                return(beginning[0])
            
        def examinationPeriod(prox):
            if(prox == True):
                exam = [examPeriod[2], examPeriod[3]]
                return(exam)
            else:
                exam = [examPeriod[0], examPeriod[1]]
                return(exam)
                
        return([matriculationRequest(next), matriculationCorrection(next), lockingDisciplines(next), beginningOfSemester(next), examinationPeriod(next)])


def listTeachers(urlTeachers):  
    try:
        html = requests.get(urlTeachers)                   
    except HTTPError as error:
        print(error.status, error.reason)
    except URLError as error:
        print(error.reason) 
    soup = BeautifulSoup(html.content, 'html.parser')     
    teachers = soup.findAll('ul')
    teachers = str(teachers[20].get_text())
    teachers = teachers.split('\n')
    teachersList = list(filter(None, teachers)) 
    for i in range(len(teachersList)):
        if("Corrêa" not in teachersList[i]):
            teachersList[i] = unidecode(teachersList[i])
        if("Jr" in teachersList[i]):
            teachersList[i] = teachersList[i].replace('Jr', '') 
        if("Correa" in teachersList[i]):
            aux = teachersList[i].split() 
            teachersList[i] = aux[0] + " " + aux[1]
        teachersList[i] = teachersList[i].replace('\xa0', ' ')
        teachersList[i] = re.sub(r'[^\w\s]','',teachersList[i])
    return teachersList

def getAbstract(project, type):
    global navigator
    aux = project[:30]
    try:
        navigator.find_element(By.PARTIAL_LINK_TEXT, aux).click()
        if(type == "research"):
            link = navigator.current_url 
            abstract = navigator.find_element(By.XPATH, '//*[@id="conteudo"]/div[1]/div[1]/div[14]').text
            researchAbstracts[project] = [abstract, link]
        elif(type == "teaching"):
            link = navigator.current_url 
            abstract = navigator.find_element(By.XPATH, '//*[@id="conteudo"]/div[1]/div[1]/div[14]').text
            teachingAbstracts[project] = [abstract, link]
        elif(type == "extension"):
            link = navigator.current_url 
            abstract = navigator.find_element(By.XPATH, '//*[@id="conteudo"]/div[1]/div[1]/div[18]').text
            extensionAbstracts[project] = [abstract, link]
        navigator.back()
    except:
        print("problem with abstract: " + project)

def teacherProjects (teacher, rows, table):
    i = 0
    research = []
    extension = []
    teaching = []
    while(i < len(rows)):
        if(i<len(rows) and "Pesquisa" in rows[i]):
            i+=1
            while(i<len(rows) and "tabela-quebra" not in rows[i]):
                if(i < len(rows) and "<tr><td><a" in rows[i]): 
                    aux = table[i].find('a').get_text()
                    research.append(aux)
                    researchProjects.append(aux)
                    getAbstract(aux, "research")
                i+=1
            if(i < len(rows)):
                i -= 1
        if(i<len(rows) and "Extensão" in rows[i]):
            i+=1
            while(i<len(rows) and "tabela-quebra" not in rows[i]):
                if(i < len(rows) and "<tr><td><a" in rows[i]): 
                    aux = table[i].find('a').get_text()
                    extension.append(aux)
                    extensionProjects.append(aux)
                    getAbstract(aux, "extension")
                i+=1
            if(i < len(rows)):
                i -= 1
        if(i<len(rows) and "Ensino" in rows[i]):
            i+=1
            while(i<len(rows) and "tabela-quebra" not in rows[i]):
                if(i < len(rows) and "<tr><td><a" in rows[i]): 
                    aux = table[i].find('a').get_text()
                    teaching.append(aux)
                    teachingProjects.append(aux)
                    getAbstract(aux, "teaching")
                i+=1
            if(i < len(rows)):
                i -= 1
        i+=1
    teacherResearchProjects[teacher] = research
    teacherExtensionProjects[teacher] = extension
    teacherTeachingProjects[teacher] = teaching


def allProjects(teachers, url):
    restTeachers = ""
    global navigator
    for i in range(len(teachers)):
        print("----> prof: " + teachers[i])
        navigator.get(url)
        navigator.find_element('xpath', '//*[@id="DataTables_Table_0_filter"]/label/input').send_keys(teachers[i])
        try:
            navigator.find_element('xpath', '//*[@id="DataTables_Table_0"]/tbody/tr/td').click()
            navigator.find_element('xpath', '//*[@id="proj-sup"]').click()
            page = requests.get(navigator.current_url)  
            soup = BeautifulSoup(page.content, 'html.parser')    
            table = soup.find('table')
            table = table.find_all('tr')
            rows = [None]*len(table)
            for j in range(len(table)):
                    rows[j] = str(table[j])
            if(i<len(teachers)):
                teacherProjects(teachers[i], rows, table)
        except:
            restTeachers = restTeachers + "-" + teachers[i]
            print(">> rest teachers: " + restTeachers)
    return [teacherExtensionProjects, teacherResearchProjects, teacherTeachingProjects, researchProjects, teachingProjects, extensionProjects, researchAbstracts, teachingAbstracts, extensionAbstracts]


def saveOnExcel(result):
    writer = pd.ExcelWriter('table.xlsx', engine='xlsxwriter')

    data = pd.Series(data= result[9])
    data.to_excel(writer, sheet_name="teachers", index=False)

    data1 = pd.DataFrame(data= result[0])
    data1.to_excel(writer, sheet_name="teacherExtensionProjects", index=False)

    data2 = pd.DataFrame(data= result[1])
    data2.to_excel(writer, sheet_name="teacherResearchProjects", index=False)

    data3 = pd.DataFrame(data= result[2])
    data3.to_excel(writer, sheet_name="teacherTeachingProjects", index=False)

    data4 = pd.Series(data= result[3])
    data4.to_excel(writer, sheet_name="researchProjects", index=False)

    data5 = pd.Series(data= result[4])
    data5.to_excel(writer, sheet_name="teachingProjects", index=False)

    data6 = pd.Series(data= result[5])
    data6.to_excel(writer, sheet_name="extensionProjects", index=False)

    data7 = pd.DataFrame(data= result[6])
    data7.to_excel(writer, sheet_name="researchAbstracts", index=False)
    
    data8 = pd.DataFrame(data= result[7])
    data8.to_excel(writer, sheet_name="teachingAbstracts", index=False)
    
    data9 = pd.DataFrame(data= result[8])
    data9.to_excel(writer, sheet_name="extensionAbstracts", index=False)

    data10 = pd.Series(data= result[10][0])
    data10.to_excel(writer, sheet_name="secretaryCS", index=False)

    data11 = pd.Series(data= result[10][1])
    data11.to_excel(writer, sheet_name="secretaryCE", index=False)

    data12 = pd.Series(data= result[10][2])
    data12.to_excel(writer, sheet_name="secretaryPOS", index=False)

    data14 = pd.Series(data= result[10][3])
    data14.to_excel(writer, sheet_name="coordination", index=False)

    data15 = pd.Series(data= result[11][0])
    data15.to_excel(writer, sheet_name="matriculation", index=False)

    data16 = pd.Series(data= result[11][1])
    data16.to_excel(writer, sheet_name="correction", index=False)

    data17 = pd.Series(data= result[11][2])
    data17.to_excel(writer, sheet_name="locking", index=False)

    data18 = pd.Series(data= result[11][3])
    data18.to_excel(writer, sheet_name="beggining", index=False)

    data19 = pd.Series(data= result[11][4])
    data19.to_excel(writer, sheet_name="examination", index=False)
    
    writer.save()


@repeat(every(90).days)
def scraping():
    global navigator
    options = webdriver.ChromeOptions()
    options.add_experimental_option('excludeSwitches', ['enable-logging'])
    navigator = webdriver.Chrome(options=options)
    teacherList = listTeachers(urlListTeachers)
    result = allProjects(teacherList, urlTeachers)
    result.append(teacherList)
    secretariesCoordination = secretariesAndCoordinationContacts(urlSecretariesCoordination)
    result.append(secretariesCoordination)
    dates = calendarDates(urlCalendar)
    result.append(dates)


    i = 0
    while i < 3:
        maxLength = 0
        for key, value in result[i].items():
            if(len(value)>maxLength):
                maxLength = len(value)
        for key, value in result[i].items():    
            while(len(value) < maxLength):
                value.append("")
        i += 1

    if(len(result[3]) >= len(result[4]) and len(result[3]) >= len(result[5])):
        maxLength = len(result[3])
    elif(len(result[4]) >= len(result[3]) and len(result[4]) >= len(result[5])):
        maxLength = len(result[4])
    else:
        maxLength = len(result[5])
    
    i = 3
    while i<6:
        while(len(result[i])<maxLength):
            result[i].append("")
        i += 1
    saveOnExcel(result)


# while True:
#     run_pending()
#     time.sleep(1)

scraping()