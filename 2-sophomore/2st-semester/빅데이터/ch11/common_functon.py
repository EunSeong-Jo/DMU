import os


def save_csv(df_ds, file_name):
    if os.path.exists(file_name):
        os.remove(file_name)
    df_ds.to_csv(file_name)
#end-def