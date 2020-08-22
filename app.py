from bson import ObjectId
from flask import Flask, render_template, jsonify, request
from pymongo import MongoClient  # pymongo를 임포트 하기(패키지 인스톨 먼저 해야겠죠?)
import datetime
app = Flask(__name__)

client = MongoClient('localhost', 27017)  # mongoDB는 27017 포트로 돌아갑니다.
db = client.todo_list  # 'todo_list'라는 이름의 db를 만듭니다.


## HTML을 주는 부분
@app.route('/')
def home():
    return render_template('index.html')


## API 역할을 하는 부분
@app.route('/todo_list', methods=['POST'])
def add_todo():
    todo_receive = request.form['todo_give']

    today = datetime.datetime.today()
    year = today.year
    month = today.month
    day = today.day
    date = datetime.datetime(year, month, day)


    todo = {
        'todo': todo_receive,
        'date': date,
        'done': False,
        'order': 0
    }

    db.todo_list.insert_one(todo)
    return jsonify({'result': 'success', 'msg': '이 요청은 POST!'})


@app.route('/todo_list', methods=['GET'])
def read_todo():
    today = datetime.datetime.today()
    year = today.year
    month = today.month
    day = today.day
    start = datetime.datetime(year, month, day)
    end = datetime.datetime(year, month, day+1)
    result =[]
    todo_list = list(db.todo_list.find({'date': {'$gte': start,'$lt': end}}).sort([("done", -1), ("order", 1)]))
    for todo in todo_list:
        result.append({
            '_id': str(todo['_id']),
            'todo': todo['todo'],
            'date': todo['date'],
            'done': todo['done'],
            'order': todo['order']
        })
    # 본래 id는 json형태로 변환하는데 방해되어서 빼고 돌려줬었는데 내 프로젝트 특성상 id가 필요하므로 위의 작업은 id를 str으로 바꿔서 id까지 불러올 수 있도록 하게 하는 작업이다.

    return jsonify({'result': 'success', 'todo_list': result})


@app.route('/todo_list/delete', methods=['POST'])
# 메서드 당 요청 URL은 고유해야함. 그래서 delete 추가
def delete_todo():
    id_receive = request.form['id_give']
    db.todo_list.delete_one({'_id': ObjectId(id_receive)})
    #id는 string 이 아니라 Object형태이기 때문에 ObjectIF()로 붙여주었다. 변환의 일종인 듯.
    return jsonify({'result': 'success'})

@app.route('/todo_list/done', methods=['POST'])
def done_todo():
    print(request.form)
    id_receive = request.form['id_give']
    db.todo_list.update_one({'_id': ObjectId(id_receive)},{'$set':{'done': True}})
    return jsonify({'result': 'success'})

@app.route('/todo_list/undone', methods=['POST'])
def undone_todo():
    print(request.form)
    id_receive = request.form['id_give']
    db.todo_list.update_one({'_id': ObjectId(id_receive)},{'$set':{'done': False}})
    return jsonify({'result': 'success'})

if __name__ == '__main__':
    app.run('0.0.0.0', port=5000, debug=True)