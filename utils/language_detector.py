from haystack import Document
from haystack import Pipeline
from haystack.nodes import BaseComponent
from transformers import AutoTokenizer, AutoModelForSequenceClassification
import torch


class LanguageDetector(BaseComponent):
    def __init__(self, model_name="papluca/xlm-roberta-base-language-detection"):
        self.tokenizer = AutoTokenizer.from_pretrained(model_name)
        self.model = AutoModelForSequenceClassification.from_pretrained(
            model_name)
        # Language labels corresponding to the model's output classes
        self.labels = ['af', 'an', 'ar', 'as', 'az', 'bg', 'bn', 'br', 'ca', 'cs', 'cy', 'da', 'de', 'dz', 'el',
                       'en', 'eo', 'es', 'et', 'eu', 'fa', 'fi', 'fr', 'gl', 'gu', 'he', 'hi', 'hr', 'hu', 'hy',
                       'id', 'is', 'it', 'ja', 'jv', 'ka', 'kk', 'km', 'kn', 'ko', 'ku', 'ky', 'lt', 'lv', 'mk',
                       'ml', 'mn', 'mr', 'ms', 'my', 'nb', 'ne', 'nl', 'nn', 'no', 'or', 'pa', 'pl', 'ps', 'pt',
                       'qu', 'ro', 'ru', 'sd', 'si', 'sk', 'sl', 'sq', 'sr', 'sv', 'sw', 'ta', 'te', 'th', 'tl',
                       'tr', 'ug', 'uk', 'ur', 'vi', 'xh', 'zh']

    def run(self, documents, **kwargs):
        # Extract the text from the documents
        texts = [doc.content for doc in documents]

        # Detect languages for each document
        language_preds = []
        for text in texts:
            inputs = self.tokenizer(text, return_tensors="pt")
            with torch.no_grad():
                outputs = self.model(**inputs)

            probabilities = torch.nn.functional.softmax(outputs.logits, dim=1)
            confidence, predicted_class = torch.max(probabilities, dim=1)
            predicted_language = self.labels[predicted_class]

            language_preds.append({
                "text": text,
                "language": predicted_language,
                "confidence": confidence.item()
            })

        return {"languages": language_preds}, "output_1"

    def run_batch(self, documents, **kwargs):
        return self.run(documents, **kwargs)


# Initialize the custom LanguageDetector node
language_detector = LanguageDetector()

# Define a Haystack pipeline with the custom node
pipeline = Pipeline()
pipeline.add_node(component=language_detector,
                  name="LanguageDetector", inputs=["Query"])

# Example input document

document = Document(content="Bonjour, comment ça va?")
result = pipeline.run(documents=[document])

print(result)
