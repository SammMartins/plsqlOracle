WITH POSIT AS (
    SELECT A.CODCLI, A.CODUSUR, SUM(A.QT) QTD
    FROM PONTUAL.PCPEDI A
    WHERE A.CODPROD IN (18173, 18159, 17883, 17884, 17885, 18057, 18058, 18584, 18585, 18921)
    AND A.DATA BETWEEN TO_DATE('01/07/2024', 'DD/MM/YYYY') AND TO_DATE('31/07/2024', 'DD/MM/YYYY')
    AND A.VLBONIFIC = 0    
    GROUP BY A.CODCLI, A.CODUSUR
    HAVING SUM(A.QT) > 5
    ORDER BY QTD DESC
)

SELECT  USUR.CODUSUR COD,
        SUBSTR(USUR.NOME, INSTR(USUR.NOME, ' ') + 1, INSTR(USUR.NOME, ' ', INSTR(USUR.NOME, ' ') + 1) - INSTR(USUR.NOME, ' ') - 1) AS RCA, -- EXTRAI O NOME
        COUNT(DISTINCT(P.CODCLI)) AS "DN"
FROM PONTUAL.PCUSUARI USUR
left JOIN POSIT P ON USUR.CODUSUR = P.CODUSUR
GROUP BY USUR.CODUSUR, USUR.NOME
HAVING USUR.NOME LIKE 'PMU %' AND USUR.CODUSUR NOT IN (2,8,10)
ORDER BY DN DESC