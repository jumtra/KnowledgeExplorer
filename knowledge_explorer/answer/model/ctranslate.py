import subprocess
from logging import getLogger
from pathlib import Path

import ctranslate2
import transformers

from .base_model import BaseModel

logger = getLogger(__name__)


class CtranslatedModel(BaseModel):
    model_name = "ctranslated_model"

    def set_params(self) -> None:
        self.use_model_name = self.config_manager.config.generate.model_name
        self.use_fast = self.config_manager.config.generate.use_fast
        self.ctranslated_model_name = str(Path(self.config_manager.config.input.model_path) / self.use_model_name.split("/")[-1])
        if not Path(self.ctranslated_model_name).exists():
            Path(self.config_manager.config.input.model_path).mkdir(exist_ok=True, parents=True)
            self.model_ctranslate()

    def build_model(self) -> None:
        self.model = ctranslate2.Generator(self.ctranslated_model_name, device=self.device)
        self.tokenizer = transformers.AutoTokenizer.from_pretrained(self.use_model_name, use_fast=self.use_fast, device=self.device)

    def model_ctranslate(self) -> None:
        command = [
            "ct2-transformers-converter",
            "--model",
            self.use_model_name,
            "--quantization",
            "int8_float16",
            "--output_dir",
            self.ctranslated_model_name,
            "--force",
        ]

        try:
            subprocess.run(command, check=True)
            logger.info("Conversion completed successfully.")
        except subprocess.CalledProcessError as e:
            logger.error("Conversion failed. Error:", e)

    def generate(self, prompt: str) -> str:
        logger.info("回答を生成")
        tokens = self.tokenizer.convert_ids_to_tokens(self.tokenizer.encode(prompt, add_special_tokens=False))
        results = self.model.generate_batch(
            [tokens],
            max_length=2048,
            sampling_topk=80,
            sampling_temperature=0.5,
            repetition_penalty=1.1,
            include_prompt_in_result=False,
            return_end_token=False,
            end_token=[self.tokenizer.eos_token_id, self.tokenizer.pad_token_id],
        )
        text = self.tokenizer.decode(results[0].sequences_ids[0])
        return text
