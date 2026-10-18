"""Random Forest Classifier for botanical and soil tabular properties."""
from sklearn.ensemble import RandomForestClassifier


def get_random_forest(
    n_estimators: int = 100,
    max_depth: int = 15,
    min_samples_split: int = 5,
    random_state: int = 42
) -> RandomForestClassifier:
    """Instantiate Random Forest Classifier with ensemble averaging."""
    return RandomForestClassifier(
        n_estimators=n_estimators,
        max_depth=max_depth,
        min_samples_split=min_samples_split,
        random_state=random_state,
        n_jobs=-1
    )
