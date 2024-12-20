# https://leetcode.com/problems/multiply-strings/description/
# Algoritmo de karatsuba

# Código adaptado para usar Karatsuba internamente em binário como feito na aula,
# mas receber e retornar números em decimal. 

class Solution:
    def multiply(self, num1: str, num2: str) -> str:
        # Se um dos números é "0"
        if num1 == "0" or num2 == "0":
            return "0"
        
        # Função auxiliar para remover zeros à esquerda
        def remove_leading_zeros(s: str) -> str:
            s = s.lstrip('0')
            return s if s != '' else '0'

        # Somar duas strings binárias
        def add_binary(a: str, b: str) -> str:
            a = a[::-1]
            b = b[::-1]
            carry = 0
            result = []
            for i in range(max(len(a), len(b))):
                bit_a = int(a[i]) if i < len(a) else 0
                bit_b = int(b[i]) if i < len(b) else 0
                s = bit_a + bit_b + carry
                carry = s // 2
                result.append(str(s % 2))
            if carry:
                result.append('1')
            return remove_leading_zeros(''.join(result[::-1]))

        # Subtrair b de a (a >= b), strings binárias
        def subtract_binary(a: str, b: str) -> str:
            # assumindo a >= b
            a = a[::-1]
            b = b[::-1]
            carry = 0
            result = []
            for i in range(len(a)):
                bit_a = int(a[i])
                bit_b = int(b[i]) if i < len(b) else 0
                diff = bit_a - bit_b - carry
                if diff < 0:
                    diff += 2
                    carry = 1
                else:
                    carry = 0
                result.append(str(diff))
            res = ''.join(result[::-1])
            return remove_leading_zeros(res)

        # Multiplicação de bits (assumindo entradas de 1 bit)
        def multiply_bits(a: str, b: str) -> str:
            return '1' if (a == '1' and b == '1') else '0'

        # Igualar tamanhos com zeros à esquerda
        def pad_left(s: str, n: int) -> str:
            return '0'*n + s

        # Função principal Karatsuba em binário
        def karatsuba_bin(x: str, y: str) -> str:
            # remover zeros a esquerda
            x = remove_leading_zeros(x)
            y = remove_leading_zeros(y)

            # se um deles for 0, retorna 0
            if x == '0' or y == '0':
                return '0'

            # Tornar tamanhos iguais
            if len(x) < len(y):
                x = pad_left(x, len(y) - len(x))
            elif len(y) < len(x):
                y = pad_left(y, len(x) - len(y))

            n = len(x)

            # caso base: se tamanho = 1
            if n == 1:
                return multiply_bits(x, y)

            half = n // 2
            # Dividir x e y em metades
            a = x[:n-half]
            b = x[n-half:]
            c = y[:n-half]
            d = y[n-half:]

            # Calcular partes:
            ac = karatsuba_bin(a, c)
            bd = karatsuba_bin(b, d)

            # (a+b) e (c+d)
            ab = add_binary(a, b)
            cd = add_binary(c, d)
            abcd = karatsuba_bin(ab, cd)

            # ad + bc = abcd - ac - bd
            ad_bc = subtract_binary(subtract_binary(abcd, ac), bd)

            # resultado = ac * 2^(2*half) + (ad+bc) * 2^(half) + bd
            ac_2n = ac + '0'*(2*half) if ac != '0' else '0'
            ad_bc_2_half = ad_bc + '0'*(half) if ad_bc != '0' else '0'

            return remove_leading_zeros(add_binary(add_binary(ac_2n, ad_bc_2_half), bd))

        # Converte num1 e num2 para binário
        x_bin = bin(int(num1))[2:]
        y_bin = bin(int(num2))[2:]

        result_bin = karatsuba_bin(x_bin, y_bin)

        # Binario convertido para int
        return str(int(result_bin, 2))


def runTests():
    sol = Solution()

    # Teste 1
    num1_1, num2_1 = "2", "3"
    print("Test Case 1:")
    result1 = sol.multiply(num1_1, num2_1)
    print(f"Input: {num1_1} * {num2_1}")
    print("Result:", result1)

    # Teste 2
    num1_2, num2_2 = "123", "456"
    print("Test Case 2:")
    result2 = sol.multiply(num1_2, num2_2)
    print(f"Input: {num1_2} * {num2_2}")
    print("Result:", result2)

def main():
    runTests()

# if __name__ == "__main__":
#     main()
