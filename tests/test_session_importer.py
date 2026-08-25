from shadowauth.pipeline.session_importer import SessionImporter

importer = SessionImporter()

importer.import_file(
    "samples/raw/cowrie/controlled-session-01.jsonl"
)

print("Import completed.")