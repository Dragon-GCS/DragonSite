# coding = utf-8
# Dragon's Python3.8 code
# Created at 2021/5/8 21:50
# Edit with PyCharm

import hashlib

def get_md5(path:str) -> str:
    #MD5计算速度比sha1快
    digest = hashlib.md5()
    with open(path, 'rb') as fobj:
        while True:
            data = fobj.read(4096)
            if not data:
                break
            digest.update(data)
    return digest.hexdigest()


def get_unique_folder_name(name:str, folder_list:list) -> str :
    ## 检查是否有重名的文件夹并按顺序生成新名称
    cont = 1
    while f'{name}({cont})' in folder_list:
        cont += 1
    name = f'{name}({cont})'
    return name