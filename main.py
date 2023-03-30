#expresie regulata -> automat finit

#componentele automatului
class Automat:
    def __init__(self, Q, D, qi, F):
        self.Q = Q #starile
        self.D = D #tranzitiile
        self.qi = qi #starea initiala
        self.F = F #starile finale

    def __str__(self):
        string = f" Starile automatului: {self.Q}\n Tranzitiile: {self.D}\n"
        string += f"Starea intiala: {self.qi}\n Stari finale: {self.F}"
        return string

    def stelare(self):
        #vrem sa adaugam o noua stare initiala, care va fi si finala
        self.Q.append('q' + str(len(self.Q))) #mai adaugam o stare
        for i in range(len(self.D)):
            q1, q2, lit = self.D[i]
            q1 = 'q' + str(int(q1[1:]) + 1)
            q2 = 'q' + str(int(q2[1:]) + 1)
            self.D[i] = [q1, q2, lit]
        #muchia de la noua stare initiala la cea veche
        qi_initial = self.qi
        qi_initial = 'q' + str(int(qi_initial[1:]) + 1)
        self.D.append(['q0', qi_initial, ' ']) 
        #muchiile de la starile finale la cea nou initiala
        self.D.extend([['q' + str(int(qf[1:]) + 1), 'q0', ' '] for qf in self.F]) 
        self.qi = 'q0'
        self.F = ['q0']

    def concat(self, a2):
        a1 = self
        nr_stari = len(a1.Q)
        a1.Q.extend(['q' + str(int(q[1:]) + nr_stari) for q in a2.Q]) #adaugam starile din a2 redenumite
        for i in range(len(a2.D)):
            q1, q2, litera = a2.D[i]
            q1 = 'q' + str(int(q1[1:]) + nr_stari)
            q2 = 'q' + str(int(q2[1:]) + nr_stari)
            a1.D.append([q1, q2, litera])
        #tranzitii din toate straile finale ale celui dintai in starea initiala a celui de-al doilea
        a1.D.extend([[qf, 'q' + str(nr_stari), ' '] for qf in a1.F]) 
        a1.F = ['q' + str(int(qf[1:]) + nr_stari) for qf in a2.F] #pastram starile finale din al doilea redenumite
        return a1
    
    def reunit(self, a2):
        a1 = self
        #reunim starile si adaugam un alt q0
        a1.Q.append('q' + str(len(self.Q))) #mai adaugam o stare (simulam ca adaugam un q0)
        nr_stari = len(a1.Q)
        a1.Q.extend(['q' + str(int(q[1:]) + nr_stari) for q in a2.Q]) #reunim starile
        #modificam tranzitiile din a1
        for i in range(len(a1.D)):
            q1, q2, lit = a1.D[i]
            q1 = 'q' + str(int(q1[1:]) + 1)
            q2 = 'q' + str(int(q2[1:]) + 1)
            a1.D[i] = [q1, q2, lit]
        #adaugam si tranzitiile din a2
        for i in range(len(a2.D)):
            q1, q2, litera = a2.D[i]
            q1 = 'q' + str(int(q1[1:]) + nr_stari)
            q2 = 'q' + str(int(q2[1:]) + nr_stari)
            a1.D.append([q1, q2, litera])
        #adaugam cele doua lambda-tranzitii suplimentare
        qi1 = 'q' + str(int(a1.qi[1:]) + 1) #redenumim starea intiala a lui a1
        qi2 = 'q' + str(int(a2.qi[1:]) + nr_stari) #redenumim starea initiala a lui a2
        a1.D.extend([['q0', qi1, ' '], ['q0', qi2, ' ']])
        a1.qi = 'q0'
        a1.F = ['q' + str(int(q[1:]) + 1) for q in a1.F] #redenumim starile finale din a1
        #adaugam starile finale din a2
        a1.F.extend(['q' + str(int(q[1:]) + nr_stari) for q in a2.F]) 
        return a1
                

def automat_litera(litera):
    a = Automat(['q0', 'q1'], [['q0', 'q1', litera]], 'q0', ['q1'])
    return a



vremSaVerificam = 1

while vremSaVerificam: 

    expresie = input("Dati expresia regulata: ")

    lista_automate = []
    CNT = 0

    #parcurgem expresia si incepem sa extindem automatul
    if expresie == "": #multimea vida
        automat_final = Automat(['q0'], [], 'q0', [])
    elif expresie == " ": #lambda
        automat_final = Automat(['q0'], [], 'q0', ['q0'])
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

    vremSaVerificam = int(input("Vreti sa mai introduceti o expresie? [0/1]: "))

    