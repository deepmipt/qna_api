import os


def read_qna(qna):
    from config import BASE_DIR
    from config import QnA
    result = []
    item = None
    if qna in QnA:
        with open(os.path.join(BASE_DIR, QnA[qna]), 'r') as f:
            for line in f.readlines():
                line = line.strip()
                if line.endswith('?'):
                    if item is not None:
                        result.append(item)
                    item = dict()
                    item['q'] = line
                else:
                    if 'a' in item:
                        item['a'] += "\n"+line
                    else:
                        item['a'] = line
            result.append(item)
    return result
