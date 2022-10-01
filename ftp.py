import ftplib
import json


def upload_file(idx, count, need_to_load):
    # print(idx)
    if not need_to_load:
        return
    # Fill Required Information
    HOSTNAME = "31.31.196.105"
    USERNAME = "u1554528"
    PASSWORD = "YFv-XSU-36m-2m3"

    # Connect FTP Server
    ftp_server = ftplib.FTP(HOSTNAME, USERNAME, PASSWORD)

    ftp_server.cwd("www/omgu-schedule.alexpl.site/")

    # force UTF-8 encoding
    ftp_server.encoding = "utf-8"

    if idx is not None:
        # Enter File Name with Extension
        filename = f"data{idx}.json"

        # ftp_server.delete(f"{filename}")

        # Read file in binary mode
        with open(filename, "rb") as file:
            # Command for Uploading the file "STOR filename"
            ftp_server.storbinary(f"STOR {filename}", file)

    else:
        with open("count.json", "w", encoding='utf-8') as jsonfile:
            json.dump({'count': count}, jsonfile, ensure_ascii=False)
        # Enter File Name with Extension
        filename = "count.json"

        # ftp_server.delete(f"{filename}")

        # Read file in binary mode
        with open(filename, "rb") as file:
            # Command for Uploading the file "STOR filename"
            ftp_server.storbinary(f"STOR {filename}", file)

    # Get list of files
    ftp_server.dir()

    # Close the Connection
    ftp_server.quit()
