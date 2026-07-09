from src.lss_paint.model.figuras import Linha, Rabisco, Retangulo, Oval, Circulo, Poligono


class PaintController:
    def __init__(self, model):
        self.model = model
        self.view = None

    def associar_visao(self, view):
        self.view = view

    def mudar_ferramenta(self, nova_ferramenta):
        self.model.ferramenta = nova_ferramenta
        self.view.atualizar_visibilidade_lados(nova_ferramenta == "poligono")

    def mudar_num_lados(self, valor):
        try:
            self.model.num_lados_poligono = max(3, int(valor))
        except ValueError:
            pass

    # ===== Cores =====

    def set_cor_alvo(self, alvo):
        self.model.cor_alvo = alvo
        self.view.atualizar_botoes_cor(alvo)

    def selecionar_cor(self, cor):
        cor_real = "" if cor == "transparente" else cor
        cor_botao = "white" if cor == "transparente" else cor

        if self.model.cor_alvo == "borda":
            self.model.cor_atual_borda = cor_real
        else:
            self.model.cor_atual_preenchimento = cor_real

        self.view.atualizar_cor_botao(self.model.cor_alvo, cor_botao)

    # ===== Desenho =====

    def iniciar_figura(self, event):
        m = self.model
        x, y = self.view.canvas_coords(event)

        match m.ferramenta:
            case 'linha':
                m.nova_figura = Linha([x, y, x, y], m.cor_atual_borda, m.cor_atual_preenchimento)
            case 'rabisco':
                m.nova_figura = Rabisco([(x, y)], m.cor_atual_borda, m.cor_atual_preenchimento)
            case 'retangulo':
                m.nova_figura = Retangulo([x, y, x, y], m.cor_atual_borda, m.cor_atual_preenchimento)
            case 'oval':
                m.nova_figura = Oval([x, y, x, y], m.cor_atual_borda, m.cor_atual_preenchimento)
            case 'circulo':
                m.nova_figura = Circulo([x, y, x, y], m.cor_atual_borda, m.cor_atual_preenchimento)
            case 'poligono':
                m.nova_figura = Poligono([x, y, x, y], m.cor_atual_borda, m.cor_atual_preenchimento, num_lados=m.num_lados_poligono)

    def atualizar_figura(self, event):
        m = self.model
        if not m.nova_figura:
            return

        x, y = self.view.canvas_coords(event)

        if isinstance(m.nova_figura, Rabisco):
            m.nova_figura.coordenadas.append((x, y))
        else:
            m.nova_figura.coordenadas[2] = x
            m.nova_figura.coordenadas[3] = y

        self.view.desenhar_preview(m.nova_figura)

    def incluir_figura(self, event):
        m = self.model
        if m.nova_figura:
            m.figuras.append(m.nova_figura)
        m.nova_figura = None

        self.view.redesenhar_tudo(m.figuras)