"""Local-only survey loading and aggregate summaries for the JOJ dashboard."""
from __future__ import annotations
from pathlib import Path
import pandas as pd

QUESTION_NAMES = ("Like", "Wish", "What_If", "Share")
COMMON = ("Timestamp", "Presenter", "Session Topic", "Please indicate your current maternal stage or support role.", "Gender", "Age")
RENAMES = {
    1: {"I like...": "Like", "I wish...": "Wish", "What if...": "What_If", "Is there anything else you would like to share about your experience?": "Share"},
    2: {"One thing, or more, that I liked...": "Like", "One thing, or more, I wished would have happened": "Wish", "One thing, or more, that could be done in the future...": "What_If", "Is there anything else you would like to share about your experience?": "Share"},
}

def load_surveys(data_dir: str | Path = 'private_data') -> pd.DataFrame:
    """Read locally stored surveys; never log or display free-text responses."""
    root = Path(data_dir)
    frames = []
    for year in (1, 2):
        path = root / f'Year{year} - Form Responses 1.csv'
        if not path.is_file():
            raise FileNotFoundError(f'Missing local survey file: {path}')
        frame = pd.read_csv(path)
        required = set(COMMON) | set(RENAMES[year])
        missing = required - set(frame.columns)
        if missing:
            raise ValueError(f'Year {year} is missing expected columns: {sorted(missing)}')
        frame = frame.rename(columns=RENAMES[year]).copy()
        frame['Year'] = f'Year {year}'
        frames.append(frame)
    return pd.concat(frames, ignore_index=True)

def count_by_year(df: pd.DataFrame) -> pd.DataFrame:
    return df.groupby('Year', sort=True).size().rename('Survey records').reset_index()

def feedback_completion(df: pd.DataFrame) -> pd.DataFrame:
    records = []
    for year, group in df.groupby('Year', sort=True):
        for question in QUESTION_NAMES:
            answered = group[question].fillna('').astype(str).str.strip().ne('').sum()
            records.append({'Year': year, 'Question': question, 'Answered': int(answered),
                            'Total': len(group), 'Completion (%)': round(100 * answered / len(group), 1) if len(group) else 0})
    return pd.DataFrame(records)

def grouped_counts(df: pd.DataFrame, column: str, min_group_size: int = 5) -> pd.DataFrame:
    """Suppress categories with fewer than min_group_size records for display."""
    if column not in ('Gender', 'Age', 'Please indicate your current maternal stage or support role.', 'Session Topic'):
        raise ValueError('Unapproved grouping column')
    values = df[column].fillna('Not provided').astype(str).str.strip().replace('', 'Not provided')
    counts = values.value_counts().rename_axis('Category').reset_index(name='Survey records')
    return counts[counts['Survey records'] >= min_group_size].reset_index(drop=True)
