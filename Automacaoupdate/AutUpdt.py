import pyodbc
import time
from datetime import datetime
import json
import pandas
import os
import smtplib
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders


Arquivo_log = "log_ajusteimpostos_notas.txt"

def conectDB2():

 Driver = "{Client Access ODBC Driver (32-bit)}"
 System = "10.1.0.2"
 #UserId  = input("Infome o ID:")
 #SenhaDb = input("Informe a Senha:")
 DNS     = "NAG0001"
 arquivo_json = "credenciais.json" 
 
 if os.path.exists(arquivo_json):
    with open(arquivo_json,"r", encoding="utf-8") as f:
       dados = json.load(f)
       UserId  = dados.get("UserId")
       SenhaDb = dados.get("SenhaDb")
       MinutosTempo = int(dados.get("MinutosTempo") or 2)
    print("[INFO] Usando Credendiais salvas")
 else:
     UserId  = input("Informe o ID:")
     SenhaDb = input("Informe a Senha:")
     MinutosTempo = int(input("Informe o tempo em minutos:"))

     dados = {"UserId": UserId,
              "SenhaDb":SenhaDb,
              "MinutosTempo": MinutosTempo}
          
     with open(arquivo_json, "w", encoding="utf-8") as f:
        json.dump(dados, f, indent=4)
        print("[INFO] Credenciais salvas no JSON")

 try:
     print("[AÇÃO] Conectando com banco de dados...")
     time.sleep(2)
     con = pyodbc.connect(f"Driver={Driver};"
                          f"System={System};"
                          f"Uid={UserId};"
                          f"Pwd={SenhaDb};"
                          f"DefaultLibraries={DNS};"
                        )
     print("Conectado com sucesso!")
     con.autocommit = False
     return con, MinutosTempo
    

 except Exception as erro:
     print("Erro ao conectar:",erro) 
     return None, MinutosTempo      



def LogMensagem(mensagem):
  with open(Arquivo_log, "a", encoding="utf-8") as log:
     log.write(f"{datetime.now()} - {mensagem}\n")


#Função para correção dos impostos dos itens - Notas de saída
# def qryNFsaidaitem(con):

#   if not con:
#      print("Conexão não estabelecida.")
#      return
#   print("[AÇÃO] Executando QrydeItens/NF de saída - Correção dos impostos.")
#   time.sleep(2)
#   cursor = con.cursor()
#   qry = """ 
#             SELECT 
#                'UPDATE COPRDD02 SET  SITTRIRTS = '''||CASE WHEN SUBSTRING(I.CODFIC,2,3) IN ('152','409') THEN '410'
#                 ELSE '000'    END ||''',CLCTRIRTS='''||CASE WHEN SUBSTRING(I.CODFIC,2,3) IN ('152','409') THEN '410002'
#                 ELSE '000001' END ||''''||',IDCDOA=''0'''||',BSECACRTS='||
#                 CASE WHEN SUBSTRING(I.CODFIC,2,3) IN ('152','409') THEN 0
#                 ELSE CAST(ROUND(I.PRCVEN + I.VALFRT + I.VALCBRBLT + I.VALOUTDSP + I.VALSEV + I.VALSGR,2) AS NUMERIC(14,2))END
#                ||',PECIBS='||CASE WHEN SUBSTRING(I.CODFIC,2,3) IN ('152','409') THEN 0.0 ELSE 0.1 END
#                ||',PECCBS='||CASE WHEN SUBSTRING(I.CODFIC,2,3) IN ('152','409') THEN 0.0 ELSE 0.9 END
#                ||',VALIBSEST='||CAST(CASE WHEN SUBSTRING(I.CODFIC,2,3) IN ('152','409') THEN 0 
#                 ELSE ROUND((I.PRCVEN + I.VALFRT + I.VALCBRBLT + I.VALOUTDSP + I.VALSEV + I.VALSGR) * 0.1 * 0.01,2) END AS NUMERIC(14,2))
#                ||',VALIBS='||CAST(CASE WHEN SUBSTRING(I.CODFIC,2,3) IN ('152','409') THEN 0
#                 ELSE ROUND((I.PRCVEN + I.VALFRT + I.VALCBRBLT + I.VALOUTDSP + I.VALSEV + I.VALSGR) * 0.1 * 0.01,2) END AS NUMERIC(14,2))
#                ||',VALCBS='||CAST(CASE WHEN SUBSTRING(I.CODFIC,2,3) IN ('152','409') THEN 0
#                 ELSE ROUND((I.PRCVEN + I.VALFRT + I.VALCBRBLT + I.VALOUTDSP + I.VALSEV + I.VALSGR) * 0.9 * 0.01,2) END AS NUMERIC(14,2))
#                ||' WHERE IDFEMP='''||I.IDFEMP||''''
#                ||' AND NUMDOC='''||I.NUMDOC||''''
#                ||' AND DATTRA='''||I.DATTRA||''''
#                ||' AND CODPRD='''||I.CODPRD||''''
#                ||' AND CODFIC='''||I.CODFIC||''''
#                ||' AND PRCVEN='||CAST(ROUND(I.PRCVEN,2) AS NUMERIC (14,2))|| ';'
#             FROM CONOTD00 P JOIN COPRDD02 I ON P.IDFEMP = I.IDFEMP 
#                                            AND P.NOTFIC = I.NUMDOC 
#                                            AND P.DATEMS = I.DATTRA 
#                                            AND I.IDFDBTCRD='2'
#                             JOIN CONOTD0M M ON M.IDFEMP = P.IDFEMP 
#                                            AND M.NOTFIC = P.NOTFIC 
#                                            AND M.DATEMS = P.DATEMS
#             WHERE P.DATEMS >= ('20260101')
#               AND M.STAPRE IN ('999', '215', '225') 

#            """
#   try:
#         cursor.execute(qry)
#         dados = cursor.fetchall()
 
#         if dados:
#          script_update = "\n".join(linha[0] for linha in dados)
#          print("[RESULTADO] " + "\n".join(linha[0] for linha in dados) + " registros encontrados na Qry de itens/NF de saída - Correção dos impostos.")
#          return script_update
#         else:
#          print("[RESULTADO] Nenhum dado encontrado na Qry de itens/NF de saída - Correção dos impostos.")
#   except Exception as erro:
#      print("Erro ao executar query:", erro)


# #Função para correção dos impostos notas de saídaCabeçalho
# def qryNFsaidacabe(con):    

#   if not con:
#      print("Query de itens não executada ou erro na conexão.")
#      return
#   print("[AÇÃO] Executando Qry do Cabeçalho/NF de saída - Correção dos impostos.") 
#   time.sleep(2)

#   cursor = con.cursor()
#   qry1 = """ 
#          SELECT 'UPDATE CONOTD00 SET '||
#             '  VALIBSEST = ' || SUM( B.VALIBSEST) ||
#             ', TOTIBS = ' || SUM( B.VALIBS) ||
#             ', TOTVBCRTS = ' || SUM( B.BSECACRTS) ||
#             ', TOTCBS = ' || SUM( B.VALCBS) ||
#             ', TOTNFERTS = ' || SUM(  B.VALIBS + B.VALCBS ) ||
#             ' WHERE IDFEMP = '''||A.IDFEMP||''' AND NOTFIC = '''||A.NOTFIC||''' AND DATEMS = '''|| A.DATEMS ||''';'||
#             'UPDATE COFICD04 SET '||
#             '  VALIBSEST = ' || SUM( B.VALIBSEST) ||
#             ', TOTIBS = ' || SUM( B.VALIBS) ||
#             ', TOTVBCRTS = ' || SUM( B.BSECACRTS) ||
#             ', TOTCBS = ' || SUM( B.VALCBS) ||
#             ', TOTNFERTS = ' || SUM(  B.VALIBS + B.VALCBS ) ||
#             ' WHERE IDFEMP = '''||A.IDFEMP||''' AND NOTFIC = '''||A.NOTFIC||''' AND DATTRA = '''|| A.DATEMS ||''';'||
#             'UPDATE CONOTD0M SET STAPRE = '''' '||
#             ' WHERE IDFEMP = '''||A.IDFEMP||''' AND NOTFIC = '''||A.NOTFIC||''' AND DATEMS = '''||A.DATEMS||''';' 
#          FROM CONOTD00 A LEFT OUTER JOIN COPRDD02 B ON B.IDFEMP = A.IDFEMP 
#                                                    AND B.NUMDOC = A.NOTFIC 
#                                                    AND B.DATTRA = A.DATEMS 
#                                                    AND B.IDFDBTCRD = '2'
#                         LEFT OUTER JOIN CONOTD0M C ON C.IDFEMP = A.IDFEMP 
#                                                   AND C.NOTFIC = A.NOTFIC 
#                                                   AND C.DATEMS = A.DATEMS
#                         LEFT OUTER JOIN COCLID01 D ON D.CODCLI = A.CODCLI
# WHERE     A.DATEMS >= '20260101'
#       AND A.STANOTFIC NOT IN ( 'C','V' )
#       AND C.STAPRE <> '100'
# GROUP BY A.IDFEMP, A.DATEMS, A.NOTFIC, A.CODFIC, A.STANOTFIC,
#        A.VALIBSEST, A.TOTIBS, A.TOTVBCRTS, A.TOTCBS, A.TOTNFERTS, C.STAPRE, C.CHVACS, D.RAZSOC
# HAVING A.TOTVBCRTS<>SUM( B.BSECACRTS)    or  a.TOTCBS <> SUM( B.VALCBS) OR a.TOTIBS <> SUM( B.VALIBS)

#            """
#   try:
#         cursor.execute(qry1)
#         dados1 = cursor.fetchall()
 
#         if dados1:
#          script_update1 = "\n".join(linha[0] for linha in dados1)
#          print("[RESULTADO] " + "\n".join(linha[0] for linha in dados1) + " registros encontrados na Qry do Cabeçalho/NF de saída - Correção dos impostos.")
#          return script_update1
#         else:
#          print("[RESULTADO] Nenhum dado encontrado na Qry do Cabeçalho/NF de saída - Correção dos impostos.")

#   except Exception as erro:
#      print("Erro ao executar query:", erro)


# #Notas de entrada

# def qryNFEntradaItens(con):
#     if not con:
#      print("Query de itens entrada não executada ou erro na conexão.")
#      return
#     print("[AÇÃO] Executando Qry de itens/NF de Entrada - Correção dos impostos.") 
#     time.sleep(2)

#     cursor = con.cursor()

#     qryenti = """
#     SELECT 'UPDATE COPRDD02 SET  SITTRIRTS = '''||
#         CASE WHEN SUBSTRING(I.CODFIC,2,3) IN ('152','409') 
#              THEN '410' ELSE '000' END ||''', CLCTRIRTS='''||
#         CASE WHEN SUBSTRING(I.CODFIC,2,3) IN ('152','409') 
#              THEN '410002' ELSE '000001' END||''''||',IDCDOA=''0''' ||',BSECACRTS='||
#         CASE WHEN SUBSTRING(I.CODFIC,2,3) IN ('152','409') 
#              THEN 0 ELSE CAST(ROUND(I.PRCVEN + I.VALFRT + I.VALCBRBLT + 
#               I.VALOUTDSP + I.VALSEV + I.VALSGR,2) AS NUMERIC(14,2))
#         END ||',PECIBS='||
#         CASE WHEN SUBSTRING(I.CODFIC,2,3) IN ('152','409') 
#              THEN 0.0 ELSE 0.1 END ||',PECCBS='||
#         CASE WHEN SUBSTRING(I.CODFIC,2,3) IN ('152','409') 
#              THEN 0.0 ELSE 0.9 END ||',VALIBSEST='||
#         CAST(CASE WHEN SUBSTRING(I.CODFIC,2,3) IN ('152','409') 
#              THEN 0 ELSE ROUND((I.PRCVEN + I.VALFRT + I.VALCBRBLT + 
#              I.VALOUTDSP + I.VALSEV + I.VALSGR) * 0.1 * 0.01,2)END AS NUMERIC(14,2)) 
#              ||',VALIBS='||
#         CAST(CASE WHEN SUBSTRING(I.CODFIC,2,3) IN ('152','409') 
#              THEN 0 ELSE ROUND((I.PRCVEN + I.VALFRT + I.VALCBRBLT + 
#              I.VALOUTDSP + I.VALSEV + I.VALSGR) * 0.1 * 0.01,2) END AS NUMERIC(14,2)) ||',VALCBS='||
#         CAST(CASE WHEN SUBSTRING(I.CODFIC,2,3) IN ('152','409') 
#              THEN 0 ELSE ROUND((I.PRCVEN + I.VALFRT + I.VALCBRBLT + 
#              I.VALOUTDSP + I.VALSEV + I.VALSGR) * 0.9 * 0.01,2) END AS NUMERIC(14,2)) ||
#         ' WHERE IDFEMP='''||I.IDFEMP||''''||
#         ' AND NUMDOC='''||I.NUMDOC||''''||
#         ' AND DATTRA='''||I.DATTRA||''''||
#         ' AND CODPRD='''||I.CODPRD||''''||
#         ' AND CODFIC='''||I.CODFIC||''''||
#         ' AND PRCVEN='||CAST(ROUND(I.PRCVEN,2) AS NUMERIC (14,2))|| ';'
#     FROM CONOTD01 P
#     JOIN COPRDD02 I 
#         ON P.IDFEMP = I.IDFEMP
#         AND P.NOTFIC = I.NUMDOC
#         AND P.DATENT = I.DATTRA
#         AND I.IDFDBTCRD = '1'
#     JOIN CONOTD0M M 
#         ON P.IDFEMP = M.IDFEMP
#         AND P.NOTFIC = M.NOTFIC
#         AND P.DATEMS = M.DATEMS
#     WHERE P.DATEMS LIKE '2026%'
#       AND SUBSTRING(P.CODFIC,2,3) IN ('202','411','102')
#       AND M.STAPRE IN ('225','215','999')
#       AND (COALESCE(I.SITTRIRTS,'')='' 
#            OR (I.SITTRIRTS = '000' AND I.VALCBS = 0))
#     """

#     try:
#         cursor.execute(qryenti)
#         dadosient = cursor.fetchall()

#         if dadosient:
#             script_updateient = "\n".join(linha[0] for linha in dadosient)
#             print("[RESULTADO] " + "\n".join(linha[0] for linha in dadosient) + " registros encontrados na Qry de itens/NF de Entrada - Correção dos impostos.")
#             return script_updateient
#         else:
#             print("[RESULTADO] Nenhum dado encontrado na Qry de itens/NF de Entrada - Correção dos impostos.")

#     except Exception as erro:
#         print("Erro ao executar query:", erro)


# def qryNFEntradaCabe(con):
#     if not con:
#      print("Query cabeçalho entrada não executada ou erro na conexão.")
#      return
#     print("[AÇÃO] Executando QrydoCabeçalho/NF de Entrada - Correção dos impostos.") 
#     time.sleep(2)

#     cursor = con.cursor()
#     qryentc = """
#          SELECT 'UPDATE CONOTD01 SET '||
#          '  VALIBSEST = ' || SUM( B.VALIBSEST) ||
#          ', TOTIBS = ' || SUM( B.VALIBS) ||
#          ', TOTVBCRTS = ' || SUM( B.BSECACRTS) ||
#          ', TOTCBS = ' || SUM( B.VALCBS) ||
#          ', TOTNFERTS = ' || SUM(  B.VALIBS + B.VALCBS ) ||
#        ' WHERE IDFEMP = '''||A.IDFEMP||''' AND NOTFIC = '''||A.NOTFIC||''' AND DATEnt = '''|| A.DATent ||''';'|| 
#        'UPDATE COFICD04 SET '||
#          '  VALIBSEST = ' || SUM( B.VALIBSEST) ||
#          ', TOTIBS = ' || SUM( B.VALIBS) ||
#          ', TOTVBCRTS = ' || SUM( B.BSECACRTS) ||
#          ', TOTCBS = ' || SUM( B.VALCBS) ||
#          ', TOTNFERTS = ' || SUM(  B.VALIBS + B.VALCBS ) ||
#        ' WHERE IDFEMP = '''||A.IDFEMP||''' AND NOTFIC = '''||A.NOTFIC||''' AND DATTRA = '''|| A.DATEnt ||''';'|| 
#        'UPDATE CONOTD0M SET STAPRE = '''' '||
#        ' WHERE IDFEMP ='''||A.IDFEMP||''' AND NOTFIC = '''||A.NOTFIC||''' AND DATEMS = '''||A.DATEMS||''';' as SQL_UPDATE
#         FROM CONOTD01 A
#         LEFT OUTER JOIN COPRDD02 B ON B.IDFEMP = A.IDFEMP AND B.NUMDOC = A.NOTFIC AND B.DATTRA = A.DATEnt AND B.IDFDBTCRD = '1'
#         LEFT OUTER JOIN CONOTD0M C ON C.IDFEMP = A.IDFEMP AND C.NOTFIC = A.NOTFIC AND C.DATEMS = A.DATEMS  
#         WHERE A.DATEMS >= '20260101'
#         AND A.STANOTFIC NOT IN ( 'C','V' )
#         AND SUBSTRING(A.CODFIC,2,3) in ('202','411', '949')
#         AND C.STAPRE IN ('215','225','999')
#         GROUP BY A.IDFEMP, A.DATEnt,A.DATEMS, A.NOTFIC, A.CODFIC, A.STANOTFIC,
#         A.VALIBSEST, A.TOTIBS, A.TOTVBCRTS, A.TOTCBS, A.TOTNFERTS
#         HAVING A.TOTVBCRTS<>SUM( B.BSECACRTS)    or  a.TOTIBS <> SUM( B.VALCBS)
#         """

#     try:
#         cursor.execute(qryentc)
#         dadoscent = cursor.fetchall()

#         if dadoscent:
#             script_updatecent = "\n".join(linha[0] for linha in dadoscent)
#             print("[RESULTADO] " + "\n".join(linha[0] for linha in dadoscent) + " registros encontrados na Qry do Cabeçalho/NF de Entrada - Correção dos impostos.")
#             return script_updatecent
#         else:
#             print("[RESULTADO] Nenhum dado encontrado na Qry do Cabeçalho/NF de Entrada - Correção dos impostos.")

#     except Exception as erro:
#         print("Erro ao executar query:", erro)

#     finally:
#         cursor.close()   

      

#Função para verificar seriais de pedidos cancelados sem NF-e e removê-los das tabelas CONOTD0E e NAGWMS.PCWMSNUMSERIE
def verificar_serial_pedidoCancelado(con):
    if not con:
        print("[ERRO] Query de verificação de serial não executada ou erro na conexão.")
        return 0

    print("[AÇÃO] Executando verificação de seriais de pedidos cancelados sem NF-e...")
    time.sleep(2)

    cursor = con.cursor()

    qry_serial = """
        SELECT
            CASE
                WHEN A.SGMCMR = 'B2C'
                THEN A.ANO || '2' || SUBSTRING(A.IDFEMP,3,2) || A.NUMPED || '1'
                ELSE
                A.ANO || '1' || SUBSTRING(A.IDFEMP,3,2) || A.NUMPED || '0'
            END AS NUMPED,
            TRIM(B.NUMSER) AS NUMSER,
            A.IDFEMP,
            A.DATEMS,
            A.NUMPED,
            B.CODPRD
        FROM COPEDD00 A JOIN CONOTD0E B ON A.IDFEMP = B.IDFEMP
                                       AND A.NUMPED = B.NUMPED
                                       AND A.DATEMS = B.DATEMS
        WHERE A.DATEMS = REPLACE(CHAR(CURRENT_DATE, ISO), '-', '')
          AND A.STAPED = 'C'
          AND A.NOTFIC = ''
          AND A.IDFEMP IN ('0001','0002','0005','0008','0021')
    """

    cursor.execute(qry_serial)
    dados_serial = cursor.fetchall()

    if not dados_serial:
        print("[RESULTADO] Nenhum serial de pedido cancelado sem NF-e encontrado.")
        cursor.close()
        return 0

    qry_delete_conotd0e = """
        DELETE FROM CONOTD0E
        WHERE IDFEMP = ?
          AND DATEMS = ?
          AND NUMPED = ?
          AND NUMSER = ?
    """

    qry_delete_wms = """
        DELETE FROM NAGWMS.PCWMSNUMSERIE
        WHERE NUMPED = ?
          AND NUMEROSERIE = ?
          AND CODPROD = ?
    """

    total = 0

    for linha in dados_serial:
        numped_wms = linha[0]
        numser = linha[1]
        idfemp = linha[2]
        datems = linha[3]
        numped = linha[4]
        codprd = linha[5]

        print(f"[RESULTADO] Removendo serial {numser} do produto {codprd} referente ao pedido cancelado de Nº: {numped_wms}.")

        # Exclui da CONOTD0E
        cursor.execute(
            qry_delete_conotd0e,
            (idfemp, datems, numped, numser)
        )

        # Exclui da tabela WMS
        cursor.execute(
            qry_delete_wms,
            (numped_wms, numser,codprd)
        )

        total += 1

    cursor.close()

    print(f"[INFO] {total} registro(s) processado(s) com sucesso.")

    return total


# Função para verificar pedidos com críticas (Stacriend) e gerar os updates correspondentes
def critica_stacriend(con):
    if not con:
        print("[ERRO] Query de verificação de Pedido com Críticas (Stacriend) não executada ou erro na conexão.")
        return ""

    print("[AÇÃO] Executando verificação de Pedido com Críticas (Stacriend)...")
    time.sleep(2)

    cursor = con.cursor()

    qry_Pedido_Critica = """
        SELECT A.NUMPED,
               A.IDFEMP,
               A.DATEMS,
               CASE
                   WHEN B.SEMAFORO = '3'
                    AND A.STAPED = 'P'
                    AND A.STAATZFCT = 'T'
                   THEN 'UPDATE COPEDD00 SET STACRIEND = ''F'' WHERE IDFEMP = ''' || A.IDFEMP || ''' ' ||
                        'AND NUMPED = ''' || A.NUMPED || ''' ' ||
                        'AND DATEMS = ''' || A.DATEMS || ''' ' ||
                        'AND STACRIEND = ''' || A.STACRIEND || ''';'
               END AS UPDATE_STACRIEND
        FROM COPEDD00 A
             JOIN (
                    SELECT NUMERO,
                           SEMAFORO
                      FROM NAGWMS.PCWMSOUTPUT
                  GROUP BY NUMERO, SEMAFORO
                  ) B
               ON A.ANO || '1' || SUBSTRING(A.IDFEMP, 3, 2) || A.NUMPED || '0' = B.NUMERO
        WHERE A.IDFEMP IN ('0001', '0002', '0005', '0008', '0021')
          AND A.STAPED = 'P'
          AND B.SEMAFORO = '3'
          AND A.STACRIEND = 'T'
          AND A.DATEMS = REPLACE(CHAR(CURRENT_DATE, ISO), '-', '')
    """

    try:
        cursor.execute(qry_Pedido_Critica)
        dados_Pedido_Critica = cursor.fetchall()

        if not dados_Pedido_Critica:
            print("[RESULTADO] Nenhum Pedido com Críticas (Stacriend) encontrado.")
            return ""

        script_update_stacriend = "\n".join(
            linha[3] for linha in dados_Pedido_Critica if linha[3]
        )

        print(f"[RESULTADO] {len(dados_Pedido_Critica)} pedido(s) com Críticas (Stacriend) encontrado(s).")

        return script_update_stacriend

    except Exception as erro:
        print("Erro ao executar query:", erro)
        return ""

    finally:
        cursor.close()

        
#consulta notas de saída com RMA para habilitar a emissão de NFe        
def qryNFsaidaRMA(con):
    if not con:
        print("[ERRO] Query de verificação de Notas de Saída com RMA não executada ou erro na conexão.")
        return ""

    print("[AÇÃO] Executando verificação de Notas de Saída com RMA...")
    time.sleep(2)

    cursor = con.cursor()

    qry_RMA = """
    
    SELECT
        'UPDATE CONOTD06 SET QTDITE = QTDITE - '''||A.QTDITE||''' '||
        'WHERE IDFEMP = '''||A.IDFEMP||''' AND NOTFIC = '''||A.NOTFICSAI||''' '||
        'AND ANO = '''||A.ANONOTFIC||''' AND CODPRD = '''||A.CODPRD||'''; '||
        'UPDATE CONOTD00 SET STANOTFIC = ''P'' '||
        'WHERE IDFEMP = '''||A.IDFEMP||''' AND NOTFIC = '''||A.NOTFICSAI||''' '||
         'AND DATEMS = '''||A.DATNOTSAI||'''; '      AS UPDATE_AJUSTE
    FROM(SELECT IDFEMP, ANO, NUMPED, NOTFICSAI,
            DATNOTSAI, QTDITE, CODPRD, ANONOTFIC
            FROM COPEDD09) A LEFT JOIN(SELECT STAPED, NOTFIC, DATEMS,
                                 CODFIC, IDFEMP, NUMPED, ANO, TPODVL, CODDVL
                                 FROM COPEDD08) B ON A.IDFEMP = B.IDFEMP
                                                 AND A.NUMPED = B.NUMPED
                                                 AND A.ANO    = B.ANO
                LEFT JOIN(SELECT STANOTFIC, NOTFIC,
                                 DATEMS,IDFEMP
                                 FROM CONOTD00) C ON A.NOTFICSAI = C.NOTFIC
                                                 AND A.DATNOTSAI = C.DATEMS
                                                 AND A.IDFEMP    = C.IDFEMP
                LEFT JOIN(SELECT CODPRD, QTDITE,
                                 NOTFIC, ANO, IDFEMP
                                 FROM CONOTD06) D ON A.NOTFICSAI = D.NOTFIC
                                                 AND A.ANONOTFIC = D.ANO
                                                 AND A.IDFEMP    = D.IDFEMP
                                                 AND A.CODPRD    = D.CODPRD
                LEFT JOIN(SELECT IDFEMP, NOTFIC,
                                 DATEMS, STANOTFIC
                                 FROM CONOTD01) E ON B.IDFEMP    = E.IDFEMP
                                                 AND B.NOTFIC    = E.NOTFIC
                                                 AND B.DATEMS    = E.DATEMS
    WHERE E.DATEMS = REPLACE(CHAR(CURRENT_DATE, ISO),'-','')
        AND A.ANO >= '26'
        AND B.STAPED = '3'
        AND C.STANOTFIC = 'T'
        AND SUBSTRING(B.CODFIC,2,3) = '949'
        AND E.STANOTFIC = 'D'
        AND (A.QTDITE - D.QTDITE) = '0'
        AND B.TPODVL = '4'
        AND B.CODDVL IN ('07')
        AND NOT EXISTS (SELECT *
                        FROM COPEDD09 X JOIN COPEDD08 Y ON X.IDFEMP = Y.IDFEMP
                                                  AND X.NUMPED = Y.NUMPED
                                                  AND X.ANO    = Y.ANO
                        WHERE X.IDFEMP = A.IDFEMP
                             AND X.ANO = A.ANO
                       AND X.NOTFICSAI = A.NOTFICSAI
                       AND SUBSTRING(Y.CODFIC,2,3) IN ('202')
                       AND Y.STAPED <> 'C')

              """

    try:
        cursor.execute(qry_RMA)
        dados_RMA = cursor.fetchall()

        if not dados_RMA:
            print("[RESULTADO] Nenhuma Nota de Saída com RMA encontrada.")
            return ""

        script_update_RMA = "\n".join(
            linha[0] for linha in dados_RMA if linha[0]
        )

        print(f"[RESULTADO] {len(dados_RMA)} Nota(s) de Saída com RMA encontrada(s). Serão habilitadas para um novo processo de RMA.")

        return script_update_RMA

    except Exception as erro:
        print("[ERRO] Erro ao executar query:", erro)
        return ""

    finally:
        cursor.close()




'''
def checaCFOP_pedido(con):
    if not con:
        print("[ERRO] Query de verificação de Notas de Saída com RMA não executada ou erro na conexão.")
        return ""
    print("[AÇÃO] Executando verificação de Notas de Saída com RMA...")
    time.sleep(2)

    cursor = con.cursor()

    qryChecaPedido = """
          """
    try:
        cursor.execute(qryChecaPedido)
        dados_checaped = cursor.fetchall()

        if not dados_checaped:
            print("[RESULTADO] Nenhuma Nota de Saída com RMA encontrada.")
            return ""

        script_update_RMA = "\n".join(
            linha[0] for linha in dados_checaped if linha[0]
        )

        print(f"[RESULTADO] {len(dados_checaped)} Nota(s) de Saída com RMA encontrada(s). Serão habilitadas para um novo processo de RMA.")

        return script_update_RMA

    except Exception as erro:
        print("[ERRO] Erro ao executar query:", erro)
        return ""

    finally:
        cursor.close() '''


def checkPedlinkpgto(con):
    if not con:
        print("[ERRO] Query de verificação de Pedidos Link Pgto não executada ou erro na conexão.")
        return ""

    print("[AÇÃO] Executando verificação de Pedidos Link Pgto...")
    time.sleep(2)

    cursor = con.cursor()

    qryChecaPedidoLnk = """

    SELECT
    CASE WHEN A.STAPED = 'W' AND A.STACFR = '3' AND B.COTLOG = 'Pedido Conferido' THEN
     'UPDATE COPEDD00 SET STACFR = ''1'', STAPED = ''P'' WHERE IDFEMP = '''||A.IDFEMP||''' AND NUMPED = '''||A.NUMPED||''' AND ANO = '''||A.ANO||''' AND STALNKPTO = '''||A.STALNKPTO||'''; '
    ELSE
    CASE WHEN A.STAPED = 'P' AND A.STACFR = '3' AND B.COTLOG = 'Pedido Conferido' THEN
     'UPDATE COPEDD00 SET STACFR = ''1'' WHERE IDFEMP = '''||A.IDFEMP||''' AND NUMPED = '''||A.NUMPED||''' AND ANO = '''||A.ANO||''' AND STALNKPTO = '''||A.STALNKPTO||'''; '
     END END AS AJUSTE_PEDCONF_STSCFR3
    FROM COPEDD00 A JOIN COLOGD02 B ON A.IDFEMP = B.IDFEMP
                                   AND A.NUMPED = B.NUMPED
                                   AND A.ANO    = B.ANO
                                   AND B.IDFPGM = 'WSPED111'
                                   AND B.COTLOG = 'Pedido Conferido'
    WHERE  A.STAATZFCT = 'T'
       AND A.STALNKPTO = '4'
       AND A.STAPED IN ('P','W')
       AND A.SGMCMR = 'LJA'
       AND A.STACFR = '3'
       AND A.DATEMS = REPLACE(CHAR(CURRENT_DATE, ISO), '-', '')

    """
    try:

        cursor.execute(qryChecaPedidoLnk)
        dados_checapedlnk = cursor.fetchall()

        if not dados_checapedlnk:
            print("[RESULTADO] Nenhum Pedido Link Pgto encontrado.")
            return ""

        script_update_checapedlnk = "\n".join(
            linha[0] for linha in dados_checapedlnk if linha[0]
        )

        print(f"[RESULTADO] {len(dados_checapedlnk)} Pedido(s) Link Pgto encontrado(s). Serão ajustados para faturamento!")

        return script_update_checapedlnk

    except Exception as erro:
        print("[ERRO] Erro ao executar query:", erro)
        return ""

    finally:
        cursor.close()


def CheckNumpedDevLja(con):

    if not con:
        print("[ERRO] Query de verificação de NF-e de devolução com critica 681 da Sefaz.")
        return ""

    print("[AÇÃO] Executando verificação de NF-e de devolução com critica 681 da Sefaz...")
    time.sleep(2)

    cursor = con.cursor()

    CheckNumpedDevLja = """
    
SELECT
CASE WHEN A.STAPRE = '681'
THEN 'UPDATE CONOTD01 SET NUMPED = '''||C.NUMPED||''' WHERE IDFEMP = '''||A.IDFEMP||''' AND NOTFIC = '''||A.NOTFIC||''' AND DATEMS = '''||A.DATEMS||''';'||
     'UPDATE CONOTD0M SET STAPRE = '''' WHERE IDFEMP = '''||A.IDFEMP||''' AND NOTFIC = '''||A.NOTFIC||''' AND DATEMS = '''||A.DATEMS||''';'
              END AS AJUSTE
FROM CONOTD0M A JOIN CONOTD01 B ON A.IDFEMP = B.IDFEMP
                               AND A.NOTFIC = B.NOTFIC
                               AND A.DATEMS = B.DATEMS
                JOIN COPEDD08 C ON A.IDFEMP = C.IDFEMP
                               AND A.NOTFIC = C.NOTFIC
                               AND A.DATEMS = C.DATTRA
WHERE 1=1
AND A.DATEMS <= REPLACE(CHAR(CURRENT_DATE, ISO), '-', '')
AND A.STAPRE = '681'
AND B.NUMPED = ''
AND B.STANOTFIC = 'D'

    """
    try:

        cursor.execute(CheckNumpedDevLja)
        dados_CheckNumpedDevLja = cursor.fetchall()

        if not dados_CheckNumpedDevLja:
            print("[RESULTADO] Nenhuma NF-e de devolução com critica 681 encontrada.")
            return ""

        script_update_CheckNumpedDevLja = "\n".join(
            linha[0] for linha in dados_CheckNumpedDevLja if linha[0]
        )

        print(f"[RESULTADO] {len(dados_CheckNumpedDevLja)} NF-e(s) de devolução com critica 681 encontrada(s). Serão ajustadas.")

        return script_update_CheckNumpedDevLja

    except Exception as erro:
        print("[ERRO] Erro ao executar query:", erro)
        return ""

    finally:
        cursor.close()



        
def enviar_email_com_excel(caminho_arquivo, destinatarios, qtd_registros):
    """Função auxiliar para enviar o arquivo Excel gerado por e-mail."""
    # ==========================================================
    # CONFIGURAÇÕES DO SERVIDOR DE E-MAIL (Ajuste conforme seu provedor)
    # ==========================================================
    smtp_server = "smtp.gmail.com"  # Ex: smtp.gmail.com ou servidor interno
    smtp_port = 587
    remetente = "augustomendes144@gmail.com.br"
    senha = os.environ.get("SMTP_PASSWORD", "")
    # ==========================================================

    msg = MIMEMultipart()
    msg["From"] = remetente
    msg["To"] = ", ".join(destinatarios)
    msg["Subject"] = f"Relatório Docs SAP Divergentes - {datetime.now().strftime('%d/%m/%Y %H:%M')}"

    corpo_email = f"""
    Olá,

    Segue em anexo o relatório com a verificação de Docs SAP.
    Total de registros encontrados: {qtd_registros}

    Atenciosamente,
    Automação SAP
    """
    msg.attach(MIMEText(corpo_email, "plain", "utf-8"))

    # Anexar o arquivo Excel
    with open(caminho_arquivo, "rb") as anexo:
        parte = MIMEBase("application", "vnd.openxmlformats-officedocument.spreadsheetml.sheet")
        parte.set_payload(anexo.read())
        encoders.encode_base64(parte)
        parte.add_header(
            "Content-Disposition",
            f"attachment; filename={os.path.basename(caminho_arquivo)}",
        )
        msg.attach(parte)

    # Enviar o e-mail
    with smtplib.SMTP(smtp_server, smtp_port) as server:
        server.starttls()  # Segurança TLS
        server.login(remetente, senha)
        server.sendmail(remetente, destinatarios, msg.as_string())


# def checkDocsap(con, lista_emails):
#     if not con:
#         print("[ERRO] Query de verificação de Docs SAP não executada ou erro na conexão.")
#         return False

#     if not lista_emails:
#         print("[AVISO] Nenhum e-mail de destinatário informado.")
#         return False

#     print("[AÇÃO] Executando verificação de Docs SAP...")
#     time.sleep(2)

#     cursor = con.cursor()

#     qry_checkDocsap = """
#     SELECT
#         SAP.BUPLA                        AS FILIAL,
#         SAP.BELNR                        AS NUMDOCSAP,
#         CASE WHEN SAP.BELNR = 0 THEN FNGDATETOCHAR(SAP.ZFBDT)
#              ELSE FNGDATETOCHAR(SAP.FDTAG) END
#                                          AS DATAVENCIMENTO,
#         CASE WHEN S05.NUMDOCSAP IS NULL
#              THEN 'NÃO INSERIDO' END     AS NUMDOCSAP_COSAPD05,
#         TRIM(SUBSTRING(SAP.XBLNR,4,10))  AS REFERENCIA,
#         PED.NUMPED                       AS NUMPEDCONAGEM,
#         PED.CODCLI                       AS CLIENTE_ORIG,
#         CLI.CODCLI                       AS CLIENTE_ERRADO,
#         CASE WHEN PED.CODCLI <> CLI.CODCLI
#              THEN 'DIVERGENTE' END       AS STATUS_CLI,
#         FNGDATETOCHAR(SAP.BLDAT)         AS DTEMISSAO,
#         CASE WHEN SAP.SHKZG='H'
#              THEN (-1)*SAP.VALOR
#              ELSE SAP.VALOR END          AS VALOR,
#         CASE WHEN SAP.SHKZG='H'
#              THEN (-1)*SAP.VALOR
#              ELSE SAP.VLPAGO END         AS VLRPAG,
#         SAP.BLART                        AS TIPODOCSAP,
#         SAP.FDLEV                        AS NIV_TESOURARIA,
#         SAP.LTEXT                        AS DESC_NVTESOURARIA,
#         PED.CODPOR                       AS PORTADORCONAGEM
#     FROM (SELECT KUNNR,BUPLA, BELNR, BUZEI, ZFBDT, FDTAG,
#                  XBLNR, SHKZG, BLDAT, VALOR, BLART, ZUONR,
#                  FDLEV, LTEXT, GJAHR, STBLG, VLPAGO
#           FROM NAGBI.RTL_ZFIT147) SAP
#     LEFT JOIN COSAPD12 BL  ON BL.IDFEMP     = SAP.BUPLA
#                           AND BL.NUMTITRCB  = SAP.BELNR
#     LEFT JOIN COSAPD11 CS  ON CS.CODSAP     = SAP.KUNNR
#                           AND CS.IDFTPOCAD  = 'C'
#     LEFT JOIN (SELECT CODCLI
#                FROM COCLID01) CLI
#                            ON CLI.CODCLI    = CS.CODCAD
#     LEFT JOIN (SELECT NUMDOCSAP, ANO, IDFEMP, NOTFIC, DATEMS
#                FROM COSAPD05) S05
#                            ON S05.NUMDOCSAP = SAP.BELNR
#                           AND S05.ANO       = RIGHT(SAP.GJAHR,2)
#     LEFT JOIN (SELECT IDFEMP, NOTFIC,
#                       ANO, NUMPED, DATEMS
#                FROM CONOTD00) NFS
#                            ON NFS.IDFEMP    = SAP.BUPLA
#                           AND NFS.NOTFIC    = RIGHT(SAP.XBLNR,9)
#                           AND NFS.ANO       = RIGHT(SAP.GJAHR,2)
#     LEFT JOIN (SELECT NUMPED, IDFEMP, DATEMS,
#                       CODPOR, CODCLI, NOTFIC
#                FROM COPEDD00) PED
#                            ON PED.IDFEMP    = NFS.IDFEMP
#                           AND PED.NOTFIC    = NFS.NOTFIC
#                           AND PED.DATEMS    = NFS.DATEMS
#     WHERE 1=1
#     AND COALESCE(SAP.STBLG,'') = ''
#     AND S05.NUMDOCSAP IS NULL
#     AND PED.CODCLI <> CLI.CODCLI
#     AND SUBSTRING(REPLACE(CHAR(SAP.BLDAT, ISO),'-',''),1,4) >= '2026'
#     AND SAP.ZUONR <> ''
#     """

#     caminho_excel = ""
#     try:
#         cursor.execute(qry_checkDocsap)
#         dados_checkDocsap = cursor.fetchall()

#         if not dados_checkDocsap:
#             print("[RESULTADO] Nenhum Doc SAP encontrado. E-mail não será enviado.")
#             return True

#         # Pega automaticamente os nomes das colunas definidos no SELECT (AS ...)
#         colunas = [desc[0] for desc in cursor.description]

#         # Cria o DataFrame e salva em Excel
#         df = pd.DataFrame.from_records(dados_checkDocsap, columns=colunas)
        
#         timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
#         caminho_excel = f"Docs_SAP_Divergentes_{timestamp}.xlsx"
        
#         df.to_excel(caminho_excel, index=False, engine="openpyxl")
#         print(f"[RESULTADO] {len(dados_checkDocsap)} Doc(s) encontrado(s). Excel gerado: {caminho_excel}")

#         # Envia o arquivo por e-mail
#         print(f"[AÇÃO] Enviando e-mail para: {', '.join(lista_emails)}...")
#         enviar_email_com_excel(caminho_excel, lista_emails, len(dados_checkDocsap))
#         print("[SUCESSO] E-mail enviado com sucesso!")

#         return True

#     except Exception as erro:
#         print("[ERRO] Erro ao processar/enviar Docs SAP:", erro)
#         return False

#     finally:
#         cursor.close()
#         # Opcional: Remove o arquivo temporário do disco após o envio para não acumular lixo
#         if caminho_excel and os.path.exists(caminho_excel):
#             os.remove(caminho_excel)       


# def rotina_agendada(con):
#     # Lista de e-mails que receberão o relatório
#     destinatarios = [
#         "augusto.mendes@nagem.com.br"
#     ]
    
#     # Horários desejados no formato HH:MM
#     horarios_execucao = ["08:00", "12:00", "16:30"]
#     ultimo_minuto_executado = ""

#     print("[SISTEMA] Monitoramento de horário iniciado...")
#     while True:
#         agora = datetime.now().strftime("%H:%M")

#         if agora in horarios_execucao and agora != ultimo_minuto_executado:
#             print(f"[AGENDADOR] Horário atingido ({agora}). Iniciando rotina...")
#             checkDocsap(con, destinatarios)
#             ultimo_minuto_executado = agora  # Evita rodar várias vezes no mesmo minuto

#        time.sleep(20)  # Verifica a cada 20 segundos

    
#função para executar os updates das queries
def Executar_updates(con,rotina_agendada):

    if not con:
        print("Sem conexão.")
        return

    cursor = con.cursor()

    try:
   #     script_itens = qryNFsaidaitem(con)
   #     script_cabe = qryNFsaidacabe(con)
   #     script_itense = qryNFEntradaItens(con)
   #     scrip_cab_e = qryNFEntradaCabe(con)
        script_stacriend = critica_stacriend(con)
        script_update_RMA = qryNFsaidaRMA(con)
        script_update_checapedlnk = checkPedlinkpgto(con)
        script_update_CheckNumpedDevLja = CheckNumpedDevLja(con)
       

        total = 0

        # Executa ITENS_SAÍDA
   #     if not script_itens:
   #         print("Update não realizado! Nenhuma linha encontrada na QrydeitensNFsaída.")
   #     else:
   #         for cmd in script_itens.split(";"):
   #             cmd = cmd.strip()
   #             if cmd:
   #                 cursor.execute(cmd)
   #                 total += 1

        # Executa CABEÇALHO_SAÍDA
   #     if not script_cabe:
   #         print("Update não realizado! Nenhuma linha encontrada na QryCabeçalhoNFsaída.")
   #     else:
   #         for cmd in script_cabe.split(";"):
   #             cmd = cmd.strip()
   #             if cmd:
   #                 cursor.execute(cmd)
   #                 total += 1

        # Executa ITENS_ENTRADA
    #if not script_itense:
    #       print("Update não realizado! Nenhuma linha encontrada na QryItensNFentrada.")
    #    else:
    #        for cmd in script_itense.split(";"):
    #            cmd = cmd.strip()
    #            if cmd:
    #                cursor.execute(cmd)
    #                total += 1

        # Executa CABEÇALHO_ENTRADA
    #    if not scrip_cab_e:
    #        print("Update não realizado! Nenhuma linha encontrada na QryCabeçalhoNFentrada.")
    #    else:
    #        for cmd in scrip_cab_e.split(";"):
    #            cmd = cmd.strip()
    #            if cmd:
    #                cursor.execute(cmd)
    #                total += 1

        # Executa STACRIEND
        if not script_stacriend:
            print("Update não realizado! Nenhuma linha encontrada na QryStacriend.")
        else:
            for cmd in script_stacriend.split(";"):
                cmd = cmd.strip()
                if cmd:
                    cursor.execute(cmd)
                    total += 1    

        # Executa UPDATE_RMA
        if not script_update_RMA:
            print("Update não realizado! Nenhuma linha encontrada na QryNFsaidaRMA.")
        else:
            for cmd in script_update_RMA.split(";"):
                cmd = cmd.strip()
                if cmd:
                    cursor.execute(cmd)
                    total += 1

        if not script_update_checapedlnk:
            print("Update não realizado! Nenhuma linha encontrada na QryChecaPedidoLnk.")
        else:
            for cmd in script_update_checapedlnk.split(";"):
                cmd = cmd.strip()
                if cmd:
                    cursor.execute(cmd)
                    total += 1   

        if not script_update_CheckNumpedDevLja:
            print("Update não realizado! Nenhuma linha encontrada na QryChecaNF-e_Critica_681.")
        else:
            for cmd in script_update_CheckNumpedDevLja.split(";"):
                cmd = cmd.strip()
                if cmd:
                            
                            cursor.execute(cmd)
                            total += 1  
                            


        # Somente após executar todos os UPDATEs
        total_serial = verificar_serial_pedidoCancelado(con)

        if total > 0 or total_serial > 0:

            con.commit()

            print("\n================ RESUMO DA EXECUÇÃO ================")
            print(f"Updates executados : {total}")
            print(f"Seriais removidos  : {total_serial}")
            print("Commit realizado com sucesso.")
            print("===================================================\n")

            LogMensagem(
                f"Commit OK | Updates: {total} | Seriais removidos: {total_serial}"
            )

        else:
            print("[INFO] Nenhuma alteração encontrada.")

    except Exception as erro:
        con.rollback()
        print("Erro detectado. Rollback executado.")
        print("Erro:", erro)
        LogMensagem(f"ERRO - Rollback executado: {erro}")

    finally:
        cursor.close()

#rotina_agendada()



def temporizador(minutos):

    intervalo = minutos * 60
    print(f"[INFO] Processo iniciado. Execução a cada {minutos} minuto(s).")

    try:
        while True:
            inicio = time.time()

            conexao,_ = conectDB2()

            if conexao:
                Executar_updates(conexao)
                conexao.close()

            tempo_execucao = time.time() - inicio
            tempo_restante = int(intervalo - tempo_execucao)

            #  Contagem regressiva
            while tempo_restante > 0:
                print(f"\r[INFO] Próxima execução em {tempo_restante} segundos... ", end="")
                time.sleep(1)
                tempo_restante -= 1

            print()  # quebra de linha quando terminar

    except KeyboardInterrupt:
        print("\n[INFO] Processo interrompido pelo usuário.")
   
    
if __name__ == "__main__":

    conexao, minutos = conectDB2()

    if conexao:
        conexao.close()  # fecha só o teste inicial

    temporizador(minutos)
  
    
     
