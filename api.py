from flask import Flask, request, jsonify, redirect, url_for
from flasgger import Swagger
from nameko.standalone.rpc import ClusterRpcProxy

import os
from qna_provider import QnAProvider

app = Flask(__name__)
Swagger(app)


@app.route('/')
def index():
    return redirect('/apidocs/')


@app.route('/answer', methods=['GET'])
def answer():
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
    qna = QnAProvider(qna_id).get_qna()
    questions = [i['q'] for i in qna]
    with ClusterRpcProxy({'AMQP_URI': os.environ['AMQP_URI']}) as rpc:
        score = rpc.paraphraser.predict(q, questions)
    for i, s in enumerate(score):
        qna[i]['s'] = s[0]
    qna = sorted(qna, key=lambda item: -float(item['s']))
    result = {
        'question': q,
        'answer': qna[0]
    }
    return jsonify(result), 200


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=80, debug=True)
