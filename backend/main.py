from flask import Flask, request, jsonify
from flask_cors import CORS
import pandas as pd
import json
import pickle
import uuid
import traceback
from gantt import util


UPLOAD_FOLDER = '/Users/taranecvadim/Desktop/app'
ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'}


app = Flask(__name__)
CORS().init_app(app=app, send_wildcard=True)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


@app.route('/upload', methods=['POST'])
def get():
    """
    Функция принимает таблицу, чистит и форматирует ее, а затем преобразует в граф.
    """
    user_id = str(uuid.uuid4())
    file_path = '/Users/taranecvadim/Desktop/app/1'
    file = request.files['myFile']
    file.save(file_path)
    try:
        table = util.read_csv(file_path)
        model = util.df2model(table)
        with open('/Users/taranecvadim/Desktop/app/serialized_graph.pkl', 'wb') as sf:
            pickle.dump(model, sf)
        with open('/Users/taranecvadim/Desktop/app/dataframe.pkl', 'wb') as sf:
            pickle.dump(table, sf)
    except Exception as e:
        app.logger.warning(traceback.format_exc(e))
        app.logger.warning(f"[500] Failed: {traceback.format_exc()}!")
        return jsonify({"code": 1, "id": None}), 500

    return jsonify({"code": 200})


@app.route('/change', methods=['POST'])
def set_duration():
    """
    Функция изменяет продолжительность работы id на len, пересчитывет
    граф и затем вычислает сдвинутые задачи и стоимость сдвига.
    """
    change_data = json.loads(request.data)
    with open('/Users/taranecvadim/Desktop/app/serialized_graph.pkl', 'rb') as f:
        sch = pickle.load(f)
    with open('/Users/taranecvadim/Desktop/app/dataframe.pkl', 'rb') as sf:
        table = pd.read_pickle(sf)
    sch[int(change_data['id'])].set_duration(int(change_data['len']))
    full_df = util.modelDict2df(sch).drop_duplicates(subset=['id']).sort_values(by='id')
    full_df['cost'] = full_df['cost'].astype(int)
    diff = (full_df.set_index('id').finish_date - table.finish_date)
    cost = full_df.set_index('id')[diff > 0].cost.sum()
    return jsonify({'cost': int(cost), 'tasks_len': len(list(diff[diff > 0].index)), 'tasks': list(diff[diff > 0].index)})


if __name__ == '__main__':
    app.run('127.0.0.1', port=1500, debug=True)

