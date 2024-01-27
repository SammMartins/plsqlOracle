select a.codprod,b.codfornec,b.descricao,
       SUM(a.qtant) "Qtd. Pedidos", 
       SUM(a.qtcorte) "Qtd. Cortes",
       (SUM(a.qtcorte) * (SELECT MAX(p.pvenda) FROM pontual.PCPRECO p WHERE p.codprod = a.codprod)) 
       AS "Valor estimado",TO_NUMBER(TO_CHAR(a.dtcorte, 'WW')) SEMANA
    from pontual.pccortefv a
    join pontual.pcprodut b on a.codprod = b.codprod
    join pontual.pcusuari c on a.codusur = c.codusur
where TO_NUMBER(TO_CHAR(a.dtcorte, 'MM')) = TO_NUMBER(TO_CHAR(SYSDATE, 'MM')) --APENAS DA MESMA SEMANA
    AND TO_NUMBER(TO_CHAR(a.dtcorte, 'YY')) = TO_NUMBER(TO_CHAR(SYSDATE, 'YY')) --APENAS DO MESMO ANO
    AND c.CODSUPERVISOR in (2,8,9)
    AND c.codfornec in (xxxx)
GROUP BY a.codprod,b.codfornec,b.descricao,a.dtcorte
order by  "Qtd. Cortes" desc
