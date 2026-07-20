import math

class Figura: 
    """
    Superclasse abstrata que define a estrutura básica de qualquer forma geométrica no sistema.
    
    Responsabilidade: Armazenar coordenadas, cores e fornecer o comportamento padrão de traçado.
    
    @author Luísa Costa, Sarah Beatriz e Sayran Felix
    @version 1.0
    @since 2026-07-13
    """
    def __init__(self, coordenadas, cor_borda, cor_preenchimento = ""):
        """
        Construtor da superclasse Figura.
        
        @param coordenadas: Lista contendo as coordenadas da figura [x1, y1, x2, y2].
        @param cor_borda: String hexadecimal representando a cor do contorno.
        @param cor_preenchimento: String hexadecimal representando a cor interna (opcional).
        @throws Nenhuma exceção.
        """
        self.coordenadas = coordenadas
        self.cor_borda = cor_borda
        self.cor_preenchimento = cor_preenchimento 

    def desenhar(self, canvas, tag = ""):
        """
        Método base de desenho que determina as propriedades visuais de visualização (preview).
        
        @param canvas: Objeto Canvas do Tkinter onde a figura será renderizada.
        @param tag: Tag de identificação ("preview" ou "definitivo").
        @return Tupla definindo o padrão de tracejado ou None.
        @throws Nenhuma exceção.
        """
        tracejado = (4, 2) if tag == "preview" else None
        return tracejado


class Linha(Figura):
    """Classe responsável pelo traçado de linhas retas. Herda de Figura."""
    def desenhar(self, canvas, tag=""):
        tracejado = super().desenhar(canvas, tag)
        canvas.create_line(self.coordenadas[0], self.coordenadas[1], self.coordenadas[2], self.coordenadas[3], fill=self.cor_borda, dash=tracejado, tags=tag)


class Rabisco(Figura):
    """Classe responsável pelo traçado à mão livre (lápis). Herda de Figura."""
    def desenhar(self, canvas, tag=""):
        tracejado = super().desenhar(canvas, tag)
        canvas.create_line(self.coordenadas, fill=self.cor_borda, dash=tracejado, tags=tag)


class Retangulo(Figura):
    """Classe responsável pela renderização de retângulos. Herda de Figura."""
    def desenhar(self, canvas, tag=""):
        tracejado = super().desenhar(canvas, tag)
        if self.cor_preenchimento != "":
            canvas.create_rectangle(self.coordenadas[0], self.coordenadas[1], self.coordenadas[2], self.coordenadas[3], outline=self.cor_borda, fill=self.cor_preenchimento, dash=tracejado, tags=tag)
        else:
            canvas.create_rectangle(self.coordenadas[0], self.coordenadas[1], self.coordenadas[2], self.coordenadas[3], outline=self.cor_borda, dash=tracejado, tags=tag)


class Oval(Figura):
    """Classe responsável pela renderização de formas ovais. Herda de Figura."""
    def desenhar(self, canvas, tag=""):
        tracejado = super().desenhar(canvas, tag)
        if self.cor_preenchimento != "":
            canvas.create_oval(self.coordenadas[0], self.coordenadas[1], self.coordenadas[2], self.coordenadas[3], outline=self.cor_borda, fill=self.cor_preenchimento, dash=tracejado, tags=tag)
        else:
            canvas.create_oval(self.coordenadas[0], self.coordenadas[1], self.coordenadas[2], self.coordenadas[3], outline=self.cor_borda, dash=tracejado, tags=tag)


class Circulo(Figura):
    """Classe responsável pela renderização de círculos perfeitos proporcionais. Herda de Figura."""
    def desenhar(self, canvas, tag=""):
        tracejado = super().desenhar(canvas, tag)
        dx = self.coordenadas[2] - self.coordenadas[0]
        dy = self.coordenadas[3] - self.coordenadas[1]
        tamanho_lado = max(abs(dx), abs(dy))
        x_final = self.coordenadas[0] + (tamanho_lado if dx > 0 else -tamanho_lado)
        y_final = self.coordenadas[1] + (tamanho_lado if dy > 0 else -tamanho_lado)
        
        if self.cor_preenchimento != "":
            canvas.create_oval(self.coordenadas[0], self.coordenadas[1], x_final, y_final, outline=self.cor_borda, fill=self.cor_preenchimento, dash=tracejado, tags=tag)
        else:
            canvas.create_oval(self.coordenadas[0], self.coordenadas[1], x_final, y_final, outline=self.cor_borda, dash=tracejado, tags=tag)


class Poligono(Figura):
    """
    Classe responsável pela renderização de polígonos regulares. Herda de Figura.
    
    @author Luísa Costa, Sarah Beatriz e Sayran Felix
    @version 1.0
    @since 2026-07-13
    """
    def __init__(self, coordenadas, cor_borda, cor_preenchimento="", num_lados=6):
        """
        Construtor da classe Poligono.
        
        @param coordenadas: Lista contendo as extremidades base [x1, y1, x2, y2].
        @param cor_borda: String hexadecimal da cor da borda.
        @param cor_preenchimento: String hexadecimal da cor de fundo.
        @param num_lados: Quantidade de lados (arestas) do polígono.
        @throws Nenhuma exceção.
        """
        super().__init__(coordenadas, cor_borda, cor_preenchimento)
        self.num_lados = num_lados

    def desenhar(self, canvas, tag=""):
        """
        Realiza o cálculo trigonométrico dos vértices e renderiza o polígono na tela.
        
        @param canvas: Objeto Canvas do Tkinter.
        @param tag: Tag de identificação ("preview" ou "definitivo").
        @return Nenhum.
        @throws Nenhuma exceção.
        """
        tracejado = super().desenhar(canvas, tag)
        x1, y1, x2, y2 = self.coordenadas

        cx = (x1 + x2) / 2
        cy = (y1 + y2) / 2
        rx = abs(x2 - x1) / 2
        ry = abs(y2 - y1) / 2

        pontos = []
        for i in range(self.num_lados):
            angulo = -math.pi / 2 + (2 * math.pi * i) / self.num_lados
            px = cx + rx * math.cos(angulo)
            py = cy + ry * math.sin(angulo)
            pontos.extend([px, py])

        if self.cor_preenchimento != "":
            canvas.create_polygon(pontos, outline=self.cor_borda, fill=self.cor_preenchimento, dash=tracejado, tags=tag)
        else:
            canvas.create_polygon(pontos, outline=self.cor_borda, fill="", dash=tracejado, tags=tag)
