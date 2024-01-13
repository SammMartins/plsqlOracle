DECLARE
    v_cod_usur1 NUMBER := 147;
    v_cod_usur2 NUMBER := 149;
BEGIN
    UPDATE PCCLIENT
    SET codusur1 = v_cod_usur1,
        codusur2 = v_cod_usur2
    WHERE codcli in (   13428,
                        13408,
                        13808,
                        850,
                        13379,
                        4608,
                        15106,
                        15329,
                        13094,
                        1780,
                        15511,
                        14628,
                        13873,
                        14937,
                        11142,
                        14491,
                        15508,
                        12222,
                        15111,
                        13096,
                        11453);

    DBMS_OUTPUT.PUT_LINE('Update realizado com sucesso!');
EXCEPTION
    WHEN OTHERS THEN
        DBMS_OUTPUT.PUT_LINE('Erro ao executar o UPDATE: ' || SQLERRM);
END;

----------------------------------------------------------------------------------------------------------------
SELECT codcli,codusur1,codusur2
FROM PCCLIENT 
WHERE codcli in (       13428,
                        13408,
                        13808,
                        850,
                        13379,
                        4608,
                        15106,
                        15329,
                        13094,
                        1780,
                        15511,
                        14628,
                        13873,
                        14937,
                        11142,
                        14491,
                        15508,
                        12222,
                        15111,
                        13096,
                        11453);
