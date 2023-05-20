import sys
from pathlib import Path
from jina import Document, DocumentArray, Flow

sys.path.insert(0, str(Path(__file__).parent))


def test_gRPC():
    with Flow(
        uses="./PlatoXLExecutor/config.yml",
        protocol="GRPC",
        port=12345,
        name="platomini_grpc",
    ) as f:
        docs = f.post(on="/generate", inputs=DocumentArray([Document(text="你叫什么？")]))
        assert isinstance(docs[0].text, str)
        assert docs[0].text


def test_websocket():
    with Flow(
        uses="./PlatoXLExecutor/config.yml",
        protocol="WEBSOCKET",
        port=12345,
        name="platomini_websocket",
    ) as f:
        docs = f.post(on="/generate", inputs=DocumentArray([Document(text="你叫什么？")]))
        assert isinstance(docs[0].text, str)
        assert docs[0].text


def test_http():
    with Flow(
        uses="./PlatoXLExecutor/config.yml",
        protocol="HTTP",
        port=12345,
        name="platomini_http",
    ) as f:
        docs = f.post(on="/generate", inputs=DocumentArray([Document(text="你叫什么？")]))
        assert isinstance(docs[0].text, str)
        assert docs[0].text
