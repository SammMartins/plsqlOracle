SELECT 
    A.CODUSUR1 RCA,
    A.CODCLI CODIGO, 
    A.CLIENTE,
    A.CGCENT,  --REPLACE(REPLACE(REPLACE(A.CGCENT, '.', ''), '-', ''), '/', '') AS CGCENT,
    A.ENDERENT ||', ' || NUMEROENT ENDEREÇO,
    A.BAIRROENT AS BAIRRO,
    B.NOMECIDADE CIDADE
FROM 
    PCCLIENT A
JOIN 
    PCCIDADE B ON A.CODCIDADE = B.CODCIDADE
WHERE 
    codcli in (select codcli from pcpedi where data > '31-jan-2024' and data < '01-may-2024')
AND
    a.CODUSUR1 IN (SELECT CODUSUR FROM pcusuari WHERE CODSUPERVISOR in (2,8))   
and
    a.codcli in (select codcli from pcpedi where codprod in (select codprod from pcprodut where codfornec = 588)) 
ORDER BY 
    CODCLI    
