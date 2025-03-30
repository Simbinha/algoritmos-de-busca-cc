# Exemplo de grafo (mapa) representando cidades da Romênia e suas distâncias
graph = {
    'Arad': {'Zerind': 75, 'Sibiu': 140, 'Timisoara': 118},
    'Zerind': {'Arad': 75, 'Oradea': 71},
    'Oradea': {'Zerind': 71, 'Sibiu': 151},
    'Sibiu': {'Arad': 140, 'Oradea': 151, 'Fagaras': 99, 'RimnicuVilcea': 80},
    'Timisoara': {'Arad': 118, 'Lugoj': 111},
    'Lugoj': {'Timisoara': 111, 'Mehadia': 70},
    'Mehadia': {'Lugoj': 70, 'Drobeta': 75},
    'Drobeta': {'Mehadia': 75, 'Craiova': 120},
    'Craiova': {'Drobeta': 120, 'RimnicuVilcea': 146, 'Pitesti': 138},
    'RimnicuVilcea': {'Sibiu': 80, 'Craiova': 146, 'Pitesti': 97},
    'Fagaras': {'Sibiu': 99, 'Bucharest': 211},
    'Pitesti': {'RimnicuVilcea': 97, 'Craiova': 138, 'Bucharest': 101},
    'Bucharest': {'Fagaras': 211, 'Pitesti': 101, 'Giurgiu': 90, 'Urziceni': 85},
    'Giurgiu': {'Bucharest': 90},
    'Urziceni': {'Bucharest': 85, 'Hirsova': 98, 'Vaslui': 142},
    'Hirsova': {'Urziceni': 98, 'Eforie': 86},
    'Eforie': {'Hirsova': 86},
    'Vaslui': {'Urziceni': 142, 'Iasi': 92},
    'Iasi': {'Vaslui': 92, 'Neamt': 87},
    'Neamt': {'Iasi': 87}
}

def validate_input(start, end):
    """Valida se as cidades de origem e destino existem no grafo"""
    if start not in graph or end not in graph:
        print("Cidade de partida ou chegada inválida. Verifique os nomes.")
        return False
    return True

def calculate_total_cost(path):
    """Calcula o custo total de um caminho"""
    if not path or len(path) < 2:
        return 0
    
    total_cost = 0
    for i in range(len(path) - 1):
        current = path[i]
        next_city = path[i + 1]
        total_cost += graph[current][next_city]
    return total_cost

# // Busca em Largura (BFS): Explora todos os vizinhos do nó atual antes de avançar.
# // Encontra o caminho com menor número de passos, mas não necessariamente o de menor custo.
def bfs(start, end):
    if not validate_input(start, end):
        return None
        
    queue = [(start, [start])]  # (nó, caminho)
    visited = set()
    
    while queue:
        node, path = queue.pop(0)  # remove o primeiro da fila (FIFO)
        
        if node == end:
            return {
                'path': path,
                'cost': calculate_total_cost(path)
            }
        
        if node not in visited:
            visited.add(node)
            for neighbor in graph[node]:
                if neighbor not in visited:
                    queue.append((neighbor, path + [neighbor]))
    
    return None

# // Busca em Profundidade (DFS): Explora o caminho até o máximo possível antes de voltar.
# // Útil para encontrar soluções quando o fator de ramificação é grande.
def dfs(start, end, path=None, visited=None, cost=0):
    if path is None:
        path = []
    if visited is None:
        visited = set()
        
    path.append(start)
    
    if start == end:
        return {'path': path.copy(), 'cost': cost}
    
    visited.add(start)
    
    for neighbor in graph[start]:
        if neighbor not in visited:
            result = dfs(neighbor, end, path, visited, cost + graph[start][neighbor])
            if result:
                return result
    
    path.pop()
    return None

# // Busca de Custo Uniforme (UCS): Explora os caminhos por ordem de custo crescente.
# // Garante encontrar o caminho com menor custo total.
def ucs(start, end):
    if not validate_input(start, end):
        return None
        
    import heapq  # Para fila de prioridade
    
    # (custo, contador, nó, caminho)
    # contador é usado para desempatar custos iguais
    queue = [(0, 0, start, [start])]
    visited = set()
    counter = 1
    
    while queue:
        cost, _, node, path = heapq.heappop(queue)
        
        if node == end:
            return {
                'path': path,
                'cost': cost
            }
        
        if node not in visited:
            visited.add(node)
            for neighbor in graph[node]:
                if neighbor not in visited:
                    new_cost = cost + graph[node][neighbor]
                    new_path = path + [neighbor]
                    heapq.heappush(queue, (new_cost, counter, neighbor, new_path))
                    counter += 1
    
    return None

# // Busca em Profundidade Limitada (DLS): DFS com limite de profundidade máxima.
# // Evita que DFS entre em caminhos muito profundos ou ciclos.
def dls(start, end, limit, path=None, visited=None, cost=0):
    if path is None:
        path = []
    if visited is None:
        visited = set()
        
    path.append(start)
    
    if start == end:
        return {'path': path.copy(), 'cost': cost}
    
    if limit <= 0:
        path.pop()
        return None
    
    visited.add(start)
    
    for neighbor in graph[start]:
        if neighbor not in visited:
            result = dls(neighbor, end, limit - 1, path, visited, cost + graph[start][neighbor])
            if result:
                return result
    
    path.pop()
    visited.remove(start)  # Importante remover ao retroceder para permitir outros caminhos
    return None

# // Busca de Aprofundamento Iterativo (IDDFS): Executa DLS com profundidade crescente.
# // Combina as vantagens de BFS (garantia de encontrar solução ótima em passos) e DFS (baixo consumo de memória).
def iddfs(start, end, max_depth):
    if not validate_input(start, end):
        return None
        
    for depth in range(max_depth + 1):
        result = dls(start, end, depth)
        if result:
            return result
    
    return None

# // Heurística: Distância estimada até o destino (neste caso, Bucharest)
def heuristic(city, end):
    # Valores heurísticos para Bucharest como destino
    heuristic_values = {
        'Arad': 366,
        'Zerind': 374,
        'Oradea': 380,
        'Sibiu': 253,
        'Timisoara': 329,
        'Lugoj': 244,
        'Mehadia': 241,
        'Drobeta': 242,
        'Craiova': 160,
        'RimnicuVilcea': 193,
        'Fagaras': 176,
        'Pitesti': 100,
        'Bucharest': 0,
        'Giurgiu': 77,
        'Urziceni': 80,
        'Hirsova': 151,
        'Eforie': 161,
        'Vaslui': 199,
        'Iasi': 226,
        'Neamt': 234
    }
    # Se o destino não for Bucharest, usamos valores fictícios 
    # (nesse caso, as heurísticas originais não fariam sentido)
    if end != 'Bucharest':
        return 0
    return heuristic_values.get(city, 0)

# // Busca Gulosa (Greedy Best-First Search): Escolhe sempre o nó mais próximo do objetivo.
# // Rápida, mas não garante caminho ótimo.
def greedy_best_first_search(start, end):
    if not validate_input(start, end):
        return None
        
    import heapq
    
    # (valor_heurístico, contador, nó, caminho)
    queue = [(heuristic(start, end), 0, start, [start])]
    visited = set()
    counter = 1
    
    while queue:
        _, _, node, path = heapq.heappop(queue)
        
        if node == end:
            return {
                'path': path,
                'cost': calculate_total_cost(path)
            }
        
        if node not in visited:
            visited.add(node)
            for neighbor in graph[node]:
                if neighbor not in visited:
                    h_value = heuristic(neighbor, end)
                    heapq.heappush(queue, (h_value, counter, neighbor, path + [neighbor]))
                    counter += 1
    
    return None

# // A* (A-Star): Combina custo real do caminho com heurística.
# // Garante o caminho ótimo se a heurística for admissível.
def a_star(start, end):
    if not validate_input(start, end):
        return None
    
    import heapq
    
    # Conjunto aberto com nós a explorar: (f_score, contador, nó)
    open_set = [(heuristic(start, end), 0, start)]
    # Para desempate quando os f_scores são iguais
    counter = 1
    
    # Dicionários para controle
    came_from = {}
    g_score = {city: float('infinity') for city in graph}
    g_score[start] = 0
    f_score = {city: float('infinity') for city in graph}
    f_score[start] = heuristic(start, end)
    
    # Conjunto para verificar se um nó está no conjunto aberto
    open_set_hash = {start}
    
    while open_set_hash:
        # Pega o nó com menor f_score
        _, _, current = heapq.heappop(open_set)
        open_set_hash.remove(current)
        
        if current == end:
            # Reconstruir caminho
            path = [current]
            while current in came_from:
                current = came_from[current]
                path.insert(0, current)
            return {'path': path, 'cost': g_score[end]}
        
        for neighbor in graph[current]:
            # Calcula novo g_score
            tentative_g_score = g_score[current] + graph[current][neighbor]
            
            if tentative_g_score < g_score[neighbor]:
                # Este caminho para o vizinho é melhor
                came_from[neighbor] = current
                g_score[neighbor] = tentative_g_score
                f_score[neighbor] = tentative_g_score + heuristic(neighbor, end)
                
                if neighbor not in open_set_hash:
                    # Adiciona à fila de prioridade
                    heapq.heappush(open_set, (f_score[neighbor], counter, neighbor))
                    counter += 1
                    open_set_hash.add(neighbor)
    
    return None

# Função para exibir resultados
def display_result(result):
    if not result:
        print("Caminho não encontrado")
        return
    
    print("Caminho:", " -> ".join(result['path']))
    print(f"Custo total: {result['cost']} km")

# Função para executar algoritmos com entrada do usuário
def run_algorithm(algorithm_name):
    start = input("Cidade de partida: ")
    end = input("Cidade de destino: ")
    
    result = None
    
    if algorithm_name == 'bfs':
        result = bfs(start, end)
    elif algorithm_name == 'dfs':
        result = dfs(start, end)
    elif algorithm_name == 'ucs':
        result = ucs(start, end)
    elif algorithm_name == 'dls':
        limit = int(input("Digite o limite de profundidade: ") or 3)
        result = dls(start, end, limit)
    elif algorithm_name == 'iddfs':
        max_depth = int(input("Digite o limite máximo de profundidade: ") or 10)
        result = iddfs(start, end, max_depth)
    elif algorithm_name == 'greedy':
        result = greedy_best_first_search(start, end)
    elif algorithm_name == 'astar':
        result = a_star(start, end)
    
    display_result(result)

# Interface de texto simples
def main():
    print("Algoritmos de Busca em Grafos - Cidades da Romênia")
    print("=" * 50)
    
    while True:
        print("\nEscolha um algoritmo:")
        print("1. BFS - Busca em Largura")
        print("2. DFS - Busca em Profundidade")
        print("3. UCS - Busca de Custo Uniforme")
        print("4. DLS - Busca em Profundidade Limitada")
        print("5. IDDFS - Busca de Aprofundamento Iterativo")
        print("6. Greedy - Busca Gulosa")
        print("7. A* - A-Star")
        print("0. Sair")
        
        choice = input("Opção: ")
        
        if choice == '0':
            break
        elif choice == '1':
            run_algorithm('bfs')
        elif choice == '2':
            run_algorithm('dfs')
        elif choice == '3':
            run_algorithm('ucs')
        elif choice == '4':
            run_algorithm('dls')
        elif choice == '5':
            run_algorithm('iddfs')
        elif choice == '6':
            run_algorithm('greedy')
        elif choice == '7':
            run_algorithm('astar')
        else:
            print("Opção inválida.")

if __name__ == "__main__":
    main()
