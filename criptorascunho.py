from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_OAEP
import base64
import os
from typing import Optional

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


# ---------- Persistência de chaves (para reutilizar entre execuções) ----------
def salvar_chave_privada(chave_privada: RSA.RsaKey, caminho: str) -> None:
    with open(caminho, "wb") as f:
        f.write(chave_privada.export_key("PEM"))


def salvar_chave_publica(chave_publica: RSA.RsaKey, caminho: str) -> None:
    with open(caminho, "wb") as f:
        f.write(chave_publica.export_key("PEM"))


def carregar_chave_privada(caminho: str) -> RSA.RsaKey:
    with open(caminho, "rb") as f:
        dados = f.read()
    return RSA.import_key(dados)


def carregar_chave_publica(caminho: str) -> RSA.RsaKey:
    with open(caminho, "rb") as f:
        dados = f.read()
    return RSA.import_key(dados)

# ---------- Exemplo de uso (interface simples) ----------
if __name__ == "__main__":
    # Tenta reutilizar chaves salvas para permitir descriptografia de mensagens antigas
    priv_path = "private.pem"
    pub_path = "public.pem"

    private_key: Optional[RSA.RsaKey] = None
    public_key: Optional[RSA.RsaKey] = None

    if os.path.exists(priv_path) and os.path.exists(pub_path):
        usar_existentes = input("Chaves existentes detectadas. Usar as chaves salvas? (s/n): ").strip().lower()
        if usar_existentes == 's':
            try:
                private_key = carregar_chave_privada(priv_path)
                public_key = carregar_chave_publica(pub_path)
                print("Chaves carregadas com sucesso.")
            except Exception as e:
                print("Falha ao carregar chaves salvas, gerando novas...", e)

    if private_key is None or public_key is None:
        private_key, public_key = gerar_chaves()
        try:
            salvar_chave_privada(private_key, priv_path)
            salvar_chave_publica(public_key, pub_path)
            print("Novas chaves geradas e salvas em 'private.pem' e 'public.pem'.")
        except Exception as e:
            print("Aviso: não foi possível salvar as chaves no disco:", e)

    # guarda a última mensagem cifrada na sessão (None se não houver)
    last_arquivo: Optional[str] = None
    cifrada_b64: Optional[str] = None

    iniciar = input("Deseja criptografar uma mensagem? (s/n): ").strip().lower()

    while iniciar == 's':
        print("""
                Criptografia em RSA-OAEP
                Criptografar - 1
                Decriptografar - 2
                Sair - 3
              """ + 20*"-")
        
        input_opcao = input("Escolha uma opção (1/2/3): ").strip()

        # ! salvar mensagem original (substitui/ou cria o arquivo)

        if input_opcao == '1':
            arquivo = input("Digite o nome do arquivo para salvar a mensagem criptografada: ").strip()
            last_arquivo = arquivo

            mensagem = input("Digite a mensagem a ser criptografada: ").strip()

            # salvar mensagem original (substitui/ou cria o arquivo)
            with open(arquivo, "w", encoding="utf-8") as f:
                f.write("Mensagem original:\n")
                f.write(mensagem + "\n\n")

            cifrada_b64 = criptografar_texto(mensagem, public_key)
            print("\n🔒 Mensagem criptografada (base64):")
            print(cifrada_b64)

            # acrescentar a versão criptografada ao arquivo
            with open(arquivo, "a", encoding="utf-8") as f:
                f.write("Mensagem criptografada (base64):\n")
                f.write(cifrada_b64 + "\n\n")

        elif input_opcao == '2':
            # Solicita ao usuário a mensagem criptografada (base64) para descriptografar
            entrada_b64 = input("Informe a mensagem criptografada (base64): ").strip()
            try:
                decifrada = descriptografar_texto(entrada_b64, private_key)
            except Exception as e:
                print("Erro ao descriptografar:", e)
            else:
                print("\n🔓 Mensagem decifrada:")
                print(decifrada)

                # Se houver um arquivo usado anteriormente, registra a decifrada nele
                if last_arquivo:
                    with open(last_arquivo, "a", encoding="utf-8") as f:
                        f.write("Mensagem decifrada:\n")
                        f.write(decifrada + "\n")
            iniciar = input("\nDeseja criptografar outra mensagem? (s/n): ").strip().lower()
        elif input_opcao == '3':
            break

print("Encerrando o programa.")


    # ? Criar código que pergunta se deseja criptografar ou descriptografar

    # guarda o último arquivo usado (evita pedir sempre ao decifrar)