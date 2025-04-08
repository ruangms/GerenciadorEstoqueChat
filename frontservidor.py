# frontservidor.py
from fastapi import FastAPI
from fastapi.responses import HTMLResponse, PlainTextResponse
from fastapi.middleware.cors import CORSMiddleware
from estoque import Estoque

app = FastAPI()
estoque = Estoque()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/", response_class=HTMLResponse)
def dashboard_html():
    return """
    <!DOCTYPE html>
    <html>
    <head>
        <title>📦 Estoque</title>
        <style>
            body { font-family: sans-serif; padding: 2rem; background: #f9f9f9; }
            pre { background: white; padding: 1rem; border-radius: 8px; box-shadow: 0 0 5px #ccc; }
            button { padding: 0.5rem 1rem; margin-bottom: 1rem; }
        </style>
    </head>
    <body>
        <h1>📦 Dashboard de Estoque</h1>
        <button onclick="carregarEstoque()">🔄 Atualizar</button>
        <pre id="saida">Carregando...</pre>
        <script>
            async function carregarEstoque() {
                const resp = await fetch('/estoque');
                const txt = await resp.text();
                document.getElementById('saida').textContent = txt;
            }
            carregarEstoque();
        </script>
    </body>
    </html>
    """

@app.get("/estoque", response_class=PlainTextResponse)
def listar_estoque():
    return estoque.listar()

# Adicione estas linhas para iniciar o servidor:
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)