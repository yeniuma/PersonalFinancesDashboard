import os


def setup_files_and_folders():
    folders = [
        "DataForFinanceDashboard",
        "DataForFinanceDashboard/raw",
        "DataForFinanceDashboard/clean",
    ]
    for f in folders:
        if not os.path.exists(f"{f}"):
            os.mkdir(f"{f}")

    if not os.path.exists("DataForFinanceDashboard/processed_excels.txt"):
        with open("DataForFinanceDashboard/processed_excels.txt", mode="w"):
            pass


if __name__ == "__main__":
    setup_files_and_folders()
