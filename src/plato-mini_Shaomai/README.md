# jina_chat

MVP: Plato-mini model based Chatbot using Jina
![](https://github.com/shaomaiguanguan/jina_chat/blob/main/platominichatbot.gif)

## Setup environments

```
python -m venv .venv
.venv/Scripts/activate
pip install -r requirements.txt
```

## Start backend

```
jina flow --uses flow.yml
```

## Start client

Start another terminal with activated virtual environment. Then run:

```
python client.py
```

# Test

```
pytest .\test\test_protocols.py
```
