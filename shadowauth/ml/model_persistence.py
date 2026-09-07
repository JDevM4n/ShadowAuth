from datetime import datetime, timezone
from pathlib import Path

import joblib


class ModelPersistence:
    """
    Persists trained ShadowAuth ML artifacts using joblib.
    """

    ARTIFACT_VERSION = "1.0"

    @classmethod
    def save(
        cls,
        model,
        path,
        metadata=None,
        feature_names=None,
    ) -> Path:

        model_path = Path(path)

        model_path.parent.mkdir(
            parents=True,
            exist_ok=True,
        )

        artifact = {
            "artifact_version": cls.ARTIFACT_VERSION,
            "saved_at": datetime.now(
                timezone.utc
            ).isoformat(),
            "model": model,
            "metadata": metadata or {},
            "feature_names": (
                list(feature_names)
                if feature_names is not None
                else None
            ),
        }

        joblib.dump(
            artifact,
            model_path,
        )

        return model_path

    @staticmethod
    def load(path) -> dict:

        model_path = Path(path)

        if not model_path.exists():

            raise FileNotFoundError(
                f"Model artifact not found: "
                f"{model_path}"
            )

        artifact = joblib.load(
            model_path
        )

        if not isinstance(
            artifact,
            dict,
        ):

            raise ValueError(
                "Invalid ShadowAuth model artifact."
            )

        if "model" not in artifact:

            raise ValueError(
                "Model artifact does not contain "
                "a trained model."
            )

        return artifact

    @classmethod
    def load_model(
        cls,
        path,
    ):

        artifact = cls.load(
            path
        )

        return artifact["model"]