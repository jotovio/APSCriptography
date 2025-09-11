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

1 from Crypto.PublicKey import RSA
Importa a classe/funções para gerar e manipular chaves RSA (PyCryptodome).

2 from Crypto.Cipher import PKCS1_OAEP
Importa o esquema de cifra/decifra com padding OAEP (implementação pronta na biblioteca).

4 key = RSA.generate(2048)
Gera um par de chaves RSA (privada + pública) com tamanho de 2048 bits — tudo em memória. (Detalhes abaixo.)

5 private_key = key
A referência key gerada contém a chave privada; aqui você só está nomeando-a private_key.

6 public_key = key.publickey()
Cria/obtém o objeto de chave pública a partir da chave privada (o objeto public_key contém n e e, não d).

8-10 definição criptografar(mensagem, chave_publica)

9 cria um objeto cipher que usa OAEP + a chave pública.

10 chama cipher.encrypt(...) recebendo mensagem.encode() (string → bytes) e retorna os bytes cifrados.

12-14 definição descriptografar(criptografada, chave_privada)

13 cria um cipher OAEP com a chave privada.

14 cipher.decrypt(...) decifra os bytes e .decode() converte de volta para string.

16-17 bloco principal — lê msg do usuário.

19 chama criptografar passando a mensagem e a chave pública, recebe bytes cifrados.

20 mostra os bytes cifrados no terminal (conteúdo binário).

22-23 decifra com a chave privada e imprime a string original.


# Explicação detalhada dos termos mencionados

Vou explicar cada ! com um pouco mais de técnica, mas simples.

## RSA.generate(2048)

O que faz: cria um novo par de chaves RSA (privada + pública) com o número de bits indicado (2048).

Por trás dos panos (resumido): a função gera dois números primos grandes p e q, calcula n = p*q, calcula phi = (p-1)*(q-1) e escolhe e e d que satisfazem as propriedades do RSA. Tudo pronto e seguro (para uso didático/produto) se o tamanho for adequado.

Observação prática: 2048 bits é um tamanho comumente considerado seguro hoje para muitos usos; a geração pode levar um pouco de tempo dependendo da máquina.

## key.publickey()

O que retorna: a chave pública correspondente ao objeto de chave privada key.

Por que usar: muitas operações (criptografar com RSA) usam somente a pública — quem tem a privada pode decifrar. key contém ambos; key.publickey() fornece só a parte pública (útil para enviar a terceiros).

## PKCS1_OAEP.new(...)

O que é: cria um objeto de cifra que implementa o padding OAEP (Optimal Asymmetric Encryption Padding) junto com RSA.

Por que padding existe: RSA puro (apenas matemática m^e mod n) é vulnerável a vários ataques. OAEP mistura a mensagem com dados aleatórios e aplica um esquema de máscara (MGF1) para tornar a cifragem probabilística e segura.

O que você passa a new(...): a chave (pública para encrypt, privada para decrypt) — o objeto resultante tem métodos encrypt/decrypt.

## cipher.encrypt(...)

O que faz: cifra os bytes passados, retornando bytes cifrados.

Importante: existe um tamanho máximo de dados que cabem numa única operação RSA+OAEP — se a mensagem for maior que esse limite, encrypt vai lançar ValueError. Por isso, em sistemas reais usa-se hybrid encryption: RSA cifra apenas uma chave simétrica e essa chave cifra a mensagem inteira (ex.: AES/Fernet).

## mensagem.encode()

O que faz: converte a string Python (tipo str) para bytes (tipo bytes). Por padrão usa UTF-8. Ex.: "Olá".encode() → b'Ol\xc3\xa1'.

Por que necessário: funções de cifra trabalham com bytes, não com str.

## cipher.decrypt(...)

O que faz: pega os bytes cifrados e aplica a operação de decifragem (verifica padding OAEP e reverte a exponenciação modular), retornando os bytes originais da mensagem.

## .decode()

O que faz: converte bytes para str usando UTF-8 por padrão. Assim b'Olá'.decode() → "Olá".

Por que usar: porque depois de decrypt você tem bytes; para imprimir/usar como texto precisa transformá-los em str.