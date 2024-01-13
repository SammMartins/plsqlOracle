DECLARE
    v_cod_usur1 NUMBER := 174;
BEGIN
    UPDATE PCMETA
    SET CLIPOSPREV = 12141
    WHERE CODIGO = 1023 --SANTA MASSA
    AND codusur = v_cod_usur1
    AND DATA = '01-SET-2023';
    
    DBMS_OUTPUT.PUT_LINE('Update realizado com sucesso!');
EXCEPTION
    WHEN OTHERS THEN
        DBMS_OUTPUT.PUT_LINE('Erro ao executar o UPDATE: ' || SQLERRM);
END;

----------------------------------------------------------------------------------------------------------------
SELECT CODIGO,CODFILIAL,CODUSUR,TIPOMETA,DATA,CLIPOSPREV
FROM PCMETA 
WHERE CODIGO = 1023
AND DATA = '01-SET-2023'
ORDER BY CODIGO
