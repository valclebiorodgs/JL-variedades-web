from typing import Union

from fastapi import FastAPI
import pyodbc
from fastapi.responses import JSONResponse
app = FastAPI()

dados_conexao = (

    "Driver={SQL Server};"
    "Server=DESKTOP-090310;"
    "Database=Produtos_Loja;"
)

conexao = pyodbc.connect(dados_conexao)
print('Conexão Bem Sucedida!')




@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.get("/items/{item_id}")
def read_item(item_id: int, q: Union[str, None] = None):
    return {"item_id": item_id, "q": q}

@app.get("/consulta-produtos")
def get_produtos():
    cursor =  conexao.cursor()
    comando = """SELECT * FROM Produtos;"""

    cursor.execute(comando)
    rows = cursor.fetchall()
    resultado = []
    for row in rows: 
        dataset = {}
        for i,  col in enumerate(cursor.description):
            if col[0] == "Valor":
                dataset[col[0]]= str(row[i])
            else:
                dataset[col[0]]= row[i]
        resultado.append(dataset)
    # print(resultado)
    return JSONResponse(content=resultado) 

@app.get("/consulta-produtos-id/{id_produto}")
def get_produtos_by_id(id_produto:int):
    cursor =  conexao.cursor()
    comando = f"""SELECT * FROM Produtos WHERE ID_Produto ={id_produto};"""

    cursor.execute(comando)
    rows = cursor.fetchall()
    resultado = []
    for row in rows: 
        dataset = {}
        for i,  col in enumerate(cursor.description):
            if col[0] == "Valor":
                dataset[col[0]]= str(row[i])
            else:
                dataset[col[0]]= row[i]
        resultado.append(dataset)
    # print(resultado)
    return JSONResponse(content=resultado) 


@app.get("/consulta-produtos-nome/{nome_produto}")
def get_produtos_by_nome(nome_produto: str):
    cursor = conexao.cursor()
    comando = "SELECT * FROM Produtos WHERE Nome_Produto = ?;"
    
    cursor.execute(comando, (nome_produto,))
    rows = cursor.fetchall()
    resultado = []
    for row in rows:
        dataset = {}
        for i, col in enumerate(cursor.description):
            if col[0] == "Valor":
                dataset[col[0]] = str(row[i])
            else:
                dataset[col[0]] = row[i]
        resultado.append(dataset)
    
    return JSONResponse(content=resultado)
