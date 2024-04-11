import argparse
import os
import dotenv
from happytransformer import HappyTextToText, TTTrainArgs
import resend

# Load environment variables
def load_environment():
    dotenv.load_dotenv()
    resend.api_key = os.getenv('RESEND_API_KEY')
    os.environ['TOKENIZERS_PARALLELISM'] = 'false'
    os.environ['PYTORCH_CUDA_ALLOC_CONF'] = 'expandable_segments:True'
    os.environ['CUDA_VISIBLE_DEVICES'] = '0'

# Parse command line arguments
def parse_arguments():
    parser = argparse.ArgumentParser(description='Train T5 model on specified datasets')
    parser.add_argument('--input_file', type=str, help='Input file path', required=True)
    parser.add_argument('--load_model_dir', type=str, help='Directory to load the model from', required=False)
    parser.add_argument('--epochs', type=int, help='Number of training epochs', required=True)
    return parser.parse_args()

# Initialize or load model
def get_model(load_model_dir):
    if load_model_dir and os.path.exists(load_model_dir):
        print(f"Loading model from {load_model_dir}")
        return HappyTextToText(load_path=load_model_dir)
    else:
        print("Initializing a new model")
        model = HappyTextToText('T5', 't5-base')
        return model

# Send email notifications
def send_email_notification(subject, message, from_email, to_email):
    params = {
        'from': from_email,
        'to': [to_email],
        'subject': subject,
        'html': f'<h1>{subject}</h1><p>{message}</p>'
    }
    resend.Emails.send(params)

# Main training function
def main():
    load_environment()
    args = parse_arguments()
    
    from_email = os.getenv('FROM_EMAIL')
    to_email = os.getenv('TO_EMAIL')
    if not from_email or not to_email:
        raise ValueError("Email configuration variables are not set properly.")

    happy_tt = get_model(args.load_model_dir)

    # Training arguments
    train_args = TTTrainArgs(
        project_name="t5-grammar-correction",
        deepspeed=True,
        batch_size=4,
        eval_ratio=0.1,
        eval_steps=0.2,
        logging_steps=1000,
        max_input_length=256,
        num_train_epochs=args.epochs,
        max_output_length=256,
        learning_rate=1e-4,
        weight_decay=0.01)
    
    dataset_filename = args.input_file
    try:
        print(f"Fine-tuning on dataset: {dataset_filename}")
        output = dataset_filename.split('/')[-1].split('.')[0]
        happy_tt.train(dataset_filename, args=train_args)
        happy_tt.save(f'./models/{output}')
        
    except Exception as e:
        print(str(e))
        send_email_notification('Grammar Training Progress Error', f'Error occurred: {str(e)}', from_email, to_email)

if __name__ == '__main__':
    main()