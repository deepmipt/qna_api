import os
import importlib.util


class QnAProvider:

    def __init__(self, qna_id):
        self.qna = None
        self.qna_id = qna_id

    def get_qna(self):
        if self.qna is None:

            spec = importlib.util.spec_from_file_location("config", "/data/config.py")
            config = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(config)

            result = []
            item = None
            if self.qna_id in config.QnA:
                with open(os.path.join("/data", config.QnA[self.qna_id]), 'r') as f:
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
                self.qna = result
        return self.qna
