#expresie regulata -> automat finit
from Automat import Automat
from grafica import desen
                
#creaza un automat care verifica o singura litera
def automat_litera(litera):
    a = Automat(['q0', 'q1'], [['q0', 'q1', litera]], 'q0', ['q1'])
    return a


vremSaVerificam = 1

while vremSaVerificam: 

    expresie = input("Dati expresia regulata: ")

    lista_automate = []
    CNT = 0 #contorizeaza expresiile "globale" (cele dintre paranteze, a caror rezultate vor fi notate intre $$)

    #parcurgem expresia si incepem sa extindem automatul
    if expresie == '': #multimea vida
        automat_final = Automat(['q0'], [], 'q0', [])
        print(automat_final)
        print("Avem un automat pentru multimea vida, dar nu putem desena un automat fara muchii =(")
    elif expresie == " ": #lambda
        automat_final = Automat(['q0'], [], 'q0', ['q0'])
        print(automat_final)
        print("Avem un automat pentru cuvantul vid, dar nu putem desena un automat fara muchii =(")
    elif len(expresie) == 1: #o singura litera
        automat_final = automat_litera(expresie[0])
        print(automat_final)
        desen(automat_final.Q, automat_final.D, automat_final.qi, automat_final.F)
    else:
        while expresie != '#': #o sa inlocuim constant ce am evaluat cu # <=> pana evaluam toata expresia
            
            #cautam paranteze
            prima_paranteza = expresie.rfind("(") #cautam ultima aparitie a unei paranteze deschise
            if prima_paranteza != -1: #daca avem paranteze
                #cautam prima aparitie a unei paranteze inchise dupa cea deschisa
                paranteza_inchisa = expresie.find(")", prima_paranteza)
                #sectionam expresia pe care o evaluam acum
                expresie_evaluata = expresie[prima_paranteza + 1 : paranteza_inchisa]
                expresie = expresie[:prima_paranteza] + '$' + str(CNT) + '$' + expresie[paranteza_inchisa + 1:]
                CNT += 1 #la finalul evaluarii vom avea un nou automat pt expresia curenta pe care il punem in lista
                #vom avea # pentru expresii evaluate "local" =) si $ pt expresii evaluate "global"

            else: #daca nu avem paranteze evaluam toata expresia
                expresie_evaluata = expresie
                expresie = '#'

            print("Initial: ", expresie_evaluata)

            lista_automate_locale = [] #vom crea niste automate intermediare pe care trebuie sa le tinem minte
            
            #am obtinut o expresie fara paranteze
                
            #cautam stelare
            stelare = expresie_evaluata.find('*')
            while stelare != -1:
                #avand in vedere ca nu avem paranteze tre sa fie (litera)* sau ($indice$)*
                if expresie_evaluata[stelare - 1] != '$':
                    litera = expresie_evaluata[stelare - 1]
                    a = automat_litera(litera)
                    start_indice = stelare - 1 #indicele literei
                else: #avem $indice$ <=> luam automatul din lista_automate
                    primul_dolar = expresie_evaluata.rfind('$', 0, stelare - 1) 
                    indice = int(expresie_evaluata[primul_dolar + 1 : stelare - 1]) #cel din $indice$
                    a = lista_automate[indice]
                    start_indice = primul_dolar
                a.stelare() #il stelam si il adaugam la lista locala
                lista_automate_locale.append(a)
                index = len(lista_automate_locale) - 1 #indexul la care se gaseste automatul creeat
                expresie_evaluata = expresie_evaluata[: start_indice] + '#' + str(index) + '#' + expresie_evaluata[stelare + 1 :]
                stelare = expresie_evaluata.find('*')

                print("Dupa stelare: ", expresie_evaluata)

            #am terminat cu stelarea, trecem la concatenare
            concat = expresie_evaluata.find('.') #folosim punctul pt concatenare
            while concat != -1:
                #nu avem paranteze => x . x unde x = litera | #indice# | $indice$
                if expresie_evaluata[concat - 1] == '#':
                    primul_hashtag = expresie_evaluata.rfind('#', 0, concat - 1)
                    index = int(expresie_evaluata[primul_hashtag + 1 : concat - 1])
                    a1 = lista_automate_locale[index]
                    start_index = primul_hashtag
                elif expresie_evaluata[concat - 1] == '$':
                    primul_dolar = expresie_evaluata.rfind('$', 0, concat - 1)
                    index = int(expresie_evaluata[primul_dolar + 1 : concat - 1])
                    a1 = lista_automate[index]
                    start_index = primul_dolar
                else:
                    litera1 = expresie_evaluata[concat - 1]
                    a1 = automat_litera(litera1)
                    start_index = concat - 1

                if expresie_evaluata[concat + 1] == '#':
                    ultimul_hashtag = expresie_evaluata.find('#', concat + 2)
                    index = int(expresie_evaluata[concat + 2 : ultimul_hashtag])
                    a2 = lista_automate_locale[index]
                    final_index = ultimul_hashtag
                elif expresie_evaluata[concat + 1] == '$':
                    ultimul_dolar = expresie_evaluata.find('$', concat + 2)
                    index = int(expresie_evaluata[concat + 2 : ultimul_dolar])
                    a2 = lista_automate[index]
                    final_index = ultimul_dolar
                else: 
                    litera2 = expresie_evaluata[concat + 1]
                    a2 = automat_litera(litera2)
                    final_index = concat + 1

                a_concat = a1.concat(a2)
                lista_automate_locale.append(a_concat)
                expresie_evaluata = expresie_evaluata[:start_index] + '#' + str(len(lista_automate_locale) - 1) + '#' + expresie_evaluata[final_index + 1:]
                concat = expresie_evaluata.find('.')

            print("Dupa concatenare: ", expresie_evaluata)

            #la final, cautam reuniune
            reuniune = expresie_evaluata.find('+')
            while reuniune != -1:
                #procedam asemanator cu modul in care am analizat concatenarea
                if expresie_evaluata[reuniune - 1] == '#':
                    primul_hashtag = expresie_evaluata.rfind('#', 0, reuniune - 1)
                    index = int(expresie_evaluata[primul_hashtag + 1 : reuniune - 1])
                    a1 = lista_automate_locale[index]
                    start_index = primul_hashtag
                elif expresie_evaluata[reuniune - 1] == '$':
                    primul_dolar = expresie_evaluata.rfind('$', 0, reuniune - 1)
                    index = int(expresie_evaluata[primul_dolar + 1 : reuniune - 1])
                    a1 = lista_automate[index]
                    start_index = primul_dolar
                else:
                    litera1 = expresie_evaluata[reuniune - 1]
                    a1 = automat_litera(litera1)
                    start_index = reuniune - 1

                if expresie_evaluata[reuniune + 1] == '#':
                    ultimul_hashtag = expresie_evaluata.find('#', reuniune + 2)
                    index = int(expresie_evaluata[reuniune + 2 : ultimul_hashtag])
                    a2 = lista_automate_locale[index]
                    final_index = ultimul_hashtag
                elif expresie_evaluata[reuniune + 1] == '$':
                    ultimul_dolar = expresie_evaluata.find('$', reuniune + 2)
                    index = int(expresie_evaluata[reuniune + 2 : ultimul_dolar])
                    a2 = lista_automate[index]
                    final_index = ultimul_dolar
                else: 
                    litera2 = expresie_evaluata[reuniune + 1]
                    a2 = automat_litera(litera2)
                    final_index = reuniune + 1

                a_reunit = a1.reunit(a2)
                lista_automate_locale.append(a_reunit)
                expresie_evaluata = expresie_evaluata[:start_index] + '#' + str(len(lista_automate_locale) - 1) + '#' + expresie_evaluata[final_index + 1:]
                reuniune = expresie_evaluata.find('+')   

            print("Dupa reuniune: ", expresie_evaluata)  
            
            #stim ca in final expresia evaluata a fost inlocuita cu un # sau cu un #contor#
            index = len(lista_automate_locale) - 1 #ultimul aparat
            lista_automate.append(lista_automate_locale[index])

        #la final afisam ultimul automat "global"
        index = len(lista_automate) - 1
        print(lista_automate[index])
        desen(lista_automate[index].Q, lista_automate[index].D, lista_automate[index].qi, lista_automate[index].F)

    vremSaVerificam = int(input("Vreti sa mai introduceti o expresie? [0/1]: "))

    