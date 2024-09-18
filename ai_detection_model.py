import torch
from transformers import GPT2LMHeadModel, GPT2Tokenizer
import numpy as np
from scipy.stats import entropy
import pickle

class AIDetectionModel:
    def __init__(self):
        self.model_name = 'gpt2'
        self.model = GPT2LMHeadModel.from_pretrained(self.model_name)
        self.tokenizer = GPT2Tokenizer.from_pretrained(self.model_name)

    def calculate_perplexity(self, text):
        tokens = self.tokenizer.encode(text, return_tensors='pt')
        with torch.no_grad():
            outputs = self.model(tokens, labels=tokens)
            loss = outputs.loss
            perplexity = torch.exp(loss)
        return perplexity.item()

    def calculate_burstiness(self, text):
        sentences = [s.strip() for s in text.split('.') if s]
        sentence_lengths = [len(sentence.split()) for sentence in sentences]
        mean_length = np.mean(sentence_lengths) if sentence_lengths else 0
        variance = np.var(sentence_lengths) if sentence_lengths else 0
        burstiness_score = variance / mean_length if mean_length > 0 else 0
        return burstiness_score

    def calculate_entropy(self, text):
        words = text.split()
        word_freq = np.bincount([hash(word) % 10000 for word in words], minlength=10000)
        return entropy(word_freq)

    def detect_ai_text(self, text):
        perplexity = self.calculate_perplexity(text)
        burstiness = self.calculate_burstiness(text)
        entropy_score = self.calculate_entropy(text)

        print(f"Perplexity: {perplexity:.2f}")
        print(f"Burstiness: {burstiness:.2f}")
        print(f"Entropy: {entropy_score:.2f}")

        if perplexity > 10:
            threshold = 0.6
        elif perplexity > 5:
            threshold = 0.5
        else:
            threshold = 0.5

        normalized_perplexity = perplexity / 100
        normalized_burstiness = burstiness / 10
        normalized_entropy = entropy_score / 10

        combined_score = (0.5 * normalized_perplexity +
                          0.3 * normalized_burstiness +
                          0.2 * normalized_entropy)

        print(f"Combined Score: {combined_score:.2f}")

        return "AI-generated text likely." if combined_score < threshold else "Human-written text likely."

# Save the model using pickle
ai_detection_model = AIDetectionModel()
with open('ai_detection_model.pkl', 'wb') as f:
    pickle.dump(ai_detection_model, f)
