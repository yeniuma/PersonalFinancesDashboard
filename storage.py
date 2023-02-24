import posixpath
from google.cloud import storage
import os


DATA_ROOT = "DataForFinanceDashboard"
CLEAN_DATA_FOLDER = posixpath.join(DATA_ROOT, "clean")
RAW_DATA_FOLDER = posixpath.join(DATA_ROOT, "raw")
BUCKET_NAME = "finance-data-storage"


def upload_raw_df_as_excel(df, df_name):
    path = posixpath.join(RAW_DATA_FOLDER, df_name)
    _upload_df_as_excel(path, df, df_name)


def upload_clean_df_as_excel(df, df_name):
    path = posixpath.join(CLEAN_DATA_FOLDER, df_name)
    _upload_df_as_excel(path, df, df_name)


def get_raw_excel_files():
    blobs = _get_bucket().list_blobs(prefix=RAW_DATA_FOLDER)
    return _get_names_from_blobs(blobs)


def get_clean_excel_files():
    blobs = _get_bucket().list_blobs(prefix=CLEAN_DATA_FOLDER)
    return _get_names_from_blobs(blobs)


def get_excel_as_bytes(folder, file_name):
    file_path = posixpath.join(folder, file_name)
    blob = _get_bucket().blob(file_path)
    return blob.download_as_bytes()


def get_processed_excel_bookkeper_file_path():
    return posixpath.join(DATA_ROOT, "processed_excels.txt")


def _get_names_from_blobs(blobs):
    names = [blob.name for blob in blobs]
    return names[1:]


def _upload_df_as_excel(path, df, df_name):
    df.to_excel(df_name)
    _get_bucket().blob(path).upload_from_filename(df_name)


def _get_bucket():
    return storage.Client().bucket(BUCKET_NAME)
    