from shadowauth.dataset.dataset_validator import DatasetValidator


validator = DatasetValidator(
    "datasets/dataset.csv"
)

validator.generate_report()