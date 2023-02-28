from jina import Flow
from uie_executor.executor import UIEExecutor


f = Flow(port=[12345, 12344, 12346], protocol=["http", "grpc", "websocket"], cors=True).add(
    name='uie', uses=UIEExecutor)

with f:
    f.block()
