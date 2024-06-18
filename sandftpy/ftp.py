import ftplib
import os
from pathlib import Path
from datetime import datetime


def ftp_connect(
    hostname: str, portnumber: int, username: str, password: str, timeout: int = 10
):
    """Connect to the server via FTP

    Args:
        hostname (str): Host name of the server to connect to
        portnumber (int): Port number of the server to connect to
        username (str): User name of the server to connect to
        password (str): Password for the server to connect to
        timeout (int, optional): Timeout time of the connection. Defaults to 10.

    Returns:
        FTP: FTP object
    """
    ftp = ftplib.FTP()
    ftp.connect(hostname, portnumber, timeout)
    ftp.login(username, password)
    return ftp


def upload_files_via_ftp(
    list_upload_files, dct_ftp, tmp_dir: str = str(Path(__file__).parent)
):
    UPLOAD_HOSTNAME: str = dct_ftp["upload_hostname"]
    UPLOAD_PORT: int = int(dct_ftp["upload_port"])
    UPLOAD_FTPUSERNAME: str = dct_ftp["upload_ftpusername"]
    UPLOAD_PASSWORD: str = dct_ftp["upload_password"]
    UPLOAD_REMOTEDIR: str = dct_ftp["upload_remotedir"]

    print(f"アップロード開始")
    remotepath_list = []
    with ftp_connect(
        UPLOAD_HOSTNAME, UPLOAD_PORT, UPLOAD_FTPUSERNAME, UPLOAD_PASSWORD
    ) as ftp:
        for file in list_upload_files:
            parsed_file_name = urllib.parse.urlparse(
                str(file)
            )  # ファイル名を取得するためにパース
            file_name = os.path.basename(parsed_file_name.path)  # ファイル名のみを取得
            remotepath = os.path.join(
                UPLOAD_REMOTEDIR, file_name
            )  # アップロード先のパス(リモート)
            remotepath_list.append(remotepath)  # アップロード先のパスをリストに追加
            localpath = str(file)  # アップロードしたいファイルのパス(ローカル)
            with open(localpath, "rb") as file_obj:
                ftp.storbinary(f"STOR {remotepath}", file_obj)  # アップロード

    print(f"アップロード完了")

    return remotepath_list


# 実行例
dct_ftp = {
    "upload_hostname": "ftp.example.com",
    "upload_port": 21,
    "upload_ftpusername": "username",
    "upload_password": "password",
    "upload_remotedir": "/remote/dir/",
}

list_upload_files = [Path(tmp_dir) / "filtered_data.csv"]
upload_files_via_ftp(list_upload_files, dct_ftp)
