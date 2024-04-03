SELECT 
    A.CODUSUR1 RCA,
    A.CODCLI CODIGO, 
    A.CLIENTE, 
    A.ENDERENT ||', ' || NUMEROENT ENDERE�O,
    A.BAIRROENT AS BAIRRO,
    B.NOMECIDADE CIDADE
FROM 
    PCCLIENT A
JOIN 
    PCCIDADE B ON A.CODCIDADE = B.CODCIDADE
WHERE 
    A.CODCLI IN (SELECT DISTINCT(CODCLI) FROM PCMOV WHERE DTMOV > SYSDATE-91 AND DTMOV < SYSDATE AND CODPROD IN (SELECT CODPROD FROM PCPRODUT WHERE CODFORNEC = 588))
ORDER BY 
    CODCLI
