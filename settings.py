#файл щляху до папок зі стилями і потрібниминам файлами
import os

FOLDER = os.getcwd()
TEMPLATE = os.path.join(FOLDER, "template")
STATIC = os.path.join(FOLDER, "static")
UPPLOADS = os.path.join(STATIC, "upploads")

sec = 'verystrongkey'