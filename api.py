from flask import Flask, request, jsonify
from flasgger import Swagger
from nameko.standalone.rpc import ClusterRpcProxy

from config import AMQP_URI
from utils import read_qna

app = Flask(__name__)
Swagger(app)


@app.route('/answer', methods=['GET'])
def compute():
    """
    Micro Service Based Compute and Mail API
    This API is made with Flask, Flasgger and Nameko
    ---
    parameters:
      - name: q
        in: query
        required: true
        type: string
      - name: qna_id
        in: query
        required: true
        type: string
    """
    q = request.args.get('q')
    qna_id = request.args.get('qna_id')
    qna = read_qna(qna_id)
    questions = [i['q'] for i in qna]
    with ClusterRpcProxy({'AMQP_URI': AMQP_URI}) as rpc:
        score = rpc.paraphraser.predict(q, questions)
    for i, s in enumerate(score):
        qna[i]['s'] = s[0]
    qna = sorted(qna, key=lambda item: -float(item['s']))
    result = {
        'question': q,
        'answer': qna[0]
    }
    return jsonify(result), 200


app.run(debug=True)
