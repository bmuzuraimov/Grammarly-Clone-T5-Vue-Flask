from flask import Flask, request, jsonify
from flask_cors import CORS
from transformers import AutoTokenizer, AutoModelForSeq2SeqLM
import os
from dotenv import load_dotenv
import logging
import torch

# Load environment variables
load_dotenv()

# Configure logging
logging.basicConfig(level=logging.INFO)

# Initialize Flask app
app = Flask(__name__)
# Configure CORS with specific origin if needed
CORS(app, resources={r"/api/*": {"origins": "*"}})

# Ensure the CUDA device is set up correctly if using GPU
os.environ['TOKENIZERS_PARALLELISM'] = 'false'
os.environ['PYTORCH_CUDA_ALLOC_CONF'] = 'expandable_segments:True'
os.environ['CUDA_VISIBLE_DEVICES'] = '0'

# Initialize Transformers model and tokenizer
model_name_or_path = os.getenv('TRANSFORMERS_MODEL_PATH', '../models/grammar-model')
tokenizer = AutoTokenizer.from_pretrained(model_name_or_path)
model = AutoModelForSeq2SeqLM.from_pretrained(model_name_or_path)
# Set up the device
if torch.cuda.is_available():
    device = torch.device("cuda")
    print(f"Using GPU: {torch.cuda.get_device_name(0)}")
elif torch.backends.mps.is_available():
    device = torch.device("mps")
    print("Using MPS")
else:
    device = torch.device("cpu")
    print("Using CPU")
model.to(device)

def clean_sentence(text):
    """
    Cleans the input text by removing unwanted characters and spaces.
    """
    text = text.replace("\n", "").replace("\r", "").replace("\t", "")
    text = " ".join(text.split())
    return text.strip()

@app.route('/api/process_text', methods=['POST'])
def process_text():
    try:
        data = request.get_json()
        if not data or 'text' not in data:
            return jsonify({'error': 'No text provided'}), 400

        input_text = clean_sentence(data['text'])
        input_ids = tokenizer.encode(input_text, return_tensors="pt")
        input_ids = input_ids.to(device)

        # Generate output
        outputs = model.generate(input_ids, max_length=256, num_beams=4, early_stopping=True)
        output_text = tokenizer.decode(outputs[0], skip_special_tokens=True)

        return jsonify({'output_text': output_text})
    except Exception as e:
        logging.error(f"Error processing text: {str(e)}")
        return jsonify({'error': 'Failed to process text'}), 500

if __name__ == '__main__':
    flask_debug = os.getenv('FLASK_DEBUG', 'False') == 'True'
    app.run(debug=flask_debug, host='0.0.0.0', port=int(os.getenv('PORT', 5000)))
