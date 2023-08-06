import re
import pandas as pd
import boto3
from boto3.session import Session

class write_s3():
    def __init__(self, s3_profile='put_s3_lambda'):
        session = Session(profile_name=s3_profile)  # s3にアクセスするためのプロファイルを指定
        self.__s3 = session.client('s3')
        
    def to_csv(self, df: pd.DataFrame, bucket, key, index=True, encoding="utf_8"):
        """
        変数dfをbucketバケットのkeyパスに書き出す
            * df: pandasのデータフレーム
            * bucket: アップロードしたいバケット名
            * key: アップロードしたバケット内のファイルパス
        ※ 存在しないバケットにもアップロードできます
        """
        bytes_to_write = df.to_csv(None, index=index, encoding=encoding).encode(encoding)
        self.__s3.put_object(ACL='private', Body=bytes_to_write, Bucket=bucket, Key=key)
