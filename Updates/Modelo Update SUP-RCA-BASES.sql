UPDATE PCCLIENT
SET codusur2 = 2
WHERE codusur1 in (SELECT CODUSUR FROM PCUSUARI WHERE CODSUPERVISOR = 2);
----------------------------------------------------------------------------------------------------------------
SELECT codcli,codusur1,codusur2
FROM PCCLIENT 
WHERE codusur1 in (SELECT CODUSUR FROM PCUSUARI WHERE CODSUPERVISOR = 2)
AND CODUSUR2 != 2;
