class Solution:
    def multiply(self, num1: str, num2: str) -> str:
        # Primeiro, lidamos com casos simples
        if num1 == "0" or num2 == "0":
            return "0"
        
        # Função para remover zeros a esquerda
        def remove_leading_zeros(s: str) -> str:
            return s.lstrip('0') or "0"
        
        # Função para somar duas strings de números
        def add_strings(a: str, b: str) -> str:
            a = a[::-1]
            b = b[::-1]
            carry = 0
            result = []
            
            for i in range(max(len(a), len(b))):
                digit_a = int(a[i]) if i < len(a) else 0
                digit_b = int(b[i]) if i < len(b) else 0
                s = digit_a + digit_b + carry
                carry = s // 10
                result.append(str(s % 10))
            
            if carry > 0:
                result.append(str(carry))
            
            return ''.join(result[::-1])
        
        # Função para subtrair duas strings de números (assumimos a >= b sem zeros a esquerda indevidos)
        def subtract_strings(a: str, b: str) -> str:
            a = a[::-1]
            b = b[::-1]
            carry = 0
            result = []
            
            for i in range(len(a)):
                digit_a = int(a[i])
                digit_b = int(b[i]) if i < len(b) else 0
                diff = digit_a - digit_b - carry
                if diff < 0:
                    diff += 10
                    carry = 1
                else:
                    carry = 0
                result.append(str(diff))
            
            # Remover zeros a esquerda do resultado
            res = ''.join(result[::-1])
            return remove_leading_zeros(res)
        
        # Função para multiplicação simples (entre números pequenos)
        def simple_multiply(a: str, b: str) -> str:
            a = a[::-1]
            b = b[::-1]
            result = [0]*(len(a)+len(b))
            
            for i in range(len(a)):
                for j in range(len(b)):
                    mul = int(a[i]) * int(b[j])
                    result[i+j] += mul
                    result[i+j+1] += result[i+j] // 10
                    result[i+j] = result[i+j] % 10
            
            # remover zeros a esquerda
            while len(result) > 1 and result[-1] == 0:
                result.pop()
            
            return ''.join(str(x) for x in result[::-1])
        
        # Pad de zeros a esquerda para igualar o tamanho
        def pad_zeros(s: str, n: int) -> str:
            return '0'*n + s
        
        # Karatsuba recursivo
        def karatsuba(x: str, y: str) -> str:
            # remover zeros a esquerda
            x = remove_leading_zeros(x)
            y = remove_leading_zeros(y)
            
            # se um deles for "0", resultado é "0"
            if x == "0" or y == "0":
                return "0"
            
            # Tornar os comprimentos iguais
            if len(x) < len(y):
                x = pad_zeros(x, len(y)-len(x))
            elif len(y) < len(x):
                y = pad_zeros(y, len(x)-len(y))
            
            n = len(x)
            # Se o tamanho for pequeno, usar multiplicação simples
            if n == 1:
                return str(int(x)*int(y))
            
            half = n // 2
            
            # Dividir em metades
            a = x[:n-half]
            b = x[n-half:]
            c = y[:n-half]
            d = y[n-half:]
            
            # ac = karatsuba(a,c)
            ac = karatsuba(a, c)
            # bd = karatsuba(b,d)
            bd = karatsuba(b, d)
            # (a+b)*(c+d)
            ab = add_strings(a, b)
            cd = add_strings(c, d)
            abcd = karatsuba(ab, cd)
            
            # ad + bc = abcd - ac - bd
            adbc = subtract_strings(subtract_strings(abcd, ac), bd)
            
            # resultado = ac * 10^(2*half) + adbc * 10^(half) + bd
            ac_10 = ac + '0'*(2*half) if ac != "0" else "0"
            adbc_10 = adbc + '0'*(half) if adbc != "0" else "0"
            
            result = add_strings(add_strings(ac_10, adbc_10), bd)
            return remove_leading_zeros(result)
        
        # Chamar Karatsuba e retornar o resultado
        return karatsuba(num1, num2)


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