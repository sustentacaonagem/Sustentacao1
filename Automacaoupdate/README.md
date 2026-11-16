# Automacaoupdate

Automa??o Python para rotinas de sustenta??o.

Instale as depend?ncias com `pip install -r requirements.txt`. A conex?o exige o driver ODBC IBM i de 32 bits e acesso ? rede interna. As credenciais do banco s?o solicitadas pela aplica??o e salvas localmente em `credenciais.json`, exclu?do do Git. Para envio de e-mail, configure a vari?vel de ambiente `SMTP_PASSWORD`.

Gere o execut?vel com `GerarExe.bat`.

Estado atual: rotinas fiscais e SAP foram comentadas a pedido. Existem refer?ncias a fun??es desativadas e assinaturas de chamadas que precisam ser ajustadas antes da execu??o. A sintaxe foi validada; n?o houve execu??o contra banco ou envio de e-mail.
