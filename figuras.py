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
# O super() chama o "desenhar" da classe mãe apenas para pegar o tracejado pronto
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
