SELECT 
    A.CODUSUR1 RCA,
    A.CODCLI CODIGO, 
    A.CLIENTE,
    a.dtultcomp,
    A.CGCENT, --REPLACE(REPLACE(REPLACE(A.CGCENT, '.', ''), '-', ''), '/', '') AS CGCENT,
    A.CEPENT CEP,
    A.ENDERENT ||', ' || NUMEROENT ENDERE�O,
    A.BAIRROENT AS BAIRRO,
    B.NOMECIDADE CIDADE
FROM 
    pontual.PCCLIENT A
JOIN 
    PONTUAL.PCCIDADE B ON A.CODCIDADE = B.CODCIDADE
WHERE
    A.CODCLI IN (SELECT CODCLI FROM PONTUAL.PCPEDI WHERE CODPROD IN (SELECT CODPROD FROM PONTUAL.PCPRODUT WHERE CODFORNEC IN (1841) AND DATA BETWEEN '01-MAI-2024' AND '31-JUL-2024' ))
ORDER BY 
    CODCLI    
