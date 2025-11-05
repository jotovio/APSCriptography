from Crypto.PublicKey import RSA # ! Importa o módulo RSA do PyCryptodome
from Crypto.Cipher import PKCS1_OAEP # ! Importa o padding OAEP para RSA
import base64 # ! Importa o módulo base64 para codificação/decodificação
from typing import Optional # ! Importa Optional para tipos opcionais

# ---------- Funções úteis ----------

def gerar_chaves(bits: int = 2048):
    """Gera um par de chaves RSA (privada + pública) e retorna (priv, pub)."""
    chave_priv = RSA.generate(bits) #! Gera a chave privada RSA
    chave_pub = chave_priv.publickey() #! Deriva a chave pública da chave privada
    return chave_priv, chave_pub 


# --- Descriptografar --



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
    bytes_originais = cipher.decrypt(bytes_cifrados)  # ! descriptografa
    return bytes_originais.decode("utf-8")


if __name__ == "__main__":
    private_key, public_key = gerar_chaves()

    # ! guarda a última mensagem cifrada na sessão (None se não houver)
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
            last_arquivo = arquivo # ! guarda o arquivo usado

            mensagem = input("Digite a mensagem a ser criptografada: ").strip()

            # ! salvar mensagem original (substitui/ou cria o arquivo)
            with open(arquivo, "w", encoding="utf-8") as f:
                f.write("Mensagem original:\n")
                f.write(mensagem + "\n\n")

            cifrada_b64 = criptografar_texto(mensagem, public_key)
            print("\n🔒 Mensagem criptografada (base64):")
            print(cifrada_b64)

            #! acrescentar a versão criptografada ao arquivo
            with open(arquivo, "a", encoding="utf-8") as f:
                f.write("Mensagem criptografada (base64):\n")
                f.write(cifrada_b64 + "\n\n")

        elif input_opcao == '2':
            # !Sem verificação de arquivo: apenas avisar se não houver mensagem cifrada
            if cifrada_b64 is None:
                print("Nenhuma mensagem criptografada disponível. Não é possível realizar a descriptografia.")
            else:
                try:
                    decifrada = descriptografar_texto(cifrada_b64, private_key) # ! Descriptografa usando a chave privada gerada anteriormente
                except Exception as e: # ! Trata erros na descriptografia
                    print("Erro ao descriptografar:", e)
                else:
                    print("\n🔓 Mensagem decifrada:")
                    print(decifrada)

                    with open(arquivo, "a", encoding="utf-8") as f: # ! registra a decifrada no arquivo usado
                        f.write("Mensagem decifrada:\n")
                        f.write(decifrada + "\n")
                iniciar = input("\nDeseja criptografar outra mensagem? (s/n): ").strip().lower()
        elif input_opcao == '3':
            break

print("Encerrando o programa.")


    # ? Criar código que pergunta se deseja criptografar ou descriptografar

    # guarda o último arquivo usado (evita pedir sempre ao decifrar)
