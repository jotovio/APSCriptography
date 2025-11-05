from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_OAEP # ! Importa o padding OAEP para RSA
import base64
from typing import Optional # ! Importa Optional para tipos opcionais
import os # ! Importa o módulo os para manipulação de arquivos

# ---------- Funções úteis ----------

def gerar_chaves(bits: int = 2048):
    """Gera um par de chaves RSA (privada + pública) e retorna (priv, pub).

    bits: tamanho do módulo RSA. 2048 é um valor seguro para uso geral.
    """
    chave_priv = RSA.generate(bits)
    chave_pub = chave_priv.publickey()
    return chave_priv, chave_pub 

def criptografar_texto(texto: str, chave_publica: RSA.RsaKey) -> str:
    """
    Criptografa uma string com RSA-OAEP (OAEP com SHA-1 por padrão do PyCryptodome)
    e retorna o resultado em base64 (string imprimível).

    Observação: RSA-OAEP cifra apenas textos curtos. Para textos grandes, use
    um esquema híbrido (AES + RSA para a chave do AES).
    """
    cipher = PKCS1_OAEP.new(chave_publica) # ! Cria o objeto de cifra com a chave pública
    bytes_cifrados = cipher.encrypt(texto.encode("utf-8")) # ! Cifra os bytes do texto
    return base64.b64encode(bytes_cifrados).decode("utf-8") # ! Retorna o texto cifrado em base64

def descriptografar_texto(b64_cifrado: str, chave_privada: RSA.RsaKey) -> str:
    """
    Descriptografa um texto base64 com RSA-OAEP usando a chave privada.

    Importante: a mensagem deve ter sido cifrada com a chave pública
    correspondente e com o mesmo padding (OAEP padrão) para funcionar.
    """
    cipher = PKCS1_OAEP.new(chave_privada) # ! Cria o objeto de cifra com a chave privada
    bytes_cifrados = base64.b64decode(b64_cifrado.encode("utf-8")) # ! Decodifica o texto base64 para bytes
    bytes_originais = cipher.decrypt(bytes_cifrados) # ! Descriptografa os bytes cifrados
    return bytes_originais.decode("utf-8")

def carregar_chave_privada(caminho: str) -> RSA.RsaKey:
    """Carrega uma chave privada RSA a partir de um arquivo PEM."""
    with open(caminho, "rb") as f:
        dados = f.read() # ! Lê os dados do arquivo PEM
    return RSA.import_key(dados) # ! Importa a chave privada dos dados lidos

def importar_chave_privada_de_texto(pem_texto: str) -> RSA.RsaKey:
    """Importa uma chave privada RSA a partir do conteúdo PEM colado no terminal."""
    return RSA.import_key(pem_texto.encode("utf-8"))

def ler_entrada_multilinha(prompt: str) -> str:
    """
    1 - Lê múltiplas linhas do terminal até uma linha vazia.

    2 - Útil para colar uma chave PEM completa (BEGIN/END ...) no Windows,
    onde Ctrl+V às vezes cola com quebras de linha.
    """
    print(prompt)
    print("(Finalize com uma linha vazia)")
    linhas = []
    while True:
        try:
            linha = input() # ! Lê uma linha do terminal
        except EOFError: # ! Trata o fim da entrada (Ctrl+D)
            break
        if linha is None: # ! Trata a entrada vazia
            break
        if linha.strip() == "": # ! Linha vazia indica fim da entrada (dar Enter duas vezes)
            break 
        linhas.append(linha)
    return "\n".join(linhas) # ! Retorna o texto completo

def salvar_chave_privada(chave_privada: RSA.RsaKey, caminho: str) -> None:
    """
    Salva a chave privada RSA em um arquivo no formato PEM.
    """
    with open(caminho, "wb") as f:
        f.write(chave_privada.export_key("PEM")) # ! Salva a chave privada em formato PEM

def salvar_chave_publica(chave_publica: RSA.RsaKey, caminho: str) -> None:
    """Salva a chave pública RSA em um arquivo no formato PEM."""
    with open(caminho, "wb") as f:
        f.write(chave_publica.export_key("PEM")) # ! Salva a chave pública em formato PEM

if __name__ == "__main__":
    
    """
    1 - Guarda o último arquivo usado (para registrar original/cifrada/decifrada)
    na sessão atual. 
    2 - Permite salvar a mensagem decifrada no mesmo arquivo
    """
    
    last_arquivo: Optional[str] = None
    cifrada_b64: Optional[str] = None

    iniciar = input("Deseja iniciar o programa? (s/n): ").strip().lower()

    while iniciar == 's':
        print("""
                Criptografia em RSA-OAEP
                Criptografar - 1
                Decriptografar - 2
                Decriptografar mensagem externa - 3
                Sair - 4
              """ + 20*"-")
        
        input_opcao = input("Escolha uma opção (1/2/3/4): ").strip()

        if input_opcao == '1':

            """
            1 - Pede para o usuário os nomes dos arquivos para salvar as chaves privada e pública.
            2 - Gera um novo par e salva em PEM para compartilhar a pública
            3 - Informa o usuário sobre onde as chaves foram salvas.
            4 - Segue com a criptografia da mensagem usando a chave pública atual.
            """
            priv_path = input("Nome do arquivo para a chave privada (default: private.pem): ").strip() or "private.pem"
            pub_path = input("Nome do arquivo para a chave pública (default: public.pem): ").strip() or "public.pem"
            try:
                private_key, public_key = gerar_chaves()
                salvar_chave_privada(private_key, priv_path) # ! gera uma nova chave privada e salva em um arquivo PEM
                salvar_chave_publica(public_key, pub_path) # ! gera uma nova chave pública e salva em um arquivo PEM
                print(f"Novas chaves salvas em '{priv_path}' e '{pub_path}'.")
            except Exception as e: # ! Trata erros ao gerar/salvar chaves
                print("Erro ao gerar/salvar chaves:", e)
            
            # ! Pede o nome do arquivo para salvar a mensagem cifrada/decifrada
            arquivo = input("Digite o nome do arquivo para salvar a mensagem criptografada: ").strip()
            last_arquivo = arquivo

            # ! Pede a mensagem para ser criptografada
            mensagem = input("Digite a mensagem a ser criptografada: ").strip()

            # ! salvar mensagem original (substitui/ou cria o arquivo)
            with open(arquivo, "w", encoding="utf-8") as f:
                f.write("Mensagem original:\n")
                f.write(mensagem + "\n\n")

            # ! mostra no terminal a mensagem cifrada em base64
            cifrada_b64 = criptografar_texto(mensagem, public_key)
            print("\n🔒 Mensagem criptografada (base64):")
            print(cifrada_b64)

            # ! acrescentar a versão criptografada ao arquivo
            with open(arquivo, "a", encoding="utf-8") as f:
                f.write("Mensagem criptografada (base64):\n")
                f.write(cifrada_b64 + "\n\n")

        elif input_opcao == '2':
            # ! Descriptografa a última mensagem cifrada nesta sessão (mesmas chaves)
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

                    with open(arquivo, "a", encoding="utf-8") as f: # ! Registra a mensagem decifrada no arquivo usado anteriormente
                        f.write("Mensagem decifrada:\n")
                        f.write(decifrada + "\n")
                iniciar = input("\nDeseja criptografar outra mensagem? (s/n): ").strip().lower()

        elif input_opcao == '3':
            # ! Descriptografa mensagem EXTERNA: permite colar a chave privada PEM
            # ! completa (BEGIN/END) ou informar o caminho do arquivo PEM.
            entrada = ler_entrada_multilinha(
                "Cole a chave PRIVADA em formato PEM OU digite o caminho do arquivo:"
            ).strip()
            try:
                if os.path.exists(entrada): # ! Verifica se a entrada é um caminho de arquivo existente
                    chave_priv_ext = carregar_chave_privada(entrada)
                else:
                    chave_priv_ext = importar_chave_privada_de_texto(entrada) # ! SE a entrada não for um arquivo, importa como texto PEM
                # ! Aceita o ciphertext em base64 (uma linha). Remova espaços/linhas extras.
                entrada_b64 = input("Informe a mensagem criptografada (base64): ").strip()
                decifrada = descriptografar_texto(entrada_b64, chave_priv_ext) # ! Descriptografa com a chave externa
            except Exception as e:
                print("Erro ao descriptografar mensagem externa:", e)
            else:
                print("\n🔓 Mensagem decifrada (externa):")
                print(decifrada)
        
        elif input_opcao == '4':
            break

print("Encerrando o programa.")