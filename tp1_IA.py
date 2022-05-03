import networkx as nx
import matplotlib.pyplot as plt

# Estado inicial -> 3 canibais, 3 missionários e o barco no lado esquerdo, e nada no lado esquerdo do rio
begin = [3, 3, 0, 0, 0]

# Estado final -> Nada no lado esquerdo do rio e 3 canibais, 3 missionários e o barco do lardo direito
end = [0, 0, 1, 3, 3]

# (nº de canibais, nº de missionários) em cada viagem
actions = [(0, 1), (0, 2), (1, 0), (2, 0), (1, 1)]
limit = 2

visited = list()
adjacent = dict()


def move_boat(current_state, n_cannibals, n_missionaries):

    # O número de pessoas no barco não pode ultrapassar 2
    if n_cannibals + n_missionaries > limit:
        return

    boat_local = current_state[2]

    # Se o barco está na direta (1), obtém os índices de origem (direita) e destino (esquerda)
    # dos canibais e missionários no estado atual. Inverte as direções caso contrário (0).
    if boat_local:
        o_cannibals = 3
        o_missionaries = 4
        d_cannibals = 0
        d_missionaries = 1
    else:
        o_cannibals = 0
        o_missionaries = 1
        d_cannibals = 3
        d_missionaries = 4

    # Caso em que não há canibais, nem missionários para transportar
    if current_state[o_cannibals] == 0 and current_state[o_missionaries] == 0:
        return

    check = 0

    # Transfere canibais e missionários de um lado para o outro se possível
    for i in range(min(n_cannibals, current_state[o_cannibals])):
        current_state[d_cannibals] += 1
        current_state[o_cannibals] -= 1
        check = 1

    for i in range(min(n_missionaries, current_state[o_missionaries])):
        current_state[d_missionaries] += 1
        current_state[o_missionaries] -= 1
        check = 1

    # Altera o lado do rio em que o barco está
    if check:
        current_state[2] = 1 - current_state[2]

    return current_state


def valid_states(current_state, graph):

    reachable_states = list()

    # Para cada ação válida
    for (n_cannibals, n_missionaries) in actions:

        # Obtém o próximo estado possível
        next_state = move_boat(current_state.copy(), n_cannibals, n_missionaries)

        # Para casos em que o nº de missionários fique menor que o nº de canibais
        if (next_state[0] > next_state[1] and next_state[1] > 0) or \
           (next_state[3] > next_state[4] and next_state[4] > 0):
            continue

        # Caso em que o estado se repete
        if next_state in visited:
            continue

        # O estado válido é adicionado à lista
        reachable_states.append(next_state)
        graph.add_node(str(next_state))
        graph.add_edge(str(current_state), str(next_state))

    # Obtém os adjacentes de cada nó (chave) em uma lista (valores)
    adjacent[str(current_state)] = list(graph[str(current_state)])
    return reachable_states, graph


def end_test(current_state):

    if current_state[3] == 3 and current_state[4] == 3:
        return True
    else:
        return False


def bidirectional_search():

    begin_visited, begin_queue, begin_border = list(), list(), list()
    end_visited, end_queue, end_border = list(), list(), list()

    begin_visited.append(begin)
    end_visited.append(end)
    begin_queue.append(begin)
    end_queue.append(end)

    # Enquanto há nós para visitar
    while begin_queue or end_queue:

        begin_node = begin_queue.pop(0)
        end_node = end_queue.pop(0)
        begin_border.append(begin_node)
        end_border.append(end_node)

        # Testa se os caminhos percorridos pelas buscas já se encontraram
        if begin_node in end_border or end_node in begin_border:
            break

        # Expansão em largura dos nós adjacentes a partir do estado inicial e final
        for adj in adjacent[str(begin_node)]:
            if adj not in begin_visited:
                begin_visited.append(adj)
                begin_queue.append(adj)

        for adj in adjacent[str(end_node)]:
            if adj not in end_visited:
                end_visited.append(adj)
                end_queue.append(adj)

    return begin_border + end_border


# TODO: Plot do grafo e solução

if __name__ == '__main__':

    graph = nx.Graph()
    graph.add_node(str(begin))
    visited.append(begin)
    reachable_states, graph = valid_states(begin, graph.copy())

    # Enquanto o estado solução não é gerado, o grafo é construído combinando os estados válidos possíveis
    while not end_test(reachable_states[0]):

        # Próximo estado na lista é marcado como visitado
        next_state = reachable_states[0]
        visited.append(next_state)

        # Geração dos estados
        aux, graph = valid_states(next_state, graph.copy())
        reachable_states += aux
        reachable_states.pop(0)

    # Obtém os adjacentes do nó objeetivo
    adjacent[str(end)] = list(graph[str(end)])

    result = bidirectional_search()
    print(result)

    plt.figure(1)
    nx.draw_networkx(graph, pos = nx.spring_layout(graph), with_labels = True)
    plt.show()
