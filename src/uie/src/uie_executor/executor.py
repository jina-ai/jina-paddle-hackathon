from jina import Executor, requests, DocumentArray, Document, Deployment
from paddlenlp import Taskflow
from typing import List, Union, Dict

Schema = Union[
    # ['时间', '赛手', '赛事名称', '情感倾向[正向，负向]']  实体抽取 分类任务需要[]来设置分类的label
    str,
    # {'歌曲名称': ['歌手', '所属专辑']} 实体属性抽取
    Dict[str, List[str]]
]


class UIEExecutor(Executor):
    def __init__(self, schema = [], **kwargs):
        super().__init__(**kwargs)
        self.uie = Taskflow('information_extraction', schema=schema)

    @requests
    async def call_uie(self, docs, parameters: Dict[str, List[Schema]], **kwargs):
        if (parameters["schema"] != None):
            self.uie.set_schema(parameters["schema"])

        for d in docs:
            d.text = str(self.uie(d.text))


if __name__ == "__main__":
    with Deployment(uses=UIEExecutor) as dep:
        response_docs = dep.post(
            on='/', inputs=DocumentArray([Document(text='2月8日上午北京冬奥会自由式滑雪女子大跳台决赛中中国选手谷爱凌以188.25分获得金牌！')]))
        print(f'Text: {response_docs[0].text}')
