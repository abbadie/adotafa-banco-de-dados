# Roteiro do vídeo demonstrativo

O vídeo final tem aproximadamente 4 minutos e 27 segundos. Ele mostra somente a aplicação funcionando; não há explicação do código. A narração usa voz masculina sintética e acompanha as operações exibidas no terminal.

## Antes de gravar

1. Confirme que a splash screen exibe `Davi Noronha da Matta Baptista`.
2. Execute os dois scripts da pasta `sql`.
3. Abra um terminal com tamanho suficiente para não cortar as tabelas.
4. Oculte senhas e informações pessoais.
5. Confirme que a narração está sincronizada com cada mudança de tela.

## Sequência da gravação

### 1. Abertura

- Apresente o nome **AdotaFá**, o objetivo do sistema e o autor.
- Mostre a tela inicial com a contagem de adotantes, animais e adoções.

### 2. Relatórios iniciais

- Abra o resumo de adoções por espécie.
- Abra o relatório detalhado com a junção das três tabelas.
- Use os resultados como referência antes das novas operações.

### 3. Inserções

- Cadastre o adotante Carlos Mendes.
- Cadastre o animal Thor.
- Registre uma adoção entre os dois e mostre a mudança do animal para `ADOTADO`.

### 4. Atualização

- Altere o nome do animal para Thor Júnior e a idade para quatro anos.
- Deixe os demais campos em branco para preservar seus valores.
- Mostre o registro atualizado.

### 5. Conferência nos relatórios

- Abra novamente o resumo por espécie e confira o novo total.
- Abra o relatório detalhado e mostre a linha de Thor Júnior e Carlos Mendes.

### 6. Remoção e integridade

- Tente excluir Carlos Mendes e mostre o aviso sobre a adoção vinculada.
- Confirme a remoção da adoção dependente e do adotante.
- Remova Thor Júnior, que voltou a ficar disponível.

### 7. Encerramento

- Volte ao menu principal e use a opção `Sair`.
- Encerre identificando o sistema e o autor: Davi Noronha da Matta Baptista.

## Conferência do vídeo

- Todos os menus apareceram em funcionamento.
- A imagem foi capturada durante a execução real do terminal conectado ao PostgreSQL.
- A splash screen exibiu o nome completo do autor.
- As quatro áreas avaliadas foram mostradas: relatórios, inserção, remoção e atualização.
- A voz masculina está compreensível, sincronizada e com pausas de no máximo cinco segundos; a fonte do terminal está legível.
- O vídeo foi publicado no YouTube e o link foi incluído no README.

