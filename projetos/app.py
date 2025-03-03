from flask import Flask, request, jsonify, render_template
import redis
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)

# Configuração do Redis
REDIS_HOST = "localhost"
REDIS_PORT = 6379
REDIS_DB = 0
r = redis.StrictRedis(host=REDIS_HOST, port=REDIS_PORT, db=REDIS_DB, decode_responses=True)

# Função para obter usuário do Redis
def get_user_from_redis(email):
    user_key = f"user:{email}"
    return r.hgetall(user_key)

# Função para resposta padronizada
def response(success, message, status=200):
    return jsonify({"success": success, "message": message}), status

@app.route('/')
def index():
    return "Página inicial"

@app.route('/about/')
def about():
    return "Sobre nós"

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        return render_template('login.html')
    
    data = request.form
    email = data.get("email")
    password = data.get("password")

    user_data = get_user_from_redis(email)
    if user_data and check_password_hash(user_data.get("password"), password):
        return response(True, f"Login bem-sucedido! Bem-vindo, {email}")
    
    return response(False, "Credenciais invalidas", 401)

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'GET':
        return render_template('register.html')
    
    data = request.form
    email = data.get("email")
    password = data.get("password")

    if not email or not password:
        return response(False, "Todos os campos sao obrigatórios", 400)

    if get_user_from_redis(email):
        return response(False, "Usuario ja registrado com esse email", 400)

    hashed_password = generate_password_hash(password)
    user_key = f"user:{email}"
    r.hset(user_key, "password", hashed_password)

    return response(True, "Usuario registrado com sucesso!", 201)

@app.route('/static/assets.js')
def static_assets():
    return "console.log('Arquivo de assets carregado');"

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
