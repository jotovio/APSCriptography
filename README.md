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




## Observações importantes

1. Caso existam conflitos entre as branches, eles precisam ser resolvidos antes do merge.  
2. Sempre use nomes claros e objetivos para os commits.