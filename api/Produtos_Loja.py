import pyodbc

dados_conexao = (

    "Driver={SQL Server};"
    "Server=DESKTOP-090310;"
    "Database=Produtos_Loja;"
)

conexao = pyodbc.connect(dados_conexao)
print('Conexão Bem Sucedida!')

cursor =  conexao.cursor()

comando = """SELECT * FROM Produtos;"""


cursor.execute(comando)
resultado = cursor.fetchall()
if len(resultado) == 0:
    print("Nenhum resultado para processar...")
else:
    for row in resultado:
        print(row)
