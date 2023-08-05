from . import Utils
import os
import shutil

__version__ = 1.1907301636

"""
    UPDATE

    Ver 1.1905081530
        - register 함수 생성
        - delete 함수 생성
"""

__fonts__ = os.path.dirname(os.path.realpath(__file__)).replace("\\","/") +"/fonts/"

def register(uri, title):
    r_path = __fonts__ + title + ".ttf"
    path = Utils.download(uri, r_path, ['ttf'])
    if path is None:
        print("경로가 잘못되었거나 호환되지 않은 font입니다. ttf 확장자만 등록가능합니다.")
        return False
    
    if r_path == path:
        return True

    shutil.copy2(path, r_path)

    return True

def delete(title):
    os.remove(__fonts__+title+".ttf")