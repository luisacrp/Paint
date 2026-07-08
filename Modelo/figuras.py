import math

# Superclasse
class Figura: 
    def __init__(self, coordenadas, cor_borda, cor_preenchimento = ""):
        self.coordenadas = coordenadas
        self.cor_borda = cor_borda
        self.cor_preenchimento = cor_preenchimento 

    def desenhar(self, canvas, tag = ""):
        tracejado = (4, 2) if tag == "preview" else None
        return tracejado


# Subclasses
class Linha(Figura):
    def desenhar(self, canvas, tag=""):
        tracejado = super().desenhar(canvas, tag)
        canvas.create_line(self.coordenadas[0], self.coordenadas[1], self.coordenadas[2], self.coordenadas[3], fill=self.cor_borda, dash=tracejado, tags=tag)


class Rabisco(Figura):
    def desenhar(self, canvas, tag=""):
        tracejado = super().desenhar(canvas, tag)
        canvas.create_line(self.coordenadas, fill=self.cor_borda, dash=tracejado, tags=tag)


class Retangulo(Figura):
    def desenhar(self, canvas, tag=""):
        tracejado = super().desenhar(canvas, tag)
        if self.cor_preenchimento != "":
            canvas.create_rectangle(self.coordenadas[0], self.coordenadas[1], self.coordenadas[2], self.coordenadas[3], outline=self.cor_borda, fill=self.cor_preenchimento, dash=tracejado, tags=tag)
        else:
            canvas.create_rectangle(self.coordenadas[0], self.coordenadas[1], self.coordenadas[2], self.coordenadas[3], outline=self.cor_borda, dash=tracejado, tags=tag)


class Oval(Figura):
    def desenhar(self, canvas, tag=""):
        tracejado = super().desenhar(canvas, tag)
        if self.cor_preenchimento != "":
            canvas.create_oval(self.coordenadas[0], self.coordenadas[1], self.coordenadas[2], self.coordenadas[3], outline=self.cor_borda, fill=self.cor_preenchimento, dash=tracejado, tags=tag)
        else:
            canvas.create_oval(self.coordenadas[0], self.coordenadas[1], self.coordenadas[2], self.coordenadas[3], outline=self.cor_borda, dash=tracejado, tags=tag)


class Circulo(Figura):
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
    def __init__(self, coordenadas, cor_borda, cor_preenchimento="", num_lados=6):
        super().__init__(coordenadas, cor_borda, cor_preenchimento)
        self.num_lados = num_lados

    def desenhar(self, canvas, tag=""):
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
