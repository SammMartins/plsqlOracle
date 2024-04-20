WITH UN AS (
    SELECT 
        D.CODUSUR,
        SUM(CASE WHEN D.CODPROD IN (18394, 18637, 18639) THEN D.QT ELSE 0 END) AS UNIDADES_TORTILLA,
        SUM(CASE WHEN D.CODPROD IN (18592,18591,18589,18590,18593,18646,18642,18644,18636,18776,18641,18766,18635,18643) THEN D.QT ELSE 0 END) AS UNIDADES_ASSADO
    FROM
        PCPEDI D
    WHERE
        D.DATA BETWEEN '01-abr-2024' AND '30-abr-2024'
    AND
        D.POSICAO NOT LIKE 'C'
    --AND 
        --D.VLBONIFIC = 0 
    GROUP BY
        D.CODUSUR
)
----------------------------------------------------------------------------------------------------------------------------------------

SELECT 
    (U.CODUSUR || ' - ' || SUBSTR(U.NOME,5,60)) AS "VENDEDOR",
    FLOOR(A.UNIDADES_TORTILLA / 20) AS "CX TORTILLA",
    FLOOR(A.UNIDADES_ASSADO / 10) AS "CX GULÃO ASSADO",
    
    TRUNC((((A.UNIDADES_TORTILLA * 3.0) + (A.UNIDADES_ASSADO * 2.0)) / 20),1) +
    (CASE WHEN (FLOOR(A.UNIDADES_TORTILLA / 20) > 100) 
            OR (FLOOR(A.UNIDADES_ASSADO / 10) > 100) THEN 100 ELSE 0 END) +
    (CASE WHEN (FLOOR(A.UNIDADES_TORTILLA / 20) > 200) 
            OR (FLOOR(A.UNIDADES_ASSADO / 10) > 200) THEN 100 ELSE 0 END) +
    (CASE WHEN (FLOOR(A.UNIDADES_TORTILLA / 20) > 300) 
            OR (FLOOR(A.UNIDADES_ASSADO / 10) > 300) THEN 100 ELSE 0 END) +
    (CASE WHEN (FLOOR(A.UNIDADES_TORTILLA / 20) > 400) 
            OR (FLOOR(A.UNIDADES_ASSADO / 10) > 400) THEN 100 ELSE 0 END) +
    (CASE WHEN (FLOOR(A.UNIDADES_TORTILLA / 20) > 500) 
            OR (FLOOR(A.UNIDADES_ASSADO / 10) > 500) THEN 100 ELSE 0 END) AS "R$ TOTAL"
FROM 
    PCUSUARI U
JOIN 
    UN A ON U.CODUSUR = A.CODUSUR
WHERE 
    U.CODUSUR IN (140, 141, 142, 143, 145, 147, 148, 150, 151, 152, 153, 154, 155, 156, 157, 158, 161, 164, 167, 168, 169, 170, 172, 174)
----------------------------------------------------------------------------------------------------------------------------------------

UNION ALL
SELECT '2 - ADAILTON' AS "VENDEDOR",
        --------------------------------------------------------------------
       (SUM(CASE WHEN A.CODUSUR IN (143, 145, 148, 150, 151, 152, 153, 154, 164, 168, 174)
                THEN A.UNIDADES_TORTILLA ELSE 0 END) / 20) AS "CX TORTILLA",
        --------------------------------------------------------------------
       (SUM(CASE WHEN A.CODUSUR IN (143, 145, 148, 150, 151, 152, 153, 154, 164, 168, 174)
                THEN A.UNIDADES_ASSADO ELSE 0 END) / 10) AS "CX GULÃO ASSADO",
        --------------------------------------------------------------------
       (CASE WHEN ((SUM(CASE WHEN A.CODUSUR IN (143, 145, 148, 150, 151, 152, 153, 154, 164, 168, 174)
                    THEN A.UNIDADES_TORTILLA ELSE 0 END) / 20) / 11) > 50 THEN 500 ELSE 0 END) +
       (CASE WHEN ((SUM(CASE WHEN A.CODUSUR IN (143, 145, 148, 150, 151, 152, 153, 154, 164, 168, 174)
                    THEN A.UNIDADES_ASSADO ELSE 0 END) / 10) / 11) > 30 THEN 300 ELSE 0 END) AS "R$ TOTAL"
FROM UN A
----------------------------------------------------------------------------------------------------------------------------------------

UNION ALL
SELECT '8 - VILMAR' AS "VENDEDOR",
        --------------------------------------------------------------------
       SUM(CASE WHEN A.CODUSUR IN (140, 141, 142, 147, 155, 156, 157, 158, 161, 167, 169, 170, 172)
                THEN A.UNIDADES_TORTILLA ELSE 0 END) / 20 AS "CX TORTILLA",
        --------------------------------------------------------------------
       SUM(CASE WHEN A.CODUSUR IN (140, 141, 142, 147, 155, 156, 157, 158, 161, 167, 169, 170, 172)
                THEN A.UNIDADES_ASSADO ELSE 0 END) / 10 AS "CX GULÃO ASSADO",
        --------------------------------------------------------------------
       ((CASE WHEN ((SUM(CASE WHEN A.CODUSUR IN (140, 141, 142, 147, 155, 156, 157, 158, 161, 167, 169, 170, 172)
                    THEN A.UNIDADES_TORTILLA ELSE 0 END) / 20) / 13) > 50 THEN 500 ELSE 0 END) +
       (CASE WHEN ((SUM(CASE WHEN A.CODUSUR IN (140, 141, 142, 147, 155, 156, 157, 158, 161, 167, 169, 170, 172)
                    THEN A.UNIDADES_ASSADO ELSE 0 END) / 10) / 13) > 30 THEN 300 ELSE 0 END)) AS "R$ TOTAL"
FROM UN A
ORDER BY VENDEDOR
----------------------------------------------------------------------------------------------------------------------------------------
/*
UNION ALL
SELECT '$ - TOTAL' AS "VENDEDOR",
        --------------------------------------------------------------------
       (SUM(CASE WHEN A.CODUSUR IN (140, 141, 142, 147, 155, 156, 157, 158, 161, 167, 169, 170, 172)
                THEN A.UNIDADES_TORTILLA ELSE 0 END) / 20) +
       (SUM(CASE WHEN A.CODUSUR IN (143, 145, 148, 150, 151, 152, 153, 154, 164, 168, 174)
                THEN A.UNIDADES_TORTILLA ELSE 0 END) / 20) AS "CX TORTILLA",                
        --------------------------------------------------------------------
       (SUM(CASE WHEN A.CODUSUR IN (140, 141, 142, 147, 155, 156, 157, 158, 161, 167, 169, 170, 172)
                THEN A.UNIDADES_ASSADO ELSE 0 END) / 10)  +
       (SUM(CASE WHEN A.CODUSUR IN (143, 145, 148, 150, 151, 152, 153, 154, 164, 168, 174)
                THEN A.UNIDADES_ASSADO ELSE 0 END) / 10) AS "CX GULÃO ASSADO",                
        --------------------------------------------------------------------
       (CASE WHEN (((SUM(CASE WHEN A.CODUSUR IN (143, 145, 148, 150, 151, 152, 153, 154, 164, 168, 174)
                    THEN A.UNIDADES_TORTILLA ELSE 0 END) / 20) / 11) + 
                  ((SUM(CASE WHEN A.CODUSUR IN (143, 145, 148, 150, 151, 152, 153, 154, 164, 168, 174)
                    THEN A.UNIDADES_ASSADO ELSE 0 END) / 10) / 11)) > 50 THEN 500 ELSE 0 END) +
                    
       (CASE WHEN (((SUM(CASE WHEN A.CODUSUR IN (140, 141, 142, 147, 155, 156, 157, 158, 161, 167, 169, 170, 172)
                    THEN A.UNIDADES_TORTILLA ELSE 0 END) / 20) / 13) + 
                  ((SUM(CASE WHEN A.CODUSUR IN (140, 141, 142, 147, 155, 156, 157, 158, 161, 167, 169, 170, 172)
                    THEN A.UNIDADES_ASSADO ELSE 0 END) / 10) / 13)) > 50 THEN 500 ELSE 0 END) AS "R$ TOTAL"
FROM UN A
ORDER BY VENDEDOR
