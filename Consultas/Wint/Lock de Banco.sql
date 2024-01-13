SELECT DISTINCT SES.PROGRAM EXECUTAVEL,
                OBJ.OBJECT_NAME TABELA,
                TO_CHAR(TRUNC(SES.LAST_CALL_ET / 60 / 60),
                        'FM999900') || ':' ||
                TO_CHAR(TRUNC(((SES.LAST_CALL_ET / 60 / 60) -
                              TRUNC(SES.LAST_CALL_ET / 60 / 60)) * 60),
                        'FM00') || ':' ||
                TO_CHAR(TRUNC(((((SES.LAST_CALL_ET / 60 / 60) -
                              TRUNC(SES.LAST_CALL_ET / 60 / 60)) * 60) -
                              TRUNC(((SES.LAST_CALL_ET / 60 / 60) -
                                    TRUNC(SES.LAST_CALL_ET / 60 / 60)) * 60))*60),
                        'FM00') TEMPO,
                SES.LAST_CALL_ET TEMPO_EM_SEGUNDOS,
                SES.STATUS,
                DECODE(LOC.LOCKED_MODE,
                       1,
                       'NO LOCK',
                       2,
                       'ROW SHARE',
                       3,
                       'ROW EXCLUSIVE',
                       4,
                       'SHARE',
                       5,
                       'SHARE ROW EXCL',
                       6,
                       'EXCLUSIVE',
                       NULL) LOCKED_MODE,
                'alter system kill session ''' || SID || ',' || SERIAL# ||
                ''' immediate;' COMANDO_DESCONEXAO,
                SES.SID SID,
                SES.SERIAL# SERIAL#,
                SQL.SQL_TEXT TEXTO_SQL,
                SES.MACHINE MAQUINA,
                SES.USERNAME USUARIO_ORACLE,
                SES.OSUSER USUARIOS_SO
  FROM V$SESSION       SES,
       V$LOCKED_OBJECT LOC,
       DBA_OBJECTS     OBJ,
       V$SQL           SQL
 WHERE SES.SID = LOC.SESSION_ID
   AND LOC.OBJECT_ID = OBJ.OBJECT_ID
   AND SES.SQL_ADDRESS = SQL.ADDRESS(+)
 ORDER BY SES.LAST_CALL_ET DESC;
