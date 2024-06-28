SELECT
    ped.codcli || '' AS Cliente,
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
    a.codcli || '' AS Cliente,
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
    a.codcli || '' AS Cliente,
    a.codusur1 AS RCA,
    'Erro Cadastro UF' AS Tipo,
    NULL AS Status
FROM PONTUAL.pcclient a
WHERE a.ESTENT LIKE '' OR a.ESTENT IS NULL
------------------------------------------------------------------------------------------------------------------
UNION ALL
SELECT DISTINCT
    a.codcli || '' AS Cliente,
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
    c.codcli || '' AS Cliente,
    c.codusur AS RCA,
    'SICOOB & ' || c.codplpag AS Tipo,
    (CASE
        WHEN c.posicao LIKE 'B' THEN c.posicao || 'loqueado' 
        WHEN c.posicao LIKE 'C' THEN c.posicao || 'ancelado'
        WHEN c.posicao LIKE 'P' THEN c.posicao || 'endente'
        WHEN c.posicao LIKE 'M' THEN c.posicao || 'ontado'
        ELSE c.posicao || 'iberado'
        END) AS Status 
FROM PONTUAL.PCPEDC c 
WHERE c.CODCOB IN ('7563') 
and c.codplpag not in (3,4,5,6,10,12,17,21,28,29,38,39,40,41,43,44,45,46,47,70)
AND c.posicao NOT IN ('F', 'C')
AND c.data > SYSDATE-6
------------------------------------------------------------------------------------------------------------------
UNION ALL
SELECT DISTINCT
    c.codcli || '' AS Cliente,
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
SELECT 
    liberados.Cliente || '',
    liberados.RCA,
    liberados.Contagem || ' Liberado(s), ' || NVL(bloqueados.Contagem, 0) || ' BLOQUEADO(s)' AS Tipo,
    '' AS Status
FROM
    (SELECT 
        c.codcli AS Cliente,
        c.codusur AS RCA,
        COUNT(DISTINCT c.numped) AS Contagem
    FROM
        PONTUAL.PCPEDC c 
    WHERE
        c.data BETWEEN SYSDATE-7 AND SYSDATE
    AND 
        c.posicao = 'L' --LIBERADO
    GROUP BY 
        c.codcli, 
        c.codusur) liberados
LEFT JOIN
    (SELECT 
        b.codcli AS Cliente,
        b.codusur AS RCA,
        COUNT(DISTINCT b.numped) AS Contagem
    FROM
        PONTUAL.PCPEDC b 
    WHERE
        b.data BETWEEN SYSDATE-7 AND SYSDATE
    AND 
        b.posicao IN ('P', 'B') --PENDENTE OU BLOQUEADO
    GROUP BY 
        b.codcli, 
        b.codusur) bloqueados
ON
    liberados.Cliente = bloqueados.Cliente --AND liberados.RCA = bloqueados.RCA
WHERE 
    bloqueados.Contagem IS NOT NULL
AND (
        (TO_CHAR(SYSDATE, 'D') BETWEEN 2 AND 5 AND TO_CHAR(SYSDATE, 'HH24:MI') > '15:30')
        OR
        (TO_CHAR(SYSDATE, 'D') = 6 AND TO_CHAR(SYSDATE, 'HH24:MI') > '11:45')
        OR
        TO_CHAR(SYSDATE, 'D') = 7
    )    
