import pandas as pd

from shadowauth.ml.dataset_splitter import (
    DatasetSplitter,
)


def create_dataset():

    rows = []

    for index in range(20):

        label = (
            "attack"
            if index < 10
            else "benign"
        )

        rows.append(
            {
                "session_id": f"session-{index}",
                "duration_seconds": 30 + index,
                "command_count": 5,
                "unique_command_count": 3,
                "login_attempts": 2,
                "successful_login": True,
                "download_count": 1,
                "source_ip": f"192.168.1.{index + 1}",
                "destination_ip": "192.168.1.100",
                "source_port": 40000 + index,
                "destination_port": 2222,
                "protocol": "ssh",
                "process_count": 0,
                "shell_spawned": False,
                "sensitive_file_access": False,
                "max_severity": 5,
                "average_severity": 2.5,
                "session_hour": 12,
                "weekend": False,
                "label": label,
            }
        )

    return pd.DataFrame(rows)


def test_dataset_splitter(
    tmp_path,
):

    dataset = create_dataset()

    dataset_path = (
        tmp_path / "dataset.csv"
    )

    dataset.to_csv(
        dataset_path,
        index=False,
    )

    splitter = DatasetSplitter(
        str(dataset_path)
    )

    (
        x_train,
        x_test,
        y_train,
        y_test,
    ) = splitter.split()

    assert len(x_train) == 16

    assert len(x_test) == 4

    assert len(y_train) == 16

    assert len(y_test) == 4

    assert (
        "session_id"
        not in x_train.columns
    )

    assert (
        "source_ip"
        not in x_train.columns
    )

    assert (
        "destination_ip"
        not in x_train.columns
    )

    assert (
        "protocol"
        not in x_train.columns
    )

    assert (
        "label"
        not in x_train.columns
    )


def test_splitter_rejects_unlabeled(
    tmp_path,
):

    dataset = create_dataset()

    dataset.loc[
        0,
        "label",
    ] = "unlabeled"

    dataset_path = (
        tmp_path / "dataset.csv"
    )

    dataset.to_csv(
        dataset_path,
        index=False,
    )

    splitter = DatasetSplitter(
        str(dataset_path)
    )

    try:

        splitter.split()

        assert False, (
            "Expected ValueError"
        )

    except ValueError as error:

        assert "unlabeled" in str(
            error
        ).lower()