from paddlenlp.transformers import (UnifiedTransformerLMHeadModel,
                                    UnifiedTransformerTokenizer)
from typing import List, Dict, Any
from jina import Executor, requests, DocumentArray, Document, Deployment
from typing import List, Dict

import paddle

paddle.set_default_dtype("float32")
if paddle.device.cuda.device_count() > 0:
    paddle.device.set_device("cuda:0")


class PlatoXLExecutor(Executor):
    def __init__(self,  **kwargs):
        super().__init__(**kwargs)
        self.tokenizer = UnifiedTransformerTokenizer.from_pretrained(
            'plato-mini')
        self.model = UnifiedTransformerLMHeadModel.from_pretrained(
            'plato-mini')

    @requests
    async def dialog_predict(
        self,
        docs: List[Document],
        parameters: Dict[str, Any], **kwargs
    ) -> str:
        history = [doc.text for doc in docs]
        output_ids, score = self.model.generate(
            **self.tokenizer.dialogue_encode(
                history,
                add_start_token_as_response=True,
                return_tensors=True,
                is_split_into_words=False
            ),
            **parameters,
        )

        token_ids = output_ids.numpy()[0]

        eos_pos = len(token_ids)
        for i, tok_id in enumerate(token_ids):
            if tok_id == self.tokenizer.sep_token_id:
                eos_pos = i
                break
        token_ids = token_ids[:eos_pos]
        tokens = self.tokenizer.convert_ids_to_tokens(token_ids)
        tokens = self.tokenizer.merge_subword(tokens)

        return DocumentArray([Document(text=''.join(tokens))])


if __name__ == "__main__":
    with Deployment(uses=PlatoXLExecutor) as dep:
        response_docs = dep.post(
            on='/', inputs=DocumentArray([Document(text='你好！')]))
        print(f'Text: {response_docs[0].text}')
