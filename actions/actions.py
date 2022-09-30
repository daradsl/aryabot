from typing import Any, Text, Dict, List 
from rasa_sdk import Action, Tracker, FormValidationAction
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.types import DomainDict
from rasa_sdk.events import FollowupAction, SlotSet, AllSlotsReset
import pandas as pd


class dataExcel():

    def getDataFromExcel():
        def dictConverter(teacherTypeProjects):
            teacherProjects = {}
            for key, value in teacherTypeProjects.items():
                projects = []
                for element in list(value.values):
                    if('nan' not in str(element)):
                        projects.append(str(element))
                teacherProjects[key] = projects
            return teacherProjects

        global teacherExtensionProjects, teacherResearchProjects, teacherTeachingProjects, extensionAbstracts, teachingAbstracts, researchAbstracts, teachersList, teachingProjects, researchProjects, extensionProjects
        teachers = pd.read_excel("table.xlsx", sheet_name="teachers")
        teachersList = list(teachers[0])
        
        tExtensionProjects = pd.read_excel("table.xlsx", sheet_name="teacherExtensionProjects")
        teacherExtensionProjects = dictConverter(tExtensionProjects)

        tResearchProjects = pd.read_excel("table.xlsx", sheet_name="teacherResearchProjects")
        teacherResearchProjects = dictConverter(tResearchProjects)

        tTeachingProjects = pd.read_excel("table.xlsx", sheet_name="teacherTeachingProjects")
        teacherTeachingProjects = dictConverter(tTeachingProjects)

        researchProjects = pd.read_excel("table.xlsx", sheet_name="researchProjects")
        researchProjects = list(researchProjects[0])

        teachingProjects = pd.read_excel("table.xlsx", sheet_name="teachingProjects")
        teachingProjects = list(teachingProjects[0])

        extensionProjects = pd.read_excel("table.xlsx", sheet_name="extensionProjects")
        extensionProjects = list(extensionProjects[0])

        extensionAbs = pd.read_excel("table.xlsx", sheet_name="extensionAbstracts")
        extensionAbstracts = dictConverter(extensionAbs)

        researchAbs = pd.read_excel("table.xlsx", sheet_name="researchAbstracts")
        researchAbstracts = dictConverter(researchAbs)

        teachingAbs = pd.read_excel("table.xlsx", sheet_name="teachingAbstracts")
        teachingAbstracts = dictConverter(teachingAbs)

        secretaryCS = pd.read_excel("table.xlsx", sheet_name="secretaryCS")
        secretaryCS = list(secretaryCS[0])

        secretaryCE = pd.read_excel("table.xlsx", sheet_name="secretaryCE")
        secretaryCE = list(secretaryCE[0])

        secretaryPOS = pd.read_excel("table.xlsx", sheet_name="secretaryPOS")
        secretaryPOS = list(secretaryPOS[0])

        coordination = pd.read_excel("table.xlsx", sheet_name="coordination")
        coordination = list(coordination[0])

        matriculation = pd.read_excel("table.xlsx", sheet_name="matriculation")
        matriculation = list(matriculation[0])

        correction = pd.read_excel("table.xlsx", sheet_name="correction")
        correction = list(correction[0])

        locking = pd.read_excel("table.xlsx", sheet_name="locking")
        locking = list(locking[0])

        beggining = pd.read_excel("table.xlsx", sheet_name="beggining")
        beggining = list(beggining[0])

        examination = pd.read_excel("table.xlsx", sheet_name="examination")
        examination = list(examination[0])

        return [teacherResearchProjects, teacherTeachingProjects, teacherExtensionProjects, researchProjects, teachingProjects, extensionProjects, researchAbstracts, teachingAbstracts, extensionAbstracts, teachersList, secretaryCS, secretaryCE, secretaryPOS, coordination, matriculation, correction, locking, beggining, examination]

data = dataExcel.getDataFromExcel()

teacherResearchProjects=data[0]
teacherTeachingProjects=data[1]
teacherExtensionProjects=data[2]
researchProjects=data[3]
teachingProjects=data[4]
extensionProjects=data[5]
researchAbstracts=data[6]
teachingAbstracts=data[7]
extensionAbstracts=data[8]
teachersList=data[9]
secretaryCS = data[10]
secretaryCE = data[11]
secretaryPOS = data[12]
coordination = data[13]
matriculation = data[14]
correction = data[15]
locking = data[16]
beggining = data[17]
examination = data[18]

class ActionCoordenacao(Action):
    def name(self) -> Text:
        return "get_coordenacao"
    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        # current_curso = next(tracker.get_latest_entity_values("curso"), None)
        global coordination
        # if not current_curso:   # coordenacao dos dois cursos
        dispatcher.utter_message(text="A coordenação atual dos cursos é:\n - Ciência da Computação: " + str(coordination[0])  + "\n - Engenharia de Computação: " + str(coordination[1]) + "\n - Pós-graduação: " + str(coordination[2]))
        return []

class ActionSecretaria(Action):
    def name(self) -> Text:
        return "get_secretaria"
    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        global secretaryCS, secretaryCE, secretaryPOS
        dispatcher.utter_message(text="Os contatos das secretarias da Computação são:")
        dispatcher.utter_message(text= "  -> " + str(secretaryCS[0]) + "\n  - " + str(secretaryCS[1]) + "\n  - " + str(secretaryCS[2]))
        dispatcher.utter_message(text= "  -> " + str(secretaryCE[0]) + "\n  - " + str(secretaryCE[1]) + "\n  - " + str(secretaryCE[2]))
        dispatcher.utter_message(text= "  -> " + str(secretaryPOS[0]) + "\n  - " + str(secretaryPOS[1]) + "\n  - " + str(secretaryPOS[2]))
        dispatcher.utter_message(text= "Sala no campus porto: " + str(secretaryCS[3]))
        return []

class ActionSolicitacaoMatricula(Action):
    def name(self) -> Text:
        return "get_solicitacao_matricula"
    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        global matriculation
        dispatcher.utter_message(text="A solicitação de matrícula ocorre de " + str(matriculation[0]) + " a " + str(matriculation[1]))
        return []

class ActionCorrecaoMatricula(Action):
    def name(self) -> Text:
        return "get_correcao_matricula"
    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        
        global correction
        dispatcher.utter_message(text="A correção de matrícula ocorre de " + str(correction[0]) + " a " + str(correction[1]))
        return []

class ActionTrancamentoDisc(Action):
    def name(self) -> Text:
        return "get_trancamento"
    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        
        
        global locking
        dispatcher.utter_message(text="O trancamento de disciplinas ocorre de " + str(locking[0]) + " a " + str(locking[1]))
        return []

class ActionInicioSemestre(Action):
    def name(self) -> Text:
        return "get_inicio_semestre"
    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        
        global beggining        
        dispatcher.utter_message(text="O início do semestre ocorre dia: " + str(beggining[0]))
        return []
    
class ActionExame(Action):
    def name(self) -> Text:
        return "get_exames"
    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        
        global examination        
        dispatcher.utter_message(text="O período de exames ocorre de " + str(examination[0]) + " a " + str(examination[1]))
        return []

class ActionDatasImportantes(Action):
    def name(self) -> Text:
        return "get_datas"
    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        
        global matriculation, correction, locking, beggining, examination
        dispatcher.utter_message(text="- Solicitação de matrícula: de " + str(matriculation[0]) + " a " + str(matriculation[1]) + ".\n" + "- Correção de matrícula: de " + str(correction[0]) + " a " + str(correction[1]) + ".\n"  + "- Inicio do semestre letivo: " + str(beggining[0]) + ".\n" + "- Trancamento de disciplinas: de " + str(locking[0]) + " a " + str(locking[1]) + ".\n" + "- Período de exames: de " + str(examination[0]) + " a " + str(examination[1]) + ".\n")
        return []

def clean_option(option):
    return "".join([c for c in option])

class ValidateProjectForm(FormValidationAction):
    global once
    once = True
    global exit
    exit = False
    def name(self) -> Text:
        return "validate_project_form"
    
    def validate_search_option(
        self,
        slot_value: Any,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: DomainDict,
    ) -> Dict[Text, Any]:
        global exit
        exit = False
        
        def getTeachersList(teachersList):
            teachers = ""
            for i in range (len(teachersList)):
                teachers += str(i+1) + ": " + teachersList[i] + '\n'
            return str(teachers)
        
        
        option = clean_option(slot_value)
        print(option)
        if option == '0':
            exit  =  True
            return {"search_option": option}
            # ActionExecutionRejected
            # return {"search_option": option}

        else:
            if option == '1':
                dispatcher.utter_message(response='utter_tipo_projeto')
                return {"search_option": option}

            if option == '2':
                global teachersList
                dispatcher.utter_message(text=getTeachersList(teachersList))
                dispatcher.utter_message(text='Digite o número correspondente ao professor desejado')
                return {"search_option": option}
    
            else:
                dispatcher.utter_message(text="Opção inválida! :(\nTente novamente ou digite '0' para sair")
                return {"search_option": None}

    async def required_slots(
        self,
        domain_slots: List[Text],
        dispatcher: "CollectingDispatcher",
        tracker: "Tracker",
        domain: "DomainDict",
    ) -> List[Text]:
        updated_slots = domain_slots.copy()
        global exit
        if(exit == True):
            print('sair é true')
            updated_slots.remove("search_option")
            updated_slots.remove("teacher_option")
            updated_slots.remove("project_teacher_option")
            updated_slots.remove("type_option")
            updated_slots.remove("project_option")
        else:
            if (tracker.slots.get("search_option") == '1' and once is True):
                print("removendo os teacher option")
                updated_slots.remove("teacher_option")
                updated_slots.remove("project_teacher_option")
            elif (tracker.slots.get("search_option") == '2' and once is True):
                print("removendo os type option")
                updated_slots.remove("type_option")
                updated_slots.remove("project_option")
        print(updated_slots)
        exit = False
        return updated_slots


    def getProjectsListByType(self, option): 
        type = option
        projectsList = []
        projectsReturn = ""
        projects = {}
        global researchProjects, teachingProjects, extensionProjects
        if type == '1': # type 1 = Pesquisa
            projects = researchProjects
        elif type == '2': # type 2 = Ensino
            projects = teachingProjects
        elif type == '3':   # type 3 = Extensao
            projects = extensionProjects
        i = 1
        projectsUnique = list(set(projects))
        for proj in projectsUnique:
            if ("Monitoria" not in proj):
                projectsList.append(proj)
                projectsReturn += (str(i) + ": " + str(proj) + '\n')
                i += 1        
        if type == '1': # type 1 = Pesquisa
            researchProjects = projectsList
        elif type == '2': # type 2 = Ensino
            teachingProjects = projectsList
        elif type == '3':   # type 3 = Extensao
            extensionProjects = projectsList
        return [projectsReturn, researchProjects, teachingProjects, extensionProjects]

    def validate_type_option(
        self,
        slot_value: Any,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: DomainDict,
    ) -> Dict[Text, Any]:
        global exit
        type_option = clean_option(slot_value)
        print(type_option)
        print('aqui')
        if (exit or type_option == '0'):
            exit  =  True
            return {"type_option": type_option}
        else:
            if (type_option == '1' or type_option == '2' or type_option == '3'):

                # chama a funcao que retorna a lista de projetos com a option
                # printa o dispatcher disso e o prox que vai ser qual projeto quer
                # print(projectsReturn)
                dispatcher.utter_message(text=self.getProjectsListByType(type_option)[0])
                dispatcher.utter_message(response='utter_escolher_projeto')
                return {"type_option": type_option}
                # chama o utter q ativa o prox formulario
            else:
                dispatcher.utter_message(text="Opção inválida! :(\nTente novamente ou digite '0' para sair")
                return {"type_option": None}
    
    

    def validate_project_option(
        self,
        slot_value: Any,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: DomainDict,
    ) -> Dict[Text, Any]:
        global exit
        project_option = clean_option(slot_value)
        print(project_option)

        def getProjectAbstractByType(self, option, type):
            print("entrouuu") 
            index = (option - 1)
            abstract = {}
            global researchAbstracts, teachingAbstracts, extensionAbstracts
            aux = self.getProjectsListByType(type)
            print("aux1")
            print(aux[1])
            researchProjects = aux[1]
            teachingProjects = aux[2]
            extensionProjects = aux[3]
            print("type:")
            print(type)
            maxOption = 0
            if(type == '1'):  # pesquisa
                projectName = researchProjects[index]
                maxOption = len(researchProjects)
                abstract = researchAbstracts
                print(projectName)
            if(type == '2'):  # ensino
                projectName = teachingProjects[index]
                print(projectName)
                maxOption = len(teachingProjects)
                abstract = teachingAbstracts
            if(type == '3'):  # extensao
                projectName = extensionProjects[index]
                print(projectName)
                maxOption = len(extensionProjects)
                abstract = extensionAbstracts
            print("maxOption" + str(maxOption))
            return [abstract[projectName][0], abstract[projectName][1], maxOption]

        try:
            abstract = getProjectAbstractByType(self, int(project_option), tracker.slots.get("type_option"))
            if (exit or project_option == '0'):
                exit = True
                return {"project_option": project_option}
            else:
                if(int(project_option)>abstract[2] or int(project_option)<1):
                    dispatcher.utter_message(text="Opção inválida! :(\nTente novamente ou digite '0' para sair")
                    return {"project_option": None}
                dispatcher.utter_message(text=str(abstract[0]))
                dispatcher.utter_message(text="Para saber mais sobre o projeto acesse: " +  str(abstract[1]))
                return {"project_option": project_option}
        except:
            dispatcher.utter_message(text="Opção inválida! :(\nTente novamente ou digite '0' para sair")
            return {"project_option": None}
    

    def validate_teacher_option(
        self,
        slot_value: Any,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: DomainDict,
    ) -> Dict[Text, Any]:
        global exit
        teacher_option = clean_option(slot_value)
        print(teacher_option)
        print('problem here')

        def getTeacherProjects(option, teachersList, teacherResearchProjects, teacherTeachingProjects, teacherExtensionProjects):
            global teacherProject
            teacherProject = []
            index = (option - 1)
            teacher = teachersList[index]
            dispatcher.utter_message(text="Projetos do professor(a): " + str(teacher))
            print(str(teacher))
            extension = list(set(teacherExtensionProjects[teacher]))
            research = list(set(teacherResearchProjects[teacher]))
            teaching = list(set(teacherTeachingProjects[teacher]))
            print(extension)
            print(research)
            print(teaching)
            i = 1
            if(research):
                for proj in research:
                    teacherProject.append(str(i) + ": " + str(proj) + '\n')
                    i += 1
            if(extension):
                for proj in extension:
                    teacherProject.append(str(i) + ": " + str(proj) + '\n')
                    i += 1
            if(teaching):
                for proj in teaching:
                    teacherProject.append(str(i) + ": " + str(proj) + '\n')
                    i += 1
            projectsReturn = ""
            for proj in teacherProject:
                projectsReturn += proj
            maxOption = len(teachersList)
            print("maxOption"+str(maxOption))
            return [str(projectsReturn), maxOption]
        global teachersList, teacherResearchProjects, teacherExtensionProjects, teacherTeachingProjects
        print(teachersList)
        try:
            print('no try')
            if (exit or teacher_option == '0'):
                exit = True
                return {"teacher_option": teacher_option}
            else:
                result = getTeacherProjects(int(teacher_option), teachersList, teacherResearchProjects, teacherTeachingProjects, teacherExtensionProjects)
                if(int(teacher_option)>=result[1] or int(teacher_option)<1):
                    dispatcher.utter_message(text="Opção inválida! :(\nTente novamente ou digite '0' para sair")
                    return {"teacher_option": None}
                if(len(result[0]) == 0):
                    dispatcher.utter_message(text="Professor(a) selecionado(a) sem projetos ativos no momento")
                    return {"project_teacher_option": '0'}
                dispatcher.utter_message(text=result[0])
                dispatcher.utter_message(response='utter_escolher_projeto')
                return {"teacher_option": teacher_option}
        except:
            dispatcher.utter_message(text="Opção inválida! :(\nTente novamente ou digite '0' para sair")
            return {"teacher_option": None}

    def validate_project_teacher_option(
        self,
        slot_value: Any,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: DomainDict,
    ) -> Dict[Text, Any]:
        global exit
        project_teacher_option = clean_option(slot_value)
        print(project_teacher_option)

        def getProjectAbstractByTeacher(option, researchAbstracts, teachingAbstracts, extensionAbstracts):
            print("ESSE")
            index = option - 1
            global teacherProject
            print(teacherProject)
            projectName = teacherProject[index]
            print(projectName)
            result = ""
            if(index+1>9):
                projectName = str(projectName[4:])
            else:
                projectName = str(projectName[3:])
            teacherProject = []
            print(projectName[:30])
            for key, value in researchAbstracts.items():
                if(str(projectName[:30]) in key):
                    print("entrou")
                    result = value
                    # return value
            for key, value in teachingAbstracts.items():
                if(str(projectName[:30]) in key):
                    print("entrou")
                    result = value
                    # return value
            for key, value in extensionAbstracts.items():
                if(str(projectName[:30]) in key):
                    print("entrou")
                    result = value
                    # return value
            return result
        global researchAbstracts, teachingAbstracts, extensionAbstracts
        try:
            if (exit or project_teacher_option == '0'):
                exit = True
                return {"project_teacher_option": project_teacher_option}
            else:
                if(int(project_teacher_option)==0):
                    dispatcher.utter_message(text="Opção inválida! :(\nTente novamente ou digite '0' para sair")
                    return {"project_teacher_option": None}    
                result = getProjectAbstractByTeacher(int(project_teacher_option), researchAbstracts, teachingAbstracts, extensionAbstracts)
                print("result:")
                print(result)
                dispatcher.utter_message(text=str(result[0]))
                dispatcher.utter_message(text="Para saber mais sobre o projeto acesse: " +  str(result[1]))
                if(len(result[0]) == 0):
                    dispatcher.utter_message(text="Professor(a) selecionado(a) sem projetos ativos no momento")
                    return {"project_teacher_option": '0'}
                return {"project_teacher_option": project_teacher_option}
        except:
            dispatcher.utter_message(text="Opção inválida! :(\nTente novamente ou digite '0' para sair")
            return {"project_teacher_option": None}

    # Ação realizada pelo bot após receber
    # todos os slots requisitados
    def submit(self, dispatcher, tracker, domain):
        dispatcher.utter_message('Coletei todos os slots!')
        # O submit deve retornar uma lista
        # Caso não haja retorno na função,
        # basta colocar uma lista vazia
        return []        

class ResetSlots(Action):
    def name(self):
        return "action_reset_slots"
    
    def run(self, dispatcher, tracker, domain):
        return [AllSlotsReset()]
