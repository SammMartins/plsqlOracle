WITH PARAMETROS                                                                                                                        
  AS (SELECT PCFILIAL.CODIGO CODFILIAL                                                                                                 
           , COALESCE(PCPARAMFILIAL.VALOR, PCCONSUM.BLOQUEIAVENDAESTPENDENTE) BLOQUEIAVENDAESTPENDENTE                                 
           , NVL(PCPARAMETROWMS.VALOR,'N') DESBLOQUEARPRODFIMOS                                                                      
           , NVL(PCFILIAL.USAWMS, 'N') USAWMS                                                                                        
           , NVL (PCFILIAL.AUTOSERVICO, 'S') AUTOSERVICO                                                                             
        FROM PONTUAL.PCFILIAL                                                                                                                  
           , PONTUAL.PCCONSUM
           , PONTUAL.PCPARAMFILIAL                                                                                                             
           , PONTUAL.PCPARAMETROWMS                                                                                                            
       WHERE PCFILIAL.CODIGO <> '99'                                                                                                 
         AND PCFILIAL.DTEXCLUSAO IS NULL                                                                                               
         AND PCFILIAL.CODIGO        = PCPARAMETROWMS.CODFILIAL(+)                                                                      
         AND PCPARAMETROWMS.NOME(+) = 'DESBLOQUEARPRODFIMOS'                                                                         
         AND PCFILIAL.CODIGO        = PCPARAMFILIAL.CODFILIAL(+)                                                                       
         AND PCPARAMFILIAL.NOME(+)  = 'BLOQUEIAVENDAESTPENDENTE'                                                                     
AND PCFILIAL.CODIGO IN('3')                                                 
  AND (PCFILIAL.CODIGO IN (SELECT PCLIB.CODIGOA                                                                                      
                           FROM PONTUAL.PCLIB                                                                                                
                           WHERE CODTABELA = 1                                                                                       
                             AND CODFUNC = 203)                                                                                 
          OR EXISTS (SELECT PCLIB.CODIGOA                                                                                            
                     FROM PONTUAL.PCLIB                                                                                                      
                     WHERE CODTABELA = 1                                                                                             
                       AND CODFUNC = 203                                                                                     
                       AND PCLIB.CODIGOA = '99'))                                                                                  
       )                                                                                                                               
   , LOGDESBLOQUEIO                                                                                                                    
     AS (SELECT PCLOGDESBLOQUEIO.CODPROD                                                                                               
              , PCLOGDESBLOQUEIO.CODFILIAL                                                                                             
              , MAX(PCLOGDESBLOQUEIO.CODFUNCDESBLOQUEIO) AS CODFUNCDESBLOQUEIO                                                         
              , MAX(PCLOGDESBLOQUEIO.OBS) OBS                                                                                          
           FROM PONTUAL.PCLOGDESBLOQUEIO                                                                                                       
              , PONTUAL.PARAMETROS                                                                                                             
          WHERE PCLOGDESBLOQUEIO.CODFILIAL = PARAMETROS.CODFILIAL                                                                      
            AND PCLOGDESBLOQUEIO.DTDESBLOQUEIO = (SELECT MAX(LOG.DTDESBLOQUEIO)                                                        
                                                    FROM PONTUAL.PCLOGDESBLOQUEIO LOG                                                          
                                                   WHERE LOG.CODFILIAL = PARAMETROS.CODFILIAL                                          
                                                     AND LOG.CODPROD   = PCLOGDESBLOQUEIO.CODPROD                                      
                                                     AND LOG.CODFILIAL = PCLOGDESBLOQUEIO.CODFILIAL                                    
                                                     AND LOG.DTDESBLOQUEIO >= (SYSDATE - 150)                                          
                                                  )                                                                                    
          GROUP                                                                                                                        
             BY PCLOGDESBLOQUEIO.CODPROD                                                                                               
              , PCLOGDESBLOQUEIO.CODFILIAL)                                                                                            
                                                                                                                                       
SELECT PCEST.CODPROD || ''
     , PCEST.DTULTENT
     , PCPRODUT.DESCRICAO
     , SUBSTR(PCPRODUT.CODFORNEC,0,20) Fornecedor
     , (SELECT F.FORNECEDOR FROM PONTUAL.PCFORNEC F WHERE F.CODFORNEC = PCPRODUT.CODFORNEC) AS FORNECEDOR                                                                                                      
     , PCPRODUT.EMBALAGEM 
     , PCEST.qtultent
     , NVL (PCPRODUT.QTUNITCX, 0) QTUNITCX
     , NVL(PCEST.QTESTGER, 0) + NVL(PCEST.QTRESERV, 0) qtdest                                                                                                                                                                                                 
     , PONTUAL.PKG_ESTOQUE.ESTOQUE_DISPONIVEL(TRUNC(PCEST.CODPROD,2), TRUNC(PCEST.CODFILIAL,2), 'V') || '' QTDISP
   , (NVL(PCEST.QTBLOQUEADA, 0) - NVL(PCEST.QTINDENIZ, 0)) QTBLOQMENOSAVARIA                                                         
   , TRUNC((NVL(PCEST.QTESTGER, 0) / DECODE(NVL(PCPRODUT.QTUNITCX, 1), 0, 1, NVL(PCPRODUT.QTUNITCX, 1))),0) || 'CX.' QTESTMASTER                       
   --, NVL(PCEST.QTBLOQUEADA, 0) QTBLOQUEADA                                                                                                                                                                                                                                                                                                                                                                                      
     --, PCEST.QTVENDMES || ''
     --, PCEST.QTVENDMES1 || ''
     --, PCEST.QTVENDMES2 || ''
     --, PCEST.QTVENDMES3 || ''
     
FROM PONTUAL.PCEST                                                                                                                           
     , PONTUAL.PCPRODUT
     , PONTUAL.PCPRODFILIAL                                                                                                                    
     , PONTUAL.PARAMETROS                                                                                                                      
     , PONTUAL.LOGDESBLOQUEIO                                                                                                                  
WHERE PARAMETROS.CODFILIAL = PCEST.CODFILIAL                                                                                           
  AND PCPRODUT.CODPROD     = PCEST.CODPROD                                                                                             
  AND PCEST.CODFILIAL      = PCPRODFILIAL.CODFILIAL                                                                                    
  AND PCEST.CODPROD        = PCPRODFILIAL.CODPROD                                                                                      
  AND PCEST.CODFILIAL      = LOGDESBLOQUEIO.CODFILIAL(+)                                                                               
  AND PCEST.CODPROD        = LOGDESBLOQUEIO.CODPROD(+)                                                                                 
AND PCEST.CODFILIAL IN('3')                                                        
   AND (((PCPRODUT.OBS2 NOT IN ('FL')) OR (PCPRODUT.OBS2 IS NULL))                                                             
   AND ((PCPRODFILIAL.FORALINHA NOT IN ('S')) OR (PCPRODFILIAL.FORALINHA IS NULL)))                                            
  AND PCPRODUT.CODPROD NOT IN (14568)

