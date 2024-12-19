# https://leetcode.com/problems/erect-the-fence/description/
# Algoritmo do par de pontos mais próximos + mediana das medianas

from typing import List
import concurrent.futures

class Solution:
    def outerTrees(self, trees: List[List[int]]) -> List[List[int]]:
        def cross(p: List[int], q: List[int], r: List[int]) -> int:
            """Produto vetorial entre os pontos p, q, r."""
            return (q[0] - p[0]) * (r[1] - q[1]) - (q[1] - p[1]) * (r[0] - q[0])

        def median_of_medians(points: List[List[int]]) -> List[int]:
            """Encontra o pivô usando Mediana das Medianas."""
            if len(points) <= 5:
                points.sort()
                return points[len(points) // 2]

            sublists = [points[i:i + 5] for i in range(0, len(points), 5)]
            medians = [sorted(sublist)[len(sublist) // 2] for sublist in sublists]
            return median_of_medians(medians)

        def closest_pair(points: List[List[int]]) -> List[List[int]]:
            """Função padrão para encontrar o Par Mais Próximo usando Divisão e Conquista."""
            points.sort(key=lambda x: x[0])

            def distance(p1, p2):
                return (p1[0] - p2[0])**2 + (p1[1] - p2[1])**2

            def closest_util(px: List[List[int]]) -> List[List[int]]:
                n = len(px)
                if n < 2:  # Retorna vazio se não houver pares suficientes
                    return []

                if n <= 3:  # Comparação direta para casos pequenos
                    return min([(px[i], px[j]) for i in range(n) for j in range(i + 1, n)],
                               key=lambda pair: distance(pair[0], pair[1]))

                mid = n // 2
                midpoint = px[mid]

                # Divide e Conquista
                dl = closest_util(px[:mid])
                dr = closest_util(px[mid:])
                d = min(distance(dl[0], dl[1]), distance(dr[0], dr[1]))

                # Checa a região central
                strip = [p for p in px if abs(p[0] - midpoint[0]) < d]
                strip.sort(key=lambda x: x[1])

                min_d = d
                closest_pair = dl if distance(dl[0], dl[1]) < distance(dr[0], dr[1]) else dr
                for i in range(len(strip)):
                    for j in range(i + 1, len(strip)):
                        if (strip[j][1] - strip[i][1])**2 >= min_d:
                            break
                        d_new = distance(strip[i], strip[j])
                        if d_new < min_d:
                            min_d = d_new
                            closest_pair = [strip[i], strip[j]]

                return closest_pair

            return closest_util(points)

        def parallel_find_closest_pair(points: List[List[int]]) -> List[List[int]]:
            """Função paralelizada para encontrar o Par Mais Próximo."""
            if len(points) < 2:  # Caso base: pontos insuficientes
                return []

            pivot = median_of_medians(points)
            left_points = [p for p in points if p[0] < pivot[0]]
            right_points = [p for p in points if p[0] >= pivot[0]]

            with concurrent.futures.ThreadPoolExecutor() as executor:
                futures = []
                if len(left_points) >= 2:
                    futures.append(executor.submit(closest_pair, left_points))
                if len(right_points) >= 2:
                    futures.append(executor.submit(closest_pair, right_points))

                results = [f.result() for f in futures]

            # Filtra resultados não vazios
            valid_results = [pair for pair in results if pair]

            if not valid_results:  # Se não houver pares válidos
                return []

            # Combina os resultados
            return min(valid_results, key=lambda pair: (pair[0][0] - pair[1][0])**2 + (pair[0][1] - pair[1][1])**2)

        # Ordena os pontos para o Convex Hull
        trees.sort(key=lambda x: (x[0], x[1]))

        # Encontra o par mais próximo de forma paralelizada
        closest_points = parallel_find_closest_pair(trees)
        if closest_points:
            print("Par de Pontos Mais Próximos:", closest_points)
        else:
            print("Nenhum par de pontos encontrados.")

        # Construção do Hull
        lower = []
        for p in trees:
            while len(lower) >= 2 and cross(lower[-2], lower[-1], p) < 0:
                lower.pop()
            lower.append(p)

        upper = []
        for p in reversed(trees):
            while len(upper) >= 2 and cross(upper[-2], upper[-1], p) < 0:
                upper.pop()
            upper.append(p)

        # Junta os dois lados e remove duplicatas
        return list(map(list, set(map(tuple, lower + upper))))


def runTests():
    sol = Solution()

    # Teste 1
    trees1 = [[1,1],[2,2],[2,0],[2,4],[3,3],[4,2]]
    print("Test Case 1:")
    result1 = sol.outerTrees(trees1)
    print("Result:", result1)

    # Teste 2
    trees2 = [[1,2],[2,2],[4,2]]
    print("Test Case 2:")
    result2 = sol.outerTrees(trees2)
    print("Result:", result2)

def main():
    runTests()

# if __name__ == "__main__":
#     main()
