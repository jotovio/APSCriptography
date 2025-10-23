from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_OAEP

# --- Gerar chaves (direto na memória) ---
key = RSA.generate(2048) # ! RSA.generate
private_key = key
public_key = key.publickey() # ! key.publickey

# --- Criptografar ---
def criptografar(mensagem, chave_publica):
    cipher = PKCS1_OAEP.new(chave_publica)  # ! PKCS1_OAEP.new
    return cipher.encrypt(mensagem.encode()) # ! cipher.encrypt , mensagem.encode()

# --- Descriptografar --
def descriptografar(criptografada, chave_privada):
    cipher = PKCS1_OAEP.new(chave_privada) 
    return cipher.decrypt(criptografada).decode() # ! cipher.decrypt , .decode()

# --- Programa principal ---
if __name__ == "__main__":
    msg = input("Digite a mensagem para criptografar: ")

    # Criptografar
    cifrada = criptografar(msg, public_key)
    print("\n🔒 Mensagem criptografada (bytes):", cifrada)

    # Descriptografar
    decifrada = descriptografar(cifrada, private_key)
    print("\n🔓 Mensagem decifrada:", decifrada)

    # ? Estudar todo o processo da biblioteca, tanto o de geração de chaves, quanto o de criptografia e descriptografia.
    # ? Verificar outras bibliotecas como PyCryptodome, cryptography, etc. (Para analisar qual é a melhor)