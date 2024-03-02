SELECT
    ped.codcli AS Cliente,
    pedc.codusur AS RCA,
    'Possível Duplicidade' AS Tipo,
    (CASE
        WHEN pedc.posicao LIKE 'B' THEN pedc.posicao || 'loqueado'
        WHEN pedc.posicao LIKE 'C' THEN pedc.posicao || 'ancelado'
        WHEN pedc.posicao LIKE 'P' THEN pedc.posicao || 'endente'
        WHEN pedc.posicao LIKE 'M' THEN pedc.posicao || 'ontado'
        ELSE pedc.posicao || 'iberado'
        END) AS Status
FROM
    PONTUAL.pcpedi ped
JOIN
    PONTUAL.pcpedc pedc ON ped.codcli = pedc.codcli
AND ped.numped = pedc.numped
AND ped.data = pedc.data
LEFT JOIN
    (
    SELECT
        ped2.codcli,
        ped2.codprod
    FROM
        PONTUAL.pcpedi ped2
    JOIN
        PONTUAL.pcpedc pedc2 ON ped2.numped = pedc2.numped
    WHERE
        ped2.data BETWEEN SYSDATE-7 AND SYSDATE
    AND ped2.posicao NOT IN ('F', 'C')
    AND pedc2.CONDVENDA NOT IN (5, 11)
    GROUP BY
        ped2.codcli,
        ped2.codprod
    HAVING COUNT(*) > 1
    ) ped2 ON ped.codcli = ped2.codcli 
WHERE
    ped.data BETWEEN SYSDATE-7 AND SYSDATE
AND ped.posicao NOT IN ('F', 'C')
AND pedc.CONDVENDA NOT IN (5, 11)
AND ped2.codcli IS NOT NULL
GROUP BY
    ped.codcli,
    pedc.codusur,
    pedc.posicao
------------------------------------------------------------------------------------------------------------------
UNION ALL
SELECT DISTINCT
    a.codcli AS Cliente,
    pedc.codusur AS RCA,
    'BNF SEM PEDIDO' AS Tipo,
    (CASE
        WHEN pedc.posicao LIKE 'B' THEN pedc.posicao || 'loqueado' 
        WHEN pedc.posicao LIKE 'C' THEN pedc.posicao || 'ancelado'
        WHEN pedc.posicao LIKE 'P' THEN pedc.posicao || 'endente'
        WHEN pedc.posicao LIKE 'M' THEN pedc.posicao || 'ontado'
        ELSE pedc.posicao || 'iberado'
        END) AS Status
FROM PONTUAL.pcpedc a
JOIN PONTUAL.pcpedc pedc ON pedc.codcli = a.codcli AND pedc.numped = a.numped AND pedc.data = a.data
WHERE a.data BETWEEN SYSDATE-7 AND SYSDATE
AND a.CONDVENDA IN (5,11)
AND a.posicao != 'F' AND a.posicao != 'C'
AND NOT EXISTS (
    SELECT 1 FROM PONTUAL.pcpedc b
    WHERE b.data BETWEEN SYSDATE-7 AND SYSDATE
    AND b.CONDVENDA = 1
    AND a.codcli = b.codcli
    AND a.posicao != 'F' AND a.posicao != 'C'
)
AND a.codcli != 11185 --Premium
------------------------------------------------------------------------------------------------------------------
UNION ALL
SELECT DISTINCT
    a.codcli AS Cliente,
    a.codusur1 AS RCA,
    'Erro Cadastro UF' AS Tipo,
    NULL AS Status
FROM PONTUAL.pcclient a
WHERE a.ESTENT LIKE '' OR a.ESTENT IS NULL
------------------------------------------------------------------------------------------------------------------
UNION ALL
SELECT DISTINCT
    a.codcli AS Cliente,
    a.codusur AS RCA,
    'PEDIDO ABAIXO DO MÍNIMO' AS Tipo,
    (CASE
        WHEN a.posicao LIKE 'B' THEN a.posicao || 'loqueado' 
        WHEN a.posicao LIKE 'C' THEN a.posicao || 'ancelado'
        WHEN a.posicao LIKE 'P' THEN a.posicao || 'endente'
        WHEN a.posicao LIKE 'M' THEN a.posicao || 'ontado'
        ELSE a.posicao || 'iberado'
        END) AS Status
FROM PONTUAL.pcpedc a
WHERE a.data > SYSDATE-6
AND a.CONDVENDA IN (1)
AND a.posicao != 'F' AND a.posicao != 'C'
AND a.vlatend < 100
------------------------------------------------------------------------------------------------------------------
UNION ALL
SELECT DISTINCT
    c.codcli AS Cliente,
    c.codusur AS RCA,
    'CODCOB != CODPLPAG' AS Tipo,
    (CASE
        WHEN c.posicao LIKE 'B' THEN c.posicao || 'loqueado' 
        WHEN c.posicao LIKE 'C' THEN c.posicao || 'ancelado'
        WHEN c.posicao LIKE 'P' THEN c.posicao || 'endente'
        WHEN c.posicao LIKE 'M' THEN c.posicao || 'ontado'
        ELSE c.posicao || 'iberado'
        END) AS Status 
FROM PONTUAL.PCPEDC c 
WHERE c.CODCOB IN ('7563') 
and c.codplpag not in (3,4,10,21,28,29,38,39,40,41,43,44,45,17)
AND c.posicao NOT IN ('F', 'C')
AND c.data > SYSDATE-6
------------------------------------------------------------------------------------------------------------------
UNION ALL
SELECT DISTINCT
    c.codcli AS Cliente,
    c.codusur AS RCA,
    'CODCOB BNF != CODPLPAG BNF' AS Tipo,
    (CASE
        WHEN c.posicao LIKE 'B' THEN c.posicao || 'loqueado' 
        WHEN c.posicao LIKE 'C' THEN c.posicao || 'ancelado'
        WHEN c.posicao LIKE 'P' THEN c.posicao || 'endente'
        WHEN c.posicao LIKE 'M' THEN c.posicao || 'ontado'
        ELSE c.posicao || 'iberado'
        END) AS Status 
FROM PONTUAL.PCPEDC c 
WHERE c.CODCOB IN ('BNF','BNFT','BNFP') 
and c.codplpag not in (8)
AND c.posicao NOT IN ('F', 'C')
------------------------------------------------------------------------------------------------------------------
UNION ALL
SELECT DISTINCT 
    c.codcli AS Cliente,
    c.codusur AS RCA,
    'PEDIDOS BLOQUEADOS' AS Tipo,
    (CASE
        WHEN c.posicao LIKE 'B' THEN c.posicao || 'loqueado' 
        WHEN c.posicao LIKE 'C' THEN c.posicao || 'ancelado'
        WHEN c.posicao LIKE 'P' THEN c.posicao || 'endente'
        WHEN c.posicao LIKE 'M' THEN c.posicao || 'ontado'
        ELSE c.posicao || 'iberado'
    END) AS Status
FROM
    PONTUAL.PCPEDC c 
WHERE
    C.data BETWEEN SYSDATE-7 AND SYSDATE
AND
    C.posicao = 'L' --LIBERADO
AND EXISTS (
        SELECT 1 
        FROM 
            PONTUAL.pcpedc b
        WHERE 
            b.data = C.DATA
        AND 
            C.codcli = b.codcli
        AND 
            B.NUMPED != C.NUMPED
        AND 
            (B.posicao = 'P' OR B.posicao = 'B') --PENDENTE OU BLOQUEADO
        )