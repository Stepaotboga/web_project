from PIL import Image, ImageDraw, ImageFont
from math import sqrt, cos, sin, tan, acos, asin, atan, log
from random import randrange

from flask import Flask, render_template, request, jsonify, url_for, logging

import io
import base64


app = Flask(__name__)
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0
logging.create_logger(app)
"""Создается приложение, кэш отключаем, чтобы картинка графика могла изменяться"""

plot_data = None

scale = 20
step = 1
nums = '0123456789'
color = 'red'
"""Параметры для построения графика"""

def coords(txt):
    txt = ''.join(txt.split()).replace('=', '').replace('y', '').replace('^', '**')
    arr = txt.split('|')
    text = arr[0]
    txt = ''
    """
        Преобразование функции в читаемый для eval вид
    """
    for i in range(len(text) - 1):
        txt += text[i]
        if text[i] in nums and (text[i + 1] == 'x' or text[i + 1] == '('):
            txt += '*'
    txt += text[-1]
    minx = -1 * scale / 2
    maxx = scale / 2
    if len(arr) > 1:
        rang = arr[1].split(':')
        minx = float(rang[0])
        maxx = float(rang[1])
    return (txt, minx, maxx)


def line(draw, arr, scale, step, color):
    """
        Построение графика по функции
    """
    txt = arr[0]
    minx = arr[1]
    maxx = arr[2]
    n = int(600 / step / 2)
    data = []
    points = []
    """
        Отрисовка графика по точкам
    """
    for i in range(-n, n + 1):
        x1 = (i + n) * step
        x = i / (600 / scale / step)
        try:
            y = (eval(txt) * (600 / scale))
            if isinstance(y, complex) or y < -500 or y > 500 or x < minx or x > maxx:
                raise ValueError
            data.append((x1, 300 - y))
            points.append((x1, 300 - y))
        except (ValueError, ZeroDivisionError):
            if len(data) > 3:
                draw.line(data, fill=color, width=3)
            data = []
            points.append("none")
    """
        Отрисовка выколотых точек
    """
    for i in range(len(points)):
        try:
            if points[i - 1] != "none" and points[i] == "none" and points[i + 1]:
                x_delta = points[i + 1][0] - points[i - 1][0]
                y_delta = points[i + 1][1] - points[i - 1][1]
                if x_delta < 10 and y_delta < 10:
                    dot_pos = (points[i - 1][0] + x_delta / 2, points[i - 1][1] + y_delta / 2)
                    x = dot_pos[0]
                    y = dot_pos[1]
                    draw.ellipse((x - 5, y - 5, x + 5, y + 5), fill=(255, 255, 255), outline=color, width=3)
        except Exception:
            pass
    return data


def func(txt):
    txt = ''.join(txt.split()).replace('=', '').replace('y', '').replace('**', '^')
    txt = txt.split('|')[0]
    return 'y=' + txt


@app.route('/', methods=['GET', 'POST'])
def index():
    """Код работы сервера"""
    global plot_data

    if request.method == 'GET':
        im = Image.open('static/img/origin.png', mode='r')
        im.save('static/img/graph.png')

        img = io.BytesIO()
        im.save(img, format='png')
        img.seek(0)
        plot_url = base64.b64encode(img.getvalue()).decode()
        plot_data = {'plot_url': plot_url}

        return render_template('index.html', plot_data=plot_data)

    if request.method == 'POST':
        if 'function' in request.form:
            function = request.form['function']
            try:
                im = Image.open('static/img/origin.png', mode='r')
                draw = ImageDraw.Draw(im)

                data = line(draw, coords(function), scale, step, color)
                if len(data) > 3:
                    draw.line(data, fill=color, width=3)

                im.save('static/img/graph.png')

                img = io.BytesIO()
                im.save(img, format='png')
                img.seek(0)
                plot_url = base64.b64encode(img.getvalue()).decode()
                plot_data = {'plot_url': plot_url}

                return jsonify(plot_data)

            except Exception as exc:
                """Обработка ошибок"""
                im = Image.open('static/img/origin.png', mode='r')

                img = io.BytesIO()
                im.save(img, format='png')
                img.seek(0)
                plot_url = base64.b64encode(img.getvalue()).decode()

                plot_data = {
                    'plot_url': plot_url,
                    'err': 'Ошибка: невозможно построить график для введенной функции',
                    'text_err': str(exc)
                }

                return jsonify(plot_data), 400
        elif 'delete' in request.form:
            plot_data = None
            im = Image.open('static/img/origin.png', mode='r')

            img = io.BytesIO()
            im.save(img, format='png')
            img.seek(0)
            plot_url = base64.b64encode(img.getvalue()).decode()

            return jsonify({'delete': True, 'plot_url': plot_url})


if __name__ == '__main__':
    app.run(port=7700, host='127.0.0.1')