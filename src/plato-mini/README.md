## Jina X plato-mini

## GetStart

please install pdm first: `pip install pdm` (Pdm is a modern Python package and
dependency manager supporting the latest PEP standards. )

after that:

```
pdm prepare
```

this commond can auto install dependencies in virtual env

then:

```
pdm start
```

this commond starts a jina flow server

then:

```
pdm test
```

this commond starts a chat with plato-mini:

```
=====================Test calling=====================
Test http: 你好,你是做什么的?
Test grpc: 你好,你是做什么工作的?
Test websocket: 你好,你是哪里人啊?
======================Plato chat======================
我: hi
Plato:  你好,你是做什么的?
我:
```
