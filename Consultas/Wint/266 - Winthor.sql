WITH PARAMETROS                                                                                                                        
  AS (SELECT PCFILIAL.CODIGO CODFILIAL                                                                                                 
           , COALESCE(PCPARAMFILIAL.VALOR, PCCONSUM.BLOQUEIAVENDAESTPENDENTE) BLOQUEIAVENDAESTPENDENTE                                 
           , NVL(PCPARAMETROWMS.VALOR,'N') DESBLOQUEARPRODFIMOS                                                                      
           , NVL(PCFILIAL.USAWMS, 'N') USAWMS                                                                                        
           , NVL (PCFILIAL.AUTOSERVICO, 'S') AUTOSERVICO                                                                             
        FROM PCFILIAL                                                                                                                  
           , PCCONSUM                                                                                                                  
           , PCPARAMFILIAL                                                                                                             
           , PCPARAMETROWMS                                                                                                            
       WHERE PCFILIAL.CODIGO <> '99'                                                                                                 
         AND PCFILIAL.DTEXCLUSAO IS NULL                                                                                               
         AND PCFILIAL.CODIGO        = PCPARAMETROWMS.CODFILIAL(+)                                                                      
         AND PCPARAMETROWMS.NOME(+) = 'DESBLOQUEARPRODFIMOS'                                                                         
         AND PCFILIAL.CODIGO        = PCPARAMFILIAL.CODFILIAL(+)                                                                       
         AND PCPARAMFILIAL.NOME(+)  = 'BLOQUEIAVENDAESTPENDENTE'                                                                     
AND PCFILIAL.CODIGO IN('3')                                                 
  AND (PCFILIAL.CODIGO IN (SELECT PCLIB.CODIGOA                                                                                      
                           FROM PCLIB                                                                                                
                           WHERE CODTABELA = 1                                                                                       
                             AND CODFUNC = :CODFUNC)                                                                                 
          OR EXISTS (SELECT PCLIB.CODIGOA                                                                                            
                     FROM PCLIB                                                                                                      
                     WHERE CODTABELA = 1                                                                                             
                       AND CODFUNC = :CODFUNC                                                                                        
                       AND PCLIB.CODIGOA = '99'))                                                                                  
       )                                                                                                                               
   , LOGDESBLOQUEIO                                                                                                                    
     AS (SELECT PCLOGDESBLOQUEIO.CODPROD                                                                                               
              , PCLOGDESBLOQUEIO.CODFILIAL                                                                                             
              , MAX(PCLOGDESBLOQUEIO.CODFUNCDESBLOQUEIO) AS CODFUNCDESBLOQUEIO                                                         
              , MAX(PCLOGDESBLOQUEIO.OBS) OBS                                                                                          
           FROM PCLOGDESBLOQUEIO                                                                                                       
              , PARAMETROS                                                                                                             
          WHERE PCLOGDESBLOQUEIO.CODFILIAL = PARAMETROS.CODFILIAL                                                                      
            AND PCLOGDESBLOQUEIO.DTDESBLOQUEIO = (SELECT MAX(LOG.DTDESBLOQUEIO)                                                        
                                                    FROM PCLOGDESBLOQUEIO LOG                                                          
                                                   WHERE LOG.CODFILIAL = PARAMETROS.CODFILIAL                                          
                                                     AND LOG.CODPROD   = PCLOGDESBLOQUEIO.CODPROD                                      
                                                     AND LOG.CODFILIAL = PCLOGDESBLOQUEIO.CODFILIAL                                    
                                                     AND LOG.DTDESBLOQUEIO >= (SYSDATE - 150)                                          
                                                  )                                                                                    
          GROUP                                                                                                                        
             BY PCLOGDESBLOQUEIO.CODPROD                                                                                               
              , PCLOGDESBLOQUEIO.CODFILIAL)                                                                                            
                                                                                                                                       
SELECT PCEST.CODPROD                                                                                                                   
     , PCEST.CODFILIAL                                                                                                                 
     , PCPRODUT.DESCRICAO                                                                                                              
     , 0 CODDEPOSITO                                                                                                                 
     , '' DEPOSITO                                                                                                                 
     , PCPRODUT.USAWMS                                                                                                                 
     , PCPRODUT.ESTOQUEPORLOTE                                                                                                         
     , PCPRODUT.EMBALAGEM                                                                                                              
     , PCPRODUT.UNIDADE                                                                                                                
     , PCPRODUT.CODFAB                                                                                                                 
     , PCPRODUT.RUA                                                                                                                    
     , PCPRODUT.MODULO                                                                                                                 
     , PCPRODUT.CODAUXILIAR                                                                                                            
     , NVL(PCPRODFILIAL.NUMEROSSERIECONTROLADOS, 0) NUMEROSSERIECONTROLADOS                                                            
     , CASE WHEN ((PCPRODUT.OBS2 = 'FL') AND (PCPRODFILIAL.FORALINHA = 'S'))                                                       
            THEN 'S' ELSE 'N' END OBS2                                                                                             
     , PCPRODUT.CLASSE                                                                                                                 
   , NVL(PCEST.QTESTGER, 0) QTESTGER                                                                                                 
   , NVL(PCEST.QTRESERV, 0) QTRESERV                                                                                                 
     , PCEST.CODDEVOL                                                                                                                  
     , PCPRODUT.TIPOESTOQUE                                                                                                            
   , PKG_ESTOQUE.ESTOQUE_DISPONIVEL(PCEST.CODPROD,                                                                                   
                                    PCEST.CODFILIAL,                                                                                 
                                               'V') QTDISP                                                                    
   , (NVL(PCEST.QTBLOQUEADA, 0) - NVL(PCEST.QTINDENIZ, 0)) QTBLOQMENOSAVARIA                                                         
   , (NVL(PCEST.QTESTGER, 0) / DECODE(NVL(PCPRODUT.QTUNITCX, 1), 0, 1, NVL(PCPRODUT.QTUNITCX, 1))) QTESTMASTER                       
   , NVL(PCEST.QTBLOQUEADA, 0) QTBLOQUEADA 
   , NVL(PCEST.QTINDENIZ, 0) QTINDENIZ                                                                                               
   ,(CASE WHEN PARAMETROS.BLOQUEIAVENDAESTPENDENTE = 'S' THEN                                                                   
             NVL(PCEST.QTPENDENTE, 0)                                                                                                
          ELSE                                                                                                                     
             0                                                                                                                       
          END) QTPENDENTE                                                                                                            
     , NVL (PCPRODUT.QTUNITCX, 0) QTUNITCX                                                                                             
     , NVL(PCEST.QTINDUSTRIA, 0) QTINDUSTRIA                                                                                           
     , PARAMETROS.USAWMS FILIALUSAWMS                                                                                                  
     , PCEST.QTVENDMES                                                                                                                 
     , PCEST.QTVENDMES1                                                                                                                
     , PCEST.QTVENDMES2                                                                                                                
     , PCEST.QTVENDMES3                                                                                                                
     , NVL((SELECT PCTABDEV.MOTIVO FROM PCTABDEV WHERE PCTABDEV.CODDEVOL = PCEST.CODDEVOL), PCEST.MOTIVOBLOQESTOQUE) MOTIVOBLOQESTOQUE 
     , LOGDESBLOQUEIO.CODFUNCDESBLOQUEIO                                                                                               
     , PCEST.DTULTENT                                                                                                                  
     , PARAMETROS.AUTOSERVICO                                                                                                          
     , CASE WHEN (PARAMETROS.USAWMS = 'S') AND (PCPRODUT.USAWMS = 'S')                                                             
            THEN PARAMETROS.DESBLOQUEARPRODFIMOS                                                                                       
            ELSE ''                                                                                                                  
       END PARAMETROWMS --'DESBLOQUEARPRODFIMOS'                                                                                     
      , (CASE WHEN (PARAMETROS.USAWMS = 'S') AND (PCPRODUT.USAWMS = 'S')                                                           
              THEN DECODE(WMS_EXISTEPENDENCIAENTRADA(PCEST.CODPROD, PCEST.CODFILIAL), NULL, 0, 1)                                      
              ELSE 0                                                                                                                   
           END) MOVIMENTACAOWMS                                                                                                        
     , 0 AS QTENT                                                                                                                  
     , 0 AS QTAVARIABONUS                                                                                                          
     , 0 NUMTRANSENT                                                                                                               
     ,'' NUMLOTE                                                                                                                     
         , PCPRODUT.TIPOMERC                                                                                                           
  FROM PCEST                                                                                                                           
     , PCPRODUT                                                                                                                        
     , PCPRODFILIAL                                                                                                                    
     , PARAMETROS                                                                                                                      
     , LOGDESBLOQUEIO                                                                                                                  
WHERE PARAMETROS.CODFILIAL = PCEST.CODFILIAL                                                                                           
  AND PCPRODUT.CODPROD     = PCEST.CODPROD                                                                                             
  AND PCEST.CODFILIAL      = PCPRODFILIAL.CODFILIAL                                                                                    
  AND PCEST.CODPROD        = PCPRODFILIAL.CODPROD                                                                                      
  AND PCEST.CODFILIAL      = LOGDESBLOQUEIO.CODFILIAL(+)                                                                               
  AND PCEST.CODPROD        = LOGDESBLOQUEIO.CODPROD(+)                                                                                 
AND PCEST.CODFILIAL IN('3')                                                        
AND PCPRODUT.CODFORNEC =:CODFORNEC
