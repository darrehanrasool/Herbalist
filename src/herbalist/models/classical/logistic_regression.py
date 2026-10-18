"""Multinomial Logistic Regression with L2 regularization."""
from sklearn.linear_model import LogisticRegression


def get_logistic_regression(
    C: float = 1.0,
    max_iter: int = 1000,
    random_state: int = 42
) -> LogisticRegression:
    """Instantiate calibrated Multinomial Logistic Regression model."""
    return LogisticRegression(
        C=C,
        penalty="l2",
        solver="lbfgs",
        max_iter=max_iter,
        random_state=random_state
    )
