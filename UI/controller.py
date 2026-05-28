import flet as ft


class Controller:
    def __init__(self, view, model):
        # the view, with the graphical elements of the UI
        self._view = view
        # the model, which implements the logic of the program and holds the data
        self._model = model
        self.anni = self._model.getAnni()


    def handleCreaGrafo(self, e):
        self._model.creaGrafo()
        self._view._btnDettagli.disabled = False
        self._view.update_page()


    def handleDettagli(self, e):
        scelta = self._view._ddSquadra.value
        print(f"{scelta} la sceltaaaaaaaa")
        if scelta:
            vicini = self._model.getVicini(scelta)
            self._view._txt_result.controls.clear()
            for nomeSquadra, stipendio in vicini:
                self._view._txt_result.controls.append(ft.Text(f"salario totale giocatori {nomeSquadra}"
                                                               f" del team : {stipendio}"))

            self._view.update_page()
            return

        else:
            print("seleziona squadra")
            return


    def handlePercorso(self, e):
        scelta = self._view._ddSquadra.value
        lista, score = self._model.getPercorsoPeso(scelta)
        print(f"peso del percorso {score}, di seguito il percorso stampato")
        for l in lista:
            print(l)


    def handleAnno(self, e):
        scelta = self._view._ddAnno.value
        print(scelta)
        #stampare il numero di
        #squadre (teams) che ha giocato in tale anno, e l’elenco
        #delle rispettive sigle, nella prima area di testo
        #(txtSquadre). Nello stesso momento occorre
        #aggiornare il contenuto della tendina “Squadre”.
        tupleSquadreAnnoX = self._model.getSquadre(int(scelta))
        if tupleSquadreAnnoX:
            numero = len(tupleSquadreAnnoX)
            self._view._txtOutSquadre.controls.clear()
            self._view._txtOutSquadre.controls.append(ft.Text(f"anno: {scelta}; numero squadre: {numero}"))
            self._view._ddSquadra.options.clear()
            for codice, nome, salarioTotale in tupleSquadreAnnoX:
                self._view._txtOutSquadre.controls.append(ft.Text(f"{codice} - {nome} - {salarioTotale}"))
                self._view._ddSquadra.options.append(ft.dropdown.Option(key = codice, text = f"{codice} - {nome}"))

        else:
            self._view._txt_result.controls.clear()
            self._view._txt_result.controls.append(ft.Text("Nessuna squadra per l'anno selezionato!", color="red"))
            self._view.update_page()
            return
        self._view._btnCreaGrafo.disabled = False
        self._view.update_page()
        return
