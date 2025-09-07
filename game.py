"""
game.py
"""
import requests
import pgzrun
import time

WIDTH = 640
HEIGHT = 480
TILE_SIZE = 32

API_URL = "http://127.0.0.1:5000"

cats = {}
coin = None
last_update = 0


class Cat:
    """
    class Cat
    """
    def __init__(self, username, x, y, coins, direction="down"):
        """_summary_

        Args:
            username (_type_): _description_
            x (_type_): _description_
            y (_type_): _description_
            coins (_type_): _description_
            direction (str, optional): _description_. Defaults to "down".
        """
        self.username = username
        self.x = x 
        self.y = y
        self.coins = coins
        self.direction = direction

        self.pixel_x = self.x * TILE_SIZE + 16
        self.pixel_y = self.y * TILE_SIZE + 16

        self.is_moving = False
        self.frame = 0
        self.last_frame_time = time.time()

        self.actor = Actor("wait_down0", (self.pixel_x, self.pixel_y))

    def update_position(self, x, y, coins):
        """_summary_

        Args:
            x (_type_): _description_
            y (_type_): _description_
            coins (_type_): _description_
        """
        if (x, y) != (self.x, self.y):
            if x > self.x:
                self.direction = "right"
            elif x < self.x:
                self.direction = "left"
            elif y > self.y:
                self.direction = "down"
            elif y < self.y:
                self.direction = "up"
            self.is_moving = True

        self.x, self.y, self.coins = x, y, coins

    def animate(self):
        """
        Анимация ходьбы
        """
        if self.is_moving:
            now = time.time()
            if now - self.last_frame_time > 0.1:
                self.last_frame_time = now
                self.frame = (self.frame + 1) % 4
                self.actor.image = f"walk_{self.direction}{self.frame}"
        else:
            self.actor.image = f"wait_{self.direction}0"

    def smooth_move(self, speed=2):
        """_summary_

        Args:
            speed (int, optional): _description_. Defaults to 2.
        """
        target_x = self.x * TILE_SIZE + 16
        target_y = self.y * TILE_SIZE + 16

        if abs(self.pixel_x - target_x) > speed:
            self.pixel_x += speed if self.pixel_x < target_x else -speed
        else:
            self.pixel_x = target_x

        if abs(self.pixel_y - target_y) > speed:
            self.pixel_y += speed if self.pixel_y < target_y else -speed
        else:
            self.pixel_y = target_y

        if self.pixel_x == target_x and self.pixel_y == target_y:
            self.is_moving = False

        self.actor.pos = (self.pixel_x, self.pixel_y)

    def draw(self):
        """_summary_
        """
        self.actor.draw()
        screen.draw.text(
            f"{self.username} ({self.coins})",
            (self.actor.x - 20, self.actor.y - 40),
            color="black",
        )


def fetch_state():
    """_summary_

    Returns:
        _type_: _description_
    """
    global cats, coin
    try:
        data = requests.get(f"{API_URL}/state").json()
        players = data.get("players", [])
        coin_data = data.get("coin")

        for p in players:
            if p["username"] not in cats:
                cats[p["username"]] = Cat(p["username"], p["x"], p["y"], p["coins"])
            cats[p["username"]].update_position(p["x"], p["y"], p["coins"])

        if coin_data:
            coin_x = coin_data["x"] * TILE_SIZE + 16
            coin_y = coin_data["y"] * TILE_SIZE + 16
            return Actor("coin", (coin_x, coin_y))
    except Exception as e:
        print("Ошибка при запросе:", e)


def update():
    """_summary_
    """
    global last_update, coin
    if time.time() - last_update > 0.3:
        coin = fetch_state()
        last_update = time.time()

    for cat in cats.values():
        cat.smooth_move(speed=4)
        time.sleep(0.03)
        cat.animate()


def draw():
    screen.clear()
    screen.fill((150, 200, 255))
    for cat in cats.values():
        cat.draw()
    if coin:
        coin.draw()


fetch_state()
pgzrun.go()
