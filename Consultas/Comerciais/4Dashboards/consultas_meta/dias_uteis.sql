-- Com base na rotina 589

SELECT * FROM PCDIASUTEIS
WHERE CODFILIAL= 3
AND DATA BETWEEN  TO_DATE('01/03/2024', 'DD/MM/YYYY') AND 
                  TO_DATE('30/04/2024', 'DD/MM/YYYY') 