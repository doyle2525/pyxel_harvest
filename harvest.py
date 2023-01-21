import pyxel


class App:
    def __init__(self):
        pyxel.init(160, 120, title="harvest")
        pyxel.load("assets/harvest.pyxres")
        self.score = 0
        self.player_x = 80
        self.player_y = 70
        self.is_alive = True
        self.far_cloud = [(-10, 75), (40, 65), (90, 60)]
        self.near_cloud = [(10, 25), (70, 35), (120, 15)]
        self.fruit = [
            (pyxel.rndi(0, 140), i * 60, pyxel.rndi(0, 2), True) for i in range(6)
        ]
        self.bomb = [
            (pyxel.rndi(0, 140), i * 60, pyxel.rndi(0, 2), True) for i in range(1)
        ]
        pyxel.playm(0, loop=True)
        pyxel.run(self.update, self.draw)

    def update(self):
        if pyxel.btnp(pyxel.KEY_Q):
            pyxel.quit()

        self.update_player()
        for i, v in enumerate(self.fruit):
            self.fruit[i] = self.update_fruit(*v)

        self.update_player()
        for i, v in enumerate(self.bomb):
            self.bomb[i] = self.update_bomb(*v)    

    def update_player(self):
        if pyxel.btn(pyxel.KEY_LEFT):
            self.player_x -= 2
        if pyxel.btn(pyxel.KEY_RIGHT):
            self.player_x += 2
        if pyxel.btn(pyxel.KEY_UP):
            self.player_y -= 2
        if pyxel.btn(pyxel.KEY_DOWN):
            self.player_y += 2
            
        self.player_x = max(self.player_x, 0)
        self.player_x = min(self.player_x, pyxel.width - 16)
        self.player_y = max(self.player_y, 0)
        self.player_y = min(self.player_y, pyxel.height - 16)    




    def update_fruit(self, x, y, kind, is_alive):
        if is_alive and abs(x - self.player_x) < 12 and abs(y - self.player_y) < 12:
            is_alive = False
            self.score += (kind + 1) * 100
            pyxel.play(3, 4)
        y += 2
        if y > 140:
            y -= 160
            x = pyxel.rndi(0, 140)
            kind = pyxel.rndi(0, 2)
            is_alive = True
        return (x, y, kind, is_alive)

    def update_bomb(self, x, y, kind, is_alive):
        if is_alive and abs(x - self.player_x) < 12 and abs(y - self.player_y) < 12:
            is_alive = False
            self.score = 0
            pyxel.play(3,5)
        y += 4
        if y > 140:
            y -= 160
            x = pyxel.rndi(0, 140)
            kind = pyxel.rndi(0, 2)
            is_alive = True
        return (x, y, kind, is_alive)    
    
    def draw(self):
        pyxel.cls(12)

        # Draw sky
        pyxel.blt(0, 88, 0, 0, 88, 160, 32)

        # Draw mountain
        pyxel.blt(0, 88, 0, 0, 64, 160, 24, 12)

        # Draw trees
        offset = pyxel.frame_count % 160
        for i in range(2):
            pyxel.blt(i * 160 - offset, 104, 0, 0, 48, 160, 16, 12)

        # Draw clouds
        offset = (pyxel.frame_count // 16) % 160
        for i in range(2):
            for x, y in self.far_cloud:
                pyxel.blt(x + i * 160 - offset, y, 0, 64, 32, 32, 8, 12)
        offset = (pyxel.frame_count // 8) % 160
        for i in range(2):
            for x, y in self.near_cloud:
                pyxel.blt(x + i * 160 - offset, y, 0, 0, 32, 56, 8, 12)

        # Draw fruits
        for x, y, kind, is_alive in self.fruit:
            if is_alive:
                pyxel.blt(x, y, 0, 16 + kind * 16, 0, 16, 16, 12)

        # Draw bomb
        for x, y, kind, is_alive in self.bomb:
            if is_alive:
                pyxel.blt(x, y, 0, 64 + kind * 16, 0, 16, 16, 12)        

        # Draw player
        pyxel.blt(
            self.player_x,
            self.player_y,
            0,
            0,
            0,
            16,
            16,
            12,
        )

        # Draw score
        s = f"SCORE {self.score:>4}"
        pyxel.text(5, 4, s, 1)
        pyxel.text(4, 4, s, 7)


App()
