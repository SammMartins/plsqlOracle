WITH UN AS (
    SELECT 
        D.CODUSUR,
        SUM(CASE WHEN D.CODPROD IN (18780) THEN D.QT ELSE 0 END) AS "18780",
        SUM(CASE WHEN D.CODPROD IN (18783) THEN D.QT ELSE 0 END) AS "18783",
        SUM(CASE WHEN D.CODPROD IN (18781) THEN D.QT ELSE 0 END) AS "18781"      
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
    U.CODUSUR,
    FLOOR(A."18780" / 8) AS "18780",
    FLOOR(A."18783" / 8) AS "18783",
    FLOOR(A."18781" / 8) AS "18781"    

FROM 
    PCUSUARI U
JOIN 
    UN A ON U.CODUSUR = A.CODUSUR
WHERE 
    U.CODUSUR IN (140, 141, 142, 143, 145, 147, 148, 150, 151, 152, 153, 154, 155, 156, 157, 158, 161, 164, 167, 168, 169, 170, 172, 174)

