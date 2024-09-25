SELECT C.CODSUPERVISOR, 
       B.CODFORNEC, 
       (SELECT X.FANTASIA FROM PONTUAL.PCFORNEC X WHERE X.CODFORNEC = B.CODFORNEC) FORNECEDOR,
       A.CODPROD,
       B.DESCRICAO,
       SUM(A.QTANT) "QTD. PEDIDO",
       SUM(A.QTCORTE) "QTD. CORTE", 
       TRUNC((SUM(A.QTCORTE)/SUM(A.QTANT))*100,2) || '%' "%",
       NVL((SELECT AVG(P.PVENDA) FROM PONTUAL.PCPEDI P WHERE P.CODPROD = A.CODPROD AND P.DATA BETWEEN TRUNC(SYSDATE, 'YEAR') AND SYSDATE),0) * SUM(A.QTCORTE) "R$"

FROM PONTUAL.PCCORTEFV A
    JOIN PONTUAL.PCPRODUT B ON A.CODPROD = B.CODPROD
    JOIN PONTUAL.PCUSUARI C ON A.CODUSUR = C.CODUSUR
    JOIN PONTUAL.PCCLIENT CLI ON CLI.CODCLI = A.CODCLI
WHERE A.DTCORTE BETWEEN TO_DATE('{dtIni}', 'DD-MM-YYYY') AND TO_DATE('{dtFim}', 'DD-MM-YYYY')
    AND C.CODSUPERVISOR {supOnOff} ({supCod})
    
GROUP BY A.CODPROD, B.DESCRICAO, C.CODSUPERVISOR, B.CODFORNEC
ORDER BY  "CODFORNEC", "R$" DESC