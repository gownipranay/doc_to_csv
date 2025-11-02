from langchain import LLMChain, PromptTemplate
from langchain.llms import HuggingFaceHub  # or use HuggingFaceInference or LocalTransformer

# Example prompt: convert document to JSON with fields invoice_number,date,total_amount, vendor
prompt = PromptTemplate(
    input_variables=["text"],
    template="""
You are a smart extractor. Extract the following fields from the text, output ONLY valid JSON.
Fields: invoice_id, invoice_date (YYYY-MM-DD), vendor, total_amount (numbers)
If a field is missing, put null.

Text:
{text}

Return JSON:
"""
)

# instantiate LLM (this requires HUGGINGFACEHUB_API_TOKEN env var if using hub)
llm = HuggingFaceHub(repo_id="google/flan-t5-small", model_kwargs={"temperature":0.0, "max_length":512})
chain = LLMChain(llm=llm, prompt=prompt)

def extract_fields_with_llm(text):
    out = chain.run(text=text)
    # out should be JSON string; parse it
    import json
    try:
        return json.loads(out)
    except Exception:
        # sometimes model outputs extra text, attempt to extract JSON substring
        import re
        match = re.search(r"\{.*\}", out, re.S)
        if match:
            return json.loads(match.group())
        raise
