WITH RELWINT AS (
    SELECT 
        PCNFENT.NUMNOTA,
        PCNFENT.DTENT,
        NVL(PCNFSAID.NUMCAR,0) NUMCARREGAMENTO,
        PCNFENT.DTSAIDA,
        DECODE(PCNFENT.VLTOTAL,0,PCESTCOM.VLDEVOLUCAO,PCNFENT.VLTOTAL) AS VLTOTAL,
        0 VLTOTAL1,
        PCNFENT.CODDEVOL,
        PCNFENT.OBS,
        PCTABDEV.MOTIVO,
        PCNFENT.NUMTRANSENT,
        PCNFENT.ROTINALANC,
        NVL(PCNFENT.TOTPESO,0) TOTPESO,
        0 TOTPESO1,
        PCNFSAID.CODFILIALNF,
        PCCLIENT.CODCLI,
        PCCLIENT.CLIENTE, 
        PCCLIENT.MUNICENT,
        PCCLIENT.ENDERENT,
        PCCLIENT.TELENT, 
        PCNFENT.CODUSURDEVOL, 
        PCNFENT.CODMOTORISTADEVOL,
        PCEMPR.NOME,
        PCUSUARI.NOME NOMERCA,
        PCUSUARI.CODSUPERVISOR,
        PCSUPERV.NOME SUPERVISOR,
        FUNC.NOME NOMEFUNC,
        PCNFENT.CODFORNEC,
        PCFORNEC.FORNECEDOR,
        0 QTAVARIA,
        0 VLAVARIA,
        PCNFENT.VLFRETE,
        PCNFENT.VLOUTRAS, 
        ( 
            SELECT SUM (
                DECODE(PCMOV.Tipoitem,'C',0, 
                    (
                        (
                            DECODE(NVL(PCMOV.QT,0),0,NVL(PCMOV.QTCONT,0),NVL(PCMOV.QT,0))
                        ) * 
                        (
                            DECODE(NVL(PCMOV.PUNIT,0),0,NVL(PCMOV.PUNITCONT,0),NVL(PCMOV.PUNIT,0)) + 
                            NVL(PCMOV.VLOUTROS,0) + 
                            NVL(PCMOV.VLFRETE,0)
                        )
                    )
                )
            ) AS VALORDEV 
            FROM   PONTUAL.PCMOV, PONTUAL.PCPRODUT
            WHERE  PCMOV.CODPROD = PCPRODUT.CODPROD
            AND    PCMOV.NUMTRANSENT = PCNFENT.NUMTRANSENT
            AND    PCMOV.CODOPER IN ('ED','EN')
            AND    PCMOV.DTCANCEL IS NULL
        ) VLPORFORNEC 
    FROM 
        PONTUAL.PCNFENT, 
        PONTUAL.PCESTCOM, 
        PONTUAL.PCTABDEV, 
        PONTUAL.PCCLIENT,
        PONTUAL.PCEMPR, 
        PONTUAL.PCUSUARI, 
        PONTUAL.PCSUPERV, 
        PONTUAL.PCEMPR FUNC, 
        PONTUAL.PCFORNEC, 
        PONTUAL.PCNFSAID, 
        PONTUAL.PCMOV M
    WHERE  
        ( 
            PCNFENT.CODDEVOL = PCTABDEV.CODDEVOL(+) 
        ) 
        AND PCNFENT.NUMTRANSENT = PCESTCOM.NUMTRANSENT(+) 
        AND PCNFENT.NUMNOTA = M.NUMNOTA 
        AND PCNFENT.DTENT = M.DTMOV 
        AND PCESTCOM.NUMTRANSVENDA = PCNFSAID.NUMTRANSVENDA(+) 
        AND PCNFENT.codfornec = PCFORNEC.codfornec(+) 
        AND   ( PCNFENT.CODFORNEC = PCCLIENT.CODCLI(+) ) 
        AND   ( PCNFENT.CODFUNCLANC = FUNC.MATRICULA(+)) 
        AND   ( PCNFENT.CODMOTORISTADEVOL = PCEMPR.MATRICULA(+))
        AND   ( PCNFENT.CODUSURDEVOL = PCUSUARI.CODUSUR) 
        AND   ( PCUSUARI.CODSUPERVISOR = PCSUPERV.CODSUPERVISOR(+) ) 
        AND   ( PCNFENT.DTENT BETWEEN TO_DATE('01-01-2024', 'DD-MM-YYYY') AND SYSDATE ) 
        AND NVL(PCNFSAID.CONDVENDA,0) NOT IN (4, 8, 10, 13, 20, 98, 99)
        AND   ( PCNFENT.TIPODESCARGA IN ('6','7','T') ) 
        AND   ( NVL(PCNFENT.OBS, 'X') <> 'NF CANCELADA') 
        AND   ( PCNFENT.CODFISCAL IN ('131','132','231','232','199','299') ) 
        AND EXISTS (
            SELECT PCPRODUT.CODPROD 
            FROM PONTUAL.PCPRODUT, PONTUAL.PCMOV
            WHERE PCMOV.CODPROD = PCPRODUT.CODPROD
            AND PCMOV.NUMTRANSENT = PCNFENT.NUMTRANSENT
            AND PCMOV.NUMNOTA = PCNFENT.NUMNOTA
            AND  ( PCNFENT.DTENT BETWEEN TO_DATE('01-01-2024', 'DD-MM-YYYY') AND SYSDATE ) 
            AND PCMOV.CODFILIAL = PCNFENT.CODFILIAL
        )
    GROUP BY 
        pcnfent.numnota,
        PCNFENT.DTENT,
        NVL(PCNFSAID.NUMCAR,0),
        PCNFENT.DTSAIDA,
        PCNFENT.CODDEVOL, 
        PCNFENT.CODUSURDEVOL,
        PCNFENT.OBS,
        PCTABDEV.MOTIVO,
        PCNFENT.NUMTRANSENT,
        PCNFENT.ROTINALANC,
        NVL(PCNFENT.TOTPESO,0),
        PCNFSAID.CODFILIALNF,
        PCCLIENT.CODCLI,
        PCCLIENT.CLIENTE, 
        PCCLIENT.MUNICENT,
        PCCLIENT.ENDERENT,
        PCCLIENT.TELENT, 
        PCNFENT.CODMOTORISTADEVOL, 
        PCEMPR.NOME,
        PCUSUARI.NOME ,
        PCUSUARI.CODSUPERVISOR,
        PCSUPERV.NOME ,
        FUNC.NOME ,
        PCNFENT.CODFORNEC,
        PCFORNEC.FORNECEDOR,
        PCNFENT.VLFRETE,
        PCNFENT.VLOUTRAS,
        PCNFENT.VLTOTAL,
        PCESTCOM.VLDEVOLUCAO,
        PCNFSAID.NUMCAR 
    ORDER BY 
        PCNFSAID.NUMCAR, 
        PCNFENT.CODFORNEC, 
        codusurdevol
)
---------------------------------------------------------------------------------------------------------------------------
SELECT
    ''|| A.NUMNOTA,
    ''|| W.NUMCARREGAMENTO AS NUMCAR,
    W.CODSUPERVISOR,
    C.CODUSUR1  || ' - ' ||    
    SUBSTR(
        USUR.NOME,
        INSTR(USUR.NOME, ' ') + 1,
        INSTR(USUR.NOME, ' ', INSTR(USUR.NOME, ' ') + 1) - INSTR(USUR.NOME, ' ') - 1
    ) AS RCA,    
    A.CODFORNEC || ' - ' || SUBSTR(A.FORNECEDOR,0,15) AS CLIENTE,
    SUBSTR(E.NOME, 1, INSTR(E.NOME, ' ') - 1) MOTORISTA,
    (CASE WHEN A.CODDEVOL = 106 THEN 0 ELSE
    (CASE WHEN A.VLTOTAL = 0 AND A.VLBONIFIC = 0 THEN A.VLTOTGER 
          WHEN A.VLTOTAL = 0 AND A.VLBONIFIC > 0 THEN A.VLBONIFIC 
          WHEN A.VLTOTAL > 0 THEN A.VLTOTAL ELSE A.VLTOTGER END) END) VLTOTAL,
    (CASE WHEN A.CODDEVOL IN (11, 5, 3, 29, 6, 17, 1, 28, 26, 30, 27, 31, 33, 14, 46, 13, 9, 32, 21, 110, 112) 
               THEN TRUNC((A.VLTOTGER * 0.10),2) ELSE 0 END) ABATIMENTO,
    (CASE WHEN A.VLBONIFIC > 0 THEN 'SIM' ELSE 'NÃO' END) "BNF",    
    A.CODDEVOL || ' - ' || B.MOTIVO MOTIVO, 
    (CASE WHEN A.CODDEVOL IN (7, 4, 41, 45, 34, 15, 25, 12, 18, 105, 36, 43, 103, 16, 104, 8, 20, 19, 10) THEN 'L'
          WHEN A.CODDEVOL IN (11, 5, 3, 29, 6, 17, 1, 28, 26, 30, 27, 31, 33, 14, 46, 13, 9, 32, 21, 110, 112) THEN 'C'
          WHEN A.CODDEVOL IN (38, 39, 22, 42, 35, 109) THEN 'A'
          WHEN A.CODDEVOL IN (23, 44, 24, 2, 106, 111) THEN 'O'
          ELSE 'NULL' END) TIPO,    
    A.OBS
FROM
    PONTUAL.PCNFENT A
JOIN
    PONTUAL.PCTABDEV B ON A.CODDEVOL = B.CODDEVOL
JOIN 
    PONTUAL.PCCLIENT C ON C.CODCLI = A.CODFORNEC
JOIN
    PONTUAL.PCUSUARI USUR ON USUR.CODUSUR = C.CODUSUR1   
JOIN
    PONTUAL.PCEMPR E ON A.codmotoristadevol = E.MATRICULA
JOIN    
    RELWINT W ON A.NUMNOTA = W.NUMNOTA
WHERE
    A.CODDEVOL IS NOT NULL
AND
    A.DTENT BETWEEN TO_DATE('{dtIni}', 'YYYY-MM-DD') AND TO_DATE('{dtFim}', 'YYYY-MM-DD')
AND 
    A.CODFILIAL = 3    
AND
    A.SITUACAONFE NOT IN (101) --101 notas canceladas
AND 
    A.DTCANCEL IS NULL --Sem data de cancelamento
ORDER BY
    MOTIVO, CLIENTE, VLTOTAL DESC