from math import gcd  # ! Importa gcd para verificar se dois números são coprimos.

# --- Aqui faremos a função para implementar o texto, pois este código está decifrando apenas números inteiros. ---




# --- Algoritmo de Euclides estendido
def egcd(a, b):                            # ? A linha 4 até a 14 precisará ser estudada
    if a == 0:
        return (b, 0, 1)
    g, y, x = egcd(b % a, a)
    return (g, x - (b // a) * y, y)

def modinv(a, m):
    g, x, y = egcd(a, m)
    if g != 1:
        raise Exception('Inverso modular não existe')
    return x % m  # já garante valor positivo em Python

# --- Parâmetros RSA de exemplo ---
p = 1000003 # ! Precisam ser coprimos entre si (primos são melhores).
q = 1000033
n = p * q
phi = (p - 1) * (q - 1) # ! função totiente de Euler

e = 65537

# Verifica se e é coprimo com phi
if gcd(e, phi) != 1:
    raise Exception("e não é coprimo com phi. Escolha outro valor para e.")

d = modinv(e, phi)  # ! Calcula o inverso modular de e mod phi (chave privada).

mensagem = int(input("Digite a mensagem (inteiro < n): "))

if mensagem >= n:  # ! MUITO IMPORTANTE: a mensagem deve ser menor que n.
    print("Erro: a mensagem deve ser menor que n.")
    exit(1)

cifrado = pow(mensagem, e, n) # ! Cifra com exponenciação modular eficiente: calcula (mensagem^e) mod n sem estourar o tamanho (muito melhor que (msg**e) % n).
print("Texto cifrado:", cifrado)

decifrado = pow(cifrado, d, n) # !Lê um número inteiro para cifrar. Importante: tem que ser 0 ≤ mensagem < n. (Se for texto, normalmente você converte para número/bytes ou divide em blocos.)
print("Texto decifrado:", decifrado)


