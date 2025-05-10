from flask import Flask, render_template, request, redirect, url_for
import csv
import os
from datetime import datetime

app = Flask(__name__)
UPLOAD_FOLDER = 'static/img'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

PROJETOS_CSV = 'projetos.csv'
TAREFAS_CSV = 'tarefas.csv'

# Funções auxiliares
def ler_csv(caminho):
    if not os.path.exists(caminho):
        return []
    with open(caminho, newline='', encoding='utf-8') as f:
        return list(csv.DictReader(f))

def escrever_csv(caminho, dados, campos):
    with open(caminho, 'w', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=campos)
        writer.writeheader()
        writer.writerows(dados)

# Rotas
@app.route('/')
def index():
    projetos = ler_csv(PROJETOS_CSV)
    return render_template('index.html', projetos=projetos)

@app.route('/criar', methods=['GET', 'POST'])
def criar_projeto():
    if request.method == 'POST':
        projetos = ler_csv(PROJETOS_CSV)
        novo_id = str(len(projetos) + 1)
        nome = request.form['nome']
        descricao = request.form['descricao']
        data = datetime.now().strftime('%Y-%m-%d')
        imagem = request.files['imagem']
        nome_img = ''

        if imagem and imagem.filename != '':
            nome_img = f"{novo_id}_{imagem.filename}"
            imagem.save(os.path.join(app.config['UPLOAD_FOLDER'], nome_img))

        projetos.append({
            'id': novo_id,
            'nome': nome,
            'descricao': descricao,
            'data': data,
            'img': nome_img
        })
        escrever_csv(PROJETOS_CSV, projetos, ['id', 'nome', 'descricao', 'data', 'img'])
        return redirect(url_for('index'))
    return render_template('criar_projeto.html')

@app.route('/editar/<id>', methods=['GET', 'POST'])
def editar_projeto(id):
    projetos = ler_csv(PROJETOS_CSV)
    projeto = next((p for p in projetos if p['id'] == id), None)

    if request.method == 'POST':
        projeto['nome'] = request.form['nome']
        projeto['descricao'] = request.form['descricao']
        escrever_csv(PROJETOS_CSV, projetos, ['id', 'nome', 'descricao', 'data', 'img'])
        return redirect(url_for('index'))

    return render_template('editar_projeto.html', projeto=projeto)

@app.route('/excluir/<id>')
def excluir_projeto(id):
    projetos = ler_csv(PROJETOS_CSV)
    tarefas = ler_csv(TAREFAS_CSV)
    projetos = [p for p in projetos if p['id'] != id]
    tarefas = [t for t in tarefas if t['id_projeto'] != id]
    escrever_csv(PROJETOS_CSV, projetos, ['id', 'nome', 'descricao', 'data', 'img'])
    escrever_csv(TAREFAS_CSV, tarefas, ['id', 'id_projeto', 'titulo', 'descricao', 'status'])
    return redirect(url_for('index'))

@app.route('/projeto/<id>', methods=['GET', 'POST'])
def visualizar_projeto(id):
    projetos = ler_csv(PROJETOS_CSV)
    tarefas = ler_csv(TAREFAS_CSV)
    projeto = next((p for p in projetos if p['id'] == id), None)
    status_filtro = request.args.get('status')

    tarefas_projeto = [t for t in tarefas if t['id_projeto'] == id]
    if status_filtro:
        tarefas_projeto = [t for t in tarefas_projeto if t['status'] == status_filtro]

    total = len(tarefas_projeto)
    concluidas = len([t for t in tarefas_projeto if t['status'] == 'Concluída'])
    progresso = int((concluidas / total) * 100) if total > 0 else 0

    return render_template('projeto.html', projeto=projeto, tarefas=tarefas_projeto, progresso=progresso)

@app.route('/adicionar_tarefa/<id_projeto>', methods=['POST'])
def adicionar_tarefa(id_projeto):
    tarefas = ler_csv(TAREFAS_CSV)
    novo_id = str(len(tarefas) + 1)
    titulo = request.form['titulo']
    descricao = request.form['descricao']
    status = request.form['status']
    tarefas.append({
        'id': novo_id,
        'id_projeto': id_projeto,
        'titulo': titulo,
        'descricao': descricao,
        'status': status
    })
    escrever_csv(TAREFAS_CSV, tarefas, ['id', 'id_projeto', 'titulo', 'descricao', 'status'])
    return redirect(url_for('visualizar_projeto', id=id_projeto))

@app.route('/editar_tarefa/<id>', methods=['GET', 'POST'])
def editar_tarefa(id):
    tarefas = ler_csv(TAREFAS_CSV)
    tarefa = next((t for t in tarefas if t['id'] == id), None)

    if request.method == 'POST':
        tarefa['titulo'] = request.form['titulo']
        tarefa['descricao'] = request.form['descricao']
        tarefa['status'] = request.form['status']
        escrever_csv(TAREFAS_CSV, tarefas, ['id', 'id_projeto', 'titulo', 'descricao', 'status'])
        return redirect(url_for('visualizar_projeto', id=tarefa['id_projeto']))

    return render_template('editar_tarefa.html', tarefa=tarefa)

@app.route('/excluir_tarefa/<id>')
def excluir_tarefa(id):
    tarefas = ler_csv(TAREFAS_CSV)
    tarefa = next((t for t in tarefas if t['id'] == id), None)
    tarefas = [t for t in tarefas if t['id'] != id]
    escrever_csv(TAREFAS_CSV, tarefas, ['id', 'id_projeto', 'titulo', 'descricao', 'status'])
    return redirect(url_for('visualizar_projeto', id=tarefa['id_projeto']))

if __name__ == '__main__':
    app.run(debug=True)
