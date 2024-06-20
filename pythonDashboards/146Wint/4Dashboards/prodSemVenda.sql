WITH DATAVENDA AS 
(
    SELECT MAX(c.DATA) data, c.CODPROD
        FROM PCPEDI C 
    WHERE c.DATA BETWEEN SYSDATE - 240 AND SYSDATE 
    GROUP BY c.CODPROD
),
PRECO AS
(
    SELECT p.codprod, MAX(p.pvenda) valor FROM PCPRECO p GROUP BY p.codprod
)
 
SELECT a.CODPROD, a.DESCRICAO produto,
       TO_CHAR(b.dtultent, 'DD/MM/YY') "Ult. Entrada",
       b.qtultent "QT. Ult. Ent.",
       (b.qtest - b.qtreserv) "Estoque",
       TRUNC(sysdate - c.data, 0) || ' Dias (' || TO_CHAR(c.data, 'DD/MM/YY') || ')' "Dias sem Venda"
       --,TRUNC(p.valor * (b.qtest - b.qtreserv),2) "Valor Aproximado perda em vendas"
       
FROM PCPRODUT a
JOIN PCest b ON a.codprod = b.codprod
JOIN DATAVENDA c ON a.codprod = c.codprod
JOIN PRECO p on a.codprod = p.codprod

WHERE c.data < SYSDATE - (:dias)
    AND (b.qtest - b.qtreserv) > 0
    AND a.codfornec in (:fornecedor)
    AND a.codprod in (:produto)
    AND b.codfilial = 3
ORDER BY "Estoque" DESC;