from transformers import pipeline

# choose a model (can be swapped)
ner_pipeline = pipeline("ner", model="dbmdz/bert-large-cased-finetuned-conll03-english", grouped_entities=True)

def extract_entities(text: str):
    entities = ner_pipeline(text)
    # entities: [{'entity_group':'PER','score':0.99,'word':'John', 'start':..., 'end':...}, ...]
    return entities
