from pymongo import MongoClient
from flask import Flask, render_template, jsonify, request
from bson.objectid import ObjectId

app = Flask(__name__, template_folder='templates')

client = MongoClient('mongodb://localhost', 27017)
db = client.dbsparta


# HTML 화면 보여주기
@app.route('/')
def home():
    return render_template('index.html')


# API 역할을 하는 부분
# 클라이언트로부터 정보를 받아서 db에 저장하는 CREATE API
@app.route('/create', methods=['POST'])
def create_input():
    # 1. 클라이언트로부터 데이터를 받기
    plant_receive = request.form['plant_give']
    name_receive = request.form['name_give']
    watering_init = ""
    fertilizing_init = ""

    list = {'plant': plant_receive, 'name': name_receive, 'watering': watering_init, 'fertilizing': fertilizing_init}

    # 2. mongoDB에 데이터를 넣기
    db.plants.insert_one(list)
    return jsonify({'result': 'success'})


# 화면 로딩할 때마다 db에 저장한 정보를 읽어오는 READ API
@app.route('/read', methods=['GET'])
def read_card():
    # 1. mongoDB에서 모든 데이터를 리스트로 조회하기 (Read)
    read_result = list(db.plants.find({}))

    # 2. 조회해 온 리스트에서 _id값을 string 값으로 바꾸기
    def id_decoder(list):
        results = []
        for document in list:
            document['_id'] = str(document['_id'])
            results.append(document)
        return results

    result = id_decoder(read_result)

    # 3. db불러온 정보들(_id값은 string으로 바꿈)을 json 형식으로 보내주기
    if not read_result:
        return jsonify({'result': 'empty'})
    else:
        return jsonify({'result': 'success', 'data': result})


# 물 줬는지 여부를 db에 업데이트하는 UPDATE API
@app.route('/update', methods=['POST'])
def update_water():
    # 1. 클라이언트가 전달한 id_give를 id_receive 변수에 넣습니다.
    watering_receive = request.form['watering_give']
    id_receive = request.form['id_give']

    # # 2. check_receive 값을 string 이 아니라 integer 로 만들기
    # # 왜인지 모르겠지만 이거 안해도 작동은 하는데 찜찜해서. 대신 이거 안했더니 다른 함수에서 checked 값 호출할때 '' 붙여줘야 인식함)
    # check_receive2 = int(check_receive)

    # 3. supplements 목록에서 _id 값이 id_received 인 문서의 watering 을 watering_receive 로 변경합니다.
    # 참고: '$set' 활용하기!
    db.plants.update_one({'_id': ObjectId(id_receive)}, {'$set': {'watering': watering_receive}})

    # 4. 성공하면 success 메시지를 반환합니다.
    return jsonify({'result': 'success', 'card_id': id_receive})

# 물 줬는지 여부를 db에 업데이트하는 UPDATE API
@app.route('/update2', methods=['POST'])
def update_fertile():
    # 1. 클라이언트가 전달한 id_give를 id_receive 변수에 넣습니다.
    fertile_receive = request.form['fertile_give']
    id_receive = request.form['id_give']

    # # 2. check_receive 값을 string 이 아니라 integer 로 만들기
    # # 왜인지 모르겠지만 이거 안해도 작동은 하는데 찜찜해서. 대신 이거 안했더니 다른 함수에서 checked 값 호출할때 '' 붙여줘야 인식함)
    # check_receive2 = int(check_receive)

    # 3. supplements 목록에서 _id 값이 id_received 인 문서의 watering 을 watering_receive 로 변경합니다.
    # 참고: '$set' 활용하기!
    db.plants.update_one({'_id': ObjectId(id_receive)}, {'$set': {'fertilizing': fertile_receive}})

    # 4. 성공하면 success 메시지를 반환합니다.
    return jsonify({'result': 'success', 'card_id': id_receive})


# 카드를 삭제하는 DELETE API
@app.route('/delete', methods=['POST'])
def delete_card():
    # 1. 클라이언트가 전달한 id_give를 id_receive 변수에 넣습니다.
    id_receive = request.form['id_give']

    # 2. mystar 목록에서 delete_one으로 name이 name_receive와 일치하는 star를 제거합니다.
    db.plants.delete_one({'_id': ObjectId(id_receive)})

    # 3. 성공하면 success 메시지를 반환합니다.
    return jsonify({'result': 'success'})


# 데이터 입력 내용을 수정하는 POST API
@app.route('/edit', methods=["POST"])
def edit_data():
    id_receive = request.form['id_give']
    name_receive = request.form['name_give']
    water_receive = request.form['water_give']
    fertile_receive = request.form['fertile_give']

    # id 기준으로 데이터를 찾아 내용을 업데이트합니다.
    db.plants.update_one({'_id': ObjectId(id_receive)}, {'$set': {'name': name_receive, 'watering': water_receive, 'fertilizing': fertile_receive}})

    return jsonify({'result': 'success'})


if __name__ == '__main__':
    app.run('0.0.0.0', port=5000, debug=True)
