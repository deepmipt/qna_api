import os
import json


class QnAProvider:

    def __init__(self, qna_id):
        self.qna = None
        self.qna_id = qna_id

    def get_qna(self, normalize=False):
        if self.qna is None:
            data_path = os.environ['QNA_DATA']
            with open(os.path.join(data_path, "config.json")) as config_file:
                config = json.load(config_file)
            if self.qna_id in config["qna"]:
                with open(os.path.join(data_path, config["qna"][self.qna_id])) as qna_file:
                    self.qna = json.load(qna_file)
        return QnAProvider.normalize_qna(self.qna) if normalize else self.qna

    @staticmethod
    def normalize_qna(qna):
        result = []
        for topic in qna["topics"]:
            for item in topic["qna"]:
                for q in item["q"]:
                    for a in item["a"]:
                        result.append({
                            "q": q,
                            "a": a
                        })
        return result
