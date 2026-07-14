import pickle
from src.lss_paint.model.figuras import Linha, Rabisco, Retangulo, Oval, Circulo, Poligono

class DesenhoModel:
    def __init__(self):
        self.figuras = []
        self.nova_figura = None
        self.ferramenta = "rabisco"
        self.cor_atual_borda = "black"
        self.cor_atual_preenchimento = "" 
        self.cor_alvo = "borda"
        self.num_lados_poligono = 6

    def salvar_arquivo(self, caminho):
        with open(caminho, 'wb') as f:
            pickle.dump(self.figuras, f)

    def carregar_arquivo(self, caminho):
        with open(caminho, 'rb') as f:
            self.figuras = pickle.load(f)
