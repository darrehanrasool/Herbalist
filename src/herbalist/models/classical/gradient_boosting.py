"""Gradient Boosting Decision Trees for agronomic and yield prediction."""
from sklearn.ensemble import GradientBoostingClassifier


def get_gradient_boosting(
    n_estimators: int = 100,
    learning_rate: float = 0.1,
    max_depth: int = 5,
    random_state: int = 42
) -> GradientBoostingClassifier:
    """Instantiate Gradient Boosting Classifier with deviance loss."""
    return GradientBoostingClassifier(
        n_estimators=n_estimators,
        learning_rate=learning_rate,
        max_depth=max_depth,
        random_state=random_state
    )
