WITH METAFAT AS (
    SELECT D.CODSUPERVISOR CODSUPERVISOR,
           M.CODUSUR RCA, M.CODIGO CODSEC,
           NVL((CASE WHEN M.CLIPOSPREV IS NULL OR M.CLIPOSPREV = 0 THEN 500 
           ELSE M.CLIPOSPREV END),100) AS CLIPOSPREV
    FROM PONTUAL.PCMETA M 
    JOIN PONTUAL.PCUSUARI C ON M.CODUSUR = C.CODUSUR
    JOIN PONTUAL.PCSUPERV D ON C.CODSUPERVISOR = D.CODSUPERVISOR
    JOIN PONTUAL.PCSECAO E ON M.CODIGO = E.CODSEC
    WHERE M.DATA = '01-OUT-2023'
    AND M.TIPOMETA = 'S'
    AND E.CODSEC IN (10044)
    AND D.CODSUPERVISOR IN (2,8,9)),
---------------------------------------------------------------------------------------------------------------
METADN AS (
    SELECT D.CODSUPERVISOR CODSUPERVISOR,
           M.CODUSUR RCA, M.CODIGO CODSEC,
           NVL((CASE WHEN M.CLIPOSPREV IS NULL OR M.CLIPOSPREV = 0 THEN 10 
           ELSE M.CLIPOSPREV END),100) AS CLIPOSPREV
    FROM PONTUAL.PCMETA M 
    JOIN PONTUAL.PCUSUARI C ON M.CODUSUR = C.CODUSUR
    JOIN PONTUAL.PCSUPERV D ON C.CODSUPERVISOR = D.CODSUPERVISOR
    WHERE M.DATA = '01-OUT-2023'
    AND M.TIPOMETA = 'S'
    AND M.CODIGO IN (1719)
    AND D.CODSUPERVISOR IN (2,8,9)),
---------------------------------------------------------------------------------------------------------------
FAT AS 
    (SELECT PED.CODUSUR AS RCA,
            SUM(PED.QT*PED.PVENDA) AS FATURAMENTO
    FROM PONTUAL.PCPEDI PED
        JOIN PONTUAL.PCPRODUT PROD ON PED.CODPROD = PROD.CODPROD
    WHERE PROD.CODFORNEC = 1719
        AND TO_NUMBER(TO_CHAR(PED.DATA, 'MM')) = TO_NUMBER(TO_CHAR(SYSDATE, 'MM'))
        AND TO_NUMBER(TO_CHAR(PED.DATA, 'YY')) = TO_NUMBER(TO_CHAR(SYSDATE, 'YY'))
        AND PED.POSICAO NOT LIKE 'C'
        AND PED.VLBONIFIC = 0
    GROUP BY PED.CODUSUR
    ORDER BY PED.CODUSUR),
---------------------------------------------------------------------------------------------------------------
DN AS
    (SELECT PED.CODUSUR AS RCA,
            COUNT(DISTINCT PED.CODCLI) AS DN
        FROM PONTUAL.PCPEDC PED
            JOIN PONTUAL.PCPEDI PEDI ON PEDI.NUMPED = PED.NUMPED
            JOIN PONTUAL.PCPRODUT PROD ON PEDI.CODPROD = PROD.CODPROD
        WHERE PROD.CODFORNEC = 1719
            AND TO_NUMBER(TO_CHAR(PED.DATA, 'MM')) = TO_NUMBER(TO_CHAR(SYSDATE, 'MM'))
            AND TO_NUMBER(TO_CHAR(PED.DATA, 'YY')) = TO_NUMBER(TO_CHAR(SYSDATE, 'YY'))
            AND PED.DTCANCEL IS NULL
            AND PED.CONDVENDA IN (1, 2, 3, 7, 9, 14, 15, 17, 18, 19, 98)
        GROUP BY PED.CODUSUR
        ORDER BY PED.CODUSUR)
        
---------------------------------------------------------------------------------------------------------------

SELECT  RANK() OVER (ORDER BY (((F.FATURAMENTO / MF.CLIPOSPREV) + (D.DN / MD.CLIPOSPREV))/2) DESC) AS "RANK", 
        USUR.CODSUPERVISOR SUP,USUR.CODUSUR COD,     
        SUBSTR(USUR.NOME, INSTR(USUR.NOME, ' ') + 1, INSTR(USUR.NOME, ' ', INSTR(USUR.NOME, ' ') + 1) - INSTR(USUR.NOME, ' ') - 1) AS RCA, -- EXTRAI O NOME  
        
        D.DN "DN",
        MD.CLIPOSPREV "META",
        (D.DN / MD.CLIPOSPREV) "% ",
        D.DN - MD.CLIPOSPREV "GAP",
        
        MF.CLIPOSPREV "META FAT.",
        F.FATURAMENTO "REALIZADO",
        (F.FATURAMENTO / MF.CLIPOSPREV) "%",
        F.FATURAMENTO - MF.CLIPOSPREV "GAP ",
        
        (((F.FATURAMENTO / MF.CLIPOSPREV) + (D.DN / MD.CLIPOSPREV))/2) AS "% M�DIA"
        
FROM PONTUAL.PCUSUARI USUR
    JOIN FAT F ON F.RCA = USUR.CODUSUR
    JOIN DN D ON D.RCA = USUR.CODUSUR
    JOIN METADN MD ON MD.RCA = USUR.CODUSUR
    JOIN METAFAT MF ON MF.RCA = USUR.CODUSUR
WHERE USUR.NOME LIKE 'PMU%'
    AND USUR.CODSUPERVISOR IN (2,8,9)
ORDER BY RANK    


