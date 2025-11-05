# Guia Completo para Colaboração no Repositório

Este guia explica o passo a passo para contribuir com o repositório, desde a criação da branch até a revisão e aceitação do Pull Request.

---

## Para o colaborador que vai fazer alterações

1. Clone o repositório (se ainda não tiver) usando os comandos:  
git clone https://github.com/jotovio/APSCriptography.git e cd NOME_DO_REPOSITORIO.

2. Atualize a branch principal para garantir que está com a versão mais recente com os comandos:  
git checkout main e git pull origin main.

3. Crie uma nova branch para a tarefa que vai realizar, com o comando:  
git checkout -b branch-seunome (Ex: branch-isaque).

4. Faça as alterações necessárias nos arquivos do projeto.

5. Adicione as alterações para o commit com o comando:  
git add . (Com espaço e .)

6. Faça o commit das alterações, usando uma mensagem clara e descritiva, como:  
git commit -m "Descrição do que foi feito".

7. Envie a branch criada para o repositório remoto no GitHub com:  
git push origin nome-da-branch.

## Instalação de Pacotes

1. pip install pycryptodome

2. py -m pip install pycryptodome

3. py -m Crypto.SelfTest

## Para o colaborador visualizar as novas alterações

1. Vá até a pasta do projeto no seu computador:
cd nome-do-projeto

2. Certifique-se de que você está na branch main
git checkout main (Neste comando, você sai da sua branch e vai para a principal, então cuidado.)

3. Baixe as atualizações do repositório remoto (GitHub):
git pull origin main

## Observações importantes

1. Caso existam conflitos entre as branches, eles precisam ser resolvidos antes do merge.  
2. Sempre use nomes claros e objetivos para os commits.




# Explicação linha a linha

## Cabeçalho / imports

1. from Crypto.PublicKey import RSA

    from ... import ... — sintaxe para trazer um nome específico de um módulo.

    Crypto.PublicKey — pacote do PyCryptodome que trata chaves públicas/privadas.

    RSA — classe que implementa operações de RSA (gerar chave, importar/exportar, etc.).

2. from Crypto.Cipher import PKCS1_OAEP

    Crypto.Cipher — pacote de cifras (algoritmos de criptografia).

    PKCS1_OAEP — esquema de padding/encapsulamento para RSA (OAEP = Optimal Asymmetric Encryption Padding). Garante segurança adicional ao cifrar com RSA.

3. import base64

    base64 — módulo que converte bytes em uma representação ASCII (e.g. para imprimir/colar): b64encode e b64decode.

4. from typing import Optional

    typing — módulo para anotações de tipos (útil para documentação e IDEs).

    Optional[...] — indica que uma variável pode ser do tipo especificado ou None.

5. import os

    os — módulo da biblioteca padrão para interagir com o sistema operacional (arquivos, caminhos, variáveis de ambiente, etc.).


## Definição de função: gerar_chaves

1. def gerar_chaves(bits: int = 2048):

    def — declara uma função.

    bits: int = 2048 — anotação de tipo dizendo que bits é int e valor padrão é 2048.

    Docstring (entre """ ... """) — explicação da função; usada também por ferramentas/IDE.

2. chave_priv = RSA.generate(bits)

    RSA.generate(bits) — cria uma chave RSA privada cujo módulo tem bits bits (ex.: 2048).

    chave_priv — objeto que representa a chave privada.

3. chave_pub = chave_priv.publickey()

    .publickey() — método do objeto chave privada que gera a chave pública correspondente.

4. return chave_priv, chave_pub

    return — devolve uma tupla com a chave privada e pública.

## Função: criptografar_texto

1. def criptografar_texto(texto: str, chave_publica: RSA.RsaKey) -> str:

    texto: str — parâmetro texto com anotação de string.

    chave_publica: RSA.RsaKey — anotação indicando que se espera um objeto de chave RSA.

    -> str — indica que a função retorna uma str (string).

2. cipher = PKCS1_OAEP.new(chave_publica)

    PKCS1_OAEP.new(...) — cria um objeto cifra configurado para usar RSA-OAEP com a chave fornecida.

    cipher — objeto que tem métodos encrypt/decrypt conforme o modo.

3. bytes_cifrados = cipher.encrypt(texto.encode("utf-8"))

    texto.encode("utf-8") — transforma a string em bytes usando UTF-8 (necessário para cifrar).

    cipher.encrypt(...) — cifra os bytes; retorno são bytes cifrados.

4. return base64.b64encode(bytes_cifrados).decode("utf-8")

    base64.b64encode(...) — codifica bytes em base64 (retorna bytes).

    .decode("utf-8") — converte os bytes base64 de volta para str para ser imprimível/colável.

### Observação importante no docstring: RSA-OAEP só cifra mensagens curtas (limite relacionado ao tamanho da chave e padding).

## Função: descriptografar_texto

1. def descriptografar_texto(b64_cifrado: str, chave_privada: RSA.RsaKey) -> str:

    b64_cifrado: str — espera o texto cifrado em base64 como str.

    chave_privada — chave privada para descriptografia.

2. cipher = PKCS1_OAEP.new(chave_privada)

    Mesmo que antes, mas usando a chave privada (objeto cipher para decrypt).

3. bytes_cifrados = base64.b64decode(b64_cifrado.encode("utf-8"))

    .encode("utf-8") — transforma o base64 string em bytes.

    base64.b64decode(...) — decodifica base64 para obter os bytes cifrados originais.

4. bytes_originais = cipher.decrypt(bytes_cifrados)

    cipher.decrypt(...) — descriptografa os bytes cifrados; retorna bytes originais (mensagem).

5. return bytes_originais.decode("utf-8")

    .decode("utf-8") — transforma bytes de volta em string legível.

## Função: carregar_chave_privada

1. def carregar_chave_privada(caminho: str) -> RSA.RsaKey:

    caminho: str — caminho para o arquivo que contém a chave (PEM).

    Função retorna um objeto RSA.RsaKey.

2. with open(caminho, "rb") as f:

    with — contexto que garante fechamento automático do arquivo.

    open(..., "rb") — abre arquivo em modo binário para leitura (read + binary).

    as f — f é o objeto arquivo.

3. dados = f.read()

    .read() — lê todo o conteúdo do arquivo (bytes).

4. return RSA.import_key(dados)

    RSA.import_key(...) — importa/parseia o conteúdo PEM (ou DER) e cria um objeto de chave RSA.

## Função: importar_chave_privada_de_texto

1. def importar_chave_privada_de_texto(pem_texto: str) -> RSA.RsaKey:

    Recebe o conteúdo PEM já em string (colado pelo usuário).

    pem_texto.encode("utf-8") — converte para bytes antes de RSA.import_key.

## Função: ler_entrada_multilinha

1. def ler_entrada_multilinha(prompt: str) -> str:

    Lê várias linhas do terminal até uma linha vazia (útil para colar PEM completo).

2. print(prompt) / print("(Finalize com uma linha vazia)") — instruções ao usuário.

3. linhas = [] — lista para acumular linhas lidas.

4. while True: — loop que continua até break.

5. try: / except EOFError:

    EOFError — exceção lançada quando não há mais entrada (Ctrl+D em Unix, por exemplo).

    try/except — trata essa situação sem quebrar o programa.

6. linha = input() — lê uma linha do usuário.

7. if linha is None: — (praticamente redundante—input() nunca retorna None em uso normal) checa caso anormal.

8. if linha.strip() == "":

    .strip() — remove espaços em branco nas extremidades; se ficar vazio, é sinal de término (linha vazia).

9. linhas.append(linha) — adiciona a linha lida à lista.

10. return "\n".join(linhas)

    "\n".join(...) — une todas as linhas com quebras de linha, retornando o texto completo.

## Funções: salvar_chave_privada / salvar_chave_publica

1. def salvar_chave_privada(chave_privada: RSA.RsaKey, caminho: str) -> None:

    -> None — indica que não retorna nada.

2. with open(caminho, "wb") as f:

    open(..., "wb") — abre arquivo em modo binário escrita, sobrescrevendo/ criando. (w + b).

3. f.write(chave_privada.export_key("PEM"))

    .export_key("PEM") — converte a chave para o formato PEM (bytes).

    f.write(...) — grava os bytes no arquivo.

### O mesmo para salvar_chave_publica, mas com a chave pública.

## Bloco principal de execução

1. if __name__ == "__main__":

    Verifica se o arquivo está sendo executado diretamente (não importado). Esse bloco só roda ao executar o script, não ao importá-lo como módulo.

### Comentários explicativos seguem.

2. last_arquivo: Optional[str] = None

    Declaração de variável; Optional[str] indica que pode ser str ou None. Guarda o último arquivo usado.

3. cifrada_b64: Optional[str] = None

    Armazena a última mensagem cifrada em base64 (ou None se nada).

4. iniciar = input("Deseja iniciar o programa? (s/n): ").strip().lower()

    input(...) — lê string do usuário.

    .strip() — remove espaços ao fim/início.

    .lower() — converte para minúsculas (normaliza resposta).

5. while iniciar == 's':

    Loop que só ocorre se o usuário respondeu 's'.

6. print(""" ... """ + 20*"-")

    """ ... """ — string multilinha.

    20*"-" — operador * repete a string "-" 20 vezes.

7. input_opcao = input("Escolha uma opção (1/2/3/4): ").strip()

    Lê a opção, tira espaços.

## Opção 1 — gerar chaves + criptografar

1. if input_opcao == '1': — ramo para criar chaves e criptografar.

2. priv_path = input("Nome do arquivo para a chave privada (default: private.pem): ").strip() or "private.pem"

    A expressão ... or "private.pem" retorna "private.pem" se a string à esquerda for vazia (útil para default).

3. public_key = ... / private_key, public_key = gerar_chaves()

    Chama gerar_chaves() e desempacota a tupla (privada, pública).

4. salvar_chave_privada(private_key, priv_path) / salvar_chave_publica(public_key, pub_path)

    Grava as chaves em arquivos PEM.

5. except Exception as e:

    try/except captura qualquer exceção (classe base Exception).

    e — objeto que descreve a exceção. Evite usar except Exception em produção sem tratamento específico, mas é comum em scripts.

6. arquivo = input("Digite o nome do arquivo para salvar a mensagem criptografada: ").strip()

    Nome do arquivo onde será salvo o conteúdo (original + cifrado).

7. last_arquivo = arquivo — guarda para uso posterior.

8. mensagem = input("Digite a mensagem a ser criptografada: ").strip()

    Lê mensagem a ser cifrada.

9. with open(arquivo, "w", encoding="utf-8") as f:

    Abre/cria o arquivo em modo texto para escrita (w) com codificação UTF-8.

10. f.write("Mensagem original:\n") / f.write(mensagem + "\n\n")

    f.write(...) grava strings no arquivo.

11. cifrada_b64 = criptografar_texto(mensagem, public_key)

    Usa função definida antes para cifrar e receber base64.

12. print(cifrada_b64) — imprime a string em base64.

13.with open(arquivo, "a", encoding="utf-8") as f:

    open(..., "a") — append: abre o arquivo para adicionar conteúdo ao final sem sobrescrever.

## Opção 2 — descriptografar última mensagem da sessão

1. elif input_opcao == '2': — ramo para descriptografia interna.

2. if cifrada_b64 is None: — verifica se existe mensagem cifrada armazenada.

3. decifrada = descriptografar_texto(cifrada_b64, private_key)

    Chama a função de descriptografia com a chave privada gerada anteriormente.

4. except Exception as e: — trata erros na descriptografia. Erros comuns: padding incorreto, chave errada, dados corrompidos.

5. with open(arquivo, "a", encoding="utf-8") as f: — registra a mensagem decifrada no arquivo (append).

6. iniciar = input("\nDeseja criptografar outra mensagem? (s/n): ").strip().lower()

    Pergunta se quer continuar; sobrescreve iniciar, que controla o while externo.

## Opção 3 — descriptografar mensagem externa

1. elif input_opcao == '3': — descriptografar usando chave privada externa.

2. entrada = ler_entrada_multilinha("Cole a chave PRIVADA ...").strip()

    Permite colar PEM (multilinha) ou fornecer caminho de arquivo. .strip() normaliza.

3. if os.path.exists(entrada):

    os.path.exists(...) — retorna True se existe um arquivo/caminho com esse nome. Serve para detectar se a entrada é caminho de arquivo.

4. chave_priv_ext = carregar_chave_privada(entrada)

    Se for caminho, carrega key do arquivo.

5. chave_priv_ext = importar_chave_privada_de_texto(entrada)

    Se não for caminho, tenta interpretar a entrada como PEM textual e importar a chave.

6. entrada_b64 = input("Informe a mensagem criptografada (base64): ").strip()

    Pede o ciphertext em base64 (uma linha).

7. decifrada = descriptografar_texto(entrada_b64, chave_priv_ext)

    Descriptografa usando a chave externa fornecida/importada.

8. except Exception as e: — captura erros (arquivo inexistente, PEM inválido, ciphertext inválido, padding/chave incompatível).

## Opção 4 — Sair

1. elif input_opcao == '4': — sai do loop com break.

## Final

1. print("Encerrando o programa.") — mensagem final.