from jina import DocumentArray, Executor, requests, Document
from typing import List, Dict
from paddlenlp.transformers import (
    UnifiedTransformerLMHeadModel,
    UnifiedTransformerTokenizer,
)

import paddle

if paddle.device.cuda.device_count() > 0:
    paddle.device.set_device("cuda:0")


class PlatoXLExecutor(Executor):
    """"""

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        model_name = "plato-mini"
        self.tokenizer = UnifiedTransformerTokenizer.from_pretrained(model_name)
        self.model = UnifiedTransformerLMHeadModel.from_pretrained(model_name)

    @requests(on="/generate")
    async def generate(self, docs: List[Document], **kwargs):
        history = [doc.text for doc in docs]
        inputs_ids = self.tokenizer.dialogue_encode(
            history,
            add_start_token_as_response=True,
            return_tensors=True,
            is_split_into_words=False,
        )

        outputs, _ = self.model.generate(
            input_ids=inputs_ids["input_ids"],
            token_type_ids=inputs_ids["token_type_ids"],
            position_ids=inputs_ids["position_ids"],
            attention_mask=inputs_ids["attention_mask"],
            max_length=64,
            decode_strategy="sampling",
            top_k=5,
            use_fast=True,
        )

        result = postprocess_response(outputs[0].numpy(), self.tokenizer)
        return DocumentArray([Document(text="".join(result))])


def postprocess_response(token_ids, tokenizer):
    eos_pos = len(token_ids)
    for i, tok_id in enumerate(token_ids):
        if tok_id == tokenizer.sep_token_id:
            eos_pos = i
            break
    token_ids = token_ids[:eos_pos]
    tokens = tokenizer.convert_ids_to_tokens(token_ids)
    return tokenizer.merge_subword(tokens)
