WITH Fat AS 
     (SELECT distinct(a.codsupervisor) codsupervisor,
             SUM(a.vlatend) Valor
        FROM pontual.PCPEDC a
        JOIN pontual.pcclient c on c.codcli = a.codcli
        WHERE a.DATA BETWEEN '{dtIni}' AND '{dtFim}'
          AND a.DTCANCEL IS NULL
          AND a.CONDVENDA IN (1, 2, 3, 7, 9, 14, 15, 17, 18, 19, 98)
          AND a.CODCOB IN ('7563','CH','C','D','DH')
          AND a.vlbonific = 0
          AND A.NUMPEDRCA IS NOT NULL -- GARANTE APENAS PEDIDOS DIGITADOS PELO RCA
          --AND c.TIPOFJ = 'J' 
          GROUP BY a.codsupervisor),
-----------------------------------------------------------------------------------------------------------------------
DN AS (SELECT ped.codsupervisor codsupervisor,
                COUNT(DISTINCT ped.codcli) AS DN
            FROM pontual.PCPEDC ped
                JOIN pontual.PCPEDI pedi on pedi.numped = ped.numped
                JOIN pontual.pcprodut prod on pedi.codprod = prod.codprod
            WHERE ped.DATA BETWEEN '{dtIni}' AND '{dtFim}'
                AND PED.DTCANCEL IS NULL
                AND PED.CONDVENDA IN (1, 2, 3, 7, 9, 14, 15, 17, 18, 19, 98)
                AND A.NUMPEDRCA IS NOT NULL -- GARANTE APENAS PEDIDOS DIGITADOS PELO RCA
            GROUP BY ped.codsupervisor)
-----------------------------------------------------------------------------------------------------------------------
SELECT (CASE WHEN f.codsupervisor = 2 THEN 'ADAILTON'
             WHEN f.codsupervisor = 8 THEN 'VILMAR'
             ELSE 'ERRO! CONTATE A TI' END) SUPERVISOR,
             f.valor VENDIDO, D.DN DN, f.codsupervisor
FROM FAT F
JOIN DN D on d.codsupervisor = f.codsupervisor
WHERE f.codsupervisor in (2,8)
ORDER BY  f.valor desc