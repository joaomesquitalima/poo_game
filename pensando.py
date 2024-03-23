

class Bloco():
    def __init__(self,colisao=False,tamanho= 10,cor = "blue"):
        self.colisao = colisao
        self.tamanho = tamanho
        self.cor = cor


class Player(Bloco):
    def __init__(self, colisao=False, tamanho=10, cor="verde"):
        super().__init__(colisao, tamanho, cor)

    def andar(self):
        pass

    def change(self):
        pass



player = Player()

print(player.cor)
        