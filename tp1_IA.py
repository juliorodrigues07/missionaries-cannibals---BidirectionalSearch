import networkx as nx
import matplotlib.pyplot as plt
from collections import OrderedDict
from queue import Queue


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

    # Lado em que está o barco
    boat_local = current_state[2]

    # Se o barco está na direta (1), obtém os índices de origem (direita) e destino (esquerda)
    # dos canibais e missionários no estado atual. Inverte as direções caso contrário (0).
    if boat_local:
        o_cannibals, o_missionaries, d_cannibals, d_missionaries = 3, 4, 0, 1
    else:
        o_cannibals, o_missionaries, d_cannibals, d_missionaries = 0, 1, 3, 4

    # Caso em que não há canibais, nem missionários para transportar
    if current_state[o_cannibals] == 0 and current_state[o_missionaries] == 0:
        return

    check = False

    # Transfere canibais e missionários de um lado para o outro se possível
    for i in range(min(n_cannibals, current_state[o_cannibals])):
        current_state[d_cannibals] += 1
        current_state[o_cannibals] -= 1
        check = True

    for i in range(min(n_missionaries, current_state[o_missionaries])):
        current_state[d_missionaries] += 1
        current_state[o_missionaries] -= 1
        check = True

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

        # Para casos em que o nº de missionários seja menor que o nº de canibais
        if (next_state[0] > next_state[1] and next_state[1] > 0) or \
           (next_state[3] > next_state[4] and next_state[4] > 0):
            continue

        # Caso em que o estado se repete
        if next_state in visited:
            continue

        # O estado válido é adicionado à lista e ao grafo
        reachable_states.append(next_state)
        graph.add_node(str(next_state))
        graph.add_edge(str(current_state), str(next_state))

    # Obtém os adjacentes de cada nó (chave) em uma lista (valores)
    adjacent[str(current_state)] = list(graph[str(current_state)])

    return reachable_states, graph


def bidirectional_search():

    begin_visited, begin_neighbour, begin_border, begin_queue = dict(), dict(), list(), Queue()
    end_visited, end_neighbour, end_border, end_queue = dict(), dict(), list(), Queue()
    middle_state = ""

    for node in adjacent.keys():
        begin_visited[node], end_visited[node] = False, False
        begin_neighbour[node], end_neighbour[node] = None, None

    begin_visited[str(begin)] = True
    end_visited[str(end)] = True
    begin_queue.put(begin)
    end_queue.put(end)

    # Buscas em largura partindo do estado inicial e também do objetivo
    while not begin_queue.empty() or not end_queue.empty():

        begin_state = begin_queue.get()
        end_state = end_queue.get()
        begin_border.append(begin_state)
        end_border.append(end_state)

        # Se um dos estados atuais das buscas está na borda do outro grafo, a busca encerra e a solução é encontrada
        if begin_state in end_border:
            middle_state = begin_state
            break

        if end_state in begin_border:
            middle_state = end_state
            break

        for i in adjacent[str(begin_state)]:
            if not begin_visited[i]:
                begin_visited[i] = True
                begin_neighbour[i] = str(begin_state)
                begin_queue.put(i)

        for i in adjacent[str(end_state)]:
            if not end_visited[i]:
                end_visited[i] = True
                end_neighbour[i] = str(end_state)
                end_queue.put(i)

    if middle_state == "":
        print("Não existe solução! O caminho entre" + str(begin) + " e " + str(end) + "não existe.\n")
        return

    begin_path, end_path = list(), list()
    begin_target = middle_state
    end_target = middle_state

    # Constrói os caminhos mais curtos do estado inicial e objetivo até o nó intermediário (Interseção)
    while begin_target is not None:
        begin_path.append(begin_target)
        begin_target = begin_neighbour[str(begin_target)]
    begin_path.reverse()

    while end_target is not None:
        end_path.append(end_target)
        end_target = end_neighbour[str(end_target)]

    return begin_path, end_path, middle_state


def print_solution(path):

    for i in range(len(path) - 1):

        if path[i][7] == '0':
            c = abs(int(path[i + 1][1]) - int(path[i][1]))
            m = abs(int(path[i + 1][4]) - int(path[i][4]))
            print("Viagem " + str(int(i + 1)) + ": " + str(c) + " canibais e "
                  + str(m) + " missionários para a direita  (->)\t Estado atual: " + path[i + 1] + "\n")

        else:
            c = abs(int(path[i][10]) - int(path[i + 1][10]))
            m = abs(int(path[i][13]) - int(path[i + 1][13]))
            print("Viagem " + str(int(i + 1)) + ": " + str(c) + " canibais e "
                  + str(m) + " missionários para a esquerda (<-)\t Estado atual: " + path[i + 1] + "\n")


def end_test(current_state):

    # Se atinge o estado objetivo
    if current_state[3] == 3 and current_state[4] == 3:
        return True
    else:
        return False


def main():
    # Construção do grafo
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

    # Obtém os adjacentes do nó objetivo
    adjacent[str(end)] = list(graph[str(end)])

    # Metades do caminho da solução final obtida pela busca bidirecional
    begin_path, end_path, middle_state = bidirectional_search()
    result = begin_path + end_path
    result = list(OrderedDict.fromkeys(result.copy()))

    # Imprime solução
    print_solution(result)

    # Executa os plots dos grafos de estados válidos e solução
    plt.figure("Estados válidos")
    nx.draw_networkx(graph, pos=nx.kamada_kawai_layout(graph),
                     node_color='skyblue', node_shape="s", linewidths=19, with_labels=True)
    plt.show()

    color_map = list()
    for node in graph:
        if node not in begin_path and node not in end_path:
            color_map.append('skyblue')
        elif node in begin_path and node not in end_path:
            color_map.append('yellow')
        elif node not in begin_path and node in end_path:
            color_map.append('red')
        else:
            color_map.append('green')

    plt.figure("Pós-aplicação da busca Bidirecional")
    nx.draw(graph, pos=nx.kamada_kawai_layout(graph),
            node_color=color_map, node_shape="s", linewidths=19, with_labels=True)
    plt.show()


if __name__ == '__main__':
    main()
