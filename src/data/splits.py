import pandas as pd
from sklearn.model_selection import train_test_split
from .config import OUT_DIR, SEED, VAL_FRACTION, SUBSET_FRACTIONS

def build_splits(df):
    train_full = df[df['is_training'] == 1].reset_index(drop=True)
    test = df[df['is_training'] == 0].reset_index(drop=True)

    train, val = train_test_split(
        train_full, test_size=VAL_FRACTION,
        stratify=train_full['class_id'], random_state=SEED
    )

    train[['image_id']].to_csv(f'{OUT_DIR}/split_train.csv', index=False)
    val[['image_id']].to_csv(f'{OUT_DIR}/split_val.csv', index=False)
    test[['image_id']].to_csv(f'{OUT_DIR}/split_test.csv', index=False)
    print(f"Train: {len(train)}, Val: {len(val)}, Test: {len(test)}")

    for frac in SUBSET_FRACTIONS:
        if frac == 1.00:
            subset = train.copy()
        else:
            subset, _ = train_test_split(
                train, train_size=frac,
                stratify=train['class_id'], random_state=SEED
            )
        subset[['image_id']].to_csv(f'{OUT_DIR}/split_train_{int(frac*100)}pct.csv', index=False)
        print(f"{int(frac*100)}% -> {len(subset)} images, {subset['class_id'].nunique()} classes")

    return train, val, test

if __name__ == '__main__':
    df = pd.read_csv(f'{OUT_DIR}/metadata.csv')
    build_splits(df)