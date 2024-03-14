WITH UN AS (
    SELECT 
        D.CODUSUR,
        SUM(CASE WHEN D.CODPROD IN (18394, 18637, 18639) THEN D.QT ELSE 0 END) AS UNIDADES_TORTILLA,
        SUM(CASE WHEN D.CODPROD IN (18636, 18776) THEN D.QT ELSE 0 END) AS UNIDADES_ASSADO
    FROM
        PCPEDI D
    WHERE
        D.DATA BETWEEN '01-MAR-2024' AND '31-MAR-2024'
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
    FLOOR(A.UNIDADES_TORTILLA / 20) AS "CAIXAS DE TORTILLA",
    FLOOR(A.UNIDADES_ASSADO / 10) AS "CAIXAS DE GUL„O ASSADO",
    TRUNC((((A.UNIDADES_TORTILLA * 3.0) + (A.UNIDADES_ASSADO * 2.0)) / 20),1) AS "R$ TOTAL"
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
       SUM(CASE WHEN A.CODUSUR IN (143, 145, 148, 150, 151, 152, 153, 154, 164, 168, 174)
                THEN A.UNIDADES_TORTILLA ELSE 0 END) / 20 AS "CAIXAS DE TORTILLA",
        --------------------------------------------------------------------
       SUM(CASE WHEN A.CODUSUR IN (143, 145, 148, 150, 151, 152, 153, 154, 164, 168, 174)
                THEN A.UNIDADES_ASSADO ELSE 0 END) / 10 AS "CAIXAS DE GUL√O ASSADO",
        --------------------------------------------------------------------
       ((SUM(CASE WHEN A.CODUSUR IN (143, 145, 148, 150, 151, 152, 153, 154, 164, 168, 174)
                THEN A.UNIDADES_TORTILLA ELSE 0 END) / 20) * 3.0) +
       ((SUM(CASE WHEN A.CODUSUR IN (143, 145, 148, 150, 151, 152, 153, 154, 164, 168, 174)
                THEN A.UNIDADES_ASSADO ELSE 0 END) / 10) * 2.0) AS "R$ TOTAL"
FROM UN A
