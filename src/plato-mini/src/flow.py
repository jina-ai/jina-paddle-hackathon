from jina import Flow
from plato_executor.executor import PlatoXLExecutor

f = Flow(port=[12345, 12344, 12346], protocol=["http", "grpc", "websocket"], cors=True).add(
    name='uie', uses=PlatoXLExecutor)

with f:
    f.block()
