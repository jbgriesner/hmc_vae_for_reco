import os
import numpy as np
from tqdm import tqdm

def concatenate_files(file, pattern):
    """
        If the ratings/checkins file exists for each dataset, we do nothing,
        otherwise we just concatenate the pieces of files
    """
    if not os.path.exists(file):
        checkins_files = glob.glob(pattern)
        with open(file, 'w') as out_file:
            input_lines = fileinput.input(checkins_files)
            prev_line = None
            for line in tqdm(input_lines):
                if not fileinput.isfirstline():  # first lines are corrupted
                    if prev_line is not None:    # last lines are corrupted
                        out_file.write(prev_line)
                    prev_line = line

def train_tune_test_split(clean_DIR, X, test_min_clicks):
    """
        Split the 'X' matrix into train, tune and test .tsv files
        in the given 'clean_DIR' folder.
    """
    train_file = f"{clean_DIR}/train.tsv"
    tune_file = f"{clean_DIR}/tune.tsv"
    test_file = f"{clean_DIR}/test.tsv"

    if os.path.exists(train_file):
        os.remove(train_file)
    if os.path.exists(tune_file):
        os.remove(tune_file)
    if os.path.exists(test_file):
        os.remove(test_file)

    all_items = []
    with open(train_file, 'w') as train, open(tune_file, 'w') as tune, open(test_file, 'w') as test:
        user = 0
        for row in tqdm(X):
            if row.sum() < test_min_clicks:
                all_items.extend(row.nonzero()[1])
        for row in tqdm(X):
            items = row.nonzero()[1]
            np.random.shuffle(items)
            if row.sum() > test_min_clicks:
                splits = np.split(items, [int(.8 * len(items)), int(.9 * len(items))])
                for item in splits[0]:
                        train.write(f"{user}\t{item}\n")
                for item in splits[1]:
                    if item in all_items:
                        tune.write(f"{user}\t{item}\n")
                for item in splits[2]:
                    if item in all_items:
                        test.write(f"{user}\t{item}\n")
            else:
                for item in items:
                    train.write(f"{user}\t{item}\n")
            user += 1
