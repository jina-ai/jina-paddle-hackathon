from jina import Client, Document, DocumentArray

ppmap = {
    "http": 12345,
    "grpc": 12344,
    "websocket": 12346
}

print("=====================Test uie calling=====================")

for protocol in ppmap:
    c = Client(port=ppmap[protocol], protocol=protocol)
    response_docs = c.post(on='/', parameters={"schema": ['时间', '选手', '赛事名称']}, inputs=DocumentArray(
        [Document(text='2月8日上午北京冬奥会自由式滑雪女子大跳台决赛中中国选手谷爱凌以188.25分获得金牌！')]))
    print(f"Test {protocol}:", response_docs[0].text)

print("======================Change schema======================")

response_docs = c.post(on='/', parameters={"schema": {'地震触发词': ['地震强度', '时间', '震中位置', '震源深度']}}, inputs=DocumentArray(
    [Document(text='中国地震台网正式测定:5月16日06时08分在云南临沧市凤庆县(北纬24.34度,东经99.98度)发生3.5级地震,震源深度10千米。')]))
print(f"Result:", response_docs[0].text)
