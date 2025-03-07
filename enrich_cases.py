from src.schema import LMRemedy, LMRuling
from pathlib import Path
import dotenv

dotenv.load_dotenv()

from nietzkit.johnllm import LMP, LLMModel
from deepseek_client import deepseek_ruling

cases_dir = Path("cases/onsc")
out_dir = Path("parsed")
SUBSET = 30

class EnrichCase(LMP):
    prompt = """
{{ruling}}

Given the legal ruling above, parse it into a structure format
"""
    response_format = LMRuling

llm_model = LLMModel()
cases = list(cases_dir.rglob("*"))[40 : 40 + SUBSET]

for case_file in cases:
    with open(case_file) as f:
        ruling = f.read()

        print("[CASEFILE]")
        print(case_file)

        # enriched_ruling = EnrichCase().invoke(
        #     model=llm_model,
        #     model_name="deepseek",
        #     ruling=ruling
        # )
        
        res = deepseek_ruling(ruling)
        with open(out_dir / f"deepseek_{case_file.stem}.json", "w") as f:
            f.write(res.model_dump_json(indent=4))

print(f"Total cost: {llm_model.get_cost()}")
print(f"Avg cost: {llm_model.get_cost() / SUBSET}")