-- CTE's: (Cada uma delas obtem valores das vendas por supervisor em diferentes seções de produtos)
WITH SUPPLF --IOGURTE DANONE
AS (SELECT  pedc.CODSUPERVISOR,
            ped.codusur,
            To_number(SUM(ped.qt*ped.pvenda)) as Fat
    FROM pontual.PCPEDI ped
        JOIN pontual.pcprodut prod on ped.codprod = prod.codprod
        JOIN pontual.pcpedc pedc on ped.NUMPED = pedc.NUMPED
    WHERE prod.codsec in (10040,10042,120239)
        AND ped.data BETWEEN '01-ago-2023' and '31-ago-2023'  --'{DATAI}' and '{DATAF}'
        AND ped.posicao NOT IN ('C')
        AND ped.vlbonific = 0
        AND NVL(ped.BONIFIC, 'N') =  'N'
        AND pedc.DTCANCEL IS NULL
        AND pedc.CONDVENDA IN (1, 2, 3, 7, 9, 14, 15, 17, 18, 19, 98)
        AND pedc.CODSUPERVISOR in (2,8,9)
    Group By ped.codusur,pedc.CODSUPERVISOR
    ORDER By FAT DESC),
    
       ---------------------------------------------------------------
       
SUPACT --ACTIVIA DANONE
AS (SELECT  pedc.CODSUPERVISOR,
            ped.codusur,
            prod.codsec,
            To_number(SUM(ped.qt*ped.pvenda)) as Fat
    FROM pontual.PCPEDI ped
        JOIN pontual.pcprodut prod on ped.codprod = prod.codprod
        JOIN pontual.pcpedc pedc on ped.NUMPED = pedc.NUMPED
    WHERE prod.codsec in (10040)
        AND ped.data BETWEEN '01-ago-2023' and '31-ago-2023' 
        AND ped.posicao NOT IN ('C')
        AND ped.vlbonific = 0
        AND NVL(ped.BONIFIC, 'N') =  'N'
        AND pedc.DTCANCEL IS NULL
        AND pedc.CONDVENDA IN (1, 2, 3, 7, 9, 14, 15, 17, 18, 19, 98)
        AND pedc.CODSUPERVISOR in (2,8,9)
    Group By ped.codusur,pedc.CODSUPERVISOR,prod.codsec
    ORDER By FAT DESC),
    
       ---------------------------------------------------------------
       
SUPDHO --DANONINHO DANONE
AS (SELECT  pedc.CODSUPERVISOR,
            ped.codusur,
            prod.codsec,
            To_number(SUM(ped.qt*ped.pvenda)) as Fat
    FROM pontual.PCPEDI ped
        JOIN pontual.pcprodut prod on ped.codprod = prod.codprod
        JOIN pontual.pcpedc pedc on ped.NUMPED = pedc.NUMPED
    WHERE prod.codsec in (10042)
        AND ped.data BETWEEN '01-ago-2023' and '31-ago-2023' 
        AND ped.posicao NOT IN ('C')
        AND ped.vlbonific = 0
        AND NVL(ped.BONIFIC, 'N') =  'N'
        AND pedc.DTCANCEL IS NULL
        AND pedc.CONDVENDA IN (1, 2, 3, 7, 9, 14, 15, 17, 18, 19, 98)
        AND pedc.CODSUPERVISOR in (2,8,9)
    Group By ped.codusur,pedc.CODSUPERVISOR,prod.codsec
    ORDER By FAT DESC),
    
       ---------------------------------------------------------------
       
SUPGRA --GRANADA DANONE
AS (SELECT  pedc.CODSUPERVISOR,
            ped.codusur,
            prod.codsec,
            To_number(SUM(ped.qt*ped.pvenda)) as Fat
    FROM pontual.PCPEDI ped
        JOIN pontual.pcprodut prod on ped.codprod = prod.codprod
        JOIN pontual.pcpedc pedc on ped.NUMPED = pedc.NUMPED
    WHERE prod.codsec in (120239)
        AND ped.data BETWEEN '01-ago-2023' and '31-ago-2023' 
        AND ped.posicao NOT IN ('C')
        AND ped.vlbonific = 0
        AND NVL(ped.BONIFIC, 'N') =  'N'
        AND pedc.DTCANCEL IS NULL
        AND pedc.CONDVENDA IN (1, 2, 3, 7, 9, 14, 15, 17, 18, 19, 98)
        AND pedc.CODSUPERVISOR in (2,8,9)
    Group By ped.codusur,pedc.CODSUPERVISOR,prod.codsec
    ORDER By FAT DESC),
    
       ---------------------------------------------------------------       
           
SUPUHT --UHT DANONE
AS (SELECT  pedc.CODSUPERVISOR,
            ped.codusur,
            prod.codsec,
            To_number(SUM(ped.qt*ped.pvenda)) as Fat
    FROM pontual.PCPEDI ped
        JOIN pontual.pcprodut prod on ped.codprod = prod.codprod
        JOIN pontual.pcpedc pedc on ped.NUMPED = pedc.NUMPED
    WHERE prod.codsec in (10046)
        AND ped.data BETWEEN '01-ago-2023' and '31-ago-2023' 
        AND ped.posicao NOT IN ('C')
        AND ped.vlbonific = 0
        AND NVL(ped.BONIFIC, 'N') =  'N'
        AND pedc.DTCANCEL IS NULL
        AND pedc.CONDVENDA IN (1, 2, 3, 7, 9, 14, 15, 17, 18, 19, 98)
        AND pedc.CODSUPERVISOR in (2,8,9)
    Group By ped.codusur,pedc.CODSUPERVISOR,prod.codsec
    ORDER By FAT DESC), 
    
       ---------------------------------------------------------------       
           
SUPREQ --REQUEIJÃO DANONE
AS (SELECT  pedc.CODSUPERVISOR,
            ped.codusur,
            prod.codsec,
            To_number(SUM(ped.qt*ped.pvenda)) as Fat
    FROM pontual.PCPEDI ped
        JOIN pontual.pcprodut prod on ped.codprod = prod.codprod
        JOIN pontual.pcpedc pedc on ped.NUMPED = pedc.NUMPED
    WHERE prod.codsec in (10047)
        AND ped.data BETWEEN '01-ago-2023' and '31-ago-2023' 
        AND ped.posicao NOT IN ('C')
        AND ped.vlbonific = 0
        AND NVL(ped.BONIFIC, 'N') =  'N'
        AND pedc.DTCANCEL IS NULL
        AND pedc.CONDVENDA IN (1, 2, 3, 7, 9, 14, 15, 17, 18, 19, 98)
        AND pedc.CODSUPERVISOR in (2,8,9)
    Group By ped.codusur,pedc.CODSUPERVISOR,prod.codsec
    ORDER By FAT DESC),    
    
       ---------------------------------------------------------------       
           
SUPYOP --YOPRO DANONE
AS (SELECT  pedc.CODSUPERVISOR,
            ped.codusur,
            prod.codsec,
            To_number(SUM(ped.qt*ped.pvenda)) as Fat
    FROM pontual.PCPEDI ped
        JOIN pontual.pcprodut prod on ped.codprod = prod.codprod
        JOIN pontual.pcpedc pedc on ped.NUMPED = pedc.NUMPED
    WHERE prod.codsec in (10048)
        AND ped.data BETWEEN '01-ago-2023' and '31-ago-2023' 
        AND ped.posicao NOT IN ('C')
        AND ped.vlbonific = 0
        AND NVL(ped.BONIFIC, 'N') =  'N'
        AND pedc.DTCANCEL IS NULL
        AND pedc.CONDVENDA IN (1, 2, 3, 7, 9, 14, 15, 17, 18, 19, 98)
        AND pedc.CODSUPERVISOR in (2,8,9)
    Group By ped.codusur,pedc.CODSUPERVISOR,prod.codsec
    ORDER By FAT DESC),       
          
--------------------------------------------------------------------------------
           
SUPSUL --SULMINAS
AS (SELECT  pedc.CODSUPERVISOR,
            ped.codusur,
            prod.codsec,
            To_number(SUM(ped.qt*ped.pvenda)) as Fat
    FROM pontual.PCPEDI ped
        JOIN pontual.pcprodut prod on ped.codprod = prod.codprod
        JOIN pontual.pcpedc pedc on ped.NUMPED = pedc.NUMPED
    WHERE prod.codsec in (10050)
        AND ped.data BETWEEN '01-ago-2023' and '31-ago-2023' 
        AND ped.posicao NOT IN ('C')
        AND ped.vlbonific = 0
        AND NVL(ped.BONIFIC, 'N') =  'N'
        AND pedc.DTCANCEL IS NULL
        AND pedc.CONDVENDA IN (1, 2, 3, 7, 9, 14, 15, 17, 18, 19, 98)
        AND pedc.CODSUPERVISOR in (2,8,9)
    Group By ped.codusur,pedc.CODSUPERVISOR,prod.codsec
    ORDER By FAT DESC),  
    
--------------------------------------------------------------------------------
           
SUPDCL --DOCILE
AS (SELECT  pedc.CODSUPERVISOR,
            ped.codusur,
            prod.codsec,
            To_number(SUM(ped.qt*ped.pvenda)) as Fat
    FROM pontual.PCPEDI ped
        JOIN pontual.pcprodut prod on ped.codprod = prod.codprod
        JOIN pontual.pcpedc pedc on ped.NUMPED = pedc.NUMPED
    WHERE prod.codsec in (120423)
        AND ped.data BETWEEN '01-ago-2023' and '31-ago-2023' 
        AND ped.posicao NOT IN ('C')
        AND ped.vlbonific = 0
        AND NVL(ped.BONIFIC, 'N') =  'N'
        AND pedc.DTCANCEL IS NULL
        AND pedc.CONDVENDA IN (1, 2, 3, 7, 9, 14, 15, 17, 18, 19, 98)
        AND pedc.CODSUPERVISOR in (2,8,9)
    Group By ped.codusur,pedc.CODSUPERVISOR,prod.codsec
    ORDER By FAT DESC),           
    
--------------------------------------------------------------------------------
           
SUPGUL --GULOSITOS
AS (SELECT  pedc.CODSUPERVISOR,
            ped.codusur,
            prod.codsec,
            To_number(SUM(ped.qt*ped.pvenda)) as Fat
    FROM pontual.PCPEDI ped
        JOIN pontual.pcprodut prod on ped.codprod = prod.codprod
        JOIN pontual.pcpedc pedc on ped.NUMPED = pedc.NUMPED
    WHERE prod.codsec in (10044)
        AND ped.data BETWEEN '01-ago-2023' and '31-ago-2023' 
        AND ped.posicao NOT IN ('C')
        AND ped.vlbonific = 0
        AND NVL(ped.BONIFIC, 'N') =  'N'
        AND pedc.DTCANCEL IS NULL
        AND pedc.CONDVENDA IN (1, 2, 3, 7, 9, 14, 15, 17, 18, 19, 98)
        AND pedc.CODSUPERVISOR in (2,8,9)
    Group By ped.codusur,pedc.CODSUPERVISOR,prod.codsec
    ORDER By FAT DESC),             
              
--------------------------------------------------------------------------------
           
SUPFLO --FLORESTAL
AS (SELECT  pedc.CODSUPERVISOR,
            ped.codusur,
            prod.codsec,
            To_number(SUM(ped.qt*ped.pvenda)) as Fat
    FROM pontual.PCPEDI ped
        JOIN pontual.pcprodut prod on ped.codprod = prod.codprod
        JOIN pontual.pcpedc pedc on ped.NUMPED = pedc.NUMPED
    WHERE prod.codsec in (10043)
        AND ped.data BETWEEN '01-ago-2023' and '31-ago-2023' 
        AND ped.posicao NOT IN ('C')
        AND ped.vlbonific = 0
        AND NVL(ped.BONIFIC, 'N') =  'N'
        AND pedc.DTCANCEL IS NULL
        AND pedc.CONDVENDA IN (1, 2, 3, 7, 9, 14, 15, 17, 18, 19, 98)
        AND pedc.CODSUPERVISOR in (2,8,9)
    Group By ped.codusur,pedc.CODSUPERVISOR,prod.codsec
    ORDER By FAT DESC),             
    
--------------------------------------------------------------------------------
           
SUPDFT --DAFRUTA
AS (SELECT  pedc.CODSUPERVISOR,
            ped.codusur,
            prod.codsec,
            To_number(SUM(ped.qt*ped.pvenda)) as Fat
    FROM pontual.PCPEDI ped
        JOIN pontual.pcprodut prod on ped.codprod = prod.codprod
        JOIN pontual.pcpedc pedc on ped.NUMPED = pedc.NUMPED
    WHERE prod.codsec in (120387)
        AND ped.data BETWEEN '01-ago-2023' and '31-ago-2023' 
        AND ped.posicao NOT IN ('C')
        AND ped.vlbonific = 0
        AND NVL(ped.BONIFIC, 'N') =  'N'
        AND pedc.DTCANCEL IS NULL
        AND pedc.CONDVENDA IN (1, 2, 3, 7, 9, 14, 15, 17, 18, 19, 98)
        AND pedc.CODSUPERVISOR in (2,8,9)
    Group By ped.codusur,pedc.CODSUPERVISOR,prod.codsec
    ORDER By FAT DESC),        
--------------------------------------------------------------------------------
           
SUPDNL --DANILLA
AS (SELECT  pedc.CODSUPERVISOR,
            ped.codusur,
            prod.codsec,
            To_number(SUM(ped.qt*ped.pvenda)) as Fat
    FROM pontual.PCPEDI ped
        JOIN pontual.pcprodut prod on ped.codprod = prod.codprod
        JOIN pontual.pcpedc pedc on ped.NUMPED = pedc.NUMPED
    WHERE prod.codsec in (120424)
        AND ped.data BETWEEN '01-ago-2023' and '31-ago-2023' 
        AND ped.posicao NOT IN ('C')
        AND ped.vlbonific = 0
        AND NVL(ped.BONIFIC, 'N') =  'N'
        AND pedc.DTCANCEL IS NULL
        AND pedc.CONDVENDA IN (1, 2, 3, 7, 9, 14, 15, 17, 18, 19, 98)
        AND pedc.CODSUPERVISOR in (2,8,9)
    Group By ped.codusur,pedc.CODSUPERVISOR,prod.codsec
    ORDER By FAT DESC),    
    
--------------------------------------------------------------------------------
           
SUPBVT --BIVOLT
AS (SELECT  pedc.CODSUPERVISOR,
            ped.codusur,
            prod.codsec,
            To_number(SUM(ped.qt*ped.pvenda)) as Fat
    FROM pontual.PCPEDI ped
        JOIN pontual.pcprodut prod on ped.codprod = prod.codprod
        JOIN pontual.pcpedc pedc on ped.NUMPED = pedc.NUMPED
    WHERE prod.codsec in (6004)
        AND ped.data BETWEEN '01-ago-2023' and '31-ago-2023' 
        AND ped.posicao NOT IN ('C')
        AND ped.vlbonific = 0
        AND NVL(ped.BONIFIC, 'N') =  'N'
        AND pedc.DTCANCEL IS NULL
        AND pedc.CONDVENDA IN (1, 2, 3, 7, 9, 14, 15, 17, 18, 19, 98)
        AND pedc.CODSUPERVISOR in (2,8,9)
    Group By ped.codusur,pedc.CODSUPERVISOR,prod.codsec
    ORDER By FAT DESC),        
     
--------------------------------------------------------------------------------
           
SUPSEA --SEARA MASSA LEVE
AS (SELECT  pedc.CODSUPERVISOR,
            ped.codusur,
            prod.codsec,
            To_number(SUM(ped.qt*ped.pvenda)) as Fat
    FROM pontual.PCPEDI ped
        JOIN pontual.pcprodut prod on ped.codprod = prod.codprod
        JOIN pontual.pcpedc pedc on ped.NUMPED = pedc.NUMPED
    WHERE prod.codsec in (10001)
        AND ped.data BETWEEN '01-ago-2023' and '31-ago-2023' 
        AND ped.posicao NOT IN ('C')
        AND ped.vlbonific = 0
        AND NVL(ped.BONIFIC, 'N') =  'N'
        AND pedc.DTCANCEL IS NULL
        AND pedc.CONDVENDA IN (1, 2, 3, 7, 9, 14, 15, 17, 18, 19, 98)
        AND pedc.CODSUPERVISOR in (2,8,9)
    Group By ped.codusur,pedc.CODSUPERVISOR,prod.codsec
    ORDER By FAT DESC),       
     
--------------------------------------------------------------------------------
           
SUPHYT --HYTS
AS (SELECT  pedc.CODSUPERVISOR,
            ped.codusur,
            prod.codsec,
            To_number(SUM(ped.qt*ped.pvenda)) as Fat
    FROM pontual.PCPEDI ped
        JOIN pontual.pcprodut prod on ped.codprod = prod.codprod
        JOIN pontual.pcpedc pedc on ped.NUMPED = pedc.NUMPED
    WHERE prod.codsec in (1005)
        AND ped.data BETWEEN '01-ago-2023' and '31-ago-2023' 
        AND ped.posicao NOT IN ('C')
        AND ped.vlbonific = 0
        AND NVL(ped.BONIFIC, 'N') =  'N'
        AND pedc.DTCANCEL IS NULL
        AND pedc.CONDVENDA IN (1, 2, 3, 7, 9, 14, 15, 17, 18, 19, 98)
        AND pedc.CODSUPERVISOR in (2,8,9)
    Group By ped.codusur,pedc.CODSUPERVISOR,prod.codsec
    ORDER By FAT DESC),     
     
--------------------------------------------------------------------------------
           
SUPSTM --SANTA MASSA
AS (SELECT  pedc.CODSUPERVISOR,
            ped.codusur,
            prod.codsec,
            To_number(SUM(ped.qt*ped.pvenda)) as Fat
    FROM pontual.PCPEDI ped
        JOIN pontual.pcprodut prod on ped.codprod = prod.codprod
        JOIN pontual.pcpedc pedc on ped.NUMPED = pedc.NUMPED
    WHERE prod.codsec in (1023)
        AND ped.data BETWEEN '01-ago-2023' and '31-ago-2023' 
        AND ped.posicao NOT IN ('C')
        AND ped.vlbonific = 0
        AND NVL(ped.BONIFIC, 'N') =  'N'
        AND pedc.DTCANCEL IS NULL
        AND pedc.CONDVENDA IN (1, 2, 3, 7, 9, 14, 15, 17, 18, 19, 98)
        AND pedc.CODSUPERVISOR in (2,8,9)
    Group By ped.codusur,pedc.CODSUPERVISOR,prod.codsec
    ORDER By FAT DESC),  
     
--------------------------------------------------------------------------------
           
SUPFTP --FRUTAP
AS (SELECT  pedc.CODSUPERVISOR,
            ped.codusur,
            prod.codsec,
            To_number(SUM(ped.qt*ped.pvenda)) as Fat
    FROM pontual.PCPEDI ped
        JOIN pontual.pcprodut prod on ped.codprod = prod.codprod
        JOIN pontual.pcpedc pedc on ped.NUMPED = pedc.NUMPED
    WHERE prod.codsec in (10041)
        AND ped.data BETWEEN '01-ago-2023' and '31-ago-2023' 
        AND ped.posicao NOT IN ('C')
        AND ped.vlbonific = 0
        AND NVL(ped.BONIFIC, 'N') =  'N'
        AND pedc.DTCANCEL IS NULL
        AND pedc.CONDVENDA IN (1, 2, 3, 7, 9, 14, 15, 17, 18, 19, 98)
        AND pedc.CODSUPERVISOR in (2,8,9)
    Group By ped.codusur,pedc.CODSUPERVISOR,prod.codsec
    ORDER By FAT DESC),  
     
--------------------------------------------------------------------------------
           
SUPMGN --MARGARINA
AS (SELECT  pedc.CODSUPERVISOR,
            ped.codusur,
            prod.codsec,
            To_number(SUM(ped.qt*ped.pvenda)) as Fat
    FROM pontual.PCPEDI ped
        JOIN pontual.pcprodut prod on ped.codprod = prod.codprod
        JOIN pontual.pcpedc pedc on ped.NUMPED = pedc.NUMPED
    WHERE prod.codsec in (1003)
        AND ped.data BETWEEN '01-ago-2023' and '31-ago-2023' 
        AND ped.posicao NOT IN ('C')
        AND ped.vlbonific = 0
        AND NVL(ped.BONIFIC, 'N') =  'N'
        AND pedc.DTCANCEL IS NULL
        AND pedc.CONDVENDA IN (1, 2, 3, 7, 9, 14, 15, 17, 18, 19, 98)
        AND pedc.CODSUPERVISOR in (2,8,9)
    Group By ped.codusur,pedc.CODSUPERVISOR,prod.codsec
    ORDER By FAT DESC),  
                                                                                     
------------------------------------------META---------------------------------------------------    
META -- (Essa CTE obtem os valores da meta dos vendedores - que posteriormente é somado para a obtenção dos valores por vendedor)
AS (
SELECT d.CODSUPERVISOR CODSUPERVISOR,
       m.codusur, m.codigo CODSEC,
       NVL((CASE WHEN m.cliposprev IS NULL or m.cliposprev = 0 THEN 500 
       ELSE m.cliposprev END),100) AS cliposprev
FROM pontual.PCMETA M 
JOIN pontual.PCUSUARI C ON M.CODUSUR = C.CODUSUR
JOIN pontual.PCSUPERV D ON C.CODSUPERVISOR = D.CODSUPERVISOR
JOIN pontual.PCSECAO E ON M.CODIGO = E.CODSEC
WHERE M.data = '01-Ago-2023' --'{DATAI}'
AND M.TIPOMETA = 'S'
AND E.CODSEC IN (10040,1003,10042,10048,120239,10050,10047,10046,120423,10044,10043,120387,120424,6004,10001,1005,1023,10041,1003)
AND d.CODSUPERVISOR IN (2,8,9)
),
-------------------------------------------------------------------------------------------------

DIAS AS -- Essa CTE foi usada para definir valores manuais referentes a quantidade de dias úteis no mês e quantos dias foram percorridos
(SELECT 24 as DIASUTEIS, 22 AS DIASDECORR FROM DUAL) -- A tabela 'DUAL' é uma tabela especial de uma linha e uma coluna presente por padrão no Oracle. É adequado para uso na seleção de uma pseudocoluna.

---------------------------------CONSULTAS PRINCIPAIS--------------------------------------------

-----------------------------------------PLF-----------------------------------------------------
SELECT 0 AS "ORDER", -- Pseudocoluna criada para fazer a ordenação das linhas
       'PLF' as CATEGORIA,
    -------------------------------------------------------------------
       to_number((SELECT SUM(m.cliposprev)
            from META m 
            WHERE M.codsec in (10040,10042,120239) 
            AND m.CODSUPERVISOR = a.CODSUPERVISOR)) AS OBJETIVO,
    -------------------------------------------------------------------
       to_number(SUM(A.fat)) AS Realizado,
    -------------------------------------------------------------------
       to_number(TRUNC((SUM(A.FAT) / (SELECT SUM(m.cliposprev)
            from META m 
            WHERE M.codsec in (10040,10042,120239) 
            AND m.CODSUPERVISOR = a.CODSUPERVISOR)),5))
            as "% ATING.",
    -------------------------------------------------------------------
       to_number(TRUNC((
       ((SUM(A.fat) / d.DIASDECORR)   *   (d.DIASuteis))    
                    /    (SELECT SUM(m.cliposprev)
                                from META m 
                                WHERE M.codsec in (10040,10042,120239) 
                                AND m.CODSUPERVISOR = a.CODSUPERVISOR)
        ),5)) AS "% TEND.",
    -------------------------------------------------------------------    
        to_number(GREATEST(TRUNC((
        ((SELECT SUM(m.cliposprev)
            from META m 
            WHERE M.codsec in (10040,10042,120239) 
            AND m.CODSUPERVISOR = a.CODSUPERVISOR)) - SUM(A.fat) 
            
         ),2),0))   as "R.A.F.",
    -------------------------------------------------------------------  
         to_number(GREATEST(( 
         ((SELECT SUM(m.cliposprev)
            from META m 
            WHERE M.codsec in (10040,10042,120239) 
            AND m.CODSUPERVISOR = a.CODSUPERVISOR) - SUM(A.fat)) 
            / (D.DIASUTEIS - D.diasdecorr) 
         ),0)) as "NECECIDADE DIA",
    -------------------------------------------------------------------    
        to_number(TRUNC((SUM(A.fat) / D.DIASDECORR),2)) AS "MEDIA DIA",
    ------------------------------------------------------------------- 
        (CASE WHEN (TRUNC(((SUM(A.FAT) / D.DIASDECORR) * D.DIASUTEIS) /
          (SELECT SUM(m.cliposprev)
            from META m 
            WHERE M.codsec in (10040,10042,120239) 
            AND m.CODSUPERVISOR = a.CODSUPERVISOR) * 100,1)) >= 100
            THEN (SELECT UNISTR('\2191')||UNISTR('\2191')||UNISTR('\2191') FROM dual) 
            ELSE (SELECT UNISTR('\2193')||UNISTR('\2193')||UNISTR('\2193') FROM dual) 
            END) AS STATUS
    -------------------------------------------------------------------              
              
FROM SUPPLF A, DIAS d
WHERE a.CODSUPERVISOR = 2
GROUP BY a.CODSUPERVISOR,d.DIASDECORR,d.DIASuteis


---------------------------------------ACTIVIA---------------------------------------------------
UNION
SELECT 1.0 AS "ORDER",
       '¬ Activia' as CATEGORIA,
    -------------------------------------------------------------------
    NVL((SELECT SUM(m.cliposprev)
            from META m 
            WHERE M.codsec in (a.codsec) 
            AND m.CODSUPERVISOR = a.CODSUPERVISOR),1) AS OBJETIVO,
    -------------------------------------------------------------------
       SUM(A.fat) AS Realizado,
    -------------------------------------------------------------------
       TRUNC((SUM(A.FAT) / NVL((SELECT SUM(m.cliposprev)
            from META m 
            WHERE M.codsec in (a.codsec) 
            AND m.CODSUPERVISOR = a.CODSUPERVISOR),1)),5) as "ATING.",
    -------------------------------------------------------------------
       TRUNC((
       ((SUM(A.fat) / d.DIASDECORR)   *   (d.DIASuteis))    
                    /    NVL((SELECT SUM(m.cliposprev)
                                from META m 
                                WHERE M.codsec in (a.codsec) 
                                AND m.CODSUPERVISOR = a.CODSUPERVISOR),1)
        ),5) AS "% TEND.",
    -------------------------------------------------------------------    
        GREATEST(TRUNC((
        (NVL((SELECT SUM(m.cliposprev)
            from META m 
            WHERE M.codsec in (a.codsec) 
            AND m.CODSUPERVISOR = a.CODSUPERVISOR),1)) - SUM(A.fat) 
            
         ),2),0)   as "R.A.F.",
    -------------------------------------------------------------------  
         GREATEST(( 
         (nvl((SELECT SUM(m.cliposprev)
            from META m 
            WHERE M.codsec in (a.codsec) 
            AND m.CODSUPERVISOR = a.CODSUPERVISOR),1) - SUM(A.fat)) 
            / (D.DIASUTEIS - D.diasdecorr) 
         ),0) as "NECECIDADE DIA",
    -------------------------------------------------------------------    
        to_number(TRUNC((SUM(A.fat) / D.DIASDECORR),2)) AS "MEDIA DIA",
    ------------------------------------------------------------------- 
        (CASE WHEN (TRUNC(((SUM(A.FAT) / D.DIASDECORR) * D.DIASUTEIS) /
          NVL((SELECT SUM(m.cliposprev)
            from META m 
            WHERE M.codsec in (a.codsec) 
            AND m.CODSUPERVISOR = a.CODSUPERVISOR),1) * 100,1)) >= 100
            THEN (SELECT UNISTR('\2191')||UNISTR('\2191')||UNISTR('\2191') FROM dual) 
            ELSE (SELECT UNISTR('\2193')||UNISTR('\2193')||UNISTR('\2193') FROM dual) 
            END) AS STATUS
    -------------------------------------------------------------------               
              
FROM SUPACT A, DIAS d
WHERE a.CODSUPERVISOR = 2
GROUP BY a.CODSUPERVISOR,d.DIASDECORR,d.DIASuteis,a.codsec


--------------------------------------DANONINHO--------------------------------------------------
UNION
SELECT 1.1 AS "ORDER",
       '¬ Danoninho' as CATEGORIA,
    -------------------------------------------------------------------
    NVL((SELECT SUM(m.cliposprev)
            from META m 
            WHERE M.codsec in (a.codsec) 
            AND m.CODSUPERVISOR = a.CODSUPERVISOR),1) AS OBJETIVO,
    -------------------------------------------------------------------
       SUM(A.fat) AS Realizado,
    -------------------------------------------------------------------
       TRUNC((SUM(A.FAT) / NVL((SELECT SUM(m.cliposprev)
            from META m 
            WHERE M.codsec in (a.codsec) 
            AND m.CODSUPERVISOR = a.CODSUPERVISOR),1)),5) as "ATING.",
    -------------------------------------------------------------------
       TRUNC((
       ((SUM(A.fat) / d.DIASDECORR)   *   (d.DIASuteis))    
                    /    NVL((SELECT SUM(m.cliposprev)
                                from META m 
                                WHERE M.codsec in (a.codsec) 
                                AND m.CODSUPERVISOR = a.CODSUPERVISOR),1)
        ),5) AS "% TEND.",
    -------------------------------------------------------------------    
        GREATEST(TRUNC((
        (NVL((SELECT SUM(m.cliposprev)
            from META m 
            WHERE M.codsec in (a.codsec) 
            AND m.CODSUPERVISOR = a.CODSUPERVISOR),1)) - SUM(A.fat) 
            
         ),2),0)   as "R.A.F.",
    -------------------------------------------------------------------  
         GREATEST(( 
         (nvl((SELECT SUM(m.cliposprev)
            from META m 
            WHERE M.codsec in (a.codsec) 
            AND m.CODSUPERVISOR = a.CODSUPERVISOR),1) - SUM(A.fat)) 
            / (D.DIASUTEIS - D.diasdecorr) 
         ),0) as "NECECIDADE DIA",
    -------------------------------------------------------------------    
        to_number(TRUNC((SUM(A.fat) / D.DIASDECORR),2)) AS "MEDIA DIA",
    ------------------------------------------------------------------- 
        (CASE WHEN (TRUNC(((SUM(A.FAT) / D.DIASDECORR) * D.DIASUTEIS) /
          NVL((SELECT SUM(m.cliposprev)
            from META m 
            WHERE M.codsec in (a.codsec) 
            AND m.CODSUPERVISOR = a.CODSUPERVISOR),1) * 100,1)) >= 100
            THEN (SELECT UNISTR('\2191')||UNISTR('\2191')||UNISTR('\2191') FROM dual) 
            ELSE (SELECT UNISTR('\2193')||UNISTR('\2193')||UNISTR('\2193') FROM dual) 
            END) AS STATUS
    -------------------------------------------------------------------                 
              
FROM SUPDHO A, DIAS d
WHERE a.CODSUPERVISOR = 2
GROUP BY a.CODSUPERVISOR,d.DIASDECORR,d.DIASuteis,a.codsec


---------------------------------------GRANADA---------------------------------------------------
UNION
SELECT 1.2 AS "ORDER",
       '¬ Granada' as CATEGORIA, 
    -------------------------------------------------------------------
    NVL((SELECT SUM(m.cliposprev)
            from META m 
            WHERE M.codsec in (a.codsec) 
            AND m.CODSUPERVISOR = a.CODSUPERVISOR),1) AS OBJETIVO,
    -------------------------------------------------------------------
       SUM(A.fat) AS Realizado,
    -------------------------------------------------------------------
       TRUNC((SUM(A.FAT) / NVL((SELECT SUM(m.cliposprev)
            from META m 
            WHERE M.codsec in (a.codsec) 
            AND m.CODSUPERVISOR = a.CODSUPERVISOR),1)),5) as "ATING.",
    -------------------------------------------------------------------
       TRUNC((
       ((SUM(A.fat) / d.DIASDECORR)   *   (d.DIASuteis))    
                    /    NVL((SELECT SUM(m.cliposprev)
                                from META m 
                                WHERE M.codsec in (a.codsec) 
                                AND m.CODSUPERVISOR = a.CODSUPERVISOR),1)
        ),5) AS "% TEND.",
    -------------------------------------------------------------------    
        GREATEST(TRUNC((
        (NVL((SELECT SUM(m.cliposprev)
            from META m 
            WHERE M.codsec in (a.codsec) 
            AND m.CODSUPERVISOR = a.CODSUPERVISOR),1)) - SUM(A.fat) 
            
         ),2),0)   as "R.A.F.",
    -------------------------------------------------------------------  
         GREATEST(( 
         (nvl((SELECT SUM(m.cliposprev)
            from META m 
            WHERE M.codsec in (a.codsec) 
            AND m.CODSUPERVISOR = a.CODSUPERVISOR),1) - SUM(A.fat)) 
            / (D.DIASUTEIS - D.diasdecorr) 
         ),0) as "NECECIDADE DIA",
    -------------------------------------------------------------------    
        to_number(TRUNC((SUM(A.fat) / D.DIASDECORR),2)) AS "MEDIA DIA",
    ------------------------------------------------------------------- 
        (CASE WHEN (TRUNC(((SUM(A.FAT) / D.DIASDECORR) * D.DIASUTEIS) /
          NVL((SELECT SUM(m.cliposprev)
            from META m 
            WHERE M.codsec in (a.codsec) 
            AND m.CODSUPERVISOR = a.CODSUPERVISOR),1) * 100,1)) >= 100
            THEN (SELECT UNISTR('\2191')||UNISTR('\2191')||UNISTR('\2191') FROM dual) 
            ELSE (SELECT UNISTR('\2193')||UNISTR('\2193')||UNISTR('\2193') FROM dual) 
            END) AS STATUS
    -------------------------------------------------------------------            
              
FROM SUPGRA A, DIAS d
WHERE a.CODSUPERVISOR = 2
GROUP BY a.CODSUPERVISOR,d.DIASDECORR,d.DIASuteis,a.codsec

-----------------------------------------UHT-----------------------------------------------------
UNION
SELECT 1.3 AS "ORDER",
       'UHT' as CATEGORIA, 
    -------------------------------------------------------------------
    NVL((SELECT SUM(m.cliposprev)
            from META m 
            WHERE M.codsec in (a.codsec) 
            AND m.CODSUPERVISOR = a.CODSUPERVISOR),1) AS OBJETIVO,
    -------------------------------------------------------------------
       SUM(A.fat) AS Realizado,
    -------------------------------------------------------------------
       TRUNC((SUM(A.FAT) / NVL((SELECT SUM(m.cliposprev)
            from META m 
            WHERE M.codsec in (a.codsec) 
            AND m.CODSUPERVISOR = a.CODSUPERVISOR),1)),5) as "ATING.",
    -------------------------------------------------------------------
       TRUNC((
       ((SUM(A.fat) / d.DIASDECORR)   *   (d.DIASuteis))    
                    /    NVL((SELECT SUM(m.cliposprev)
                                from META m 
                                WHERE M.codsec in (a.codsec) 
                                AND m.CODSUPERVISOR = a.CODSUPERVISOR),1)
        ),5) AS "% TEND.",
    -------------------------------------------------------------------    
        GREATEST(TRUNC((
        (NVL((SELECT SUM(m.cliposprev)
            from META m 
            WHERE M.codsec in (a.codsec) 
            AND m.CODSUPERVISOR = a.CODSUPERVISOR),1)) - SUM(A.fat) 
            
         ),2),0)   as "R.A.F.",
    -------------------------------------------------------------------  
         GREATEST(( 
         (nvl((SELECT SUM(m.cliposprev)
            from META m 
            WHERE M.codsec in (a.codsec) 
            AND m.CODSUPERVISOR = a.CODSUPERVISOR),1) - SUM(A.fat)) 
            / (D.DIASUTEIS - D.diasdecorr) 
         ),0) as "NECECIDADE DIA",
    -------------------------------------------------------------------    
        to_number(TRUNC((SUM(A.fat) / D.DIASDECORR),2)) AS "MEDIA DIA",
    ------------------------------------------------------------------- 
        (CASE WHEN (TRUNC(((SUM(A.FAT) / D.DIASDECORR) * D.DIASUTEIS) /
          NVL((SELECT SUM(m.cliposprev)
            from META m 
            WHERE M.codsec in (a.codsec) 
            AND m.CODSUPERVISOR = a.CODSUPERVISOR),1) * 100,1)) >= 100
            THEN (SELECT UNISTR('\2191')||UNISTR('\2191')||UNISTR('\2191') FROM dual) 
            ELSE (SELECT UNISTR('\2193')||UNISTR('\2193')||UNISTR('\2193') FROM dual) 
            END) AS STATUS
    -------------------------------------------------------------------                 
              
FROM SUPUHT A, DIAS d
WHERE a.CODSUPERVISOR = 2
GROUP BY a.CODSUPERVISOR,d.DIASDECORR,d.DIASuteis,a.codsec

----------------------------------------REQUEIJÃO------------------------------------------------
UNION
SELECT 1.4 AS "ORDER",
       'REQUEIJÃO' as CATEGORIA, 
    -------------------------------------------------------------------
    NVL((SELECT SUM(m.cliposprev)
            from META m 
            WHERE M.codsec in (a.codsec) 
            AND m.CODSUPERVISOR = a.CODSUPERVISOR),1) AS OBJETIVO,
    -------------------------------------------------------------------
       SUM(A.fat) AS Realizado,
    -------------------------------------------------------------------
       TRUNC((SUM(A.FAT) / NVL((SELECT SUM(m.cliposprev)
            from META m 
            WHERE M.codsec in (a.codsec) 
            AND m.CODSUPERVISOR = a.CODSUPERVISOR),1)),5) as "ATING.",
    -------------------------------------------------------------------
       TRUNC((
       ((SUM(A.fat) / d.DIASDECORR)   *   (d.DIASuteis))    
                    /    NVL((SELECT SUM(m.cliposprev)
                                from META m 
                                WHERE M.codsec in (a.codsec) 
                                AND m.CODSUPERVISOR = a.CODSUPERVISOR),1)
        ),5) AS "% TEND.",
    -------------------------------------------------------------------    
        GREATEST(TRUNC((
        (NVL((SELECT SUM(m.cliposprev)
            from META m 
            WHERE M.codsec in (a.codsec) 
            AND m.CODSUPERVISOR = a.CODSUPERVISOR),1)) - SUM(A.fat) 
            
         ),2),0)   as "R.A.F.",
    -------------------------------------------------------------------  
         GREATEST(( 
         (nvl((SELECT SUM(m.cliposprev)
            from META m 
            WHERE M.codsec in (a.codsec) 
            AND m.CODSUPERVISOR = a.CODSUPERVISOR),1) - SUM(A.fat)) 
            / (D.DIASUTEIS - D.diasdecorr) 
         ),0) as "NECECIDADE DIA",
    -------------------------------------------------------------------    
        to_number(TRUNC((SUM(A.fat) / D.DIASDECORR),2)) AS "MEDIA DIA",
    ------------------------------------------------------------------- 
        (CASE WHEN (TRUNC(((SUM(A.FAT) / D.DIASDECORR) * D.DIASUTEIS) /
          NVL((SELECT SUM(m.cliposprev)
            from META m 
            WHERE M.codsec in (a.codsec) 
            AND m.CODSUPERVISOR = a.CODSUPERVISOR),1) * 100,1)) >= 100
            THEN (SELECT UNISTR('\2191')||UNISTR('\2191')||UNISTR('\2191') FROM dual) 
            ELSE (SELECT UNISTR('\2193')||UNISTR('\2193')||UNISTR('\2193') FROM dual) 
            END) AS STATUS
    -------------------------------------------------------------------                 
              
FROM SUPREQ A, DIAS d
WHERE a.CODSUPERVISOR = 2
GROUP BY a.CODSUPERVISOR,d.DIASDECORR,d.DIASuteis,a.codsec

-------------------------------------------YOPRO-------------------------------------------------
UNION
SELECT 1.5 AS "ORDER",
       'YOPRO' as CATEGORIA, 
    -------------------------------------------------------------------
    NVL((SELECT SUM(m.cliposprev)
            from META m 
            WHERE M.codsec in (a.codsec) 
            AND m.CODSUPERVISOR = a.CODSUPERVISOR),1) AS OBJETIVO,
    -------------------------------------------------------------------
       SUM(A.fat) AS Realizado,
    -------------------------------------------------------------------
       TRUNC((SUM(A.FAT) / NVL((SELECT SUM(m.cliposprev)
            from META m 
            WHERE M.codsec in (a.codsec) 
            AND m.CODSUPERVISOR = a.CODSUPERVISOR),1)),5) as "ATING.",
    -------------------------------------------------------------------
       TRUNC((
       ((SUM(A.fat) / d.DIASDECORR)   *   (d.DIASuteis))    
                    /    NVL((SELECT SUM(m.cliposprev)
                                from META m 
                                WHERE M.codsec in (a.codsec) 
                                AND m.CODSUPERVISOR = a.CODSUPERVISOR),1)
        ),5) AS "% TEND.",
    -------------------------------------------------------------------    
        GREATEST(TRUNC((
        (NVL((SELECT SUM(m.cliposprev)
            from META m 
            WHERE M.codsec in (a.codsec) 
            AND m.CODSUPERVISOR = a.CODSUPERVISOR),1)) - SUM(A.fat) 
            
         ),2),0)   as "R.A.F.",
    -------------------------------------------------------------------  
         GREATEST(( 
         (nvl((SELECT SUM(m.cliposprev)
            from META m 
            WHERE M.codsec in (a.codsec) 
            AND m.CODSUPERVISOR = a.CODSUPERVISOR),1) - SUM(A.fat)) 
            / (D.DIASUTEIS - D.diasdecorr) 
         ),0) as "NECECIDADE DIA",
    -------------------------------------------------------------------    
        to_number(TRUNC((SUM(A.fat) / D.DIASDECORR),2)) AS "MEDIA DIA",
    ------------------------------------------------------------------- 
        (CASE WHEN (TRUNC(((SUM(A.FAT) / D.DIASDECORR) * D.DIASUTEIS) /
          NVL((SELECT SUM(m.cliposprev)
            from META m 
            WHERE M.codsec in (a.codsec) 
            AND m.CODSUPERVISOR = a.CODSUPERVISOR),1) * 100,1)) >= 100
            THEN (SELECT UNISTR('\2191')||UNISTR('\2191')||UNISTR('\2191') FROM dual) 
            ELSE (SELECT UNISTR('\2193')||UNISTR('\2193')||UNISTR('\2193') FROM dual) 
            END) AS STATUS
    -------------------------------------------------------------------              
              
FROM SUPYOP A, DIAS d
WHERE a.CODSUPERVISOR = 2
GROUP BY a.CODSUPERVISOR,d.DIASDECORR,d.DIASuteis,a.codsec

----------------------------------------SULMINAS-------------------------------------------------
UNION
SELECT 2 AS "ORDER",
       'SULMINAS' as CATEGORIA, 
    -------------------------------------------------------------------
    NVL((SELECT SUM(m.cliposprev)
            from META m 
            WHERE M.codsec in (a.codsec) 
            AND m.CODSUPERVISOR = a.CODSUPERVISOR),1) AS OBJETIVO,
    -------------------------------------------------------------------
       SUM(A.fat) AS Realizado,
    -------------------------------------------------------------------
       TRUNC((SUM(A.FAT) / NVL((SELECT SUM(m.cliposprev)
            from META m 
            WHERE M.codsec in (a.codsec) 
            AND m.CODSUPERVISOR = a.CODSUPERVISOR),1)),5) as "ATING.",
    -------------------------------------------------------------------
       TRUNC((
       ((SUM(A.fat) / d.DIASDECORR)   *   (d.DIASuteis))    
                    /    NVL((SELECT SUM(m.cliposprev)
                                from META m 
                                WHERE M.codsec in (a.codsec) 
                                AND m.CODSUPERVISOR = a.CODSUPERVISOR),1)
        ),5) AS "% TEND.",
    -------------------------------------------------------------------    
        GREATEST(TRUNC((
        (NVL((SELECT SUM(m.cliposprev)
            from META m 
            WHERE M.codsec in (a.codsec) 
            AND m.CODSUPERVISOR = a.CODSUPERVISOR),1)) - SUM(A.fat) 
            
         ),2),0)   as "R.A.F.",
    -------------------------------------------------------------------  
         GREATEST(( 
         (nvl((SELECT SUM(m.cliposprev)
            from META m 
            WHERE M.codsec in (a.codsec) 
            AND m.CODSUPERVISOR = a.CODSUPERVISOR),1) - SUM(A.fat)) 
            / (D.DIASUTEIS - D.diasdecorr) 
         ),0) as "NECECIDADE DIA",
    -------------------------------------------------------------------    
        to_number(TRUNC((SUM(A.fat) / D.DIASDECORR),2)) AS "MEDIA DIA",
    ------------------------------------------------------------------- 
        (CASE WHEN (TRUNC(((SUM(A.FAT) / D.DIASDECORR) * D.DIASUTEIS) /
          NVL((SELECT SUM(m.cliposprev)
            from META m 
            WHERE M.codsec in (a.codsec) 
            AND m.CODSUPERVISOR = a.CODSUPERVISOR),1) * 100,1)) >= 100
            THEN (SELECT UNISTR('\2191')||UNISTR('\2191')||UNISTR('\2191') FROM dual) 
            ELSE (SELECT UNISTR('\2193')||UNISTR('\2193')||UNISTR('\2193') FROM dual) 
            END) AS STATUS
    -------------------------------------------------------------------              
              
FROM SUPSUL A, DIAS d
WHERE a.CODSUPERVISOR = 2
GROUP BY a.CODSUPERVISOR,d.DIASDECORR,d.DIASuteis,a.codsec

----------------------------------------DOCILE--------------------------------------------
UNION
SELECT 2 AS "ORDER",
       'DOCILE' as CATEGORIA, 
    -------------------------------------------------------------------
    NVL((SELECT SUM(m.cliposprev)
            from META m 
            WHERE M.codsec in (a.codsec) 
            AND m.CODSUPERVISOR = a.CODSUPERVISOR),1) AS OBJETIVO,
    -------------------------------------------------------------------
       SUM(A.fat) AS Realizado,
    -------------------------------------------------------------------
       TRUNC((SUM(A.FAT) / NVL((SELECT SUM(m.cliposprev)
            from META m 
            WHERE M.codsec in (a.codsec) 
            AND m.CODSUPERVISOR = a.CODSUPERVISOR),1)),5) as "ATING.",
    -------------------------------------------------------------------
       TRUNC((
       ((SUM(A.fat) / d.DIASDECORR)   *   (d.DIASuteis))    
                    /    NVL((SELECT SUM(m.cliposprev)
                                from META m 
                                WHERE M.codsec in (a.codsec) 
                                AND m.CODSUPERVISOR = a.CODSUPERVISOR),1)
        ),5) AS "% TEND.",
    -------------------------------------------------------------------    
        GREATEST(TRUNC((
        (NVL((SELECT SUM(m.cliposprev)
            from META m 
            WHERE M.codsec in (a.codsec) 
            AND m.CODSUPERVISOR = a.CODSUPERVISOR),1)) - SUM(A.fat) 
            
         ),2),0)   as "R.A.F.",
    -------------------------------------------------------------------  
         GREATEST(( 
         (nvl((SELECT SUM(m.cliposprev)
            from META m 
            WHERE M.codsec in (a.codsec) 
            AND m.CODSUPERVISOR = a.CODSUPERVISOR),1) - SUM(A.fat)) 
            / (D.DIASUTEIS - D.diasdecorr) 
         ),0) as "NECECIDADE DIA",
    -------------------------------------------------------------------    
        to_number(TRUNC((SUM(A.fat) / D.DIASDECORR),2)) AS "MEDIA DIA",
    ------------------------------------------------------------------- 
        (CASE WHEN (TRUNC(((SUM(A.FAT) / D.DIASDECORR) * D.DIASUTEIS) /
          NVL((SELECT SUM(m.cliposprev)
            from META m 
            WHERE M.codsec in (a.codsec) 
            AND m.CODSUPERVISOR = a.CODSUPERVISOR),1) * 100,1)) >= 100
            THEN (SELECT UNISTR('\2191')||UNISTR('\2191')||UNISTR('\2191') FROM dual) 
            ELSE (SELECT UNISTR('\2193')||UNISTR('\2193')||UNISTR('\2193') FROM dual) 
            END) AS STATUS
    -------------------------------------------------------------------              
              
FROM SUPDCL A, DIAS d
WHERE a.CODSUPERVISOR = 2
GROUP BY a.CODSUPERVISOR,d.DIASDECORR,d.DIASuteis,a.codsec

----------------------------------------DOCILE--------------------------------------------
UNION
SELECT 2 AS "ORDER",
       'GULOSITOS' as CATEGORIA, 
    -------------------------------------------------------------------
    NVL((SELECT SUM(m.cliposprev)
            from META m 
            WHERE M.codsec in (a.codsec) 
            AND m.CODSUPERVISOR = a.CODSUPERVISOR),1) AS OBJETIVO,
    -------------------------------------------------------------------
       SUM(A.fat) AS Realizado,
    -------------------------------------------------------------------
       TRUNC((SUM(A.FAT) / NVL((SELECT SUM(m.cliposprev)
            from META m 
            WHERE M.codsec in (a.codsec) 
            AND m.CODSUPERVISOR = a.CODSUPERVISOR),1)),5) as "ATING.",
    -------------------------------------------------------------------
       TRUNC((
       ((SUM(A.fat) / d.DIASDECORR)   *   (d.DIASuteis))    
                    /    NVL((SELECT SUM(m.cliposprev)
                                from META m 
                                WHERE M.codsec in (a.codsec) 
                                AND m.CODSUPERVISOR = a.CODSUPERVISOR),1)
        ),5) AS "% TEND.",
    -------------------------------------------------------------------    
        GREATEST(TRUNC((
        (NVL((SELECT SUM(m.cliposprev)
            from META m 
            WHERE M.codsec in (a.codsec) 
            AND m.CODSUPERVISOR = a.CODSUPERVISOR),1)) - SUM(A.fat) 
            
         ),2),0)   as "R.A.F.",
    -------------------------------------------------------------------  
         GREATEST(( 
         (nvl((SELECT SUM(m.cliposprev)
            from META m 
            WHERE M.codsec in (a.codsec) 
            AND m.CODSUPERVISOR = a.CODSUPERVISOR),1) - SUM(A.fat)) 
            / (D.DIASUTEIS - D.diasdecorr) 
         ),0) as "NECECIDADE DIA",
    -------------------------------------------------------------------    
        to_number(TRUNC((SUM(A.fat) / D.DIASDECORR),2)) AS "MEDIA DIA",
    ------------------------------------------------------------------- 
        (CASE WHEN (TRUNC(((SUM(A.FAT) / D.DIASDECORR) * D.DIASUTEIS) /
          NVL((SELECT SUM(m.cliposprev)
            from META m 
            WHERE M.codsec in (a.codsec) 
            AND m.CODSUPERVISOR = a.CODSUPERVISOR),1) * 100,1)) >= 100
            THEN (SELECT UNISTR('\2191')||UNISTR('\2191')||UNISTR('\2191') FROM dual) 
            ELSE (SELECT UNISTR('\2193')||UNISTR('\2193')||UNISTR('\2193') FROM dual) 
            END) AS STATUS
    -------------------------------------------------------------------              
              
FROM SUPGUL A, DIAS d
WHERE a.CODSUPERVISOR = 2
GROUP BY a.CODSUPERVISOR,d.DIASDECORR,d.DIASuteis,a.codsec

---------------------------------------FLORESTAL-----------------------------------------
UNION
SELECT 2 AS "ORDER",
       'FLORESTAL' as CATEGORIA, 
    -------------------------------------------------------------------
    NVL((SELECT SUM(m.cliposprev)
            from META m 
            WHERE M.codsec in (a.codsec) 
            AND m.CODSUPERVISOR = a.CODSUPERVISOR),1) AS OBJETIVO,
    -------------------------------------------------------------------
       SUM(A.fat) AS Realizado,
    -------------------------------------------------------------------
       TRUNC((SUM(A.FAT) / NVL((SELECT SUM(m.cliposprev)
            from META m 
            WHERE M.codsec in (a.codsec) 
            AND m.CODSUPERVISOR = a.CODSUPERVISOR),1)),5) as "ATING.",
    -------------------------------------------------------------------
       TRUNC((
       ((SUM(A.fat) / d.DIASDECORR)   *   (d.DIASuteis))    
                    /    NVL((SELECT SUM(m.cliposprev)
                                from META m 
                                WHERE M.codsec in (a.codsec) 
                                AND m.CODSUPERVISOR = a.CODSUPERVISOR),1)
        ),5) AS "% TEND.",
    -------------------------------------------------------------------    
        GREATEST(TRUNC((
        (NVL((SELECT SUM(m.cliposprev)
            from META m 
            WHERE M.codsec in (a.codsec) 
            AND m.CODSUPERVISOR = a.CODSUPERVISOR),1)) - SUM(A.fat) 
            
         ),2),0)   as "R.A.F.",
    -------------------------------------------------------------------  
         GREATEST(( 
         (nvl((SELECT SUM(m.cliposprev)
            from META m 
            WHERE M.codsec in (a.codsec) 
            AND m.CODSUPERVISOR = a.CODSUPERVISOR),1) - SUM(A.fat)) 
            / (D.DIASUTEIS - D.diasdecorr) 
         ),0) as "NECECIDADE DIA",
    -------------------------------------------------------------------    
        to_number(TRUNC((SUM(A.fat) / D.DIASDECORR),2)) AS "MEDIA DIA",
    ------------------------------------------------------------------- 
        (CASE WHEN (TRUNC(((SUM(A.FAT) / D.DIASDECORR) * D.DIASUTEIS) /
          NVL((SELECT SUM(m.cliposprev)
            from META m 
            WHERE M.codsec in (a.codsec) 
            AND m.CODSUPERVISOR = a.CODSUPERVISOR),1) * 100,1)) >= 100
            THEN (SELECT UNISTR('\2191')||UNISTR('\2191')||UNISTR('\2191') FROM dual) 
            ELSE (SELECT UNISTR('\2193')||UNISTR('\2193')||UNISTR('\2193') FROM dual) 
            END) AS STATUS
    -------------------------------------------------------------------              
              
FROM SUPFLO A, DIAS d
WHERE a.CODSUPERVISOR = 2
GROUP BY a.CODSUPERVISOR,d.DIASDECORR,d.DIASuteis,a.codsec

---------------------------------------DAFRUTA-----------------------------------------
UNION
SELECT 2 AS "ORDER",
       'DAFRUTA' as CATEGORIA, 
    -------------------------------------------------------------------
    NVL((SELECT SUM(m.cliposprev)
            from META m 
            WHERE M.codsec in (a.codsec) 
            AND m.CODSUPERVISOR = a.CODSUPERVISOR),1) AS OBJETIVO,
    -------------------------------------------------------------------
       SUM(A.fat) AS Realizado,
    -------------------------------------------------------------------
       TRUNC((SUM(A.FAT) / NVL((SELECT SUM(m.cliposprev)
            from META m 
            WHERE M.codsec in (a.codsec) 
            AND m.CODSUPERVISOR = a.CODSUPERVISOR),1)),5) as "ATING.",
    -------------------------------------------------------------------
       TRUNC((
       ((SUM(A.fat) / d.DIASDECORR)   *   (d.DIASuteis))    
                    /    NVL((SELECT SUM(m.cliposprev)
                                from META m 
                                WHERE M.codsec in (a.codsec) 
                                AND m.CODSUPERVISOR = a.CODSUPERVISOR),1)
        ),5) AS "% TEND.",
    -------------------------------------------------------------------    
        GREATEST(TRUNC((
        (NVL((SELECT SUM(m.cliposprev)
            from META m 
            WHERE M.codsec in (a.codsec) 
            AND m.CODSUPERVISOR = a.CODSUPERVISOR),1)) - SUM(A.fat) 
            
         ),2),0)   as "R.A.F.",
    -------------------------------------------------------------------  
         GREATEST(( 
         (nvl((SELECT SUM(m.cliposprev)
            from META m 
            WHERE M.codsec in (a.codsec) 
            AND m.CODSUPERVISOR = a.CODSUPERVISOR),1) - SUM(A.fat)) 
            / (D.DIASUTEIS - D.diasdecorr) 
         ),0) as "NECECIDADE DIA",
    -------------------------------------------------------------------    
        to_number(TRUNC((SUM(A.fat) / D.DIASDECORR),2)) AS "MEDIA DIA",
    ------------------------------------------------------------------- 
        (CASE WHEN (TRUNC(((SUM(A.FAT) / D.DIASDECORR) * D.DIASUTEIS) /
          NVL((SELECT SUM(m.cliposprev)
            from META m 
            WHERE M.codsec in (a.codsec) 
            AND m.CODSUPERVISOR = a.CODSUPERVISOR),1) * 100,1)) >= 100
            THEN (SELECT UNISTR('\2191')||UNISTR('\2191')||UNISTR('\2191') FROM dual) 
            ELSE (SELECT UNISTR('\2193')||UNISTR('\2193')||UNISTR('\2193') FROM dual) 
            END) AS STATUS
    -------------------------------------------------------------------              
              
FROM SUPDFT A, DIAS d
WHERE a.CODSUPERVISOR = 2
GROUP BY a.CODSUPERVISOR,d.DIASDECORR,d.DIASuteis,a.codsec

---------------------------------------DANILLA-----------------------------------------
UNION
SELECT 2 AS "ORDER",
       'DANILLA' as CATEGORIA, 
    -------------------------------------------------------------------
    NVL((SELECT SUM(m.cliposprev)
            from META m 
            WHERE M.codsec in (a.codsec) 
            AND m.CODSUPERVISOR = a.CODSUPERVISOR),1) AS OBJETIVO,
    -------------------------------------------------------------------
       SUM(A.fat) AS Realizado,
    -------------------------------------------------------------------
       TRUNC((SUM(A.FAT) / NVL((SELECT SUM(m.cliposprev)
            from META m 
            WHERE M.codsec in (a.codsec) 
            AND m.CODSUPERVISOR = a.CODSUPERVISOR),1)),5) as "ATING.",
    -------------------------------------------------------------------
       TRUNC((
       ((SUM(A.fat) / d.DIASDECORR)   *   (d.DIASuteis))    
                    /    NVL((SELECT SUM(m.cliposprev)
                                from META m 
                                WHERE M.codsec in (a.codsec) 
                                AND m.CODSUPERVISOR = a.CODSUPERVISOR),1)
        ),5) AS "% TEND.",
    -------------------------------------------------------------------    
        GREATEST(TRUNC((
        (NVL((SELECT SUM(m.cliposprev)
            from META m 
            WHERE M.codsec in (a.codsec) 
            AND m.CODSUPERVISOR = a.CODSUPERVISOR),1)) - SUM(A.fat) 
            
         ),2),0)   as "R.A.F.",
    -------------------------------------------------------------------  
         GREATEST(( 
         (nvl((SELECT SUM(m.cliposprev)
            from META m 
            WHERE M.codsec in (a.codsec) 
            AND m.CODSUPERVISOR = a.CODSUPERVISOR),1) - SUM(A.fat)) 
            / (D.DIASUTEIS - D.diasdecorr) 
         ),0) as "NECECIDADE DIA",
    -------------------------------------------------------------------    
        to_number(TRUNC((SUM(A.fat) / D.DIASDECORR),2)) AS "MEDIA DIA",
    ------------------------------------------------------------------- 
        (CASE WHEN (TRUNC(((SUM(A.FAT) / D.DIASDECORR) * D.DIASUTEIS) /
          NVL((SELECT SUM(m.cliposprev)
            from META m 
            WHERE M.codsec in (a.codsec) 
            AND m.CODSUPERVISOR = a.CODSUPERVISOR),1) * 100,1)) >= 100
            THEN (SELECT UNISTR('\2191')||UNISTR('\2191')||UNISTR('\2191') FROM dual) 
            ELSE (SELECT UNISTR('\2193')||UNISTR('\2193')||UNISTR('\2193') FROM dual) 
            END) AS STATUS
    -------------------------------------------------------------------              
              
FROM SUPDNL A, DIAS d
WHERE a.CODSUPERVISOR = 2
GROUP BY a.CODSUPERVISOR,d.DIASDECORR,d.DIASuteis,a.codsec

---------------------------------------BIVOLT-----------------------------------------
UNION
SELECT 2 AS "ORDER",
       'BIVOLT' as CATEGORIA, 
    -------------------------------------------------------------------
    NVL((SELECT SUM(m.cliposprev)
            from META m 
            WHERE M.codsec in (a.codsec) 
            AND m.CODSUPERVISOR = a.CODSUPERVISOR),1) AS OBJETIVO,
    -------------------------------------------------------------------
       SUM(A.fat) AS Realizado,
    -------------------------------------------------------------------
       TRUNC((SUM(A.FAT) / NVL((SELECT SUM(m.cliposprev)
            from META m 
            WHERE M.codsec in (a.codsec) 
            AND m.CODSUPERVISOR = a.CODSUPERVISOR),1)),5) as "ATING.",
    -------------------------------------------------------------------
       TRUNC((
       ((SUM(A.fat) / d.DIASDECORR)   *   (d.DIASuteis))    
                    /    NVL((SELECT SUM(m.cliposprev)
                                from META m 
                                WHERE M.codsec in (a.codsec) 
                                AND m.CODSUPERVISOR = a.CODSUPERVISOR),1)
        ),5) AS "% TEND.",
    -------------------------------------------------------------------    
        GREATEST(TRUNC((
        (NVL((SELECT SUM(m.cliposprev)
            from META m 
            WHERE M.codsec in (a.codsec) 
            AND m.CODSUPERVISOR = a.CODSUPERVISOR),1)) - SUM(A.fat) 
            
         ),2),0)   as "R.A.F.",
    -------------------------------------------------------------------  
         GREATEST(( 
         (nvl((SELECT SUM(m.cliposprev)
            from META m 
            WHERE M.codsec in (a.codsec) 
            AND m.CODSUPERVISOR = a.CODSUPERVISOR),1) - SUM(A.fat)) 
            / (D.DIASUTEIS - D.diasdecorr) 
         ),0) as "NECECIDADE DIA",
    -------------------------------------------------------------------    
        to_number(TRUNC((SUM(A.fat) / D.DIASDECORR),2)) AS "MEDIA DIA",
    ------------------------------------------------------------------- 
        (CASE WHEN (TRUNC(((SUM(A.FAT) / D.DIASDECORR) * D.DIASUTEIS) /
          NVL((SELECT SUM(m.cliposprev)
            from META m 
            WHERE M.codsec in (a.codsec) 
            AND m.CODSUPERVISOR = a.CODSUPERVISOR),1) * 100,1)) >= 100
            THEN (SELECT UNISTR('\2191')||UNISTR('\2191')||UNISTR('\2191') FROM dual) 
            ELSE (SELECT UNISTR('\2193')||UNISTR('\2193')||UNISTR('\2193') FROM dual) 
            END) AS STATUS
    -------------------------------------------------------------------              
              
FROM SUPBVT A, DIAS d
WHERE a.CODSUPERVISOR = 2
GROUP BY a.CODSUPERVISOR,d.DIASDECORR,d.DIASuteis,a.codsec

---------------------------------------SEARA-----------------------------------------
UNION
SELECT 2 AS "ORDER",
       'MASSA LEVE' as CATEGORIA, 
    -------------------------------------------------------------------
    NVL((SELECT SUM(m.cliposprev)
            from META m 
            WHERE M.codsec in (a.codsec) 
            AND m.CODSUPERVISOR = a.CODSUPERVISOR),1) AS OBJETIVO,
    -------------------------------------------------------------------
       SUM(A.fat) AS Realizado,
    -------------------------------------------------------------------
       TRUNC((SUM(A.FAT) / NVL((SELECT SUM(m.cliposprev)
            from META m 
            WHERE M.codsec in (a.codsec) 
            AND m.CODSUPERVISOR = a.CODSUPERVISOR),1)),5) as "ATING.",
    -------------------------------------------------------------------
       TRUNC((
       ((SUM(A.fat) / d.DIASDECORR)   *   (d.DIASuteis))    
                    /    NVL((SELECT SUM(m.cliposprev)
                                from META m 
                                WHERE M.codsec in (a.codsec) 
                                AND m.CODSUPERVISOR = a.CODSUPERVISOR),1)
        ),5) AS "% TEND.",
    -------------------------------------------------------------------    
        GREATEST(TRUNC((
        (NVL((SELECT SUM(m.cliposprev)
            from META m 
            WHERE M.codsec in (a.codsec) 
            AND m.CODSUPERVISOR = a.CODSUPERVISOR),1)) - SUM(A.fat) 
            
         ),2),0)   as "R.A.F.",
    -------------------------------------------------------------------  
         GREATEST(( 
         (nvl((SELECT SUM(m.cliposprev)
            from META m 
            WHERE M.codsec in (a.codsec) 
            AND m.CODSUPERVISOR = a.CODSUPERVISOR),1) - SUM(A.fat)) 
            / (D.DIASUTEIS - D.diasdecorr) 
         ),0) as "NECECIDADE DIA",
    -------------------------------------------------------------------    
        to_number(TRUNC((SUM(A.fat) / D.DIASDECORR),2)) AS "MEDIA DIA",
    ------------------------------------------------------------------- 
        (CASE WHEN (TRUNC(((SUM(A.FAT) / D.DIASDECORR) * D.DIASUTEIS) /
          NVL((SELECT SUM(m.cliposprev)
            from META m 
            WHERE M.codsec in (a.codsec) 
            AND m.CODSUPERVISOR = a.CODSUPERVISOR),1) * 100,1)) >= 100
            THEN (SELECT UNISTR('\2191')||UNISTR('\2191')||UNISTR('\2191') FROM dual) 
            ELSE (SELECT UNISTR('\2193')||UNISTR('\2193')||UNISTR('\2193') FROM dual) 
            END) AS STATUS
    -------------------------------------------------------------------              
              
FROM SUPSEA A, DIAS d
WHERE a.CODSUPERVISOR = 2
GROUP BY a.CODSUPERVISOR,d.DIASDECORR,d.DIASuteis,a.codsec

---------------------------------------HYTS-----------------------------------------
UNION
SELECT 2 AS "ORDER",
       'HYTS' as CATEGORIA, 
    -------------------------------------------------------------------
    NVL((SELECT SUM(m.cliposprev)
            from META m 
            WHERE M.codsec in (a.codsec) 
            AND m.CODSUPERVISOR = a.CODSUPERVISOR),1) AS OBJETIVO,
    -------------------------------------------------------------------
       SUM(A.fat) AS Realizado,
    -------------------------------------------------------------------
       TRUNC((SUM(A.FAT) / NVL((SELECT SUM(m.cliposprev)
            from META m 
            WHERE M.codsec in (a.codsec) 
            AND m.CODSUPERVISOR = a.CODSUPERVISOR),1)),5) as "ATING.",
    -------------------------------------------------------------------
       TRUNC((
       ((SUM(A.fat) / d.DIASDECORR)   *   (d.DIASuteis))    
                    /    NVL((SELECT SUM(m.cliposprev)
                                from META m 
                                WHERE M.codsec in (a.codsec) 
                                AND m.CODSUPERVISOR = a.CODSUPERVISOR),1)
        ),5) AS "% TEND.",
    -------------------------------------------------------------------    
        GREATEST(TRUNC((
        (NVL((SELECT SUM(m.cliposprev)
            from META m 
            WHERE M.codsec in (a.codsec) 
            AND m.CODSUPERVISOR = a.CODSUPERVISOR),1)) - SUM(A.fat) 
            
         ),2),0)   as "R.A.F.",
    -------------------------------------------------------------------  
         GREATEST(( 
         (nvl((SELECT SUM(m.cliposprev)
            from META m 
            WHERE M.codsec in (a.codsec) 
            AND m.CODSUPERVISOR = a.CODSUPERVISOR),1) - SUM(A.fat)) 
            / (D.DIASUTEIS - D.diasdecorr) 
         ),0) as "NECECIDADE DIA",
    -------------------------------------------------------------------    
        to_number(TRUNC((SUM(A.fat) / D.DIASDECORR),2)) AS "MEDIA DIA",
    ------------------------------------------------------------------- 
        (CASE WHEN (TRUNC(((SUM(A.FAT) / D.DIASDECORR) * D.DIASUTEIS) /
          NVL((SELECT SUM(m.cliposprev)
            from META m 
            WHERE M.codsec in (a.codsec) 
            AND m.CODSUPERVISOR = a.CODSUPERVISOR),1) * 100,1)) >= 100
            THEN (SELECT UNISTR('\2191')||UNISTR('\2191')||UNISTR('\2191') FROM dual) 
            ELSE (SELECT UNISTR('\2193')||UNISTR('\2193')||UNISTR('\2193') FROM dual) 
            END) AS STATUS
    -------------------------------------------------------------------              
              
FROM SUPHYT A, DIAS d
WHERE a.CODSUPERVISOR = 2
GROUP BY a.CODSUPERVISOR,d.DIASDECORR,d.DIASuteis,a.codsec

--------------------------------------SANTA MASSA---------------------------------------
UNION
SELECT 2 AS "ORDER",
       'SANTA MASSA' as CATEGORIA, 
    -------------------------------------------------------------------
    NVL((SELECT SUM(m.cliposprev)
            from META m 
            WHERE M.codsec in (a.codsec) 
            AND m.CODSUPERVISOR = a.CODSUPERVISOR),1) AS OBJETIVO,
    -------------------------------------------------------------------
       SUM(A.fat) AS Realizado,
    -------------------------------------------------------------------
       TRUNC((SUM(A.FAT) / NVL((SELECT SUM(m.cliposprev)
            from META m 
            WHERE M.codsec in (a.codsec) 
            AND m.CODSUPERVISOR = a.CODSUPERVISOR),1)),5) as "ATING.",
    -------------------------------------------------------------------
       TRUNC((
       ((SUM(A.fat) / d.DIASDECORR)   *   (d.DIASuteis))    
                    /    NVL((SELECT SUM(m.cliposprev)
                                from META m 
                                WHERE M.codsec in (a.codsec) 
                                AND m.CODSUPERVISOR = a.CODSUPERVISOR),1)
        ),5) AS "% TEND.",
    -------------------------------------------------------------------    
        GREATEST(TRUNC((
        (NVL((SELECT SUM(m.cliposprev)
            from META m 
            WHERE M.codsec in (a.codsec) 
            AND m.CODSUPERVISOR = a.CODSUPERVISOR),1)) - SUM(A.fat) 
            
         ),2),0)   as "R.A.F.",
    -------------------------------------------------------------------  
         GREATEST(( 
         (nvl((SELECT SUM(m.cliposprev)
            from META m 
            WHERE M.codsec in (a.codsec) 
            AND m.CODSUPERVISOR = a.CODSUPERVISOR),1) - SUM(A.fat)) 
            / (D.DIASUTEIS - D.diasdecorr) 
         ),0) as "NECECIDADE DIA",
    -------------------------------------------------------------------    
        to_number(TRUNC((SUM(A.fat) / D.DIASDECORR),2)) AS "MEDIA DIA",
    ------------------------------------------------------------------- 
        (CASE WHEN (TRUNC(((SUM(A.FAT) / D.DIASDECORR) * D.DIASUTEIS) /
          NVL((SELECT SUM(m.cliposprev)
            from META m 
            WHERE M.codsec in (a.codsec) 
            AND m.CODSUPERVISOR = a.CODSUPERVISOR),1) * 100,1)) >= 100
            THEN (SELECT UNISTR('\2191')||UNISTR('\2191')||UNISTR('\2191') FROM dual) 
            ELSE (SELECT UNISTR('\2193')||UNISTR('\2193')||UNISTR('\2193') FROM dual) 
            END) AS STATUS
    -------------------------------------------------------------------              
              
FROM SUPSTM A, DIAS d
WHERE a.CODSUPERVISOR = 2
GROUP BY a.CODSUPERVISOR,d.DIASDECORR,d.DIASuteis,a.codsec

------------------------------------------FRUTAP----------------------------------------
UNION
SELECT 2 AS "ORDER",
       'FRUTAP' as CATEGORIA, 
    -------------------------------------------------------------------
    NVL((SELECT SUM(m.cliposprev)
            from META m 
            WHERE M.codsec in (a.codsec) 
            AND m.CODSUPERVISOR = a.CODSUPERVISOR),1) AS OBJETIVO,
    -------------------------------------------------------------------
       SUM(A.fat) AS Realizado,
    -------------------------------------------------------------------
       TRUNC((SUM(A.FAT) / NVL((SELECT SUM(m.cliposprev)
            from META m 
            WHERE M.codsec in (a.codsec) 
            AND m.CODSUPERVISOR = a.CODSUPERVISOR),1)),5) as "ATING.",
    -------------------------------------------------------------------
       TRUNC((
       ((SUM(A.fat) / d.DIASDECORR)   *   (d.DIASuteis))    
                    /    NVL((SELECT SUM(m.cliposprev)
                                from META m 
                                WHERE M.codsec in (a.codsec) 
                                AND m.CODSUPERVISOR = a.CODSUPERVISOR),1)
        ),5) AS "% TEND.",
    -------------------------------------------------------------------    
        GREATEST(TRUNC((
        (NVL((SELECT SUM(m.cliposprev)
            from META m 
            WHERE M.codsec in (a.codsec) 
            AND m.CODSUPERVISOR = a.CODSUPERVISOR),1)) - SUM(A.fat) 
            
         ),2),0)   as "R.A.F.",
    -------------------------------------------------------------------  
         GREATEST(( 
         (nvl((SELECT SUM(m.cliposprev)
            from META m 
            WHERE M.codsec in (a.codsec) 
            AND m.CODSUPERVISOR = a.CODSUPERVISOR),1) - SUM(A.fat)) 
            / (D.DIASUTEIS - D.diasdecorr) 
         ),0) as "NECECIDADE DIA",
    -------------------------------------------------------------------    
        to_number(TRUNC((SUM(A.fat) / D.DIASDECORR),2)) AS "MEDIA DIA",
    ------------------------------------------------------------------- 
        (CASE WHEN (TRUNC(((SUM(A.FAT) / D.DIASDECORR) * D.DIASUTEIS) /
          NVL((SELECT SUM(m.cliposprev)
            from META m 
            WHERE M.codsec in (a.codsec) 
            AND m.CODSUPERVISOR = a.CODSUPERVISOR),1) * 100,1)) >= 100
            THEN (SELECT UNISTR('\2191')||UNISTR('\2191')||UNISTR('\2191') FROM dual) 
            ELSE (SELECT UNISTR('\2193')||UNISTR('\2193')||UNISTR('\2193') FROM dual) 
            END) AS STATUS
    -------------------------------------------------------------------              
              
FROM SUPFTP A, DIAS d
WHERE a.CODSUPERVISOR = 2
GROUP BY a.CODSUPERVISOR,d.DIASDECORR,d.DIASuteis,a.codsec

-----------------------------------------MARGARINA----------------------------------------
UNION
SELECT 2 AS "ORDER",
       'MARGARINA' as CATEGORIA, 
    -------------------------------------------------------------------
    NVL((SELECT SUM(m.cliposprev)
            from META m 
            WHERE M.codsec in (a.codsec) 
            AND m.CODSUPERVISOR = a.CODSUPERVISOR),1) AS OBJETIVO,
    -------------------------------------------------------------------
       SUM(A.fat) AS Realizado,
    -------------------------------------------------------------------
       TRUNC((SUM(A.FAT) / NVL((SELECT SUM(m.cliposprev)
            from META m 
            WHERE M.codsec in (a.codsec) 
            AND m.CODSUPERVISOR = a.CODSUPERVISOR),1)),5) as "ATING.",
    -------------------------------------------------------------------
       TRUNC((
       ((SUM(A.fat) / d.DIASDECORR)   *   (d.DIASuteis))    
                    /    NVL((SELECT SUM(m.cliposprev)
                                from META m 
                                WHERE M.codsec in (a.codsec) 
                                AND m.CODSUPERVISOR = a.CODSUPERVISOR),1)
        ),5) AS "% TEND.",
    -------------------------------------------------------------------    
        GREATEST(TRUNC((
        (NVL((SELECT SUM(m.cliposprev)
            from META m 
            WHERE M.codsec in (a.codsec) 
            AND m.CODSUPERVISOR = a.CODSUPERVISOR),1)) - SUM(A.fat) 
            
         ),2),0)   as "R.A.F.",
    -------------------------------------------------------------------  
         GREATEST(( 
         (nvl((SELECT SUM(m.cliposprev)
            from META m 
            WHERE M.codsec in (a.codsec) 
            AND m.CODSUPERVISOR = a.CODSUPERVISOR),1) - SUM(A.fat)) 
            / (D.DIASUTEIS - D.diasdecorr) 
         ),0) as "NECECIDADE DIA",
    -------------------------------------------------------------------    
        to_number(TRUNC((SUM(A.fat) / D.DIASDECORR),2)) AS "MEDIA DIA",
    ------------------------------------------------------------------- 
        (CASE WHEN (TRUNC(((SUM(A.FAT) / D.DIASDECORR) * D.DIASUTEIS) /
          NVL((SELECT SUM(m.cliposprev)
            from META m 
            WHERE M.codsec in (a.codsec) 
            AND m.CODSUPERVISOR = a.CODSUPERVISOR),1) * 100,1)) >= 100
            THEN (SELECT UNISTR('\2191')||UNISTR('\2191')||UNISTR('\2191') FROM dual) 
            ELSE (SELECT UNISTR('\2193')||UNISTR('\2193')||UNISTR('\2193') FROM dual) 
            END) AS STATUS
    -------------------------------------------------------------------              
              
FROM SUPMGN A, DIAS d
WHERE a.CODSUPERVISOR = 2
GROUP BY a.CODSUPERVISOR,d.DIASDECORR,d.DIASuteis,a.codsec



------------------ORDENAÇÃO------------------
    ORDER BY "ORDER" ASC, "R.A.F." DESC
