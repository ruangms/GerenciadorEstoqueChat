##Gerado por IA
# 📦 Sistema de Gerenciamento de Estoque

## 📌 Visão Geral
Este projeto é um sistema completo de gerenciamento de estoque com:
- **Backend** em Python (FastAPI + Socket)
- **Frontend** web responsivo
- **Persistência** em JSON e histórico em CSV
- **Comunicação** em tempo real via sockets

## 🏗️ Estrutura do Projeto

```
estoque/
│
├── frontservidor.py    # Frontend web (FastAPI)
├── Servidor.py         # Servidor principal (Socket)
├── Cliente.py          # Cliente para interação via terminal
├── estoque.py          # Lógica de negócios do estoque
├── estoque.json        # Dados persistidos (gerado automaticamente)
└── historico.csv       # Registro de operações (gerado automaticamente)
```

## 🔧 Funcionalidades Principais

### 1. `estoque.py` (Núcleo do Sistema)
```python
class NoArvore:
    """Estrutura de árvore para organização hierárquica do estoque"""
    def adicionar(self, caminho, quantidade): ...
    def remover(self, caminho, quantidade): ...
    def listar(self, nivel=0): ...

class Estoque:
    """Gerencia todas as operações de estoque"""
    def adicionar(self, categoria, produto, quantidade): ...
    def remover(self, categoria, produto, quantidade): ...
    def listar(self): ...
    def _salvar(self): ...          # Persiste os dados em JSON
    def _carregar(self): ...        # Carrega dados do arquivo
    def _backup(self): ...          # Cria backup automático
    def _registrar_historico(...):  # Log de operações em CSV
```

### 2. `Servidor.py` (Servidor Socket)
```python
def lidar_com_cliente(cliente): 
    """Processa comandos recebidos dos clientes"""
    # Comandos suportados:
    # /estoque add [categoria] [produto] [quantidade]
    # /estoque rm [categoria] [produto] [quantidade]
    # /estoque (lista tudo)

def broadcast(mensagem, remetente):
    """Envia mensagens para todos os clientes conectados"""
```

### 3. `frontservidor.py` (Interface Web)
```python
@app.get("/")            # Dashboard HTML
@app.get("/estoque")     # Retorna dados em texto puro
# Interface auto-atualizável a cada 3 segundos
```

### 4. `Cliente.py` (CLI Interativo)
```python
def receber(sock):       # Thread para receber mensagens
def iniciar_cliente():   # Conexão e loop de comandos
```

## 🚀 Como Executar

1. **Inicie o servidor principal**:
   ```bash
   python Servidor.py
   ```

2. **Inicie o frontend web**:
   ```bash
   python frontservidor.py
   ```
   Acesse: http://localhost:8000

3. **Conecte clientes** (em terminais separados):
   ```bash
   python Cliente.py
   ```

## 📋 Comandos Disponíveis (via Cliente)

| Comando | Exemplo | Descrição |
|---------|---------|-----------|
| `/estoque add` | `/estoque add Alimentos Arroz 50` | Adiciona itens |
| `/estoque rm` | `/estoque rm Alimentos Arroz 10` | Remove itens |
| `/estoque` | `/estoque` | Lista todo o estoque |
| `/sair` | `/sair` | Desconecta o cliente |

## 🔄 Fluxo de Dados

1. Cliente envia comando via socket
2. Servidor processa e atualiza o estoque
3. Alterações são salvas em `estoque.json`
4. Frontend web busca atualizações periodicamente
5. Histórico é registrado em `historico.csv`

## 📊 Exemplo de Saída

```
- Estoque
  - Alimentos (40 unid.)
    - Arroz (30 unid.)
    - Feijão (10 unid.)
  - Bebidas
    - Refrigerante (15 unid.)
```
