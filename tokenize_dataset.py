import pandas as pd
import os
import dotenv
from transformers import T5Tokenizer
from tqdm.auto import tqdm
import resend

# Load environment variables
def load_env():
    dotenv.load_dotenv()
    resend.api_key = os.getenv('RESEND_API_KEY')

# Read data from CSV
def read_csv(filepath):
    return pd.read_csv(filepath)

# Tokenize and truncate batches of text
def batch_tokenize_and_truncate(df, column_name, tokenizer, max_length=256, batch_size=32):
    num_batches = (len(df) + batch_size - 1) // batch_size
    pbar = tqdm(total=num_batches, desc=f"Tokenizing {column_name}")
    result_series = []
    
    for start_idx in range(0, len(df), batch_size):
        end_idx = start_idx + batch_size
        batch = df[column_name][start_idx:end_idx].tolist()
        tokenized = tokenizer(batch, max_length=max_length, truncation=True, padding="max_length", return_tensors="pt")
        decoded = [tokenizer.decode(tokens, skip_special_tokens=True) for tokens in tokenized.input_ids]
        result_series.extend(decoded)
        pbar.update(1)
    
    pbar.close()
    return pd.Series(result_series)

# Preprocess the DataFrame
def preprocess_dataframe(df, tokenizer, batch_size=32):
    for column in ['input', 'target']:
        df[column] = batch_tokenize_and_truncate(df, column, tokenizer, batch_size=batch_size)
    return df

# Save DataFrame to CSV
def save_csv(df, filepath):
    df.to_csv(filepath, index=False)

# Send email notification
def send_email(subject, message, from_email, to_email):
    params = {
        'from': from_email,
        'to': [to_email],
        'subject': subject,
        'html': f'<h1>{subject}</h1><p>{message}</p>'
    }
    resend.Emails.send(params)

def main():
    load_env()
    tokenizer = T5Tokenizer.from_pretrained('t5-base')
    
    try:
        train_df = read_csv('./data/raw/train.csv')
        test_df = read_csv('./data/raw/test.csv')
        
        train_df = preprocess_dataframe(train_df, tokenizer, batch_size=4)
        test_df = preprocess_dataframe(test_df, tokenizer, batch_size=4)
        
        save_csv(train_df, './data/processed/train/tokenized_train.csv')
        save_csv(test_df, './data/processed/test/tokenized_test.csv')
    except Exception as e:
        print(e)
        send_email(
            'Dataset Tokenization Error',
            f'Error occurred: {str(e)}',
            os.getenv('FROM_EMAIL'),
            os.getenv('TO_EMAIL')
        )

if __name__ == '__main__':
    main()
