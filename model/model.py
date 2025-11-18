from database.impianto_DAO import ImpiantoDAO

'''
    MODELLO:
    - Rappresenta la struttura dati
    - Si occupa di gestire lo stato dell'applicazione
    - Interagisce con il database
'''

class Model:
    def __init__(self):
        self._impianti = None
        self.load_impianti()

        self.__sequenza_ottima = []
        self.__costo_ottimo = -1

    def load_impianti(self):
        """ Carica tutti gli impianti e li setta nella variabile self._impianti """
        self._impianti = ImpiantoDAO.get_impianti()

    def get_consumo_medio(self, mese:int):
        """
        Calcola, per ogni impianto, il consumo medio giornaliero per il mese selezionato.
        :param mese: Mese selezionato (un intero da 1 a 12)
        :return: lista di tuple --> (nome dell'impianto, media), es. (Impianto A, 123)
        """
        # TODO
        risultati = []
        for impianto in self._impianti:
            consumi = impianto.get_consumi()
            if not consumi:
                risultati.append((impianto.nome, 0))
                continue
            consumi_mese = [c for c in consumi if c.data.month == mese]
            if not consumi_mese:
                risultati.append((impianto.nome, 0))
                continue

            somma_kwh = sum(c.kwh for c in consumi_mese)
            giorni = len(consumi_mese)
            media = somma_kwh / giorni

            risultati.append((impianto.nome, media))

    def get_sequenza_ottima(self, mese:int):
        """
        Calcola la sequenza ottimale di interventi nei primi 7 giorni
        :return: sequenza di nomi impianto ottimale
        :return: costo ottimale (cioè quello minimizzato dalla sequenza scelta)
        """
        self.__sequenza_ottima = []
        self.__costo_ottimo = -1
        consumi_settimana = self.__get_consumi_prima_settimana_mese(mese)

        self.__ricorsione([], 1, None, 0, consumi_settimana)

        # Traduci gli ID in nomi
        id_to_nome = {impianto.id: impianto.nome for impianto in self._impianti}
        sequenza_nomi = [f"Giorno {giorno}: {id_to_nome[i]}" for giorno, i in enumerate(self.__sequenza_ottima, start=1)]
        return sequenza_nomi, self.__costo_ottimo

    def __ricorsione(self, sequenza_parziale, giorno, ultimo_impianto, costo_corrente, consumi_settimana):
        """ Implementa la ricorsione """
        # TODO

        if giorno==8:
            if self.__costo_ottimo == -1 or costo_corrente < self.__costo_ottimo:
                self.__costo_ottimo = costo_corrente
                self.__sequenza_ottima = sequenza_parziale.copy()
            return

        for impianto in self._impianti:
            costo_giorno = consumi_settimana[impianto.id][giorno-1]

            if ultimo_impianto is not None and ultimo_impianto != impianto.id:
                costo_giorno += 5

            nuovo_costo = costo_corrente + costo_giorno

            if self.__costo_ottimo != -1 and nuovo_costo > self.__costo_ottimo:
                continue
            sequenza_parziale.append(impianto.id)

            self.__ricorsione(sequenza_parziale, giorno+1, impianto.id, nuovo_costo, consumi_settimana, consumi_settimana)

            sequenza_parziale.pop()

    def __get_consumi_prima_settimana_mese(self, mese: int):
        """
        Restituisce i consumi dei primi 7 giorni del mese selezionato per ciascun impianto.
        :return: un dizionario: {id_impianto: [kwh_giorno1, ..., kwh_giorno7]}
        """
        # TODO
        consumi = {}
        for impianto in self._impianti:
            lista = impianto.get_consumi()

            consumi_mese = [c for c in lista if c.data.month == mese]
            giorno_to_kwh = {c.data.day: c.kwh for c in consumi_mese}

            kwh_settimana = []
            for g in range(1,8):
                kwh_settimana.append(giorno_to_kwh.get(g,0))
            consumi[impianto.id] = kwh_settimana

        return consumi

