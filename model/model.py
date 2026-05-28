import itertools
import networkx as nx

from database.DAO import DAO


class Model:
    def __init__(self):
        self._grafo = nx.Graph()
        self._nodi = []
        self._idMap = {}
        self.bestPercorso = []
        self.bestScore = 0  # cammino di peso massimo, decrescente, SCORE è FONDAMENTALE

    def getPercorsoPeso(self, source):
        self.bestPercorso = []
        self.bestScore = 0

        parziale = [source]
        self.ricorsione(parziale)
        return self.bestPercorso, self.bestScore

    def ricorsione(self, parziale):
        # 1) CONDIZIONE DI OTTIMALITÀ (Valuto la soluzione attuale)
        score_attuale = self.getScore(parziale)
        if score_attuale > self.bestScore:
            self.bestScore = score_attuale
            self.bestPercorso = list(parziale)  # list() per fare la copia!

        # 2) CONDIZIONE DI TERMINAZIONE
        # Omessa, si ferma da sola quando il for non trova più vicini validi

        # 3) ESPANSIONE 'ALBERO' + BACKTRACKING
        for a in self._grafo.neighbors(parziale[-1]):
            if a not in parziale:

                # --- CONTROLLO IL PESO DECRESCENTE ---
                # Caso A: È il primo passo in assoluto. Non ho un "arco precedente".
                # Posso andare dove voglio!
                if len(parziale) == 1:
                    parziale.append(a)
                    self.ricorsione(parziale)
                    parziale.pop()

                # Caso B: Ho già fatto almeno un passo. Devo confrontare l'arco nuovo con quello vecchio.
                else:  # parziale[-2] --> penultimo nodo; parziale[-1] ultimo nodo
                    peso_vecchio = self._grafo[parziale[-2]][parziale[-1]]['weight']
                    peso_nuovo = self._grafo[parziale[-1]][a]['weight']

                    # La regola della traccia: il peso deve essere strettamente decrescente
                    if peso_nuovo < peso_vecchio:
                        parziale.append(a)
                        self.ricorsione(parziale)
                        parziale.pop()

    # Il tuo metodo classico per calcolare lo score
    def getScore(self, lista_nodi):
        score = 0
        # Ciclo da 0 alla penultima posizione per prendere le coppie (i, i+1)
        for i in range(len(lista_nodi) - 1):
            nodo1 = lista_nodi[i]
            nodo2 = lista_nodi[i + 1]
            score += self._grafo[nodo1][nodo2]['weight']

        return score

    def getAnni(self):
        return DAO.getAnni()

    def getSquadre(self, anno):
        listaTuple = DAO.getSquadreAnno(anno)
        self._nodi.clear()
        for tupla in listaTuple:
            self._nodi.append(tupla)
            self._idMap[tupla[0]] = (tupla[1], tupla[2])  # nome e salario
            print(tupla[0])
        return listaTuple

    def creaGrafo(self):
        self._grafo = nx.Graph()
        for squadra in self._nodi:
            self._grafo.add_node(squadra[0])

        lunghezza = self._grafo.number_of_nodes()
        archi = list(itertools.combinations(self._nodi, 2))  # è una lista, gli archi non esistono ancora

        for coppia in archi:
            peso1 = coppia[0][2]
            peso2 = coppia[1][2]

            # CORREZIONE QUI: Ho rimosso _idMap, passando l'ID puro di sq1 (coppia[0][0]) e sq2 (coppia[1][0])
            self._grafo.add_edge(coppia[0][0], coppia[1][0], weight=peso1 + peso2)

            # Ho lasciato la tua print come volevi tu
            print(coppia[0][1])

        print(self._grafo.number_of_edges(), self._grafo.number_of_nodes())

    def getVicini(self, codiceSquadra):
        vicini = self._grafo.neighbors(codiceSquadra)
        print("vicccccc")
        for v in vicini:
            print(v)
        vicinCompleti = []
        for v in vicini:
            vicinCompleti.append(self._idMap[v])
        vicinCompleti.sort(key=lambda x: x[1], reverse=True)
        return vicinCompleti