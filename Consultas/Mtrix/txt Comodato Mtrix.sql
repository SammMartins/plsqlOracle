WITH FREEZER AS 
(SELECT M.CODCLI, 
        M.NUMNOTA, REPLACE(REPLACE(REPLACE(C.CGCENT, '.', ''), '/', ''),'-','') AS CNPJ, 
        TO_CHAR(M.DTMOV, 'YYYYMMDD') AS DT,
        P.CODPROD, NVL(P.CODAUXILIARTRIB,'0') EAN, TO_CHAR(ROUND(M.QT, 4), '000000000000000.0000') AS QT, 
        TO_CHAR(ROUND(M.PUNIT, 2), '00000.00') AS PUNIT, C.CODUSUR1,
        (CASE WHEN INSTR(C.CEPCOB, '-') = 0 THEN SUBSTR(C.CEPCOB, 1, 5) || '-' || SUBSTR(C.CEPCOB, 6)
                ELSE C.CEPCOB
                END) AS CEPCOB,
        M.CODOPER
    FROM PONTUAL.PCMOV M
    JOIN PONTUAL.PCCLIENT C ON C.CODCLI = M.CODCLI
    JOIN PONTUAL.PCPRODUT P ON P.CODPROD = M.CODPROD
    WHERE M.CODPROD IN (18772,18662,18773,18664,18774,18771,18663)
    AND M.CODCLI IS NOT NULL
    AND M.CODOPER = 'SR'
    AND M.DTCANCEL IS NULL
    AND M.DTMOV BETWEEN '01-nov-2023' AND SYSDATE
    ORDER BY M.CODCLI DESC)

SELECT ('H' || 'COMODATO13' || (SELECT REPLACE(REPLACE(REPLACE(CGC, '.', ''), '/', ''),'-','') FROM PCFORNEC WHERE CODFORNEC = 1841)) AS " " FROM DUAL

UNION ALL 
SELECT (RPAD('D' || '04831827000106' || F.CNPJ, 51, ' ') ||
       RPAD(F.DT || '1' || F.NUMNOTA, 27, ' ') ||
       RPAD(REPLACE(TO_CHAR(F.EAN, '90000000000000') || F.QT || F.PUNIT, ' ', ''), 41, ' ') ||
       RPAD(F.CODUSUR1, 19, ' ') || RPAD('C' || F.CEPCOB, 16, ' ') || '1' || RPAD(F.CODUSUR1, 19, ' ') || 
       (CASE WHEN F.CODOPER = 'SR' THEN '1 ' ELSE '2 ' END)
       || '00000000000000000000' --SEM COD PRATIMONIO
) AS " "
FROM DUAL JOIN FREEZER F ON F.CODPROD = 18663