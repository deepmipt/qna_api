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
    Return most similar item to specified question from specified QnA
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
      - name: sort_by
        in: query
        required: false
        type: string
    """
    q = request.args.get('q')
    qna_id = request.args.get('qna_id')
    sort_by = request.args.get('sort_by')
    sort_by = "top" if not sort_by else sort_by
    qna = QnAProvider(qna_id).get_qna(normalize=True)
    questions = [i['q'] for i in qna]
    with ClusterRpcProxy({'AMQP_URI': os.environ['AMQP_URI']}) as rpc:
        score = rpc.paraphraser.predict(q, questions)
    for i, s in enumerate(score):
        qna[i]['s'] = s

    groups = {}
    for item in qna:
        print(item)
        if item["id"] not in groups:
            groups[item["id"]] = {
                "answer": item["a"],
                "top": 0.0,
                "avg": 0.0,
                "score": 0.0,
                "questions": [],
            }
        qs = groups[item["id"]]["questions"];
        qs.append({"q": item["q"], "s": item["s"]})

    for g in groups.items():
        scores = [q["s"] for q in g[1]["questions"]]
        g[1]["top"] = max(scores)
        g[1]["avg"] = sum(scores)/len(scores)
        g[1]["score"] = g[1]["top"] * g[1]["avg"]

    group_list = sorted([g for g in groups.items()], key=lambda item: -float(item[1][sort_by]))

    print(group_list)

    # qna = sorted(qna, key=lambda item: -float(item['s']))
    result = {
        'question': q,
        'answers': group_list[:20]
    }
    return jsonify(result), 200


@app.route('/questions', methods=['GET'])
def questions():
    """
        Return list of questions from specified QnA
        ---
        parameters:
          - name: qna_id
            in: query
            required: true
            type: string
        """
    qna_id = request.args.get('qna_id')
    qna = QnAProvider(qna_id).get_qna(normalize=True)
    result = {
        'qna_id': qna_id,
        'total': 0,
        'questions': []
    }
    for q in qna:
        result['questions'].append(q['q'])
    result['total'] = len(result['questions'])
    return jsonify(result), 200


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=80, debug=True)
