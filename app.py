from flask import Flask, render_template, request, redirect, url_for, session, flash, send_from_directory
import os
import sqlite3
import tempfile



app = Flask(
    __name__, static_folder='/home/gustavson-barros/Área de trabalho/apae-system-python/static')
app.secret_key = 'sua_chave_secreta_aqui'


usuarios = {
    'admin': 'senha123',
    'funcionario': 'senha456'
}


@app.route('/')
def home():
    if 'usuario' in session:
        return render_template('index.html')
    return redirect(url_for('login'))


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        usuario = request.form['usuario']
        senha = request.form['senha']

        if usuario in usuarios and usuarios[usuario] == senha:
            session['usuario'] = usuario
            flash('Login realizado com sucesso!', 'success')
            return redirect(url_for('home'))
        else:
            flash('Usuário ou senha incorretos', 'danger')

    return render_template('login.html')


@app.route('/esqueci-senha', methods=['GET', 'POST'])
def esqueci_senha():
    if request.method == 'POST':
        email = request.form.get('email')
        # Aqui você poderia verificar se o e-mail existe e enviar um e-mail de recuperação
        flash('Se o e-mail informado estiver cadastrado, enviaremos instruções para recuperar a senha.', 'info')
        return redirect(url_for('login'))
    return render_template('esqueci_senha.html')


@app.route('/logout')
def logout():
    session.pop('usuario', None)
    return redirect(url_for('login'))


@app.route('/usuario/<int:id>/editar', methods=['GET', 'POST'])
def editar_usuario(id):
    if 'usuario' not in session:
        return redirect(url_for('login'))

    conn = sqlite3.connect('usuarios.db')
    cursor = conn.cursor()

    if request.method == 'POST':
        dados = request.form.to_dict(flat=False)
        dados_limpos = {}

        for chave, valor in dados.items():
            if isinstance(valor, list):
                dados_limpos[chave] = ','.join(valor)
            else:
                dados_limpos[chave] = valor

        campos = [
            'nome', 'nome_social', 'prontuario', 'situacao_cadastro', 'data_entrada_saida',
            'cpf', 'rg', 'data_emissao_rg', 'cartao_nascimento', 'livro_folha', 'cartorio',
            'naturalidade', 'sexo', 'data_nascimento', 'ocupacao', 'carteira_pcd', 'cartao_nis',
            'cartao_sus', 'raca_cor', 'mobilidade', 'tipo_deficiencia', 'transtornos',
            'cid10', 'cid10_opcional1', 'cid10_opcional2', 'cid11', 'area', 'cep', 'endereco',
            'numero', 'complemento', 'bairro', 'cidade', 'uf', 'email', 'telefone_residencial',
            'telefone_recados', 'pessoa_contato', 'mae_nome', 'mae_cpf', 'mae_telefone',
            'mae_email', 'mae_ocupacao', 'pai_nome', 'pai_cpf', 'pai_telefone', 'pai_email',
            'pai_ocupacao', 'medicamento', 'qual_medicamento', 'alergia', 'qual_alergia',
            'comorbidade', 'qual_comorbidade', 'convenio', 'qual_convenio', 'atividade_fisica',
            'data_liberacao', 'uso_imagem', 'transporte_ida', 'transporte_volta',
            'observacoes', 'notificacao_whatsapp'
        ]

        # Monta a string de atualização
        set_clause = ', '.join([f"{campo} = ?" for campo in campos])
        valores = [dados_limpos.get(campo, '') for campo in campos]
        valores.append(id)  # Adiciona o ID no final para o WHERE

        cursor.execute(f'''
            UPDATE usuarios 
            SET {set_clause}
            WHERE id = ?
        ''', valores)
        conn.commit()
        conn.close()

        flash('Usuário atualizado com sucesso!', 'success')
        return redirect(url_for('listar_usuarios'))

    # Se for GET, busca os dados do usuário
    cursor.execute("SELECT * FROM usuarios WHERE id = ?", (id,))
    usuario = cursor.fetchone()
    conn.close()

    if not usuario:
        flash('Usuário não encontrado', 'danger')
        return redirect(url_for('listar_usuarios'))

    # Converte a linha do banco em um dicionário para facilitar no template
    campos = [desc[0] for desc in cursor.description]
    usuario_dict = dict(zip(campos, usuario))

    return render_template('editar_usuario.html', usuario=usuario_dict)


@app.route('/usuario/<int:id>/excluir', methods=['POST'])
def excluir_usuario(id):
    if 'usuario' not in session:
        return redirect(url_for('login'))

    conn = sqlite3.connect('usuarios.db')
    cursor = conn.cursor()
    cursor.execute("DELETE FROM usuarios WHERE id = ?", (id,))
    conn.commit()
    conn.close()

    flash('Usuário excluído com sucesso!', 'success')
    return redirect(url_for('listar_usuarios'))


@app.route('/cadastro', methods=['GET', 'POST'])
def cadastro():
    if 'usuario' not in session:
        return redirect(url_for('login'))

    if request.method == 'POST':
        dados = request.form.to_dict(flat=False)  # flat=False pega listas
        dados_limpos = {}

        for chave, valor in dados.items():
            if isinstance(valor, list):
                dados_limpos[chave] = ','.join(
                    valor)  # Junta listas com vírgula
            else:
                dados_limpos[chave] = valor

        campos = [
            'nome', 'nome_social', 'prontuario', 'situacao_cadastro', 'data_entrada_saida',
            'cpf', 'rg', 'data_emissao_rg', 'cartao_nascimento', 'livro_folha', 'cartorio',
            'naturalidade', 'sexo', 'data_nascimento', 'ocupacao', 'carteira_pcd', 'cartao_nis',
            'cartao_sus', 'raca_cor', 'mobilidade', 'tipo_deficiencia', 'transtornos',
            'cid10', 'cid10_opcional1', 'cid10_opcional2', 'cid11', 'area', 'cep', 'endereco',
            'numero', 'complemento', 'bairro', 'cidade', 'uf', 'email', 'telefone_residencial',
            'telefone_recados', 'pessoa_contato', 'mae_nome', 'mae_cpf', 'mae_telefone',
            'mae_email', 'mae_ocupacao', 'pai_nome', 'pai_cpf', 'pai_telefone', 'pai_email',
            'pai_ocupacao', 'medicamento', 'qual_medicamento', 'alergia', 'qual_alergia',
            'comorbidade', 'qual_comorbidade', 'convenio', 'qual_convenio', 'atividade_fisica',
            'data_liberacao', 'uso_imagem', 'transporte_ida', 'transporte_volta',
            'observacoes', 'notificacao_whatsapp'
        ]

        # Completa com valores vazios
        valores = [dados_limpos.get(campo, '') for campo in campos]

        conn = sqlite3.connect('usuarios.db')
        cursor = conn.cursor()
        cursor.execute(f'''
            INSERT INTO usuarios ({','.join(campos)})
            VALUES ({','.join(['?'] * len(campos))})
        ''', valores)
        conn.commit()
        conn.close()

        flash('Cadastro realizado com sucesso!', 'success')
        return redirect(url_for('home'))

    return render_template('cadastro.html')


@app.route('/usuarios')
def listar_usuarios():
    situacao = request.args.get('situacao')
    busca = request.args.get('busca')

    conn = sqlite3.connect('usuarios.db')
    cursor = conn.cursor()

    query = "SELECT id, nome, cpf, situacao_cadastro FROM usuarios"
    conditions = []
    params = []

    if situacao:
        conditions.append("situacao_cadastro = ?")
        params.append(situacao)

    if busca:
        conditions.append("(nome LIKE ? OR cpf LIKE ?)")
        params.extend([f"%{busca}%", f"%{busca}%"])

    if conditions:
        query += " WHERE " + " AND ".join(conditions)

    cursor.execute(query, params)
    usuarios = cursor.fetchall()
    conn.close()

    return render_template('usuarios.html', usuarios=usuarios)




@app.route('/sobre')
def sobre():
    return render_template('sobre.html')


if __name__ == '__main__':
    app.run(debug=True)
