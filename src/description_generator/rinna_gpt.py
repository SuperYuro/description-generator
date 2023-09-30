import torch
from transformers import (
    AutoTokenizer,
    AutoModelForCausalLM,
    PreTrainedTokenizer,
    PreTrainedTokenizerFast,
)

from description_generator.wikipedia import (
    get_description_from_wikipedia,
    get_title_from_keyword,
)

MODEL_NAME = "rinna/japanese-gpt-neox-3.6b-instruction-sft-v2"


class RinnaGPT:
    __tokenizer: PreTrainedTokenizer | PreTrainedTokenizerFast
    __model: any
    __prompt: list[dict[str, str]] = []

    def __init__(self, model_name: str, use_fast: bool = False) -> None:
        self.__tokenizer = AutoTokenizer.from_pretrained(
            model_name, use_fast=use_fast
        )

        model = AutoModelForCausalLM.from_pretrained(model_name)

        if torch.cuda.is_available():
            model = model.to("cuda")

        self.__model = model

    def __generate_prompt(self, question: str) -> str:
        # こちら側の質問を追加
        user_prompt: dict[str, str] = {"speaker": "ユーザー", "text": question}
        self.__prompt.append(user_prompt)

        prompt = [
            f"{uttr['speaker']}: {uttr['text']}" for uttr in self.__prompt
        ]

        if len(prompt) > 1:
            prompt = "<NL>".join(prompt)
        else:
            prompt = prompt[0]

        prompt += "<NL>" + "システム: "

        return prompt

    def ask(self, question: str) -> str:
        prompt = self.__generate_prompt(question=question)

        token_ids = self.__tokenizer.encode(
            prompt, add_special_tokens=False, return_tensors="pt"
        )

        with torch.no_grad():
            output_ids = self.__model.generate(
                token_ids.to(self.__model.device),
                do_sample=True,
                max_new_tokens=128,
                temperature=0.7,
                pad_token_id=self.__tokenizer.pad_token_id,
                bos_token_id=self.__tokenizer.bos_token_id,
                eos_token_id=self.__tokenizer.eos_token_id,
            )

        output = self.__tokenizer.decode(
            output_ids.tolist()[0][token_ids.size(1) :]
        )
        output = output.replace("<NL>", "\n")

        return output


def chat_with_rinna():
    rinna = RinnaGPT(model_name=MODEL_NAME)

    print("あなた: ", end="")
    question = input()

    while question != "exit":
        answer = rinna.ask(question=question)
        print("システム: " + answer)

        print("あなた: ", end="")
        question = input()


def summary_article():
    keyword = "カワラバト"
    title = get_title_from_keyword(keyword=keyword)
    description = get_description_from_wikipedia(title=title)

    print("title: " + title)
    print("description: " + description)

    rinna = RinnaGPT(model_name=MODEL_NAME)

    prompt = "以下の記事を100文字程度で要約してください．\n" + description

    summary = rinna.ask(question=prompt)

    print(summary)


def main():
    rinna = RinnaGPT(model_name=MODEL_NAME)
    answer = rinna.ask("GAFAMは何の略ですか？")

    print(answer)


if __name__ == "__main__":
    summary_article()
