## Introdução

Bem-vindo! Aqui você encontrará uma coleção de consultas SQL e outros códigos PL/SQL abrangendo diversas áreas de manipulação e análise de dados. Explore os arquivos para ver diversas consultas criadas por mim durante minha atuação como Programador SQL. Abaixo você verá uma introdução a consultas SQL.

## Como Criar Consultas SQL

Se você é novo em SQL ou deseja aprimorar suas habilidades, você está no lugar certo! Aqui estão algumas dicas básicas para começar a criar consultas SQL de forma simples.

## Selecionando Dados Básicos

Para recuperar dados de uma tabela, use a cláusula `SELECT`:

```sql
SELECT * FROM exemplo;
```
Isso seleciona tudo que a tabela exemplo contém.

## Selecionando Dados Básicos com filtros

Selecione apenas os registros que atendem a uma condição específica usando a cláusula WHERE:

```sql
SELECT nome, idade
FROM pessoa
WHERE nome = 'Lucas';
```
Isso seleciona as colunas nome e idade na tabela pessoa ONDE (WHERE) nome é Lucas.

## Ordenando dados selecionados

Faça o ordenamento dos dados usando ORDER BY:

```sql
SELECT nome, idade
FROM pessoa
WHERE nome = 'Marcos'
ORDER BY idade DESC;
```
Isso ordena da maior idade para a menor, onde o nome é Marcos, atrevés do ORDER BY e DESC. O contrário do DESC é o ASC. Ele torna a ordenação do menor para o maior.
```sql
ORDER BY nome; -- Em caso de não haver a especificação ASC ou DESC, o padrão sempre será ASC.
```
O ASC e DESC também são usados para ordem alfabética.

## Avançando em Consultas

Agora, vamos explorar maneiras de ir além e aprimorar suas habilidades.

### A Importância da Prática e Desafios

O avanço no PL/SQL, assim como em qualquer linguagem, vem através da prática e da resolução de desafios mais complexos. Experimente projetos práticos e desafie-se com problemas do mundo real para consolidar seu conhecimento.

### Entendendo JOINs
O JOIN é uma parte crucial para manipular dados em várias tabelas. Comece com o básico:

```sql
SELECT A.nome, B.cargo, A.idade, B.salario
FROM pessoa A
JOIN empregado B ON A.cpf = B.cpf; /* A e B são aliases ou apelidos para as tabelas envolvidas na consulta.
                                       Isso substitui usar o nome completo da coluna ex.: pessoa.cpf */
```
Isso retorna dados combinados das duas tabelas com base nas colunas especificadas.

#### INNER JOIN

O INNER JOIN é a forma mais comum de JOIN e retorna registros que têm correspondências nas duas tabelas. A sintaxe básica é:

```sql
SELECT A.nome, B.cargo, A.idade, B.salario
FROM pessoa A
INNER JOIN empregado B ON A.cpf = B.cpf; /* Nesta consulta, apenas as linhas em que há correspondência entre
                                             pessoa e empregados serão retornadas. */
```
#### LEFT e RIGHT JOIN

O LEFT JOIN retorna todas as linhas da tabela à esquerda (primeira tabela mencionada após o 'ON' - pessoa A) e as linhas correspondentes da tabela à direita. Se não houver correspondência, os resultados da tabela à direita serão NULL.

O RIGHT JOIN é semelhante ao LEFT JOIN, mas retorna todas as linhas da tabela à direita (segunda tabela mencionada após o 'ON' - empregados B) e as linhas correspondentes da tabela à esquerda. Se não houver correspondência, os resultados da tabela à esquerda serão NULL.

### Explorando Subconsultas
As subconsultas são poderosas para filtrar dados complexos. Experimente:
```sql
SELECT pessoa.nome, pessoa.idade, pessoa.cpf
FROM pessoa
WHERE cpf IN (SELECT cpf FROM empregado); /* Isso fará um filtro onde apenas as pessoas que forem empregadas
                                              (que seu cpf está na tabela empregado) serão apresentadas no
                                              resultado da consulta. */
```
Uma outra forma de se usar subconsultas é complementando colunas:
```sql
SELECT A.nome, A.idade, A.cpf, (SELECT B.id FROM empregado B WHERE B.cpf = A.cpf) AS id -- redefine nome da coluna
FROM pessoa A;
```
Nesse caso a subconsulta retornará a coluna id da tabela funcionário onde há o mesmo cpf nas duas tabelas.

### Utilizando CTE (Common Table Expressions)
As CTEs são uma forma eficiente de melhorar a legibilidade e a otimização das consultas. 
```sql
WITH cteEmpregado AS (
    SELECT EMP.nome, EMP.cargo, EMP.salario, CART.funcao
    FROM empregado EMP
    JOIN carteira CART ON EMP.id = CART.id
    WHERE EMP.salario > 2000
) -- A CTE criar uma nova tabela "temporária" com as colunas que vc irá ultilizar na sua consulta princiapal

SELECT A.nome, B.cargo, B.funcao, B.salario
FROM pessoa A
INNER JOIN cteEmpregado B on A.nome = B.nome; /* O ideal é sempre ultilizar chaves únicas, mas também
                                                 é possível usar chaves como 'nome'. Corre o risco de
                                                 haver outro nome igual ou nomes escritos errados em
                                                 alguma das tabelas. Esteja ciente ao usar. */
```
As CTEs tornam as consultas mais organizadas e podem melhorar o desempenho em relação a subconsultas. Então prefira usá-las em lugar de subconsultas.

### Pesquisando com Inteligência Artificial
Chats de Inteligência Artificial são poderosas formas para você saber como fazer algo. Uma forma de você usar da maneira correta pode ser através do seguinte prompt:
```
Como faço para filtrar dados em uma consulta PL/SQL onde a data se encontra entre o primeiro dia do mês e hoje?
```
###### ChatGPT: 
Para filtrar dados em uma consulta PL/SQL onde a data está entre o primeiro dia do mês e hoje, você pode usar a função TRUNC para obter o primeiro dia do mês atual e comparar com a data desejada. Aqui está um exemplo:
```
SELECT *
FROM sua_tabela
WHERE sua_coluna_data >= TRUNC(SYSDATE, 'MM') -- Primeiro dia do mês atual
  AND sua_coluna_data <= SYSDATE; -- Hoje
```
Neste exemplo:

TRUNC(SYSDATE, 'MM') retorna o primeiro dia do mês atual.
sua_coluna_data >= TRUNC(SYSDATE, 'MM') filtra datas a partir do primeiro dia do mês.
sua_coluna_data <= SYSDATE filtra datas até o dia atual.
Certifique-se de substituir sua_tabela pelo nome real da tabela e sua_coluna_data pelo nome real da coluna que armazena as datas. Essa consulta retornará todas as linhas onde a data está entre o primeiro dia do mês atual e hoje.

