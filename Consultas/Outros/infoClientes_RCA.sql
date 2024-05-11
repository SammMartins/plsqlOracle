SELECT 
    A.CODUSUR1 RCA,
    A.CODCLI CODIGO, 
    A.CLIENTE,
    A.CGCENT,  --REPLACE(REPLACE(REPLACE(A.CGCENT, '.', ''), '-', ''), '/', '') AS CGCENT,
    A.ENDERENT ||', ' || NUMEROENT ENDEREÇO,
    A.BAIRROENT AS BAIRRO,
    B.NOMECIDADE CIDADE,
    A.dtultcomp
FROM 
    PCCLIENT A
JOIN 
    PCCIDADE B ON A.CODCIDADE = B.CODCIDADE
WHERE 
    A.dtultcomp > '31-jan-2024' and A.dtultcomp < '01-may-2024'
AND
    a.CODUSUR1 IN (SELECT CODUSUR FROM pcusuari WHERE CODSUPERVISOR in (2,8))   
and
    a.codcli in (select codcli from pcpedi where codprod in (select codprod from pcprodut where codfornec = 588)) 
ORDER BY 
    CODCLI    
