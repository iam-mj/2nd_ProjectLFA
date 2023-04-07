#componentele automatului
class Automat:
    def __init__(self, Q, D, qi, F):
        self.Q = Q #starile
        self.D = D #tranzitiile
        self.qi = qi #starea initiala
        self.F = F #starile finale

    def __str__(self):
        string = f" Starile automatului: {self.Q}\n Tranzitiile: {self.D}\n"
        string += f" Starea intiala: {self.qi}\n Stari finale: {self.F}"
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