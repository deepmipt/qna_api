import os
import json


def main():
    faq2json('faq_with_table2.csv', 'faq_with_table2.json')


def faq2json(csv_file, json_file):
    data_path = os.environ['QNA_DATA']
    with open(os.path.join(data_path, csv_file),'r') as csv:
        data = {
            "topics": [
                {
                    "topic": "Default",
                    "qna": []
                }
            ]
        }
        qna = data["topics"][0]["qna"]
        for i, line in enumerate(csv.readlines()):
            parts = line.split('$')
            if len(parts)!=2:
                print(parts)

            questions = [q.strip() for q in parts[0].split('~') if len(q.strip()) > 0]

            answer = parts[1].strip()

            if answer != "":
                item = {
                    "id": i,
                    "q": questions,
                    "a": [answer]
                }
                qna.append(item)
        with open(os.path.join(data_path, json_file), 'w+') as f:
            f.write(json.dumps(data))



if __name__ == '__main__':
    main()