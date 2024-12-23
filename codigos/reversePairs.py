# https://leetcode.com/problems/reverse-pairs/description/
# Algoritmo do contagem de inversões


class Solution:
    def reversePairs(self, nums):
        # Função para realizar o merge sort e contar os pares reversos
        def merge_sort_and_count(start, end):
            # Caso base: se a sublista tiver um único elemento ou estiver vazia, não há pares reversos
            if start >= end:
                return 0

            # Dividimos o array no meio
            mid = (start + end) // 2
            # Contamos os pares reversos na metade esquerda, na metade direita e entre as duas metades
            count = merge_sort_and_count(start, mid) + merge_sort_and_count(mid + 1, end)

            # Contando os pares reversos entre as duas metades
            j = mid + 1
            for i in range(start, mid + 1):
                # Procuramos os elementos na segunda metade que satisfazem nums[i] > 2 * nums[j]
                while j <= end and nums[i] > 2 * nums[j]:
                    j += 1
                # Adicionamos ao contador o número de elementos que satisfazem a condição
                count += j - (mid + 1)

            # Realizamos o merge das duas metades
            temp = []
            i, j = start, mid + 1
            while i <= mid and j <= end:
                # Inserimos no array temporário o menor elemento entre as duas metades
                if nums[i] <= nums[j]:
                    temp.append(nums[i])
                    i += 1
                else:
                    temp.append(nums[j])
                    j += 1

            # Inserimos os elementos restantes da primeira metade, se houver
            while i <= mid:
                temp.append(nums[i])
                i += 1

            # Inserimos os elementos restantes da segunda metade, se houver
            while j <= end:
                temp.append(nums[j])
                j += 1

            # Copiamos os valores ordenados do array temporário de volta para o original
            for i in range(len(temp)):
                nums[start + i] = temp[i]

            return count

        # Chamamos a função de merge sort para o array inteiro
        return merge_sort_and_count(0, len(nums) - 1)

def runTests():
    sol = Solution()

    # Teste 1
    nums1 = [1, 3, 2, 3, 1]
    print("Test Case 1:")
    print(f"Input: {nums1}")
    result1 = sol.reversePairs(nums1)
    print("Result:", result1)

    # Teste 2
    nums2 = [2, 4, 3, 5, 1]
    print("Test Case 2:")
    print(f"Input: {nums2}")
    result2 = sol.reversePairs(nums2)
    print("Result:", result2)

    # Teste 3
    nums3 = [5, 4, 3, 2, 1]
    print("Test Case 3:")
    print(f"Input: {nums3}")
    result3 = sol.reversePairs(nums3)
    print("Result:", result3)

    # Teste 4
    nums4 = [1, 2, 3, 4, 5]
    print("Test Case 4:")
    print(f"Input: {nums4}")
    result4 = sol.reversePairs(nums4)
    print("Result:", result4)

def main():
    runTests()

# if __name__ == "__main__":
#     main()