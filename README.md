```bash
grammar-corrector-project/
│
├── data/                        # Directory for raw and processed data
│   ├── raw/                     # Store raw data here
│   │   ├── lang-8-en-1.0/       # Lang-8 dataset
│   │   ├── jfleg/               # JFLEG dataset
│   │   └── cola_public/         # CoLA dataset
│   │
│   └── processed/               # Processed and tokenized data ready for training
│       ├── train/
│       ├── val/
│       └── test/
│
├── models/                      # Trained models and model checkpoints
│   ├── t5-base/                 # T5-base model checkpoints
│   └── ...
│
├── notebooks/                   # Jupyter notebooks for experimentation and demos
│   ├── DataExploration.ipynb
│   └── ModelDemo.ipynb
│
├── requirements.txt             # Project dependencies and libraries
├── setup.py                     # Setup script for installing the project as a module
└── README.md                    # Project overview, setup, and usage instructions
```

# Run Frontend

To run the frontend, follow these steps:

1. Navigate to the frontend directory:

   ```bash
   cd frontend/
   ```

2. Install the required libraries:

   ```bash
   npm i
   ```

3. Start the development server:
   ```bash
   npm run dev
   ```

This will start the frontend server and you can access it in your browser at the specified URL.

# Run Backend

To run the backend, follow these steps:

1. Navigate to the backend directory:

   ```bash
   cd backend/
   ```

2. Install the required libraries:

   ```bash
   pip install -r requirements.txt
   ```

3. Start the backend server:
   ```bash
   python server.py
   ```

This will start the backend server and you can access it in your browser at the specified URL.

# Train model on remote GPU server

```bash
nohup ./train_sequential.sh > output.log &
```

# Monitor training progress

```bash
tail -f output.log
```

# Kill training job on remote GPU server

```bash
ps -ef | grep train.py
kill -9 <PID>
```
