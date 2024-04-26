WITH Fat AS 
     (SELECT a.CODCLI,
            a.codusur codusur,
            a.CODSUPERVISOR,
            SUM(a.vlatend) Valor
        FROM pontual.PCPEDC a
        JOIN pontual.pcclient c on c.codcli = a.codcli
        WHERE a.DATA BETWEEN sysdate-7 AND sysdate
          AND a.DTCANCEL IS NULL
          AND a.CONDVENDA IN (1, 2, 3, 7, 9, 14, 15, 17, 18, 19, 98)
          AND a.CODCOB IN ('7563','CH','C','D','DH')
          AND a.vlbonific = 0
          --AND c.TIPOFJ = 'J' 
          GROUP BY a.codusur,a.CODCLI,a.CODSUPERVISOR)
-----------------------------------------------------------------------------------------------------------------------
SELECT  f.codcli || ' - ' || C.CLIENTE,
        U.codsupervisor, 
        f.codusur || ' - ' || SUBSTR(U.nome, INSTR(U.nome, ' ') + 1, INSTR(U.nome, ' ', INSTR(U.nome, ' ') + 1) - INSTR(U.nome, ' ') - 1) || ' Sup. ' || U.codsupervisor AS RCA,
        F.valor
FROM FAT F
JOIN pontual.pcusuari u on u.codusur = f.codusur
JOIN PONTUAL.PCCLIENT C ON C.CODCLI = F.CODCLI
WHERE f.codusur not in (10,50)
ORDER BY  f.valor desc