from flask import Flask, request, jsonify, render_template
import redis

app = Flask(__name__)

# Conectar ao Redis
r = redis.StrictRedis(host='localhost', port=6379, db=0, decode_responses=True)

# Função para verificar se o usuário existe no Redis
def get_user_from_redis(email):
    user_key = f"user:{email}"
    user_data = r.hgetall(user_key)
    return user_data

@app.route('/')
def index():
    return "Página inicial"

@app.route('/about/')
def about():
    return "Sobre nós"

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        return render_template('login.html')  # Exibe o formulário de login
    
    elif request.method == 'POST':
        data = request.form
        email = data.get("email")
        password = data.get("password")

        # Tentar obter o usuário do Redis
        user_data = get_user_from_redis(email)

        if user_data and user_data.get("password") == password:
            return jsonify({"message": f"Login bem-sucedido! Bem-vindo, {email}"}), 200

        return jsonify({"error": "Credenciais invalidas"}), 401

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'GET':
        return render_template('register.html')  # Renderiza o formulário de cadastro
    elif request.method == 'POST':
        data = request.form
        email = data.get("email")
        password = data.get("password")

        if not email or not password:
            return jsonify({"error": "Todos os campos sao obrigatórios"}), 400

        # Verificar se o usuário já existe
        if get_user_from_redis(email):
            return jsonify({"error": "Usuario ja registrado com esse email"}), 400

        # Salvar o usuário no Redis usando um hash
        user_key = f"user:{email}"
        r.hset(user_key, "password", password)

        return jsonify({"message": "Usuario registrado com sucesso!"}), 201

@app.route('/static/assets.js')
def static_assets():
    return "console.log('Arquivo de assets carregado');"

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
