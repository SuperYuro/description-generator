import torch
from transformers import (
    AutoModelForCausalLM,
    AutoTokenizer,
    PreTrainedTokenizer,
    PreTrainedTokenizerFast,
)

from description_generator.wikipedia import (
    get_description_from_wikipedia,
    get_title_from_keyword,
)


def summary_article(description: str) -> str:
    B_INST, E_INST = "[INST]", "[/INST]"
    B_SYS, E_SYS = "<<SYS>>\n", "\n<</SYS>>\n\n"

    DEFAULT_SYSTEM_PROMPT = "あなたは誠実で優秀な日本人のアシスタントです．"

    text = "以下のWikipediaの記事を100文字程度で要約してください．\n\n" + description

    model_name = "elyza/ELYZA-japanese-Llama-2-7b-instruct"
    tokenizer = AutoTokenizer.from_pretrained(model_name)
    model = AutoModelForCausalLM.from_pretrained(
        model_name, torch_dtype=torch.float32
    )

    if torch.cuda.is_available():
        model = model.to("cuda")

    prompt = "{bos_token}{b_inst} {system}{prompt} {e_inst} ".format(
        bos_token=tokenizer.bos_token,
        b_inst=B_INST,
        system=f"{B_SYS}{DEFAULT_SYSTEM_PROMPT}{E_SYS}",
        prompt=text,
        e_inst=E_INST,
    )

    with torch.no_grad():
        token_ids = tokenizer.encode(
            prompt, add_special_tokens=False, return_tensors="pt"
        )

        output_ids = model.generate(
            token_ids.to(model.device),
            max_new_tokens=256,
            pad_token_id=tokenizer.pad_token_id,
            eos_token_id=tokenizer.eos_token_id,
        )
    output = tokenizer.decode(
        output_ids.tolist()[0][token_ids.size(1) :], skip_special_tokens=True
    )
    return output


if __name__ == "__main__":
    keyword = "Lycoris radiata"
    title = get_title_from_keyword(keyword)
    description = get_description_from_wikipedia(title)

    print(description)

    summary = summary_article(description)

    print(summary)
