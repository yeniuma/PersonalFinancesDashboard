from google.cloud import storage
import os

DATA_ROOT = "DataForFinanceDashboard"
BUCKET_NAME = "finance-data-storage"


def upload_raw_df_as_excel(df, df_name):
    path = os.path.join([DATA_ROOT, "raw", df_name])
    _upload_df_as_excel(path, df)


def upload_clean_df_as_excel(df, df_name):
    path = os.path.join([DATA_ROOT, "clean", df_name])
    _upload_df_as_excel(path, df)


def _upload_df_as_excel(path, df):
    _get_bucket().blob(path).upload_from_string(df.to_excel())


def _get_bucket():
    storage_client = storage.Client()
    return storage_client.bucket(BUCKET_NAME)



    