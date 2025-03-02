from locust import HttpUser, task, between
import random
import string

class UserBehavior(HttpUser):
    wait_time = between(1, 3)  # Tempo entre as requisições (1 a 3 segundos)

    def on_start(self):
        """Essa função é executada quando o usuário começa a simular a carga"""
        self.email = self.generate_random_email()
        self.password = "password123"  # Senha fixa para todos os usuários

    def generate_random_email(self):
        """Gera um e-mail aleatório para o cadastro"""
        return ''.join(random.choices(string.ascii_lowercase + string.digits, k=10)) + "@example.com"

    @task(2)
    def register_user(self):
        """Simula o cadastro de um usuário"""
        response = self.client.post("/register", data={
            "email": self.email,
            "password": self.password
        })
        if response.status_code == 201:
            print(f"Usuário {self.email} registrado com sucesso!")
        else:
            print(f"Erro ao registrar o usuário {self.email}.")

    @task(1)
    def login_user(self):
        """Simula o login de um usuário"""
        response = self.client.post("/login", data={
            "email": self.email,
            "password": self.password
        })
        if response.status_code == 200:
            print(f"Login bem-sucedido para o usuário {self.email}")
        else:
            print(f"Erro no login para o usuário {self.email}.")

