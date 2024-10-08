WITH FREEZER AS 
(SELECT M.CODCLI, 
        M.NUMNOTA, REPLACE(REPLACE(REPLACE(C.CGCENT, '.', ''), '/', ''),'-','') AS CNPJ, 
        TO_CHAR(M.DTMOV, 'YYYYMMDD') AS DT,
        P.CODPROD, 
        (CASE WHEN P.CODAUXILIARTRIB IS NULL OR P.CODAUXILIARTRIB < 1 THEN P.CODFAB||'     ' ELSE P.CODAUXILIARTRIB||'' END) EAN,
        TO_CHAR(ROUND(M.QT, 4), '000000000000000.0000') AS QT, 
        TO_CHAR(ROUND(M.PUNIT, 2), '00000.00') AS PUNIT, C.CODUSUR1,
        (CASE WHEN INSTR(C.CEPCOB, '-') = 0 THEN SUBSTR(C.CEPCOB, 1, 5) || '-' || SUBSTR(C.CEPCOB, 6)
                ELSE C.CEPCOB
                END) AS CEPCOB,
        M.CODOPER
    FROM PONTUAL.PCMOV M
    JOIN PONTUAL.PCCLIENT C ON C.CODCLI = M.CODCLI
    JOIN PONTUAL.PCPRODUT P ON P.CODPROD = M.CODPROD
    WHERE M.CODPROD IN (18663,18771,18772,18773,18774,18787,18946,18947)
    AND M.CODCLI IS NOT NULL
    AND M.CODOPER = 'SR'
    AND M.DTCANCEL IS NULL
    AND M.DTMOV BETWEEN '01-nov-2023' AND SYSDATE
    ORDER BY M.CODCLI DESC),
ESTOQ AS (
  SELECT CODPROD, NVL(DATA,SYSDATE) DATA, NVL(QTEST,0) QTEST, DTGERACAO FROM PCHISTEST
  WHERE CODPROD IN (18663,18771,18772,18773,18774,18787,18946,18947)
  AND CODFILIAL = 3
  AND DATA BETWEEN '17-SEP-2024' AND '17-SEP-2024'
)


SELECT 'H' || 'ESTOQ12' || (SELECT REPLACE(REPLACE(REPLACE(CGC, '.', ''), '/', ''),'-','') || (SELECT TO_CHAR(MAX(DATA), 'YYYYMMDD') FROM ESTOQ) FROM PCFORNEC WHERE CODFORNEC = 1841) as " " FROM DUAL

UNION ALL 
SELECT (RPAD('E' || '04831827000106' || RPAD(F.EAN, 14, ' '), 29, ' ') ||
       RPAD(LPAD(E.QTEST, 8, '0') || 'C', 9, ' ')
       --|| '00000000000000000000' --SEM COD PRATIMONIO
) AS " "
FROM DUAL 
JOIN FREEZER F ON F.CODPROD IN (18663,18771,18772,18773,18774,18787,18946,18947)--:PRODUTO
JOIN ESTOQ E ON E.CODPROD = F.CODPROD
GROUP BY F.EAN, E.QTEST