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
        usuario = request.form['usuario'].strip()
        senha = request.form['senha'].strip()

        if not usuario or not senha:
            flash('Preencha todos os campos', 'danger')
            return redirect(url_for('login'))

        # Verificação simples (substitua por verificação no banco de dados)
        if usuario in usuarios and usuarios[usuario] == senha:
            session['usuario'] = usuario
            session['nome_usuario'] = usuario.capitalize()  # Armazena o nome do usuário
            flash(f'Bem-vindo, {usuario.capitalize()}!', 'success')
            return redirect(url_for('home'))
        else:
            flash('Usuário ou senha incorretos', 'danger')
            return redirect(url_for('login'))

    # Se já estiver logado, redireciona para home
    if 'usuario' in session:
        return redirect(url_for('home'))

    return render_template('login.html')

@app.route('/esqueci-senha', methods=['GET', 'POST'])
def esqueci_senha():
    if request.method == 'POST':
        email = request.form.get('email', '').strip()
        
        if not email:
            flash('Por favor, informe seu e-mail', 'danger')
            return redirect(url_for('esqueci_senha'))
        
        # Aqui você implementaria o envio real do e-mail
        flash('Se o e-mail estiver cadastrado, enviaremos instruções para recuperação', 'info')
        return redirect(url_for('login'))
    
    return render_template('esqueci_senha.html')


@app.route('/logout')
def logout():
    session.pop('usuario', None)
    session.pop('nome_usuario', None)
    flash('Você saiu do sistema', 'info')
    return redirect(url_for('login'))

def criar_banco_de_dados():
    conn = sqlite3.connect('usuarios.db')
    cursor = conn.cursor()
    
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS usuarios (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nome TEXT NOT NULL,
        nome_social TEXT,
        prontuario TEXT,
        situacao_cadastro TEXT,
        data_entrada_saida TEXT,
        cpf TEXT,
        rg TEXT,
        data_emissao_rg TEXT,
        cartao_nascimento TEXT,
        livro_folha TEXT,
        cartorio TEXT,
        naturalidade TEXT,
        sexo TEXT,
        data_nascimento TEXT,
        ocupacao TEXT,
        carteira_pcd TEXT,
        cartao_nis TEXT,
        cartao_sus TEXT,
        raca_cor TEXT,
        mobilidade TEXT,
        tipo_deficiencia TEXT,
        transtornos TEXT,
        cid10 TEXT,
        cid10_opcional1 TEXT,
        cid10_opcional2 TEXT,
        cid11 TEXT,
        area TEXT,
        cep TEXT,
        endereco TEXT,
        numero TEXT,
        complemento TEXT,
        bairro TEXT,
        cidade TEXT,
        uf TEXT,
        email TEXT,
        telefone_residencial TEXT,
        telefone_recados TEXT,
        pessoa_contato TEXT,
        mae_nome TEXT,
        mae_cpf TEXT,
        mae_telefone TEXT,
        mae_email TEXT,
        mae_ocupacao TEXT,
        pai_nome TEXT,
        pai_cpf TEXT,
        pai_telefone TEXT,
        pai_email TEXT,
        pai_ocupacao TEXT,
        medicamento TEXT,
        qual_medicamento TEXT,
        alergia TEXT,
        qual_alergia TEXT,
        comorbidade TEXT,
        qual_comorbidade TEXT,
        convenio TEXT,
        qual_convenio TEXT,
        atividade_fisica TEXT,
        data_liberacao TEXT,
        uso_imagem TEXT,
        transporte_ida TEXT,
        transporte_volta TEXT,
        observacoes TEXT,
        notificacao_whatsapp TEXT,
        data_cadastro TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    ''')
    conn.commit()
    conn.close()

# Chamar a função para criar o banco quando o aplicativo iniciar
criar_banco_de_dados()

@app.route('/usuario/<int:id>/editar', methods=['GET', 'POST'])
def editar_usuario(id):
    if 'usuario' not in session:
        return redirect(url_for('login'))

    conn = sqlite3.connect('usuarios.db')
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()

    if request.method == 'POST':
        try:
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

            set_clause = ', '.join([f"{campo} = ?" for campo in campos])
            valores = [dados_limpos.get(campo, '') for campo in campos]
            valores.append(id)

            cursor.execute(f'''
                UPDATE usuarios 
                SET {set_clause}
                WHERE id = ?
            ''', valores)
            conn.commit()
            conn.close()

            flash('Usuário atualizado com sucesso!', 'success')
            return redirect(url_for('visualizar_usuario', id=id))

        except Exception as e:
            conn.rollback()
            conn.close()
            flash(f'Erro ao atualizar usuário: {str(e)}', 'danger')
            return redirect(url_for('editar_usuario', id=id))

    # GET - Buscar usuário para edição
    cursor.execute("SELECT * FROM usuarios WHERE id = ?", (id,))
    usuario = cursor.fetchone()
    conn.close()

    if not usuario:
        flash('Usuário não encontrado', 'danger')
        return redirect(url_for('listar_usuarios'))

    return render_template('editar_usuario.html', usuario=usuario)


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
        try:
            dados = request.form.to_dict(flat=False)
            dados_limpos = {}

            # Processa os dados do formulário
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

            valores = [dados_limpos.get(campo, '') for campo in campos]

            conn = sqlite3.connect('usuarios.db')
            cursor = conn.cursor()
            
            # Insere os dados no banco
            cursor.execute(f'''
                INSERT INTO usuarios ({','.join(campos)})
                VALUES ({','.join(['?'] * len(campos))})
            ''', valores)
            
            conn.commit()
            conn.close()

            flash('Cadastro realizado com sucesso!', 'success')
            return redirect(url_for('listar_usuarios'))

        except Exception as e:
            flash(f'Erro ao cadastrar: {str(e)}', 'danger')
            return redirect(url_for('cadastro'))

    return render_template('cadastro.html')

@app.route('/usuarios')
def listar_usuarios():
    if 'usuario' not in session:
        return redirect(url_for('login'))

    situacao = request.args.get('situacao')
    busca = request.args.get('busca')

    conn = sqlite3.connect('usuarios.db')
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()

    query = "SELECT id, nome, cpf, situacao_cadastro, data_cadastro FROM usuarios"
    conditions = []
    params = []

    if situacao and situacao != 'todos':
        conditions.append("situacao_cadastro = ?")
        params.append(situacao)

    if busca:
        conditions.append("(nome LIKE ? OR cpf LIKE ?)")
        params.extend([f"%{busca}%", f"%{busca}%"])

    if conditions:
        query += " WHERE " + " AND ".join(conditions)

    query += " ORDER BY nome ASC"
    cursor.execute(query, params)
    usuarios = cursor.fetchall()
    conn.close()

    return render_template('usuarios.html', usuarios=usuarios, situacao=situacao, busca=busca)

@app.route('/usuario/<int:id>')
def visualizar_usuario(id):
    if 'usuario' not in session:
        return redirect(url_for('login'))

    conn = sqlite3.connect('usuarios.db')
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM usuarios WHERE id = ?", (id,))
    usuario = cursor.fetchone()
    conn.close()

    if not usuario:
        flash('Usuário não encontrado', 'danger')
        return redirect(url_for('listar_usuarios'))

    return render_template('visualizar_usuario.html', usuario=usuario)



@app.route('/sobre')
def sobre():
    return render_template('sobre.html')


if __name__ == '__main__':
    app.run(debug=True)
