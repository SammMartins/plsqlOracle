DECLARE
  cod_sup0 NUMBER := 9;
  cod_sup1 NUMBER := 8;
BEGIN
  UPDATE PCUSUARI
  SET CODSUPERVISOR = cod_sup1
  WHERE CODSUPERVISOR = cod_sup0;
END;

SELECT CODUSUR,CODSUPERVISOR
  FROM PCUSUARI
 WHERE CODSUPERVISOR = 2;

