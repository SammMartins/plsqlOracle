WITH SENHA AS(
SELECT '123999' AS SENHA1, '080789' AS SENHA2, '061218' AS SENHA3, {senha} AS SENHADIG FROM DUAL
),
VERBA AS (
SELECT
PCUSUARI.CODUSUR,
PCUSUARI.NOME RCA,
PCSUPERV.CODSUPERVISOR, PCSUPERV.NOME SUPERVISOR,
PONTUAL.pc_pkg_controlarsaldorca.ccrca_checar_disponivel_atual(PCUSUARI.CODUSUR) SALDO
FROM PONTUAL.PCUSUARI, PONTUAL.PCSUPERV
WHERE PCUSUARI.CODSUPERVISOR = PCSUPERV.CODSUPERVISOR AND PCUSUARI.CODUSUR <> '9999'
AND NVL(PCSUPERV.POSICAO,'A') = 'A'
AND PCUSUARI.DTTERMINO IS NULL
ORDER BY PCUSUARI.CODSUPERVISOR, PCUSUARI.CODUSUR
)

SELECT A.CODUSUR, A.RCA, A.SALDO
FROM VERBA A
WHERE A.CODSUPERVISOR = (SELECT (CASE WHEN S.SENHADIG = S.SENHA1 THEN 9
                                      WHEN S.SENHADIG = S.SENHA2 THEN 2
                                      WHEN S.SENHADIG = S.SENHA3 THEN 8
                                      END) FROM SENHA S)
ORDER BY SALDO ASC