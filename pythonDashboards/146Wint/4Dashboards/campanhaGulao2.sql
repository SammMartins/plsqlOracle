WITH BASE_ATIVA AS (
    SELECT  
        COUNT(DISTINCT(USUARI.CODCLI)) QTCLIATIVOS,
        USUARI.codusur
    FROM (
        SELECT 
            PCCLIENT.CODCLI,
            PCCLIENT.CODusur1 codusur 
        FROM 
            PCCLIENT, 
            PCUSUARI, 
            PCSUPERV, 
            PCPRACA                                                         
        WHERE 
            PCCLIENT.CODUSUR1 = PCUSUARI.CODUSUR 
            AND PCUSUARI.CODSUPERVISOR = PCSUPERV.CODSUPERVISOR(+)          
            AND PCCLIENT.CODPRACA = PCPRACA.CODPRACA          
            AND PCCLIENT.DTULTCOMP >= sysdate - 90            
            AND (PCUSUARI.CODFILIAL IN ('3') OR NVL(PCUSUARI.CODFILIAL, '99') = '99')
            AND PCUSUARI.CODSUPERVISOR IN (2, 8)
            AND (PCUSUARI.CODFILIAL IN ('3') OR NVL(PCUSUARI.CODFILIAL, '99') = '99')
        
        UNION                                                                      
                                                                                   
        SELECT                                                                  
            PCCLIENT.CODCLI,
            PCCLIENT.CODusur1 codusur                                                
        FROM                                                                    
            PCCLIENT,                                                             
            PCUSUARI, 
            PCSUPERV, 
            PCPRACA                                                         
        WHERE                                                                   
            PCCLIENT.CODUSUR2 = PCUSUARI.CODUSUR                             
            AND PCUSUARI.CODSUPERVISOR = PCSUPERV.CODSUPERVISOR(+)                 
            AND PCCLIENT.CODPRACA = PCPRACA.CODPRACA          
            AND PCCLIENT.DTULTCOMP >= sysdate - 90             
            AND (PCUSUARI.CODFILIAL IN ('3') OR NVL(PCUSUARI.CODFILIAL, '99') = '99')
            AND PCUSUARI.CODSUPERVISOR IN (2, 8)
            AND (PCUSUARI.CODFILIAL IN ('3') OR NVL(PCUSUARI.CODFILIAL, '99') = '99')
                    
        UNION                                                                      
                                                                                   
        SELECT                                                                
            PCCLIENT.CODCLI,
            PCCLIENT.CODusur1 codusur                                        
        FROM                                                                  
            PCUSURCLI,                                                         
            PCCLIENT,                                                          
            PCUSUARI, 
            PCSUPERV, 
            PCPRACA                                                         
        WHERE     
            PCUSURCLI.CODUSUR = PCUSUARI.CODUSUR                        
            AND PCUSUARI.CODSUPERVISOR = PCSUPERV.CODSUPERVISOR(+)           
            AND PCCLIENT.CODPRACA = PCPRACA.CODPRACA                         
            AND PCUSURCLI.CODCLI = PCCLIENT.CODCLI                        
            AND PCCLIENT.DTULTCOMP >= sysdate - 90       
            AND (PCUSUARI.CODFILIAL IN ('3') OR NVL(PCUSUARI.CODFILIAL, '99') = '99')
            AND PCUSUARI.CODSUPERVISOR IN (2, 8)
            AND (PCUSUARI.CODFILIAL IN ('3') OR NVL(PCUSUARI.CODFILIAL, '99') = '99')
       
    ) USUARI

    GROUP BY
        USUARI.CODUSUR        
),

( 
SELECT 
    A.CODCLI,
    A.CODUSUR
FROM
    PCPEDI A
WHERE
    A.CODPROD IN (SELECT CODPROD FROM PONTUAL.PCPRODUT WHERE CODFORNEC = 1719)
    AND A.DATA BETWEEN '01-AGO-2024' AND '31-AGO-2024'
    AND A.VLBONIFIC = 0
    AND (A.CODPROD IN (18645, 18944)
    OR (A.CODPROD = 18639 OR A.CODPROD = 18637))
GROUP BY
    A.CODCLI, 
    A.CODUSUR
HAVING
    COUNT(DISTINCT A.CODPROD) = 3
    AND COUNT(DISTINCT CASE WHEN A.CODPROD IN (18645, 18944) THEN A.CODPROD END) = 2
    AND COUNT(DISTINCT CASE WHEN A.CODPROD IN (18639, 18637) THEN A.CODPROD END) = 1
)