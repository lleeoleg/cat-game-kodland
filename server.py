"""
server.py
"""
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask import request, jsonify
import random
from datetime import datetime

GRID_WIDTH = 20
GRID_HEIGHT = 15

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///cats.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

class User(db.Model):
    """_summary_

    Args:
        db (_type_): _description_

    Returns:
        _type_: _description_
    """
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    coins = db.Column(db.Integer, default=0)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    x = db.Column(db.Integer, nullable=False)
    y = db.Column(db.Integer, nullable=False)
    
    def to_dict(self):
        return {
            "username": self.username,
            "coins": self.coins,
            "x": self.x,
            "y": self.y
        }

class Coin(db.Model):
    """_summary_

    Args:
        db (_type_): _description_
    """
    id = db.Column(db.Integer, primary_key=True)
    x = db.Column(db.Integer, nullable=False)
    y = db.Column(db.Integer, nullable=False)
    
@app.route('/join', methods=['POST'])
def api_join():
    """_summary_

    Returns:
        _type_: _description_
    """
    username = request.json.get('username')
    if not username:
        return jsonify({"error": "Имя пользователя обязательно"}), 400
    
    player = User.query.filter_by(username=username).first()
    if player:
        return jsonify({"message": "Вы уже в игре", "player": player.to_dict()}), 200
    
    x = random.randint(0, GRID_WIDTH-1)
    y = random.randint(0, GRID_HEIGHT-1)
    new_user = User(username=username, x=x, y=y)
    db.session.add(new_user)

    if Coin.query.first() is None:
        cx = random.randint(0, GRID_WIDTH-1)
        cy = random.randint(0, GRID_HEIGHT-1)
        db.session.add(Coin(x=cx, y=cy))

    db.session.commit()
    
    return jsonify({"message": "Игрок добавлен", "player": new_user.to_dict()}), 201

@app.route('/action', methods=['POST'])
def api_action():
    """_summary_

    Returns:
        _type_: _description_
    """
    username = request.json.get('username')
    action = request.json.get('action')

    if not username or not action:
        return jsonify({"error": "username и action обязательны"}), 400

    player = User.query.filter_by(username=username).first()
    if not player:
        return jsonify({"error": "Игрок не найден"}), 404

    if action == "up" and player.y > 0:
        player.y -= 1
    elif action == "down" and player.y < GRID_HEIGHT - 1:
        player.y += 1
    elif action == "left" and player.x > 0:
        player.x -= 1
    elif action == "right" and player.x < GRID_WIDTH - 1:
        player.x += 1

    coin = Coin.query.first()
    if coin and player.x == coin.x and player.y == coin.y:
        player.coins += 1
        coin.x = random.randint(0, GRID_WIDTH-1)
        coin.y = random.randint(0, GRID_HEIGHT-1)

    db.session.commit()

    return jsonify({
        "message": "Действие выполнено",
        "player": player.to_dict(),
        "coin": {"x": coin.x, "y": coin.y} if coin else None
    }), 200

@app.route('/state', methods=['GET'])
def api_state():
    """_summary_

    Returns:
        _type_: _description_
    """
    players = [p.to_dict() for p in User.query.all()]
    coin = Coin.query.first()

    return jsonify({
        "players": players,
        "coin": {"x": coin.x, "y": coin.y} if coin else None
    }), 200
    

@app.route('/leaderboard')
def leaderboard():
    """
    _summary_
    """
    players = User.query.order_by(User.coins.desc()).all()

    html = """
    <html>
    <head>
        <title>Leaderboard</title>
        <style>
            body { font-family: Arial, sans-serif; background: #f5f5f5; padding: 20px; }
            h1 { color: #333; }
            table { border-collapse: collapse; width: 60%; background: white; }
            th, td { border: 1px solid #ccc; padding: 8px; text-align: center; }
            th { background: #eee; }
        </style>
    </head>
    <body>
        <h1>Leaderboard</h1>
        <table>
            <tr>
                <th>Username</th>
                <th>Coins</th>
                <th>Duration</th>
            </tr>
    """

    for p in players:
        duration = datetime.utcnow() - p.created_at
        html += f"""
            <tr>
                <td>{p.username}</td>
                <td>{p.coins}</td>
                <td>{str(duration).split('.')[0]}</td>
            </tr>
        """

    html += """
        </table>
    </body>
    </html>
    """
    return html

if __name__ == "__main__":
    with app.app_context():
        db.create_all()
        if not Coin.query.first():
            from random import randint
            db.session.add(Coin(x=randint(0, GRID_WIDTH-1), y=randint(0, GRID_HEIGHT-1)))
            db.session.commit()

    app.run(debug=True)