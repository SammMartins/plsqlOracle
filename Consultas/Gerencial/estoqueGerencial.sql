SELECT c.codfornec "FORNECEDOR", 
       a.codprod,
       c.descricao, a.qtest "ESTOQUE", 
       a.custoultent "CUSTO + IMP.", 
       (a.valorultent + vlultpcompra) / 2 "PREÇO",
       a.qtvendmes1 "MÊS 1", a.qtvendmes2 "MÊS 2", a.qtvendmes3 "MÊS 3"
FROM Pontual.PCEST A
JOIN Pontual.pcprodut c on a.codprod = c.codprod
JOIN Pontual.PCPRECO p on a.codprod = p.codprod
where a.codfilial = 3
AND c.codfornec in ({COMBOBOX1})
AND TO_DATE(a.dtultent, 'DD/MM/YY') > SYSDATE-120          
GROUP BY a.codprod, c.codfornec, c.descricao, a.qtest, a.custoultent, a.valorultent, vlultpcompra,a.qtvendmes1, a.qtvendmes2, a.qtvendmes3
HAVING SUM(a.qtvendmes1 + a.qtvendmes2 + a.qtvendmes3) > 0 or a.qtest > 0
ORDER BY c.codfornec, a.codprod