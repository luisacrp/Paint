class DesenhoModel:
    def __init__(self):
        self.figuras = []
        self.nova_figura = None
        self.ferramenta = "rabisco"
        self.cor_atual_borda = "black"
        self.cor_atual_preenchimento = "" 
        self.cor_alvo = "borda"
        self.num_lados_poligono = 6
        
