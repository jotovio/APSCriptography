from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_OAEP
import base64

# ---------- Funções úteis ----------

def gerar_chaves(bits: int = 2048):
    """Gera um par de chaves RSA (privada + pública) e retorna (priv, pub)."""
    chave_priv = RSA.generate(bits)
    chave_pub = chave_priv.publickey()
    return chave_priv, chave_pub 


def criptografar_texto(texto: str, chave_publica: RSA.RsaKey) -> str:
    """
    Criptografa uma string com RSA-OAEP e retorna o resultado em base64 (str).
    Usamos OAEP por ser o padding seguro.
    """
    cipher = PKCS1_OAEP.new(chave_publica) # ! PKCS1_OAEP
    bytes_cifrados = cipher.encrypt(texto.encode("utf-8")) # ! utf-8
    return base64.b64encode(bytes_cifrados).decode("utf-8")  # ! retorna base64 (texto)


def descriptografar_texto(b64_cifrado: str, chave_privada: RSA.RsaKey) -> str:
    """Descriptografa um texto em base64 usando a chave privada e retorna a string original."""
    cipher = PKCS1_OAEP.new(chave_privada) 
    bytes_cifrados = base64.b64decode(b64_cifrado.encode("utf-8")) # ! b64_cifrado.encode
    bytes_originais = cipher.decrypt(bytes_cifrados) 
    return bytes_originais.decode("utf-8")

# ---------- Exemplo de uso (interface simples) ----------
if __name__ == "__main__":
    # 1) Gerar chaves (ou você poderia carregar de arquivos com carregar_chave_pem)
    private_key, public_key = gerar_chaves()


    # 2) Ler mensagem do usuário

    iniciar = input("Deseja criptografar uma mensagem? (s/n): ").strip().lower()

    while iniciar == 's':

        mensagem = input("Digite a mensagem a ser criptografada: ").strip()

    # 3) Criptografar
        cifrada_b64 = criptografar_texto(mensagem, public_key)
        print("\n🔒 Mensagem criptografada (base64):")
        print(cifrada_b64)

    # 4) Descriptografar (para demonstrar)
        decifrada = descriptografar_texto(cifrada_b64, private_key)
        print("\n🔓 Mensagem decifrada:")
        print(decifrada)
        iniciar = input("\nDeseja criptografar outra mensagem? (s/n): ").strip().lower()

    print("Encerrando o programa.")


    # ? Criar código que pergunta se deseja criptografar ou descriptografar