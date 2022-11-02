from flask import Flask, render_template, flash, redirect, url_for
from flask import request
import random
from flask import Markup
app = Flask(__name__)
app.config['SECRET_KEY'] = "my very secret key"

game={
    'choice': 0,
    'win': 0,
    'enemy_win': 0,
    'round':0,
    'first_cube':0,
    'second_cube':0,
}
cubes= {
    'cubes/cube_1.png':1,
    'cubes/cube_2.png':2,
    'cubes/cube_3.png':3,
    'cubes/cube_4.png':4,
    'cubes/cube_5.png':5,
    'cubes/cube_6.png':6,
}


@app.route('/')
def index():
    return render_template('html/start_page.html')

@app.route('/start/')
def start():
    game['win'] = 0
    game['choice'] = 0
    game['enemy_win'] = 0
    game['round'] = 0
    game['first_cube'] = 0
    game['second_cube'] = 0
    return render_template('html/game.html', game=game)

@app.route('/game/',methods=['POST','GET'])
def game_start():

    if game['round'] < 3:
        game['round'] += 1
        flash(f"ROUND {game['round']} ")
        enemy_cube_one = random.randint(1, 6)
        enemy_cube_second = random.randint(1, 6)
        display_cubes(cubes, game, enemy_cube_one, enemy_cube_second)
        if game['choice'] > enemy_cube_one + enemy_cube_second:
            game['win']+=1
            flash(f"You win")
        elif game['choice'] < enemy_cube_one + enemy_cube_second:
            game['enemy_win'] +=1
            flash(f"You lose")
        else:
            flash(f"Draw")
    else:
        if game['win'] > game['enemy_win']:
            flash(f' You won this match\t, score:\n wins({game["win"]}) , loses({game["enemy_win"]})')

        if game['win'] < game['enemy_win']:
            flash(f' You lost this match\t, score:\n wins({game["win"]}) , loses({game["enemy_win"]})')

        if game['win'] == game['enemy_win']:
            flash(f'Draw\t, score:\n wins({game["win"]}) , loses({game["enemy_win"]})')

    return render_template('html/game.html', game=game)


def display_cubes(cubes, game, enemy_cube_one, enemy_cube_second):
    flash('Your cubes')
    for key in cubes:
        if cubes[key] == game['first_cube']:
            flash(Markup(f"<img src='{url_for('static', filename=key, )}'width='50'>"))
        if cubes[key] == game['second_cube']:
            flash(Markup(f"<img src='{url_for('static', filename=key, )}'width='50'>"))
    flash("Enemy cubes:")
    for key in cubes:
        if cubes[key] == enemy_cube_one:
            flash(Markup(f" <img src='{url_for('static', filename=key, )}'width='50'>"))

        if cubes[key] == enemy_cube_second:
            flash(Markup(f"<img src='{url_for('static', filename=key, )}'width='50'>"))
    return

@app.route('/drop/')
def select():
    cube_one = random.randint(1, 6)
    cube_second = random.randint(1, 6)
    game['first_cube'] = cube_one
    game['second_cube'] = cube_second
    game['choice'] = cube_one + cube_second
    return redirect(url_for('game_start'))


if __name__ == '__main__':
    app.run(debug=True)