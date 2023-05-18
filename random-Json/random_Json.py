# codeing by https://github.com/Xcating
import inspect
import random 
import os 
import json
import time
import threading

def _init():
    global colors
    global last_color

    last_color = None
    colors = {
    'green': '\033[32m',
    'yellow': '\033[33m',
    'blue': '\033[34m',
    'magenta': '\033[35m',
    'cyan': '\033[36m',
    'bright_red': '\033[1;31m',
    'bright_green': '\033[1;32m', 
    'bright_yellow': '\033[1;33m',
    'bright_blue': '\033[1;34m',  
    'bright_magenta': '\033[1;35m',  
    'bright_cyan': '\033[1;36m',
    'bright_white': '\033[1;37m',  
    'crimson': '\033[38;5;196m',
    'coral': '\033[38;5;216m',
    'teal': '\033[38;5;33m',
    'steel_blue': '\033[38;5;37m',
    'eggshell': '\033[38;5;252m',
    'lavender': '\033[38;5; 181m',
}
def LOG_INFO(text): #记录日志部分
    frame = inspect.currentframe()
    info = inspect.getframeinfo(frame)
    if frame.f_back is None:
        pass
    else:
        frame = frame.f_back
    caller_info = inspect.getframeinfo(frame)
    color = random.choice(list(colors.keys()))
    print(colors[color] + "[DEBUG] ---[" + inspect.stack()[1][3] + "+" + str(caller_info.lineno) + "]" +text + '\033[0m')
def LOG_WARN(text): #记录错误信息日志部分
    print('\033[31m' + "[WARN] ---[" + inspect.stack()[1][3] + "] " + text + '\033[0m')
### 获取用户输入的内容
def getInput():
    global descriptions
    global folder_name
    global num
    global _prefix
    while True:
        folder_name=input("[Tea] 要创建的文件夹名称(放置生成的Json点位文件):")
        if(folder_name=="" or folder_name == None):
            folder_name = "teleports"
        try:
            os.mkdir(folder_name)  # 创建文件夹
            LOG_INFO("[Tea] 已创建文件夹")
            break
        except (Exception, BaseException) as e:
            LOG_WARN(f"[Tea] 创建文件夹失败:  {e}  ")

    while True:
        num=input("[Tea] 要生成的Json点位个数:")
        if num.isdigit():
            break
        LOG_WARN('[Tea] 请输入一个数字')

    num=int(num)

    _prefix=input("[Tea] 要生成的Json点位，内部名称信息前缀(例如 TetQing- ):")
    descriptions=input("[Tea] 要生成的Json点位，内部简介信息:")
def generate_json(start, end):
    for i in range(start, end):  
        filename = f'{_prefix}{i}'
        x = round(random.uniform(-7000, 6000), 13)
        y = round(random.uniform(40, 200), 13)
        z = round(random.uniform(-7000, 6000), 13)
        json_data = {
            "description": descriptions,  
            "name": filename,  
            "position": [x, y, z] 
        }
        json_data = json.dumps(json_data)
        with open(f'{folder_name}/{filename}.json', 'x') as f:  
            f.write(json_data)
### 生成内部文件结构并在目标文件夹内写入文件
def generate():
    start = time.time()
    for i in range(1, num):  
        filename = f'{_prefix}{i}'
        x = round(random.uniform(-180, 180), 13)
        y = round(random.uniform(-90, 90), 13)
        z = round(random.uniform(-180, 180), 13)
        #json文件内部格式
        json_data = {
            "description": descriptions, #简介字段
            "name": filename,  #名称字段
            "position": [x, y, z] #坐标字段
        }
        json_data = json.dumps(json_data)
        with open(f'{folder_name}/{filename}.json', 'x') as f:  
            f.write(json_data)
    end = time.time()
    return round(end-start, 2)
# 优化后的程序    

_init()
getInput()
start_time = time.time() 
# 分割任务,每个线程负责一部分
step = num // 32  
threads = []
for i in range(32):
    start = i * step + 1
    end = (i + 1) * step + 1
    if i == 31:  
        end = num + 1 
    t = threading.Thread(target=generate_json, args=(start, end))
    threads.append(t)
    t.start()
# 等待所有线程完成
for t in threads:
    t.join()

LOG_INFO(f'[Tea] 完成用时: {time.time() - start_time}s')