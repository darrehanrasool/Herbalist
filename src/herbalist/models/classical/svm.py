"""Support Vector Machine with Radial Basis Function (RBF) kernel."""
from sklearn.svm import SVC


def get_svm(
    C: float = 1.0,
    kernel: str = "rbf",
    gamma: str = "scale",
    probability: bool = True,
    random_state: int = 42
) -> SVC:
    """Instantiate Support Vector Classifier with Platt probability calibration."""
    return SVC(
        C=C,
        kernel=kernel,
        gamma=gamma,
        probability=probability,
        random_state=random_state
    )
