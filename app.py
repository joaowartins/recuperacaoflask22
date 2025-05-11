from flask import Flask, render_template, request, redirect, url_for
import csv
import os

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'static/img'

PROJETOS_CSV = 'projetos.csv'
TAREFAS_CSV = 'tarefas.csv'

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

@app.route('/')
def index():
    projetos = ler_csv(PROJETOS_CSV)
    return render_template('index.html', projetos=projetos)

@app.route('/criar', methods=['GET', 'POST'])
def criar():
    if request.method == 'POST':
        projetos = ler_csv(PROJETOS_CSV)
        novo_id = str(len(projetos) + 1)
        nome = request.form['nome']
        descricao = request.form['descricao']
        imagem = request.files['imagem']
        nome_img = ''

        if imagem and imagem.filename != '':
            nome_img = f"{novo_id}_{imagem.filename}"
            imagem.save(os.path.join(app.config['UPLOAD_FOLDER'], nome_img))

        projetos.append({
            'id': novo_id,
            'nome': nome,
            'descricao': descricao,
            'img': nome_img
        })

        escrever_csv(PROJETOS_CSV, projetos, ['id', 'nome', 'descricao', 'img'])
        return redirect('/')
    return render_template('criar_projeto.html')

@app.route('/editar/<id>', methods=['GET', 'POST'])
def editar(id):
    projetos = ler_csv(PROJETOS_CSV)
    for projeto in projetos:
        if projeto['id'] == id:
            if request.method == 'POST':
                projeto['nome'] = request.form['nome']
                projeto['descricao'] = request.form['descricao']
                escrever_csv(PROJETOS_CSV, projetos, ['id', 'nome', 'descricao', 'img'])
                return redirect('/')
            return render_template('editar_projeto.html', projeto=projeto)
    return 'Projeto não encontrado'

@app.route('/excluir/<id>')
def excluir(id):
    projetos = ler_csv(PROJETOS_CSV)
    tarefas = ler_csv(TAREFAS_CSV)
    projetos = [p for p in projetos if p['id'] != id]
    tarefas = [t for t in tarefas if t['id_projeto'] != id]
    escrever_csv(PROJETOS_CSV, projetos, ['id', 'nome', 'descricao', 'img'])
    escrever_csv(TAREFAS_CSV, tarefas, ['id', 'id_projeto', 'titulo', 'descricao', 'status'])
    return redirect('/')

@app.route('/projeto/<id>', methods=['GET', 'POST'])
def projeto(id):
    projetos = ler_csv(PROJETOS_CSV)
    tarefas = ler_csv(TAREFAS_CSV)

    for p in projetos:
        if p['id'] == id:
            projeto = p
            break
    else:
        return 'Projeto não encontrado'

    tarefas_projeto = [t for t in tarefas if t['id_projeto'] == id]

    total = len(tarefas_projeto)
    concluidas = 0
    for t in tarefas_projeto:
        if t['status'] == 'Concluída':
            concluidas += 1
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
    return redirect(f'/projeto/{id_projeto}')

@app.route('/editar_tarefa/<id>', methods=['GET', 'POST'])
def editar_tarefa(id):
    tarefas = ler_csv(TAREFAS_CSV)
    for tarefa in tarefas:
        if tarefa['id'] == id:
            if request.method == 'POST':
                tarefa['titulo'] = request.form['titulo']
                tarefa['descricao'] = request.form['descricao']
                tarefa['status'] = request.form['status']
                escrever_csv(TAREFAS_CSV, tarefas, ['id', 'id_projeto', 'titulo', 'descricao', 'status'])
                return redirect(f"/projeto/{tarefa['id_projeto']}")
            return render_template('editar_tarefa.html', tarefa=tarefa)
    return 'Tarefa não encontrada'

@app.route('/excluir_tarefa/<id>')
def excluir_tarefa(id):
    tarefas = ler_csv(TAREFAS_CSV)
    nova_lista = []
    id_projeto = ''

    for tarefa in tarefas:
        if tarefa['id'] == id:
            id_projeto = tarefa['id_projeto']
        else:
            nova_lista.append(tarefa)

    escrever_csv(TAREFAS_CSV, nova_lista, ['id', 'id_projeto', 'titulo', 'descricao', 'status'])
    return redirect(f"/projeto/{id_projeto}")

if __name__ == '__main__':
    app.run(debug=True)