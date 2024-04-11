#!/bin/bash

# Run the first training iteration
eval python3 train.py --input_file ./data/raw/train_0.csv --epochs 5
if [ $? -ne 0 ]; then
    echo "Training failed at iteration 0 with input file ./data/raw/train_0.csv"
    exit 1
fi
    
for i in {1..39}
do
    input_file="./data/raw/train_$i.csv"
    # train on i-1 model
    output_dir="./models/train_$((i-1))"
    command="python3 train.py --input_file $input_file --load_model_dir $output_dir --epochs 5"

    echo "Running command: $command"
    eval $command

    # Update load_model_dir for the next iteration, assuming the script saves the model to a directory named after the input file
    output_dir="./models/train_$i"

    # Check if the command was successful
    if [ $? -ne 0 ]; then
        echo "Training failed at iteration $i with input file $input_file"
        exit 1
    fi
done

mv ./models/train_39 ./models/final_model

eval python3 notify.py

echo "Training completed for all files."