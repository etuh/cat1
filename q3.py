import json
import pandas as pd
import glob

file_path = 'data/en-US.jsonl'
directory_path = 'data'
output_folder = 'output/q3'

en_df = pd.read_json(path_or_buf=file_path, lines=True)
# Select only the desired columns
selected_columns = ['id', 'utt']
en_df = en_df[selected_columns]

jsonl_files = glob.glob(f'{directory_path}/*.jsonl')

for file_path in jsonl_files:
    df = pd.read_json(path_or_buf=file_path, lines=True)

    with open(file_path, 'r', encoding='utf-8') as file:  # Use the current file_path in the loop
        # Read each line as a JSON object
        for line in file:
            data = json.loads(line)

            # Filter for the "train" partition
            if data['partition'] == 'train':
                # Check if 'utt' column exists in the current DataFrame
                if 'utt' in df.columns:
                    df = df[selected_columns]
                    df = df.rename(columns={'utt': f'utt-{file_path[:2]}'})
                    merged_df = pd.merge(en_df, df, on='id', how='inner')

# Create a JSON file containing all translations
output_json = f'{output_folder}/all_translations.json'

with open(output_json, 'w', encoding='utf-8') as output_file:
    # Pretty print the JSON structure
    json.dump(merged_df.to_dict(orient='records'), output_file, indent=4, ensure_ascii=False)
