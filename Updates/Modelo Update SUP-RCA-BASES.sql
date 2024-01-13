DECLARE
  rca_sup_2 NumArray;
  cod_usur_sup2 NUMBER := 2;
BEGIN
  -- Inicializando o array
  rca_sup_2 := NumArray(148, 145, 150, 151, 152, 168, 174, 164, 153, 143);
  
  -- Realizando o Update
  FOR i IN 1..rca_sup_2.COUNT LOOP
    UPDATE PCCLIENT
    SET codusur2 = cod_usur_sup2
    WHERE codusur1 = rca_sup_2(i);
  END LOOP;

  DBMS_OUTPUT.PUT_LINE('Update realizado com sucesso!');
EXCEPTION
  WHEN OTHERS THEN
    DBMS_OUTPUT.PUT_LINE('Erro ao executar o UPDATE: ' || SQLERRM);
END;

SELECT codcli,codusur1,codusur2 FROM pcclient 
WHERE codusur1 in (148,145,150,151,152,168,174,164,153,143)

