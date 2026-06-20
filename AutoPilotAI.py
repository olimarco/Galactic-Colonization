from DataStructures import HashTable
from GameModels import Sector

class AutoPilotAI:
   
    def __init__(self, universe):
        self.universe = universe
    
    def calculate_next_move(self, current, fuel_left):
        visitati = HashTable(50)
        visitati.put(current.id, True)

        archi_adiacenti = self.universe.core_graph.get_adjacent_vertices(current)
        if archi_adiacenti is None:
            return None

        miglior_mossa = None
        miglior_risorse = -1

        # Prova ogni vicino come possibile prima mossa
        arco = archi_adiacenti.head
        while arco is not None:
            nodo_successivo = arco.data.destination
            costo = arco.data.weight

            if costo <= fuel_left and nodo_successivo.resources != 0:
                carburante_dopo = fuel_left - costo

                pericolo = 1.0 - (nodo_successivo.danger_level / 100.0)
                risorse_pesate = nodo_successivo.resources * pericolo

                visitati.put(nodo_successivo.id, True)
                risorse_totali = risorse_pesate + self._backtracking(nodo_successivo, carburante_dopo, visitati)
                visitati.put(nodo_successivo.id, False)

                if risorse_totali > miglior_risorse:
                    miglior_risorse = risorse_totali
                    miglior_mossa = nodo_successivo
                    
            arco = arco.next

        return miglior_mossa
    
    def _backtracking(self, settore, carburante, visitati):
        
        if carburante <= 0:
            return 0

        archi = self.universe.core_graph.get_adjacent_vertices(settore)
        if archi is None:
            return 0

        migliore = 0
        arco = archi.head
        while arco is not None:
            nodo_successivo = arco.data.destination
            costo = arco.data.weight

        if costo <= carburante and visitati.get(nodo_successivo.id) is not True:
            carburante_dopo = carburante - costo

            fattore_sicurezza = 1.0 - (nodo_successivo.danger_level / 100.0)
            risorse_pesate = nodo_successivo.resources * fattore_sicurezza

            visitati.put(nodo_successivo.id, True)
            risorse = risorse_pesate + self._backtracking(nodo_successivo, carburante_dopo, visitati)
            visitati.put(nodo_successivo.id, False)

            if risorse > migliore:
                migliore = risorse
            arco = arco.next

        return migliore