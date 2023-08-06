import os
import re
import json
import time
import hashlib
import datetime
import subprocess

def getTime():
    """
    获取时间
    :return: example(2019-05-14 18:57:04.199382)
    """
    return datetime.datetime.now()

def getData():
    """
    获取日期
    :return: example(2019-05-14)
    """
    return time.strftime('%Y-%m-%d', time.localtime())

def writeFile(grade, outFile, info):
    """
    向文件写入信息
    :param grade: 写入方式(1:追加, 2:覆盖)
    :param outFile: 文件路径
    :param info: 信息
    :return: 无
    """
    if grade == 1:
        f = open(outFile, 'a+', encoding='utf-8')
        f.write((info + '\n').encode('utf-8', 'ignore').decode('utf-8'))
        f.close()
    elif grade == 2:
        f = open(outFile, 'w+', encoding='utf-8')
        f.write(info.encode('utf-8', 'ignore').decode('utf-8'))
        f.close()

def getFileMd5(filePath):
    """
    获取文件md5
    :param filePath: 文件路径
    :return: 文件md5
    """
    f = open(filePath, 'rb')
    md5 = hashlib.md5(f.read()).hexdigest()
    f.close()
    return md5

def jsonToDict(jsonPath):
    """
    json文件转dict
    :param jsonPath: json文件路径
    :return: dict
    """
    f = open(jsonPath, 'r', encoding='utf-8')
    jsonDict = json.load(f)
    f.close()
    return jsonDict

def funcRunTime(func):
    """
    装饰器函数，输出函数运行时间
    :param func: 函数
    :return: 函数运行时间
    """
    def wrapper(*args, **kwargs):
        startTime = getTime()
        funcName = str(func).split()[1]
        output = func(*args, **kwargs)
        endTime = getTime()
        printInfo(1, str(endTime - startTime) + ' : ' + funcName)
        return output
    return wrapper

def printInfo(grade, info):
    """
    打印信息
    :param grade: log等级(1:普通信息, 2:捕获错误信息, 3:可预料错误信息)
    :param info: 信息
    :return: 无
    """
    if grade == 1:
        info = info
    elif grade == 2:
        info = "\033[0;31m%s\033[0m" % "Error: {0} : {1} : {2}".format(
            str(info),
            str(info.__traceback__.tb_frame.f_globals['__file__']),
            str(info.__traceback__.tb_lineno))
    elif grade == 3:
        info = "\033[0;31m%s\033[0m" % "Error: {0}".format(str(info))
    print(info)

def renameFile(filePath):
    """
    重命名文件，避免文件名中含有特殊字符造成解析失败
    :param filePath: 文件路径
    :return: 重命名信息
    """
    temp_name = re.sub('[^A-Za-z0-9.]', '_', os.path.basename(filePath))
    os.rename(filePath, os.path.dirname(filePath) + '/' + temp_name)
    return os.path.dirname(filePath) + '/' + temp_name

def osSystem(command):
    """
    以os.system方式执行shell命令
    :param command: shell命令
    :return: 无
    """
    try:
        os.system(command)
    except Exception as msg:
        printInfo(2, msg)

def getOutputStatus(command):
    """
    以subprocess的方式执行shell命令
    :param command: shell命令
    :return: 执行状态，命令执行结果
    """
    try:
        (status, outPut) = subprocess.getstatusoutput(command)
        return status, outPut
    except Exception as msg:
        printInfo(2, msg)
        return -1, ''
