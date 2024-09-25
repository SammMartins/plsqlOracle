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
                              )          
          OR EXISTS (SELECT PCLIB.CODIGOA                     
                     FROM PONTUAL.PCLIB                               
                     WHERE CODTABELA = 1                            
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
              , PCLOGDESBLOQUEIO.CODFILIAL),

preco as (SELECT distinct PCPRODUT.NUMORIGINAL,
            PCPRODUT.INFORMACOESTECNICAS,
            PCPRODUT.PERCIVA,
            PCPRODUT.CLASSIFICFISCAL,
            PCPRODUT.CODPROD,
            PCPRODUT.DESCRICAO,
            PCPRODUT.CODFAB,
            PCPRODUT.MODULO,
            PCPRODUT.RUA,
            PCPRODUT.CODAUXILIAR,
            PCPRODUT.EMBALAGEM,
            PCPRODUT.UNIDADE,
            NVL(PCPRODUT.QTUNIT, 1) QTUNIT,
            PCPRODUT.QTUNITCX,
            PCPRODUT.CODMARCA,
            PCEST.CODFILIAL,
            PCPRODUT.ALTURA,
            PCPRODUT.ALTURATOTAL,
            PCPRODUT.DIAMETROINTERNO,
            PCPRODUT.DIAMETROEXTERNO,
            PCPRODUT.CODEPTO    codigo_depto,
            PCDEPTO.DESCRICAO   descricao_depto,
            PCSECAO.CODSEC      codigo_secao,
            PCSECAO.DESCRICAO   descricao_secao,
    (SELECT M.MARCA FROM PONTUAL.PCMARCA M WHERE M.CODMARCA = PCPRODUT.CODMARCA) MARCA,
            NVL(PCEST.QTESTGER, 0) QTESTGER,
            NVL(PCEST.QTRESERV, 0) QTRESERV,
            PCCONSUM.UTILIZAPERCFINPRECOPROM,
            pcprodut.NUMERO, 
          pcprodut.APTO,
    ( CASE WHEN PCCONSUM.SUGVENDA = 1 THEN 
          PCEST.CUSTOREAL
      ELSE CASE WHEN PCCONSUM.SUGVENDA = 2 THEN
          PCEST.CUSTOFIN
      ELSE PCEST.CUSTOULTENT END END ) PCUSTO,
    ( SELECT PCPRECOPROM.PRECOFIXO 
    FROM PONTUAL.PCPRECOPROM
    WHERE TRUNC(SYSDATE) BETWEEN pcprecoprom.dtiniciovigencia AND pcprecoprom.dtfimvigencia
    AND PCPRECOPROM.CODPROD = pcprodut.codprod
    AND PCPRECOPROM.NUMREGIAO IN (1)
    AND NVL(PCPRECOPROM.CODFILIAL,3) = 3
    AND PCPRECOPROM.CODPLPAGMAX IS NULL AND PCPRECOPROM.CODCLI IS NULL and rownum = 1) PRECOFIXO_SEM_PLPAG,
    ( SELECT PCPRECOPROM.PRECOFIXO
    FROM PONTUAL.PCPRECOPROM
    WHERE TRUNC(SYSDATE) BETWEEN pcprecoprom.dtiniciovigencia AND pcprecoprom.dtfimvigencia
    AND PCPRECOPROM.CODPROD = pcprodut.codprod
    AND PCPRECOPROM.NUMREGIAO IN (1)
    AND NVL(PCPRECOPROM.CODFILIAL,3) = 3
    AND PCPRECOPROM.CODPLPAGMAX = :CODPLPAGMAX AND PCPRECOPROM.CODCLI IS NULL and rownum = 1) PRECOFIXO_COM_PLPAG,
    pcest.custoreal, pcest.custofin, pcest.custoultent,
    nvl(pcest.qtbloqueada,0) qtbloqueada,
    pcprodut.obs2, pcprodut.obs, pctabpr.numregiao,
    CASE 
            WHEN NVL((SELECT PCPRECOPROM.PRECOFIXO 
                        FROM PONTUAL.PCPRECOPROM 
                      WHERE TRUNC(SYSDATE) BETWEEN PCPRECOPROM.DTINICIOVIGENCIA AND 
                            PCPRECOPROM.DTFIMVIGENCIA 
                        AND PCPRECOPROM.CODPROD = PCPRODUT.CODPROD 
                        AND PCPRECOPROM.NUMREGIAO IN (1)
                        AND PCPRECOPROM.CODPLPAGMAX IS NULL 
                        AND PCPRECOPROM.CODCLI IS NULL 
    AND NVL(PCPRECOPROM.CODFILIAL,3) = 3
                        AND ROWNUM = 1), 
                      0) <> 0 THEN 
              (SELECT PCPRECOPROM.PRECOFIXO 
                FROM PONTUAL.PCPRECOPROM 
                WHERE TRUNC(SYSDATE) BETWEEN PCPRECOPROM.DTINICIOVIGENCIA AND 
                      PCPRECOPROM.DTFIMVIGENCIA 
                  AND PCPRECOPROM.CODPROD = PCPRODUT.CODPROD 
                  AND PCPRECOPROM.NUMREGIAO IN (1)
                  AND PCPRECOPROM.CODPLPAGMAX IS NULL 
    AND NVL(PCPRECOPROM.CODFILIAL,3) = 3
                  AND PCPRECOPROM.CODCLI IS NULL 
                  AND ROWNUM = 1) 
            ELSE 
              DECODE(:TipoPreco, 
                    1, 
                    (PCTABPR.PVENDA1 * (1 + (:PERTXFIM / 100))), 
                    2, 
                    (PCTABPR.PVENDA2 * (1 + (:PERTXFIM/ 100))), 
                    3, 
                    (PCTABPR.PVENDA3 * (1 + (:PERTXFIM / 100))), 
                    4, 
                    (PCTABPR.PVENDA4 * (1 + (:PERTXFIM / 100))), 
                    5, 
                    (PCTABPR.PVENDA5 * (1 + (:PERTXFIM / 100))), 
                    6, 
                    (PCTABPR.PVENDA6 * (1 + (:PERTXFIM / 100))), 
                    7, 
                    (PCTABPR.PVENDA7 * (1 + (:PERTXFIM / 100)))) 
          END PVENDA, 
    decode(:TipoPreco, 1, (pctabpr.PVENDA1 * (1 + (:PERTXFIM /100)))
                    , 2, (pctabpr.PVENDA2 * (1 + (:PERTXFIM /100)))
                    , 3, (pctabpr.PVENDA3 * (1 + (:PERTXFIM /100)))
                    , 4, (pctabpr.PVENDA4 * (1 + (:PERTXFIM /100)))
                    , 5, (pctabpr.PVENDA5 * (1 + (:PERTXFIM /100)))
                    , 6, (pctabpr.PVENDA6 * (1 + (:PERTXFIM /100)))
                    , 7, (pctabpr.PVENDA7 * (1 + (:PERTXFIM /100))))  /  decode( NVL(pcprodut.QTUNIT,1),0,1, NVL(pcprodut.QTUNIT,1)) PUNIT,
    NVL(PCTRIBUT.TIPOCALCULOGNRE,'P') TIPOCALCULOGNRE, PCTRIBUT.IVA, PCTRIBUT.ALIQICMS1,
    PCTRIBUT.ALIQICMS2, PCTRIBUT.PAUTA, PCTRIBUT.PERCBASEREDST, pctabpr.DTULTALTPVENDA, 
    PCTABPR.PTABELA,
    PCTABPR.PERDESCMAXBALCAO, 
    PCTABPR.PERDESCMAX 
    FROM PONTUAL.pcprodut, PONTUAL.pcest, PONTUAL.pctabpr, PONTUAL.pctribut, PONTUAL.pcfornec, PONTUAL.pcconsum,  PONTUAL.PCDEPTO, PONTUAL.PCSECAO, PONTUAL.PCFILIAL, PONTUAL.PCEMBALAGEM
    WHERE  pcprodut.codprod = pcest.codprod
    AND    pcprodut.codprod = pctabpr.codprod
    AND    nvl(pctabpr.EXCLUIDO,'N') <> 'S' 
    AND    PCFILIAL.codigo = pcest.codfilial 
    AND    pcembalagem.codprod(+) = pcest.codprod 
    and    pcembalagem.codfilial(+) = pcest.codfilial 
    AND    PCTABPR.CODST = PCTRIBUT.CODST
      AND PCPRODUT.CODEPTO = PCDEPTO.CODEPTO(+)
      AND PCPRODUT.CODSEC = PCSECAO.CODSEC(+)
    AND  pcfornec.codfornec = pcprodut.codfornec
    AND PCPRODUT.DTEXCLUSAO IS NULL
    AND  pcest.codfilial = 3
    AND    pctabpr.numregiao IN (1)
    AND PCPRODUT.DESCRICAO LIKE '%'
    AND    (NVL(PCPRODUT.OBS,'X') <> 'PV')
    AND GREATEST(NVL(PCEST.QTESTGER, 0) - NVL(PCEST.QTRESERV, 0) - NVL(PCEST.QTBLOQUEADA, 0) - DECODE((:BLOQUEIAVENDAESTPENDENTE),'S',(NVL(PCEST.QTPENDENTE, 0)),0),0)  > 0
      AND ((PCPRODUT.CODEPTO IN (SELECT CODIGON
                                  FROM PONTUAL.PCLIB
                                  WHERE PCLIB.CODTABELA = 2
                                    AND CODIGON <> 9999
                                    AND CODFUNC = 203)) OR
            EXISTS (SELECT CODIGON
                      FROM PONTUAL.PCLIB
                    WHERE PCLIB.CODTABELA = 2
                      AND CODIGON = 9999
                      AND CODFUNC = 203))
    AND PCFORNEC.CODFORNEC NOT IN ('1')
    ORDER BY pcprodut.codprod)              
              
                                   
                                                                
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
     , NVL((SELECT AVG(P.PVENDA) 
              FROM PONTUAL.PCPEDI P 
              WHERE P.CODPROD = PCEST.CODPROD 
                AND P.DATA BETWEEN TRUNC(SYSDATE, 'YEAR') AND SYSDATE), 0) * 
                PONTUAL.PKG_ESTOQUE.ESTOQUE_DISPONIVEL(TRUNC(PCEST.CODPROD, 2), TRUNC(PCEST.CODFILIAL, 2), 'V') AS "VALOR EST."
   , (NVL(PCEST.QTBLOQUEADA, 0) - NVL(PCEST.QTINDENIZ, 0)) QTBLOQMENOSAVARIA                                                         
   , TRUNC((NVL(PCEST.QTESTGER, 0) / DECODE(NVL(PCPRODUT.QTUNITCX, 1), 0, 1, NVL(PCPRODUT.QTUNITCX, 1))),0) || 'CX.' QTESTMASTER                       
     
FROM PONTUAL.PCEST                                                    
     , PONTUAL.PCPRODUT
     , PONTUAL.PCPRODFILIAL                                             
     , PONTUAL.PARAMETROS                                               
     , PONTUAL.LOGDESBLOQUEIO
     , preco                                      
WHERE PARAMETROS.CODFILIAL = PCEST.CODFILIAL                    
  AND PCPRODUT.CODPROD     = PCEST.CODPROD                      
  AND PCEST.CODFILIAL      = PCPRODFILIAL.CODFILIAL             
  AND PCEST.CODPROD        = PCPRODFILIAL.CODPROD               
  AND PCEST.CODFILIAL      = LOGDESBLOQUEIO.CODFILIAL(+)        
  AND PCEST.CODPROD        = LOGDESBLOQUEIO.CODPROD(+)        
  AND PCEST.CODPROD        = preco.codprod(+)
AND PCEST.CODFILIAL IN('3')                                                        
   AND (((PCPRODUT.OBS2 NOT IN ('FL')) OR (PCPRODUT.OBS2 IS NULL))                                                             
   AND ((PCPRODFILIAL.FORALINHA NOT IN ('S')) OR (PCPRODFILIAL.FORALINHA IS NULL)))                                            
  AND PCPRODUT.CODPROD NOT IN (14568)
  AND PCPRODUT.DESCRICAO NOT LIKE '%FREEZER%'
  AND PCPRODUT.DESCRICAO NOT LIKE '%PALLET%'
  AND PCPRODUT.DESCRICAO NOT LIKE '%PALET%'
  AND PCEST.DTULTENT IS NOT NULL

