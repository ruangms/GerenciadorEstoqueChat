# estoque.py
import json
import os
from datetime import datetime

class NoArvore:
    def __init__(self, nome):
        self.nome = nome
        self.filhos = {}
        self.quantidade = 0

    def adicionar(self, caminho, quantidade):
        if not caminho:
            self.quantidade += quantidade
            return
        nome_filho = caminho[0]
        if nome_filho not in self.filhos:
            self.filhos[nome_filho] = NoArvore(nome_filho)
        self.filhos[nome_filho].adicionar(caminho[1:], quantidade)

    def remover(self, categoria, produto, quantidade):
        caminho = [categoria, produto]
        quantidade_atual = self._obter_quantidade(caminho)  # você pode implementar esse método
        if quantidade_atual < quantidade:
            return False
        self.raiz.remover(caminho, quantidade)
        self._registrar_historico("REMOVER", caminho, quantidade)
        self._salvar()
        return True


    def listar(self, nivel=0):
        espacos = "  " * nivel
        saida = f"{espacos}- {self.nome} ({self.quantidade} unid.)\n" if self.quantidade > 0 else f"{espacos}- {self.nome}\n"
        for filho in self.filhos.values():
            saida += filho.listar(nivel + 1)
        return saida

    def listar_categorias(self, nivel=0):
        espacos = "  " * nivel
        saida = f"{espacos}- {self.nome}\n"
        for filho in self.filhos.values():
            saida += filho.listar_categorias(nivel + 1)
        return saida

    def to_dict(self):
        return {
            "nome": self.nome,
            "quantidade": self.quantidade,
            "filhos": {k: v.to_dict() for k, v in self.filhos.items()}
        }

    @staticmethod
    def from_dict(d):
        no = NoArvore(d['nome'])
        no.quantidade = d.get('quantidade', 0)
        for k, v in d.get('filhos', {}).items():
            no.filhos[k] = NoArvore.from_dict(v)
        return no

class Estoque:
    def __init__(self, arquivo='estoque.json', historico_arquivo='historico.csv'):
        self.arquivo = arquivo
        self.historico_arquivo = historico_arquivo
        self.raiz = NoArvore("Estoque")
        self._carregar()

    def _salvar(self):
        with open(self.arquivo, 'w', encoding='utf-8') as f:
            json.dump(self.raiz.to_dict(), f, ensure_ascii=False, indent=2)
        self._backup()

    def _carregar(self):
        if os.path.exists(self.arquivo):
            with open(self.arquivo, 'r', encoding='utf-8') as f:
                dados = json.load(f)
                self.raiz = NoArvore.from_dict(dados)

    def _backup(self):
        data = datetime.now().strftime('%Y%m%d_%H%M%S')
        nome_backup = f"estoque_backup_{data}.json"
        with open(nome_backup, 'w', encoding='utf-8') as f:
            json.dump(self.raiz.to_dict(), f, ensure_ascii=False, indent=2)

    def _registrar_historico(self, acao, caminho, quantidade):
        data = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        categoria = caminho[0] if caminho else ""
        produto = caminho[-1] if len(caminho) > 1 else ""
        linha = f"{data};{acao};{categoria};{produto};{quantidade}\n"
        with open(self.historico_arquivo, 'a', encoding='utf-8') as f:
            f.write(linha)

    def adicionar(self, categoria, produto, quantidade):
        caminho = [categoria, produto]
        self.raiz.adicionar(caminho, quantidade)
        self._registrar_historico("ADICIONAR", caminho, quantidade)
        self._salvar()

    def remover(self, categoria, produto, quantidade):
        caminho = [categoria, produto]
        self.raiz.remover(caminho, quantidade)
        self._registrar_historico("REMOVER", caminho, quantidade)
        self._salvar()

    def adicionar_categoria(self, categoria):
        self.raiz.adicionar([categoria], 0)
        self._registrar_historico("ADD_CATEGORIA", [categoria], 0)
        self._salvar()

    def adicionar_subcategoria(self, categoria, subcategoria):
        self.raiz.adicionar([categoria, subcategoria], 0)
        self._registrar_historico("ADD_SUBCATEGORIA", [categoria, subcategoria], 0)
        self._salvar()

    def adicionar_caminho(self, caminho, quantidade):
        self.raiz.adicionar(caminho, quantidade)
        self._registrar_historico("ADICIONAR_CAMINHO", caminho, quantidade)
        self._salvar()

    def listar(self):
        return self.raiz.listar()

    def listar_categorias(self):
        return self.raiz.listar_categorias()
