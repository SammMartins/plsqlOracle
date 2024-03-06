SELECT 
    A.CODUSUR1 RCA,
    A.CODCLI CODIGO, 
    A.CLIENTE, 
    A.ENDERENT ENDERE�O,
    A.BAIRROENT AS BAIRRO,
    B.NOMECIDADE CIDADE
FROM 
    PCCLIENT A
JOIN 
    PCCIDADE B ON A.CODCIDADE = B.CODCIDADE
WHERE 
    A.CODCLI IN (SELECT CODCLI FROM PCMOV WHERE DTMOV > '01-DEZ-2023' AND DTMOV < '29-FEV-2024')
ORDER BY 
    CODCLI
