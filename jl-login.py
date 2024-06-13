from flask import Flask, render_template, redirect, request, flash
import json
import ast #usei pra converter uma str em dicionario
import os #usei pra trabalhar com diretorios

app = Flask(__name__)
app.config['SECRET_KEY'] = 'SCTKYDEV'

logado = False

@app.route('/')
def home():
    global logado
    logado = False
    return render_template('login.html')

@app.route('/adm')
def adm(): 
    if logado == True:
        with open('usuario.json') as usuariosTemp:
            usuarios = json.load(usuariosTemp)
        return render_template("adm.html",usuarios=usuarios)
    if logado == False:
        return redirect('/')


@app.route('/login', methods=['POST'])
def login():

    global logado

    nome = request.form.get('nome')
    senha = request.form.get('senha')

    with open('usuario.json') as usuariosTemp:
        usuarios = json.load(usuariosTemp)
        contador = 0
        for usuario in usuarios:
            contador += 1
            if nome == 'adm' and senha == '123456':
                logado = True
                return redirect("/adm")
            
            if usuario['nome'] == nome and usuario['senha'] == senha:
                return render_template("index.html")
            
            if contador >= len(usuarios):
                flash('USUARIO INVALIDO')
                return redirect("/")

@app.route('/cadastrarUsuario', methods=['POST'])
def cadastrarUsuario():
    user = []
    nome = request.form.get('nome')
    senha = request.form.get('senha')
    user = [
        {
            "nome": nome,
            "senha": senha
        }
    ]
    with open('usuario.json') as usuariosTemp:
        usuarios = json.load(usuariosTemp)
    
    usuarioNovo = usuarios + user

    with open('usuario.json', 'w') as gravarTemp:
        json.dump(usuarioNovo, gravarTemp, indent=4)
    return redirect("/adm")

@app.route('/excluirUsuario', methods=['POST'])
def excluirUsuario():
    global logado
    logado = True
    usuario = request.form.get('usuario_para_excluir')
    print(usuario)
    usuarioDict = ast.literal_eval(usuario) #usuario antes tava indo como str e assim to transformando em dicionario
    nome = usuarioDict['nome']
    with open('usuario.json') as usuariosTemp:
        usuarioJson = json.load(usuariosTemp)
        for c in usuarioJson:
            if c == usuarioDict:
                usuarioJson.remove(usuarioDict)
                with open('usuario.json', 'w') as usuarioAexcluir:
                    json.dump(usuarioJson,usuarioAexcluir, indent=4)

    flash(f'{nome}EXCLUIDO')
    return redirect('/adm')

@app.route('/upload', methods=['POST'])
def upload():
    global logado
    logado = True
    arquivo = request.files.get('documento')
    nome_arquivo = arquivo.filename.replace(" ", "-")
    arquivo.save(os.path.join('arquivos/', nome_arquivo))
    flash('ARQUIVO SALVO')

    return redirect('/adm')

if __name__ in "__main__":
    app.run(debug=True)