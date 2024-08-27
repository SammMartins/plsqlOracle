SELECT  a.codsupervisor,
        A.codusur RCA,
        A.CODCLI || ' ' || SUBSTR(B.CLIENTE,0,20) CLIENTE, 
        (CASE WHEN 
            (SELECT DISTINCT(X.CODCLI) 
                FROM PCPEDI X 
                WHERE X.CODCLI = A.CODCLI 
                AND TO_NUMBER(TO_CHAR(X.DATA, 'WW')) = TO_NUMBER(TO_CHAR(SYSDATE, 'WW'))
                AND TO_NUMBER(TO_CHAR(X.DATA, 'YY')) = TO_NUMBER(TO_CHAR(SYSDATE, 'YY'))
                AND X.POSICAO IN ('B','P') ) IS NOT NULL THEN 'SIM'
         ELSE 'NÃO' END
        ) AS "PED. SISTEMA",
        'R$' || REPLACE(round(A.valor,2), '.', ',') Título,
        'R$' || REPLACE(round((A.valor * 0.00333) * round(SYSDATE-A.dtvenc,0),2), '.', ',') "JUROS APROXIMADOS", 
        'R$' || REPLACE(round(A.valor + ((A.valor * 0.00333) * round(SYSDATE-A.dtvenc,0)), 2), '.', ',') Total,
        (CASE WHEN A.codcob LIKE 'SERA' THEN 'SERASA'
              WHEN A.codcob LIKE 'CHD1' THEN 'CHEQUE'
              WHEN A.codcob LIKE '7563' THEN 'BOLETO'
              ELSE 'OUTROS' END) AS "COB.", 
        round(SYSDATE-A.dtvenc,0)  "DIAS VENCIMENTO", 
        A.dtemissao EMISSAO,
        A.dtvenc VENCIMENTO
       
from pontual.pcprest A
join pontual.pcclient B on A.codcli = B.codcli
where A.dtvenc between SYSDATE-732 and SYSDATE-1
and A.vpago is NULL
and A.codUSUR in ({VENDEDOR})
and A.codcob in ('7563','SERA','C','CHD1')

order by "DIAS VENCIMENTO" Desc, TÍTULO Desc

