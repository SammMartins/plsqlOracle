 SELECT NVL(VENDAS.CODUSUR, DEVOLUCAO.CODUSURDEVOL) CODUSUR, 
        NVL(VENDAS.NOME, DEVOLUCAO.NOME) NOME,
        (CASE WHEN VENDAS.CODUSUR = 160 THEN 0
              WHEN VENDAS.CODUSUR = 2 THEN 0 ELSE
        SUM(NVL(VENDAS.VLVENDA,0) - NVL(DEVOLUCAO.VLDEVOLUCAO,0)) END) VLVENDA,
        (CASE WHEN VENDAS.CODUSUR = 160 THEN 2000+((2000/6)*5)
              WHEN VENDAS.CODUSUR = 2 THEN 2000+((2000/6)) ELSE
        (SUM(NVL(VENDAS.VLVENDA,0) - NVL(DEVOLUCAO.VLDEVOLUCAO,0))) * 0.0175 END) AS VERBA,
        (CASE WHEN VENDAS.CODUSUR = 160 THEN 0 
              WHEN VENDAS.CODUSUR = 2 THEN 0
         ELSE 0 END) AS ABATIMENTOS, 0 AS TOTAL
      
FROM  (SELECT CODUSUR,
              NOME,
              SUM(NVL(QTVENDA,0)) QTVENDA,
              SUM(NVL(VLVENDA,0) + NVL(VALORST,0) + NVL(VALORIPI,0)) VLVENDA,
              SUM(NVL(VLVENDA_SEMST,0)) VLVENDA_SEMST,
              SUM(NVL(TOTPESO,0)) TOTPESO,
              SUM(NVL(VLCUSTOFIN,0) - 0) VLCUSTOFIN, 
              SUM(NVL(VLBONIFIC,0)) VLBONIFIC,
              COUNT(DISTINCT(QTCLIPOS)) QTCLIPOS,
              COUNT(DISTINCT(QTMIX)) QTMIX,
              SUM(NVL(VOLUME,0)) VOLUME,
              SUM(NVL(VLREPASSE,0)) VLREPASSE,
              SUM(NVL(LITRAGEM,0)) LITRAGEM, SUM(NVL(VLREPASSEBNF,0)) VLREPASSEBNF FROM (  SELECT PCMOV.CODCLI, 
         PCATIVI.RAMO, 
         PCATIVI.CODATIV, 
       PCNFSAID.NUMTRANSVENDA, 
 PCNFSAID.CODUSUR  CODUSUR, 
 NVL(PCNFSAID.CODSUPERVISOR,PCSUPERV.CODSUPERVISOR)  CODSUPERVISOR, 
       PCMOV.CODPROD, 
       PCNFSAID.CODFILIAL, 
      PCPRODUT.CODAUXILIAR, 
       PCCLIENT.CLIENTE,
       PCFORNEC.CODFORNECPRINC,
     PCFORNEC.FORNECEDOR,
       PCFORNEC.CODFORNEC,
       PCUSUARI.NOME, 
       PCSUPERV.NOME SUPERV, 
       PCPRODUT.CODEPTO, 
       PCPRODUT.CODSEC, 
       PCDEPTO.DESCRICAO DEPARTAMENTO, 
       PCSECAO.DESCRICAO SECAO, 
       PCNFSAID.CODPRACA, 
       PCPRACA.PRACA, 
       PCPRODUT.CODMARCA, 
       PCPRODUT.QTUNIT, 
       PCMARCA.MARCA, 
       PCCLIENT.ESTENT, 
       PCCLIENT.MUNICENT,
       PCCLIENT.CODCIDADE,
       PCCIDADE.NOMECIDADE,
       NVL(PCCLIENT.CODCLIPRINC, PCCLIENT.CODCLI) CODCLIPRINC, 
       (SELECT X.CLIENTE 
          FROM PCCLIENT X 
         WHERE X.CODCLI = NVL(PCCLIENT.CODCLIPRINC, PCCLIENT.CODCLI)) CLIENTEPRINC, 
       ROUND( (NVL(PCPRODUT.VOLUME, 0) * NVL(PCMOV.QT, 0)),2)  VOLUME, 
      (NVL(PCPRODUT.LITRAGEM, 0) * NVL(PCMOV.QT, 0))  LITRAGEM, 
       PCPRODUT.DESCRICAO,
       PCPRODUT.EMBALAGEM,
       PCPRODUT.UNIDADE,
       PCPRODUT.CODFAB,
       PCNFSAID.CODPLPAG,
       PCNFSAID.NUMPED,
       PCNFSAID.CODCOB,
       PCCLIENT.CODPLPAG CODPLANOCLI,
       PCPLPAG.DESCRICAO DESCRICAOPCPLPAG,
       PCPLPAG.NUMDIAS, 
       0 QTMETA,
       0 QTPESOMETA,
       0 MIXPREV,
       0 CLIPOSPREV,
       ROUND((DECODE(PCMOV.CODOPER,  
                     'SB',         
                     PCMOV.QTCONT,   
                     0)) *           
       NVL(PCMOV.VLREPASSE, 0),      
       2) VLREPASSEBNF,              
         ROUND((NVL(PCMOV.QT, 0) * 
         DECODE(PCNFSAID.CONDVENDA,
                 5,
                 0,
                 6,
                 0,
                 11,
                 0,
                 12,
                 0,
                 DECODE(PCMOV.CODOPER,'SB',0,nvl(pcmov.VLIPI,0)))),2) VALORIPI,
                 0 VALORIPIX,
         ROUND(NVL(PCMOV.QT, 0) * 
         DECODE(PCNFSAID.CONDVENDA,
                 5,
                 0,
                 6,
                 0,
                 11,
                 0,
                 12,
                 0,
                 DECODE(PCMOV.CODOPER,'SB',0,(nvl(pcmov.ST,0)+NVL(PCMOVCOMPLE.VLSTTRANSFCD,0)))),2) VALORST,
                 0 VALORSTX,
         (SELECT PCCLIENT.CODPLPAG || ' - ' || PCPLPAG.DESCRICAO  FROM PCPLPAG WHERE PCCLIENT.CODPLPAG = PCPLPAG.CODPLPAG) DESCRICAOPLANOCLI,
       ((DECODE(PCMOV.CODOPER,  
                           'S', 
                           (NVL(DECODE(PCNFSAID.CONDVENDA, 
                                       7, 
                                       PCMOV.QTCONT, 
                                       PCMOV.QT), 
                                0)), 
                           'SM', 
                           (NVL(DECODE(PCNFSAID.CONDVENDA, 
                                       7, 
                                       PCMOV.QTCONT, 
                                       PCMOV.QT), 
                                0)), 
                           'ST', 
                           (NVL(DECODE(PCNFSAID.CONDVENDA, 
                                       7, 
                                       PCMOV.QTCONT, 
                                       PCMOV.QT), 
                                0)), 
                           'SB', 
                           (NVL(DECODE(PCNFSAID.CONDVENDA, 
                                       7, 
                                       PCMOV.QTCONT, 
                                       PCMOV.QT), 
                                0)), 
                           0))) QTVENDA, 
                  ((DECODE(PCMOV.CODOPER                                
                          ,'S'                                        
                          ,(NVL(DECODE(PCNFSAID.CONDVENDA,              
                                       7,                               
                                       PCMOV.QTCONT,                    
                                       PCMOV.QT),                       
                                0))                                     
                          ,'ST'                                       
                          ,(NVL(DECODE(PCNFSAID.CONDVENDA,              
                                       7,                               
                                       PCMOV.QTCONT,                    
                                       PCMOV.QT),                       
                                0))                                     
                          ,'SM'                                       
                          ,(NVL(DECODE(PCNFSAID.CONDVENDA,              
                                       7,                               
                                       PCMOV.QTCONT,                    
                                       PCMOV.QT),                       
                                0))                                     
                          ,'SB'                                       
                          ,(NVL(DECODE(PCNFSAID.CONDVENDA,              
                                       7,                               
                                       PCMOV.QTCONT,                    
                                       PCMOV.QT),                       
                                0))                                     
                          ,0)) * (NVL(PCMOV.CUSTOFIN, 0)   
                          )) VLCUSTOFIN,  
 CASE WHEN NVL(PCMOVCOMPLE.VLSUBTOTITEM,0) <> 0 THEN  
  DECODE(NVL(PCMOV.TIPOITEM,'N'),'I',0,NVL(PCMOVCOMPLE.VLSUBTOTITEM,0) + (DECODE(NVL(PCMOV.TIPOITEM,'N'),'I', NVL(PCMOV.QTCONT, 0), 0) * NVL(PCMOV.VLFRETE, 0))) - 
       (  ROUND((NVL(PCMOV.QT, 0) * 
         DECODE(PCNFSAID.CONDVENDA,
                 5,
                 0,
                 6,
                 0,
                 11,
                 0,
                 12,
                 0,
                 DECODE(PCMOV.CODOPER,'SB',0,nvl(pcmov.VLIPI,0)))),2)) -  
       (  ROUND(NVL(PCMOV.QT, 0) * 
         DECODE(PCNFSAID.CONDVENDA,
                 5,
                 0,
                 6,
                 0,
                 11,
                 0,
                 12,
                 0,
                 DECODE(PCMOV.CODOPER,'SB',0,nvl(pcmov.ST,0))),2)) 
 ELSE                                                
       ROUND((((DECODE(PCMOV.CODOPER,                                           
                       'S',                                                   
                       (NVL(DECODE(PCNFSAID.CONDVENDA,                          
                                   7,                                           
                                   PCMOV.QTCONT,                                
                                   PCMOV.QT),                                   
                            0)),                                                
                       'ST',                                                  
                       (NVL(DECODE(PCNFSAID.CONDVENDA,                          
                                   7,                                           
                                   PCMOV.QTCONT,                                
                                   PCMOV.QT),                                   
                            0)),                                                
                       'SM',                                                  
                       (NVL(DECODE(PCNFSAID.CONDVENDA,                          
                                   7,                                           
                                   PCMOV.QTCONT,                                
                                   PCMOV.QT),                                   
                            0)),                                                
                       0)) *                                                    
             (NVL(DECODE(PCNFSAID.CONDVENDA,                                    
                           7,                                                   
                           (NVL(PUNITCONT, 0) - NVL(PCMOV.VLIPI, 0) -           
                           (nvl(pcmov.ST,0)+NVL(PCMOVCOMPLE.VLSTTRANSFCD,0))) + NVL(PCMOV.VLFRETE, 0) +          
                           NVL(PCMOV.VLOUTRASDESP, 0) +                         
                           NVL(PCMOV.VLFRETE_RATEIO, 0) +                       
                           DECODE(PCMOV.TIPOITEM,                               
                                  'C',                                        
                                  (SELECT NVL((SUM(M.QTCONT *                   
                                                   NVL(M.VLOUTROS, 0)) /        
                                          PCMOV.QT), 0) VLOUTROS                
                                     FROM PCMOV M                               
                                    WHERE M.NUMTRANSVENDA =                     
                                          PCMOV.NUMTRANSVENDA                   
                                      AND M.TIPOITEM = 'I'                    
                                      AND CODPRODPRINC = PCMOV.CODPROD),        
 'I', NVL(PCMOV.VLOUTROS, 0),DECODE(NVL(PCNFSAID.SOMAREPASSEOUTRASDESPNF,'N'),'N',NVL((PCMOV.VLOUTROS), 0),'S',NVL((NVL(PCMOV.VLOUTROS,0)-NVL(PCMOV.VLREPASSE,0)), 0)))
                           ,(NVL(PCMOV.PUNIT, 0) - NVL(PCMOV.VLIPI, 0) -         
                           (nvl(pcmov.ST,0)+NVL(PCMOVCOMPLE.VLSTTRANSFCD,0))) + NVL(PCMOV.VLFRETE, 0) +          
                           NVL(PCMOV.VLOUTRASDESP, 0) +                         
                           NVL(PCMOV.VLFRETE_RATEIO, 0) +                       
                           DECODE(PCMOV.TIPOITEM,                               
                                  'C',                                        
                                  (SELECT NVL((SUM(M.QTCONT *                   
                                                   NVL(M.VLOUTROS, 0)) /        
                                          PCMOV.QT), 0) VLOUTROS                
                                     FROM PCMOV M                               
                                    WHERE M.NUMTRANSVENDA =                     
                                          PCMOV.NUMTRANSVENDA                   
                                      AND M.TIPOITEM = 'I'                    
                                      AND CODPRODPRINC = PCMOV.CODPROD),        
 'I', NVL(PCMOV.VLOUTROS, 0), DECODE(NVL(PCNFSAID.SOMAREPASSEOUTRASDESPNF,'N'),'N',NVL((PCMOV.VLOUTROS), 0),'S',NVL((NVL(PCMOV.VLOUTROS,0)-NVL(PCMOV.VLREPASSE,0)), 0)))
                    ),0)))),                                                    
             2) END AS VLVENDA,                                                 
                                                                                
       (((DECODE(PCMOV.CODOPER,                                                 
                 'S',                                                         
                 (NVL(DECODE(PCNFSAID.CONDVENDA, 7, PCMOV.QTCONT, PCMOV.QT),    
                      0)),                                                      
                 'ST',                                                        
                 (NVL(DECODE(PCNFSAID.CONDVENDA, 7, PCMOV.QTCONT, PCMOV.QT),    
                      0)),                                                      
                 'SM',                                                        
                 (NVL(DECODE(PCNFSAID.CONDVENDA, 7, PCMOV.QTCONT, PCMOV.QT),    
                      0)),                                                      
                 0)) *                                                          
       (NVL(DECODE(PCNFSAID.CONDVENDA,                                          
                     7,                                                         
                     PCMOV.PUNITCONT,                                           
                     NVL(PCMOV.PUNIT, 0) + NVL(PCMOV.VLFRETE, 0) +              
                     NVL(PCMOV.VLOUTRASDESP, 0) +                               
                     NVL(PCMOV.VLFRETE_RATEIO, 0) +                             
                     DECODE(PCMOV.TIPOITEM,                                     
                            'C',                                              
                            (SELECT (SUM(M.QTCONT * NVL(M.VLOUTROS, 0)) /       
                                    PCMOV.QT) VLOUTROS                          
                               FROM PCMOV M                                     
                              WHERE M.NUMTRANSVENDA = PCMOV.NUMTRANSVENDA       
                                AND M.TIPOITEM = 'I'                          
                                AND CODPRODPRINC = PCMOV.CODPROD),              
 'I', NVL(PCMOV.VLOUTROS, 0), DECODE(NVL(PCNFSAID.SOMAREPASSEOUTRASDESPNF,'N'),'N',NVL((PCMOV.VLOUTROS), 0),'S',NVL((NVL(PCMOV.VLOUTROS,0)-NVL(PCMOV.VLREPASSE,0)), 0)))
                      - (nvl(pcmov.ST,0)+NVL(PCMOVCOMPLE.VLSTTRANSFCD,0))),               
              0)))) VLVENDA_SEMST,                                              
      ROUND(    (NVL(PCMOV.QT, 0) *(
       DECODE(PCNFSAID.CONDVENDA,
               5,
               DECODE(PCMOV.PBONIFIC, NULL, PCMOV.PTABELA, PCMOV.PBONIFIC)
               ,6,
               DECODE(PCMOV.PBONIFIC, NULL, PCMOV.PTABELA, PCMOV.PBONIFIC),
               11,
               DECODE(PCMOV.PBONIFIC, NULL, PCMOV.PTABELA, PCMOV.PBONIFIC),
               1,
               NVL(PCMOV.PBONIFIC,0),                                      
               14,
               NVL(PCMOV.PBONIFIC,0),                                      
               12,
               DECODE(PCMOV.PBONIFIC, NULL, PCMOV.PTABELA, PCMOV.PBONIFIC),
               0)) 
),2) VLBONIFIC,
               ((DECODE(PCMOV.CODOPER,
                           'S',
                           (NVL(DECODE(PCNFSAID.CONDVENDA,
                                       7,
                                       PCMOV.QTCONT,
                                       PCMOV.QT),
                                0)),
                           'ST',
                           (NVL(DECODE(PCNFSAID.CONDVENDA,
                                       7,
                                       PCMOV.QTCONT,
                                       PCMOV.QT),
                                0)),
                           'SM',
                           (NVL(DECODE(PCNFSAID.CONDVENDA,
                                       7,
                                       PCMOV.QTCONT,
                                       PCMOV.QT),
                                0)),
                           0))) QTVENDIDA,
       ROUND( (NVL(PCPRODUT.PESOBRUTO,PCMOV.PESOBRUTO) * NVL(PCMOV.QT, 0)),2) AS TOTPESO,
       ROUND(PCMOV.QT * (PCMOV.PTABELA
                       + NVL (pcmov.vlfrete, 0) + NVL (pcmov.vloutrasdesp, 0) + NVL (pcmov.vlfrete_rateio, 0) + NVL (pcmov.vloutros, 0) 
  ),2) VLTABELA,
       PCMOV.CODCLI QTCLIPOS,
       PCNFSAID.NUMTRANSVENDA QTNUMTRANSVENDA, 
      (SELECT PCFILIAL.FANTASIA 
              FROM PCFILIAL  
             WHERE PCFILIAL.CODIGO = PCNFSAID.CODFILIAL AND ROWNUM = 1) FILIAL,
       PCPRODUT.CODPROD AS QTMIXCAD,
       PCMOV.CODPROD AS QTMIX, 
   (SELECT COUNT(*) FROM PCPRODUT P
WHERE P.CODFORNEC = PCFORNEC.CODFORNEC AND NVL(P.REVENDA,'S')  = 'S' ) QTMIXCADNOVO,
 PCGERENTE.NOMEGERENTE,
 DECODE(PCNFSAID.CODGERENTE,NULL,PCSUPERV.CODGERENTE,PCNFSAID.CODGERENTE) CODGERENTE, 
 PCPRACA.ROTA,
 PCROTAEXP.DESCRICAO DESCROTA,
               (NVL(PCMOV.VLREPASSE,0) * DECODE(PCNFSAID.CONDVENDA,
              5,0,6,0,11,0,12,0,DECODE(PCMOV.CODOPER,'SB',0,NVL(PCMOV.QT, 0)) ))  AS VLREPASSE
  FROM PCNFSAID,
       PCPRODUT,
       PCMOV,
       PCCLIENT,
       PCUSUARI,
       PCSUPERV,
       PCPLPAG,
       PCFORNEC,
       PCATIVI, 
       PCPRACA,
       PCDEPTO,
       PCSECAO,
       PCPEDC,
       PCGERENTE,
       PCCIDADE,
       PCMARCA,
       PCROTAEXP,
       PCMOVCOMPLE
 WHERE PCMOV.NUMTRANSVENDA = PCNFSAID.NUMTRANSVENDA
   AND PCMOV.CODFILIAL = PCNFSAID.CODFILIAL 
   AND PCMOV.DTMOV BETWEEN  TO_DATE('01/04/2024', 'DD/MM/YYYY') AND 
                                 TO_DATE('30/04/2024', 'DD/MM/YYYY') 
   AND PCMOV.CODPROD = PCPRODUT.CODPROD
   AND PCNFSAID.CODPRACA = PCPRACA.CODPRACA(+)
   AND PCATIVI.CODATIV(+) = PCCLIENT.CODATV1
   AND PCMOV.CODCLI = PCCLIENT.CODCLI
   AND PCFORNEC.CODFORNEC = PCPRODUT.CODFORNEC
   AND  PCNFSAID.CODUSUR   = PCUSUARI.CODUSUR 
   AND PCPRACA.ROTA = PCROTAEXP.CODROTA(+)
   AND PCMOV.NUMTRANSITEM = PCMOVCOMPLE.NUMTRANSITEM(+)
   AND PCPRODUT.CODMARCA = PCMARCA.CODMARCA(+)
   AND PCCLIENT.CODCIDADE = PCCIDADE.CODCIDADE(+)
  AND PCMOV.CODOPER <> 'SR' 
  AND NVL(PCNFSAID.TIPOVENDA,'X') NOT IN ('SR', 'DF')
  AND PCMOV.CODOPER <> 'SO' 
   AND  NVL(PCNFSAID.CODSUPERVISOR,PCSUPERV.CODSUPERVISOR)   = PCSUPERV.CODSUPERVISOR
   AND PCNFSAID.CODPLPAG = PCPLPAG.CODPLPAG
   AND PCNFSAID.NUMPED = PCPEDC.NUMPED(+)
   AND PCPRODUT.CODEPTO = PCDEPTO.CODEPTO(+)
   AND PCPRODUT.CODSEC = PCSECAO.CODSEC(+)
   AND DECODE(PCNFSAID.CODGERENTE,NULL,PCSUPERV.CODGERENTE,PCNFSAID.CODGERENTE) = PCGERENTE.CODGERENTE 
   AND PCNFSAID.CODFISCAL NOT IN (522, 622, 722, 532, 632, 732)
   AND PCNFSAID.CONDVENDA NOT IN (4, 8, 10, 13, 20, 98, 99)
   AND (PCNFSAID.DTCANCEL IS NULL)
       AND PCPRODUT.CODSEC IN ('10040','10042','120239')
   AND PCNFSAID.DTSAIDA BETWEEN  TO_DATE('01/04/2024', 'DD/MM/YYYY') AND 
                                 TO_DATE('30/04/2024', 'DD/MM/YYYY') 
           AND PCMOV.CODFILIAL IN('3')
           AND PCNFSAID.CODFILIAL IN('3')
)
        GROUP BY CODUSUR,
              NOME
              ) VENDAS, 
     (SELECT CODUSUR, 
             SUM(NVL(VLMETA, 0)) VLMETA,
             SUM(NVL(QTMETA, 0)) QTMETA,
             SUM(NVL(QTPESOMETA, 0)) QTPESOMETA,
             SUM(NVL(MIXPREV, 0)) MIXPREV,
             SUM(NVL(CLIPOSPREV, 0)) CLIPOSPREV
       FROM (SELECT 
PCMETA.CODIGO,
       PCUSUARI.CODUSUR,
       PCUSUARI.CODSUPERVISOR,
       PCSUPERV.NOME SUPERV,
       PCUSUARI.NOME,
       0 NUMTRANSVENDA,
       0 QTDEVOLUCAO,
       0 VLDEVOLUCAO,
       0 TOTPESO,
       0 QTCLIPOS,
       0 QTMIXCAD,
       0 QTMIX,
       0 QTVENDA,
       0 VLVENDA,
       0 LITRAGEM,
       0 VLCUSTOFIN,
       PCMETA.CODFILIAL,
       (SELECT PCFILIAL.FANTASIA FROM PCFILIAL WHERE PCMETA.CODFILIAL = PCFILIAL.CODIGO) FILIAL,
       NVL(PCMETA.VLVENDAPREV, 0) VLMETA,
       NVL(PCMETA.QTVENDAPREV, 0) QTMETA,
       NVL(PCMETA.QTPESOPREV, 0) QTPESOMETA,
       NVL(PCMETA.MIXPREV, 0) MIXPREV,
       NVL(PCMETA.CLIPOSPREV, 0) CLIPOSPREV,
       NVL(PCMETA.VOLUMEPREV,0) VOLUMEPREV,
 PCSECAO.CODSEC, PCSECAO.DESCRICAO SECAO, PCDEPTO.CODEPTO, PCDEPTO.DESCRICAO DEPARTAMENTO, PCPRODUT.CODFAB,
 PCPRODUT.DESCRICAO, PCPRODUT.EMBALAGEM, PCPRODUT.UNIDADE, PCPRODUT.CODPROD,
   PCFORNEC.CODFORNEC, PCFORNEC.FORNECEDOR
  FROM PCMETA, PCUSUARI, PCSUPERV  
   , PCPRODUT, PCDEPTO, PCSECAO, PCFORNEC 
 WHERE PCMETA.CODUSUR = PCUSUARI.CODUSUR
   AND   PCUSUARI.CODSUPERVISOR = PCSUPERV.CODSUPERVISOR
   AND PCUSUARI.CODSUPERVISOR NOT IN ('9999')
   AND PCMETA.TIPOMETA = 'P'
   AND PCPRODUT.CODPROD = PCMETA.CODIGO
   AND PCPRODUT.CODEPTO = PCDEPTO.CODEPTO(+)
   AND PCPRODUT.CODSEC = PCSECAO.CODSEC(+)
   AND PCPRODUT.CODFORNEC = PCFORNEC.CODFORNEC(+)
   AND PCMETA.DATA BETWEEN  TO_DATE('01/04/2024', 'DD/MM/YYYY') AND 
                            TO_DATE('30/04/2024', 'DD/MM/YYYY') 
   AND NVL(PCMETA.CODFILIAL, ' ') IN('3')
)
   GROUP BY CODUSUR) META,
      
      ( SELECT CODUSURDEVOL, NOME,
               SUM(QTDEVOLUCAO) QTDEVOLUCAO,
               SUM(VLDEVOLUCAO) VLDEVOLUCAO,
               SUM(VLDEVOLUCAO_SEMST) VLDEVOLUCAO_SEMST,
               SUM(TOTPESO) TOTPESO,
               SUM(VOLUME) VOLUME,
               COUNT(DISTINCT(DEVOLVIDO)) QTCLIPOSNEG,
               SUM(NVL(VLBONIFIC,0)) VLBONIFIC, 
               SUM(NVL(VLREPASSEBNF, 0)) VLREPASSEBNF, 
               SUM(NVL(VLREPASSE,0)) VLREPASSE,
   SUM(NVL(LITRAGEM,0)) LITRAGEM FROM  (SELECT PCFORNEC.CODFORNEC, 
       PCFORNEC.FORNECEDOR, 
       PCFORNEC.CODFORNECPRINC,
      (SELECT A.FORNECEDOR FROM PCFORNEC A WHERE A.CODFORNEC = PCFORNEC.CODFORNECPRINC) FORNECEDORPRINC,
       PCNFENT.CODFORNEC CODCLI,
       PCCLIENT.CODATV1,
       DECODE(NVL(PCPEDC.NUMCAIXA,0),0,0,NVL(PCPEDC.NUMCAIXA,0)) CAIXA,
       PCNFENT.NUMNOTA ,
       PCNFENT.CODDEVOL,
       NVL(PCNFENT.VLOUTRAS,0) VLOUTRAS,
       NVL(PCNFENT.VLFRETE,0) VLFRETE,
       PCNFENT.CODFILIAL ,
       PCNFENT.CODMOTORISTADEVOL,
    (SELECT X.CLIENTE 
       FROM PCCLIENT X
      WHERE X.CODCLI = NVL(PCCLIENT.CODCLIPRINC, PCCLIENT.CODCLI)) CLIENTEPRINC,
       (SELECT DISTINCT PCEMPR.NOME  
          FROM PCEMPR                
         WHERE PCEMPR.MATRICULA = PCNFENT.CODMOTORISTADEVOL) NOMEMOTORISTA,
       PCNFENT.DTENT,
       PCNFENT.NUMTRANSENT,
       PCESTCOM.NUMTRANSVENDA, 
       PCEMPR.NOME NOMEFUNC,
       PCTABDEV.MOTIVO,
       PCCLIENT.CLIENTE,
       PCCLIENT.CODCIDADE,
       PCCIDADE.NOMECIDADE,
       PCMOV.CUSTOFIN,
       PCMOV.CODDEVOL DEVOLITEM,
       PCTABDEV2.MOTIVO MOTIVO2,
       PCCLIENT.ESTENT,
       PCCLIENT.MUNICENT,
       PCCLIENT.VIP,
       PCESTCOM.VLESTORNO,
       PCNFENT.OBS,
       PCMOV.CODOPER,
       PCMOV.ST,
       (DECODE(PCNFSAID.CONDVENDA,7,NVL(PCMOV.PUNITCONT,0),NVL(PCMOV.PUNIT,0))) PUNIT,
       PCPRODUT.DESCRICAO,
       PCPRODUT.CODAUXILIAR,
       PCPRODUT.EMBALAGEM,
       PCPRODUT.UNIDADE,
       PCMOV.CODPROD,
       NVL(PCPRODUT.QTUNIT,0) QTUNIT, 
       PCPRODUT.CODEPTO, 
       PCPRODUT.CODSEC, 
       PCPRODUT.CODFAB, 
       PCUSUARI.PERCENT, 
       PCUSUARI.PERCENT2, 
       PCDEPTO.DESCRICAO DEPARTAMENTO, 
       PCSECAO.DESCRICAO SECAO, 
 NVL(PCNFSAID.CODSUPERVISOR,PCSUPERV.CODSUPERVISOR)  CODSUPERVISOR, 
       PCMARCA.MARCA,
       PCATIVI.CODATIV,
       PCATIVI.RAMO,
       PCPRACA.CODPRACA, 
       DECODE(PCMOV.NUMREGIAO, NULL, PCPRACA.NUMREGIAO, PCMOV.NUMREGIAO) NUMREGIAO, 
       PCPRACA.ROTA, 
       PCPRACA.PRACA, 
       0 QTMETA,
       0 QTPESOMETA,
       0 MIXPREV,
       0 CLIPOSPREV,
       NVL(PCNFSAID.CODPLPAG,PCCLIENT.CODPLPAG) CODPLPAG, 
       PCNFSAID.NUMPED,
       PCNFSAID.CODCOB,
       PCNFSAID.CONDVENDA,
       PCNFSAID.PRAZOMEDIO,
       PCNFSAID.CODEMITENTE,
       PCPLPAG.DESCRICAO DESCRICAOPCPLPAG,
       NVL(PCPLPAG.NUMDIAS,0) NUMDIAS,
       PCUSUARI.NOME,
       PCNFENT.VLST,
       PCSUPERV.NOME AS SUPERV,
       ROUND(DECODE(PCNFSAID.CONDVENDA,                      
                    5,                                       
                    0,                        
                    DECODE(NVL(PCMOVCOMPLE.BONIFIC, 'N'),  
                           'N',                            
                           NVL(PCMOV.QT, 0),                 
                           0)) * NVL(PCMOV.VLREPASSE, 0),    
                2) VLREPASSE,                                
       ROUND(DECODE(PCNFSAID.CONDVENDA,                      
                    5,                                       
                    NVL(PCMOV.QT, 0),                        
                    DECODE(NVL(PCMOVCOMPLE.BONIFIC, 'N'),  
                           'N',                            
                           0,                                
                           NVL(PCMOV.QT, 0),                 
                           0)) * NVL(PCMOV.VLREPASSE, 0),    
                2) VLREPASSEBNF,                             
       0 VLVENDA, 
       0 QTBONIFIC,
      (SELECT PCFILIAL.FANTASIA 
              FROM PCNFENT P, PCFILIAL  
             WHERE P.CODFILIAL = PCFILIAL.CODIGO 
               AND P.NUMTRANSENT = PCNFENT.NUMTRANSENT  AND ROWNUM = 1) FILIAL,
 (NVL(PCMOV.QT,0)) QT,        
     (NVL(PCMOV.QT,0)) QTDEVOLUCAO,
 CASE WHEN NVL(PCMOVCOMPLE.VLSUBTOTITEM,0) <> 0 THEN  
  NVL(PCMOVCOMPLE.VLSUBTOTITEM,0) -                  
       (  ROUND((NVL(PCMOV.QT, 0) * 
         DECODE(PCNFSAID.CONDVENDA,
                 5,
                 0,
                 6,
                 0,
                 11,
                 0,
                 12,
                 0,
                 DECODE(PCMOV.CODOPER,'SB',0,nvl(pcmov.VLIPI,0)))),2)) -  
       (  ROUND(NVL(PCMOV.QT, 0) * 
         DECODE(PCNFSAID.CONDVENDA,
                 5,
                 0,
                 6,
                 0,
                 11,
                 0,
                 12,
                 0,
                 DECODE(PCMOV.CODOPER,'SB',0,nvl(pcmov.ST,0))),2)) 
 ELSE                                                
  (DECODE(PCNFSAID.CONDVENDA, 5, 0, DECODE(NVL(PCMOVCOMPLE.BONIFIC, 'N'), 'N', NVL(PCMOV.QT, 0), 0)) * 
  DECODE(PCNFSAID.CONDVENDA,                                                    
          5,                                                                    
          0,                                                                    
          6,                                                                    
          0,                                                                    
          11,                                                                   
          0,                                                                    
          (DECODE(PCMOV.PUNIT,                                                  
                  0,                                                            
                  PCMOV.PUNITCONT,                                              
                  NULL,                                                         
                  PCMOV.PUNITCONT,                                              
                  PCMOV.PUNIT) + NVL(PCMOV.VLFRETE, 0) +                        
          NVL(PCMOV.VLOUTRASDESP, 0) + NVL(PCMOV.VLFRETE_RATEIO, 0)             
  - (decode(NVL(PCNFSAID.SOMAREPASSEOUTRASDESPNF,'N'),'N', (DECODE(NVL(PCMOV.VLOUTROS,0),0,NVL(PCMOV.VLREPASSE,0),0)),'S',(NVL(PCMOV.VLREPASSE,0)))) 
          + NVL(PCMOV.VLOUTROS, 0)))) END AS VLDEVOLUCAO,                          
  (DECODE(PCNFSAID.CONDVENDA, 5, 0, DECODE(NVL(PCMOVCOMPLE.BONIFIC, 'N'), 'N', NVL(PCMOV.QT, 0), 0)) * 
  DECODE(PCNFSAID.CONDVENDA,                                                    
          5,                                                                    
          0,                                                                    
          6,                                                                    
          0,                                                                    
          11,                                                                   
          0,                                                                    
          (nvl(PCMOV.ST,0) + NVL(PCMOVCOMPLE.VLSTTRANSFCD,0)) )) VALORST,                                          
          0 VALORSTX,                                                          
  (DECODE(PCNFSAID.CONDVENDA, 5, 0, DECODE(NVL(PCMOVCOMPLE.BONIFIC, 'N'), 'N', NVL(PCMOV.QT, 0), 0)) * 
  DECODE(PCNFSAID.CONDVENDA,                                                    
          5,                                                                    
          0,                                                                    
          6,                                                                    
          0,                                                                    
          11,                                                                   
          0,                                                                    
          nvl(PCMOV.VLIPI,0) )) VALORIPI,                                          
          0 VALORIPIX,                                                          
  (NVL(PCMOV.QT, 0) *                                                           
  DECODE(PCNFSAID.CONDVENDA,                                                    
          5,                                                                    
          0,                                                                    
          6,                                                                    
          0,                                                                    
          11,                                                                   
          0,                                                                    
          (DECODE(PCMOV.PUNIT,                                                  
                  0,                                                            
                  PCMOV.PUNITCONT,                                              
                  NULL,                                                         
                  PCMOV.PUNITCONT,                                              
                  PCMOV.PUNIT) + NVL(PCMOV.VLOUTROS, 0) -                       
          (NVL(PCMOV.ST,0) + NVL(PCMOVCOMPLE.VLSTTRANSFCD,0)) + NVL(PCMOV.VLFRETE, 0)))) VLDEVOLUCAO_SEMST,        
  (NVL(PCMOV.QT, 0) *                                                           
  (DECODE(PCNFSAID.CONDVENDA,                                                   
          5,                                                                    
          NVL(PCMOV.PUNITCONT, 0),                                              
          0) + NVL(PCMOV.VLOUTROS, 0) +                                         
               NVL(PCMOV.VLFRETE, 0))) VLDEVOLUCAOBNF,                          
  (NVL(PCMOV.QT, 0) *                                                           
  (DECODE(PCNFSAID.CONDVENDA,                                                   
           5,                                                                   
           NVL(PCMOV.PUNITCONT, 0),                                             
           6,                                                                   
           NVL(PCMOV.PUNITCONT, 0),                                             
           11,                                                                  
           NVL(PCMOV.PUNITCONT, 0),                                             
           12,                                                                  
           NVL(PCMOV.PUNITCONT, 0),                                             
           0) + DECODE(PCNFSAID.CONDVENDA,                                      
                         5,                                                     
                         NVL(PCMOV.VLOUTROS, 0),                                
                         6,                                                     
                         NVL(PCMOV.VLOUTROS, 0),                                
                         11,                                                    
                         NVL(PCMOV.VLOUTROS, 0),                                
                         12,                                                    
                         NVL(PCMOV.VLOUTROS, 0)) +                              
  DECODE(PCNFSAID.CONDVENDA,                                                    
           5,                                                                   
           NVL(PCMOV.VLFRETE, 0),                                               
           6,                                                                   
           NVL(PCMOV.VLFRETE, 0),                                               
           11,                                                                  
           NVL(PCMOV.VLFRETE, 0),                                               
           12,                                                                  
           NVL(PCMOV.VLFRETE, 0)))) VLDEVOLUCAOBONI,                            
  (NVL(PCMOV.QT, 0) * NVL(PCMOV.CUSTOFIN, 0)) VLCMVDEVOL,                       
  (NVL(PCMOV.QT, 0) * (NVL(PCMOV.CUSTOFIN, 0)                                   
   )) VLCUSTOFIN,                                                               
  (NVL(PCPRODUT.LITRAGEM, 0) * NVL(PCMOV.QT, 0)) LITRAGEM,                      
  (NVL(PCPRODUT.VOLUME, 0) * NVL(PCMOV.QT, 0)) VOLUME,                          
  (DECODE(PCMOV.PBASERCA,                                                       
          NULL,                                                                 
          NVL(PCMOV.PBASERCA, NVL(PCMOV.PTABELA, 0)),                           
          NVL(PCMOV.PTABELA, 0)) * NVL(PCMOV.QT, 0)) DEVOLTAB,                  
  (NVL(PCPRODUT.PESOBRUTO,PCMOV.PESOBRUTO) * NVL(PCMOV.QT, 0)) AS TOTPESO,     
  
  ROUND((NVL(PCMOV.QT, 0) *                                                     
        DECODE(PCNFSAID.CONDVENDA,                                              
                5,                                                              
                DECODE(PCMOV.PBONIFIC,                                          
                       NULL,                                                    
                       PCMOV.PTABELA,                                           
                       PCMOV.PBONIFIC) /*+ NVL(PCMOV.VLFRETE, 0)*/ +                
                NVL(PCMOV.VLOUTRASDESP, 0) +                                    
                NVL(PCMOV.VLFRETE_RATEIO, 0) + NVL(PCMOV.VLOUTROS, 0)           
                ,6,                                                             
                DECODE(PCMOV.PBONIFIC,                                          
                       NULL,                                                    
                       PCMOV.PTABELA,                                           
                       PCMOV.PBONIFIC),                                         
                1,                                                              
                NVL(PCMOV.PBONIFIC,0),                                           
                14,                                                             
                NVL(PCMOV.PBONIFIC,0),                                           
                11,                                                             
                DECODE(PCMOV.PBONIFIC,                                          
                       NULL,                                                    
                       PCMOV.PTABELA,                                           
                       PCMOV.PBONIFIC),                                         
                12,                                                             
                DECODE(PCMOV.PBONIFIC,                                          
                       NULL,                                                    
                       PCMOV.PTABELA,                                           
                       PCMOV.PBONIFIC),                                         
                0)                                                              
        ),2) VLBONIFIC,                                                        

       NVL(PCCLIENT.CODCLIPRINC,PCCLIENT.CODCLI) CODCLIPRINC,  
 PCNFENT.CODUSURDEVOL  CODUSUR, 
 PCNFENT.CODUSURDEVOL  CODUSURDEVOL, 
       CASE WHEN  (  SELECT SUM ( NVL(PCMOV.QT, 0) * (NVL(PCMOV.PUNIT, 0) + NVL(PCMOV.VLOUTROS, 0)) ) FROM PCMOV M, PCESTCOM E, PCNFENT  F
         WHERE E.NUMTRANSENT = F.NUMTRANSENT AND M.NUMTRANSENT = F.NUMTRANSENT
         AND M.CODOPER = 'ED' AND M.DTCANCEL IS NULL
         AND PCNFSAID.NUMTRANSVENDA = E.NUMTRANSVENDA )  >= NVL(PCNFSAID.VLTOTAL,0) THEN
            PCFORNEC.CODFORNEC 
            ELSE
            0 END DEVOLVIDO, 
      (SELECT PCCLIENT.CODPLPAG || ' - ' || PCPLPAG.DESCRICAO  FROM PCPLPAG WHERE PCCLIENT.CODPLPAG = PCPLPAG.CODPLPAG) DESCRICAOPLANOCLI,
      PCGERENTE.NOMEGERENTE,
      DECODE(PCNFSAID.CODGERENTE,NULL,PCSUPERV.CODGERENTE,PCNFSAID.CODGERENTE) CODGERENTE  
      , PCROTAEXP.DESCRICAO DESCROTA
  FROM PCNFENT, PCESTCOM, PCEMPR, PCNFSAID, PCMOV, PCPRODUT, PCCLIENT, PCFORNEC, PCPRACA, PCTABDEV, PCTABDEV PCTABDEV2, 
       PCDEPTO, PCSECAO, PCUSUARI, PCPLPAG, PCSUPERV, PCATIVI, PCPEDC, PCCIDADE, PCMARCA, PCGERENTE, PCMOVCOMPLE,PCROTAEXP 
 ,(SELECT DISTINCT CASE                                          
            WHEN PED.CONDVENDA = 7 THEN                          
             (SELECT DISTINCT P1.NUMPED                          
                FROM PCPEDC P1, PCESTCOM E1                      
               WHERE E1.NUMTRANSENT = ESTC.NUMTRANSENT           
                 AND P1.NUMTRANSVENDA = E1.NUMTRANSVENDA         
                 AND P1.NUMPEDENTFUT = PED.NUMPED                
                 AND P1.CONDVENDA = 8)                           
            WHEN PED.CONDVENDA = 8 THEN                          
             (SELECT DISTINCT P2.NUMPED                          
                FROM PCPEDC P2, PCESTCOM E2                      
               WHERE E2.NUMTRANSENT = ESTC.NUMTRANSENT           
                 AND P2.NUMTRANSVENDA = E2.NUMTRANSVENDA         
                 AND P2.NUMPED = PED.NUMPEDENTFUT                
                 AND P2.CONDVENDA = 7)                           
          END TEMVENDATV8,                                       
          PED.NUMTRANSVENDA,                                     
          ESTC.NUMTRANSENT                                       
     FROM PCPEDC PED, PCESTCOM ESTC                              
    WHERE PED.NUMTRANSVENDA(+) = ESTC.NUMTRANSVENDA
   AND PED.DATA BETWEEN  TO_DATE('01/04/2024', 'DD/MM/YYYY') AND 
                              TO_DATE('30/04/2024', 'DD/MM/YYYY') 
      ) TEMVENDATV8 
 WHERE PCNFENT.NUMTRANSENT = PCESTCOM.NUMTRANSENT
   AND PCCLIENT.CODPRACA = PCPRACA.CODPRACA
   AND PCESTCOM.NUMTRANSENT = PCMOV.NUMTRANSENT
   AND PCFORNEC.CODFORNEC = PCPRODUT.CODFORNEC
   AND PCNFSAID.NUMPED  = PCPEDC.NUMPED(+)
   AND PCNFENT.CODDEVOL = PCTABDEV.CODDEVOL(+)
   AND PCMOV.CODDEVOL = PCTABDEV2.CODDEVOL(+)
   AND PCPRODUT.CODEPTO = PCDEPTO.CODEPTO(+)
   AND PCPRACA.ROTA = PCROTAEXP.CODROTA(+)
AND PCNFENT.CODUSURDEVOL = PCUSUARI.CODUSUR(+)
AND NVL(PCNFSAID.CODSUPERVISOR,PCUSUARI.CODSUPERVISOR) = PCSUPERV.CODSUPERVISOR
   AND PCPRODUT.CODSEC = PCSECAO.CODSEC(+)
   AND PCCLIENT.CODATV1 = PCATIVI.CODATIV(+)
   AND PCNFENT.CODFUNCLANC  = PCEMPR.MATRICULA(+)
   AND PCESTCOM.NUMTRANSVENDA = PCNFSAID.NUMTRANSVENDA(+)
   AND PCCLIENT.CODCIDADE = PCCIDADE.CODCIDADE(+)
   AND NVL(PCNFSAID.CODPLPAG,PCCLIENT.CODPLPAG) = PCPLPAG.CODPLPAG
   AND PCPRODUT.CODMARCA = PCMARCA.CODMARCA(+)
   AND PCMOV.NUMTRANSITEM = PCMOVCOMPLE.NUMTRANSITEM(+)
 AND DECODE(PCNFSAID.CODGERENTE,NULL,PCSUPERV.CODGERENTE,PCNFSAID.CODGERENTE) = PCGERENTE.CODGERENTE
      -- numtransvenda = 0 refere-se a devolucoes avulsas que nao
      -- devem ser incluidas no resumo de faturamento
   AND PCMOV.CODPROD = PCPRODUT.CODPROD
   AND PCNFENT.CODFORNEC = PCCLIENT.CODCLI 
   AND PCNFENT.TIPODESCARGA IN ('6', '7', 'T')
   AND NVL(PCNFENT.CODFISCAL,0) IN (131, 132, 231, 232, 199, 299)
   AND PCMOV.DTCANCEL IS NULL
   AND PCMOV.CODOPER = 'ED' 
   AND NVL(PCNFENT.TIPOMOVGARANTIA, -1) = -1
   AND NVL(PCNFENT.OBS, 'X') <> 'NF CANCELADA'
    AND TEMVENDATV8.NUMTRANSENT(+) = PCNFENT.NUMTRANSENT       
          AND NVL(PCNFSAID.CONDVENDA, 0) NOT IN (4, 8, 10, 13, 20, 98, 99)
   AND PCNFENT.DTENT BETWEEN  TO_DATE('01/04/2024', 'DD/MM/YYYY') AND 
                              TO_DATE('30/04/2024', 'DD/MM/YYYY') 


       AND PCPRODUT.CODSEC IN ('10040','10042','120239')
           AND PCMOV.CODFILIAL IN('3')
           AND PCNFENT.CODFILIAL IN('3')
   AND PCNFENT.DTENT BETWEEN  TO_DATE('01/04/2024', 'DD/MM/YYYY') AND 
                              TO_DATE('30/04/2024', 'DD/MM/YYYY') 
   AND PCMOV.DTMOV BETWEEN  TO_DATE('01/04/2024', 'DD/MM/YYYY') AND 
                              TO_DATE('30/04/2024', 'DD/MM/YYYY') 
)

        GROUP BY CODUSURDEVOL, NOME) DEVOLUCAO,
     PCUSUARI
WHERE PCUSUARI.CODUSUR = VENDAS.CODUSUR(+)
  AND PCUSUARI.CODUSUR = DEVOLUCAO.CODUSURDEVOL(+)
  AND PCUSUARI.CODUSUR = META.CODUSUR(+)
  AND ( ( NVL(VENDAS.QTVENDA,0) <> 0) or  ( NVL(DEVOLUCAO.QTDEVOLUCAO,0) <> 0) or  ( NVL(DEVOLUCAO.VLDEVOLUCAO,0) <> 0) OR 
 (NVL(VENDAS.TOTPESO,0) <> 0) OR (NVL(VENDAS.VLVENDA,0) <> 0) OR  (NVL(VENDAS.CODUSUR,0) <> 0) OR (NVL(VENDAS.VLBONIFIC,0) <> 0)  OR (NVL(vendas.QTCLIPOS,0) <> 0) ) 
GROUP BY VENDAS.CODUSUR,
       VENDAS.NOME,
       DEVOLUCAO.CODUSURDEVOL,
       DEVOLUCAO.NOME,
       (NVL(VLMETA, 0)),
       (NVL(QTMETA, 0)),
       (NVL(QTPESOMETA, 0)),
       (NVL(MIXPREV, 0)),
       (NVL(CLIPOSPREV, 0))
ORDER BY codusur

