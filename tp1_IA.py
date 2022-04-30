import networkx as nx

# (nº de canibais, nº de missionários) em cada viagem
actions = [(0, 1), (0, 2), (1, 0), (2, 0), (1, 1)]

# Estado inicial -> 3 canibais, 3 missionários e o barco no lado esquedo, e nada no lado direito do rio
begin = [3, 3, 0, 0, 0]

# TODO: Gerar as combinações de estados possíveis
# TODO: Implementação do método busca (largura ou profundidade)
# TODO: Adaptar para busca bidirecional
# TODO: Plot do grafo e solução
