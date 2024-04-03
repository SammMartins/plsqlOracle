WITH FatStm AS 
    (SELECT ped.codusur as RCA,
            SUM(ped.qt*ped.pvenda) + 0 as Faturamento
    FROM pontual.PCPEDI ped
        JOIN pontual.pcprodut prod on ped.codprod = prod.codprod
    WHERE prod.codfornec = 1541
        AND ped.data BETWEEN '01-mar-2024' and '31-mar-2024'
        AND prod.CODSEC = 10001
        AND ped.posicao NOT LIKE 'C'
        AND ped.vlbonific = 0
    Group By ped.codusur),

DNDIST AS
    (SELECT ped.codusur AS RCA,
            COUNT(DISTINCT ped.codcli) AS DN
        FROM pontual.PCPEDC ped
            JOIN pontual.PCPEDI pedi on pedi.numped = ped.numped
            JOIN pontual.pcprodut prod on pedi.codprod = prod.codprod
        WHERE prod.codfornec = 1541
            AND ped.data BETWEEN '01-mar-2024' and '31-mar-2024'
            AND prod.CODSEC = 10001            
            AND PED.DTCANCEL IS NULL
            AND PED.CONDVENDA IN (1, 2, 3, 7, 9, 14, 15, 17, 18, 19, 98)
        GROUP BY ped.codusur),
        
META AS (
    SELECT C.codusur,
            (CASE 
            WHEN C.codusur = 140 THEN ROUND(800 / 24,0)
            WHEN C.codusur = 141 THEN ROUND(800 / 24,0)
            WHEN C.codusur = 142 THEN ROUND(800 / 24,0)
            WHEN C.codusur = 143 THEN ROUND(800 / 24,0)
            WHEN C.codusur = 145 THEN ROUND(800 / 24,0)
            WHEN C.codusur = 147 THEN ROUND(800 / 24,0)
            WHEN C.codusur = 148 THEN ROUND(800 / 24,0)
            WHEN C.codusur = 150 THEN ROUND(800 / 24,0)
            WHEN C.codusur = 151 THEN ROUND(800 / 24,0)
            WHEN C.codusur = 152 THEN ROUND(800 / 24,0)
            WHEN C.codusur = 153 THEN ROUND(800 / 24,0)
            WHEN C.codusur = 154 THEN ROUND(800 / 24,0)
            WHEN C.codusur = 155 THEN ROUND(800 / 24,0)
            WHEN C.codusur = 156 THEN ROUND(800 / 24,0)
            WHEN C.codusur = 157 THEN ROUND(800 / 24,0)
            WHEN C.codusur = 158 THEN ROUND(800 / 24,0)
            WHEN C.codusur = 160 THEN ROUND(800 / 24,0)
            WHEN C.codusur = 161 THEN ROUND(800 / 24,0)
            WHEN C.codusur = 164 THEN ROUND(800 / 24,0)
            WHEN C.codusur = 167 THEN ROUND(800 / 24,0)
            WHEN C.codusur = 168 THEN ROUND(800 / 24,0)
            WHEN C.codusur = 169 THEN ROUND(800 / 24,0)
            WHEN C.codusur = 170 THEN ROUND(800 / 24,0)
            WHEN C.codusur = 172 THEN ROUND(800 / 24,0)
            WHEN C.codusur = 174 THEN ROUND(800 / 24,0)
            ELSE 0 
            END) AS METADN
    FROM pontual.PCUSUARI C
    )

-----------------------------------------------------------------------------------------------------------

SELECT  RANK() OVER (ORDER BY (((a.DN / m.METADN))) DESC, fat.faturamento DESC) AS "Rank",
        USUR.CODSUPERVISOR SUP,usur.codusur cod,
        SUBSTR(usur.nome, INSTR(usur.nome, ' ') + 1, INSTR(usur.nome, ' ', INSTR(usur.nome, ' ') + 1) - INSTR(usur.nome, ' ') - 1) AS RCA, -- Extrai o nome
        fat.faturamento AS "VENDIDO",
        m.METADN "META DN",
        a.DN AS "DN",
        ((m.METADN - a.DN) * 1) as "GAP",
        (a.DN / m.METADN) AS " %"
FROM pontual.PCUSUARI usur
    JOIN FatStm fat ON usur.codusur = fat.RCA
    JOIN DNDIST a ON usur.codusur = a.RCA
    JOIN META m ON m.codusur = usur.codusur 
WHERE usur.nome like 'PMU%'


UNION ALL
SELECT 25 AS "Rank",
       0 AS SUP,
       0 AS COD,
       '- TOTAL PREMIUM -' AS RCA,
       SUM(fat.faturamento) AS "VENDIDO",
       800 AS "META DN",
       SUM(a.DN) AS "DN",
       SUM(m.METADN - a.DN) as "GAP",
       SUM(a.DN) / SUM(m.METADN) AS " %"       
FROM pontual.PCUSUARI usur
    JOIN FatStm fat ON usur.codusur = fat.RCA
    JOIN DNDIST a ON usur.codusur = a.RCA
    JOIN META m ON m.codusur = usur.codusur 
WHERE usur.nome like 'PMU%'
ORDER BY "Rank", "VENDIDO" DESC       
