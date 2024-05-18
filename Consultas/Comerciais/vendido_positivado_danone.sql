WITH FATSTM AS 
    (SELECT PED.CODUSUR AS RCA,
            SUM(PED.QT*PED.PVENDA) + 0 AS FATURAMENTO
    FROM PONTUAL.PCPEDI PED
        JOIN PONTUAL.PCPRODUT PROD ON PED.CODPROD = PROD.CODPROD
    WHERE PROD.CODFORNEC = 588
        AND PED.DATA BETWEEN '01-apr-2024' AND '31-MAY-2024'
        --AND PROD.CODSEC = 10001
        AND PED.POSICAO NOT LIKE 'C'
        AND PED.VLBONIFIC = 0
    GROUP BY PED.CODUSUR),
    
DNDIST AS
    (SELECT PED.CODUSUR AS RCA,
            COUNT(DISTINCT PED.CODCLI) AS DN
        FROM PONTUAL.PCPEDC PED
            JOIN PONTUAL.PCPEDI PEDI ON PEDI.NUMPED = PED.NUMPED
            JOIN PONTUAL.PCPRODUT PROD ON PEDI.CODPROD = PROD.CODPROD
        WHERE PROD.CODFORNEC = 588
            AND PED.DATA BETWEEN '01-APR-2024' AND '30-APR-2024'
            --AND PROD.CODSEC = 10001            
            AND PED.DTCANCEL IS NULL
            AND PED.CONDVENDA IN (1, 2, 3, 7, 9, 14, 15, 17, 18, 19, 98)
        GROUP BY PED.CODUSUR),
DNDIST2 AS
    (SELECT PED.CODUSUR AS RCA,
            COUNT(DISTINCT PED.CODCLI) AS DN
        FROM PONTUAL.PCPEDC PED
            JOIN PONTUAL.PCPEDI PEDI ON PEDI.NUMPED = PED.NUMPED
            JOIN PONTUAL.PCPRODUT PROD ON PEDI.CODPROD = PROD.CODPROD
        WHERE PROD.CODFORNEC = 588
            AND PED.DATA BETWEEN '01-MAY-2024' AND '31-MAY-2024'
            --AND PROD.CODSEC = 10001            
            AND PED.DTCANCEL IS NULL
            AND PED.CONDVENDA IN (1, 2, 3, 7, 9, 14, 15, 17, 18, 19, 98)
        GROUP BY PED.CODUSUR)        
        
-----------------------------------------------------------------------------------------------------------

SELECT  USUR.CODUSUR COD,
        SUBSTR(USUR.NOME, INSTR(USUR.NOME, ' ') + 1, INSTR(USUR.NOME, ' ', INSTR(USUR.NOME, ' ') + 1) - INSTR(USUR.NOME, ' ') - 1) AS RCA, -- EXTRAI O NOME
        FAT.FATURAMENTO AS "VENDIDO",
        NVL(A.DN,0) + NVL(B.DN,0) AS "DN"
FROM PONTUAL.PCUSUARI USUR
    left JOIN FATSTM FAT ON USUR.CODUSUR = FAT.RCA
    left JOIN DNDIST A ON USUR.CODUSUR = A.RCA
    left JOIN DNDIST2 B ON USUR.CODUSUR = B.RCA    
WHERE USUR.NOME LIKE 'PMU%'        
AND USUR.CODUSUR NOT IN (2,10,160)
ORDER BY VENDIDO DESC, DN DESC
