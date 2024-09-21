import asyncio
import torch
import json

from transformers import AutoModelForCausalLM, AutoTokenizer
from cqilserver.cqil_model import CQILWrapper
from channels.generic.websocket import AsyncWebsocketConsumer


class TextGeneratorConsumer(AsyncWebsocketConsumer):
    max_new_tokens = 100
    input_ids = []
    gen_ids = []
    base_model_path = "models/Qwen1.5-14B"
    cqil_model_path = "models/cqil-qwen1.5b-14b"

    tokenizer = AutoTokenizer.from_pretrained(base_model_path, trust_remote_code=True)
    base_model = AutoModelForCausalLM.from_pretrained(base_model_path, trust_remote_code=True, torch_dtype="auto", device_map=1)
    base_model_2 = AutoModelForCausalLM.from_pretrained(cqil_model_path, trust_remote_code=True, torch_dtype="auto", device_map="cpu")
    cqil_model = CQILWrapper(base_model_2, start_l=17, end_l=37).to(0)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    async def connect(self):
        await self.accept()

    async def disconnect(self, close_code):
        await self.close()

    async def receive(self, text_data):
        data = json.loads(text_data)
        user_prompt = data["prompt"]
        print(data)
        if data["selected_model"] == "base":
            self.model = self.base_model
        else:
            self.model = self.cqil_model
        await self.generate_text(user_prompt)

    def _generate_id(self, *args):
        with torch.no_grad():
            input = torch.tensor([self.input_ids])
            if self.model is self.base_model:
                input = input.to(1)
            logits = self.model(input_ids=input)[0]
            id = torch.argmax(logits[0][-1]).item()

        self.gen_ids.append(id)
        self.input_ids.append(id)

        self.gen_id = id
        self.gen_char = self.tokenizer.decode([id], skip_special_tokens=True)

    async def async_wrapper(self, func):
        loop = asyncio.get_event_loop()
        return await loop.run_in_executor(None, func, self)

    async def generate_text(self, prompt):
        self.input_ids = self.tokenizer(prompt)["input_ids"]
        self.gen_ids = []

        self.base_model.eval()

        # Greedy search
        for i in range(self.max_new_tokens):
            await self.async_wrapper(self._generate_id)
            await self.send(text_data=json.dumps({
                'char': self.gen_char, 
                'isStart': len(self.gen_ids) == 1,
                'isEnd': (self.gen_id == self.tokenizer.eos_token_id or i == self.max_new_tokens - 1)
            }))

            if self.gen_id == self.tokenizer.eos_token_id:
                break
