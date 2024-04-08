WITH FATSTM AS 
    (SELECT PED.CODUSUR AS RCA,
            SUM(PED.QT*PED.PVENDA) + 0 AS FATURAMENTO
    FROM PONTUAL.PCPEDI PED
        JOIN PONTUAL.PCPRODUT PROD ON PED.CODPROD = PROD.CODPROD
    WHERE PROD.CODFORNEC = 1658
        AND PED.DATA BETWEEN '01-FEv-2024' AND '30-abr-2024'
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
        WHERE PROD.CODFORNEC = 1658
            AND PED.DATA BETWEEN '01-FEv-2024' AND '29-FEv-2024'
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
        WHERE PROD.CODFORNEC = 1658
            AND PED.DATA BETWEEN '01-MAR-2024' AND '31-MAR-2024'
            --AND PROD.CODSEC = 10001            
            AND PED.DTCANCEL IS NULL
            AND PED.CONDVENDA IN (1, 2, 3, 7, 9, 14, 15, 17, 18, 19, 98)
        GROUP BY PED.CODUSUR),      
DNDIST3 AS
    (SELECT PED.CODUSUR AS RCA,
            COUNT(DISTINCT PED.CODCLI) AS DN
        FROM PONTUAL.PCPEDC PED
            JOIN PONTUAL.PCPEDI PEDI ON PEDI.NUMPED = PED.NUMPED
            JOIN PONTUAL.PCPRODUT PROD ON PEDI.CODPROD = PROD.CODPROD
        WHERE PROD.CODFORNEC = 1658
            AND PED.DATA BETWEEN '01-abr-2024' AND '30-abr-2024'
            --AND PROD.CODSEC = 10001            
            AND PED.DTCANCEL IS NULL
            AND PED.CONDVENDA IN (1, 2, 3, 7, 9, 14, 15, 17, 18, 19, 98)
        GROUP BY PED.CODUSUR)        
        
-----------------------------------------------------------------------------------------------------------

SELECT  usur.codusur cod,
        SUBSTR(usur.nome, INSTR(usur.nome, ' ') + 1, INSTR(usur.nome, ' ', INSTR(usur.nome, ' ') + 1) - INSTR(usur.nome, ' ') - 1) AS RCA, -- Extrai o nome
        fat.faturamento AS "VENDIDO",
        a.DN + b.DN + c.DN AS "DN"
FROM pontual.PCUSUARI usur
    JOIN FatStm fat ON usur.codusur = fat.RCA
    JOIN DNDIST a ON usur.codusur = a.RCA
    JOIN DNDIST2 b ON usur.codusur = b.RCA    
    JOIN DNDIST3 c ON usur.codusur = c.RCA        
WHERE usur.nome like 'PMU%'        
ORDER BY VENDIDO DESC, DN DESC
