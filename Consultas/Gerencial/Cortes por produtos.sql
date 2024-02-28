select b.CODFORNEC,a.codprod,b.descricao,
       SUM(a.qtcorte) "Qtd. Cortes"
       /*,(SUM(a.qtcorte) * (SELECT MAX(p.pvenda) FROM pontual.PCPRECO p WHERE p.codprod = a.codprod)) 
       AS "Valor estimado",TO_NUMBER(TO_CHAR(a.dtcorte, 'WW')) SEMANA*/
    from pontual.pccortefv a
    join pontual.pcprodut b on a.codprod = b.codprod
    join pontual.pcusuari c on a.codusur = c.codusur
    WHERE A.DTCORTE >= '01-JAN-2024'
    AND A.DTCORTE <= '31-JAN-2024'
    /*where TO_NUMBER(TO_CHAR(a.dtcorte, 'MM')) = TO_NUMBER(TO_CHAR(SYSDATE, 'MM')) --APENAS DA MESMA SEMANA
    AND TO_NUMBER(TO_CHAR(a.dtcorte, 'YY')) = TO_NUMBER(TO_CHAR(SYSDATE, 'YY')) --APENAS DO MESMO ANO*/
    AND c.CODSUPERVISOR in (2)
    --AND B.codfornec in (1634)
GROUP BY a.codprod,b.descricao,b.CODFORNEC
order by  "Qtd. Cortes" desc
