# **Locust - Teste de Carga e Performance**

O **Locust** é uma ferramenta open-source para teste de carga que permite definir o comportamento do usuário utilizando código Python, simulando milhões de usuários simultâneos em seu sistema.

Para mais informações, acesse:  
[Locust.io](https://locust.io/)

### Instalação

Para instalar o Locust, siga as instruções disponíveis [aqui](https://locust.io/#install).

---

## **Exemplo de locustfile.py**

O arquivo `locustfile.py` define o comportamento dos usuários simulados. Aqui está um exemplo simples de como usar o Locust para testar um site.

```python
from locust import HttpUser, between, task

class WebsiteUser(HttpUser):
    # Define o tempo de espera entre as requisições
    wait_time = between(5, 15)  # Espera entre 5 e 15 segundos após cada tarefa
    
    # Função executada quando o usuário inicia
    def on_start(self):
        # Realiza o login simulando uma requisição POST
        self.client.post("/login", {
            "username": "test_user",
            "password": "senha_segura"
        })
    
    # Tarefa para acessar a página inicial
    @task
    def index(self):
        self.client.get("/")  # Requisição GET para a página inicial
        self.client.get("/static/assets.js")  # Requisição GET para um arquivo JS estático
        
    # Tarefa para acessar a página "Sobre"
    @task
    def about(self):
        self.client.get("/about/")  # Requisição GET para a página "Sobre"
```

### **Execução do Teste**

Para executar o teste de carga, use o seguinte comando no terminal:

```bash
locust -f locustfile.py
```

Isso iniciará o Locust com o arquivo de configuração `locustfile.py`, permitindo que você simule usuários e realize o teste de carga em seu sistema.

---

### **Principais Componentes**

- **HttpUser**: A classe base para definir usuários que fazem requisições HTTP.
- **wait_time**: Define o intervalo de tempo entre as requisições feitas pelos usuários simulados.
- **task**: Decorador utilizado para marcar funções que devem ser executadas como tarefas.

