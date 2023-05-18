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
def LOG_INFO(text): #��¼��־����
    frame = inspect.currentframe()
    info = inspect.getframeinfo(frame)
    if frame.f_back is None:
        pass
    else:
        frame = frame.f_back
    caller_info = inspect.getframeinfo(frame)
    color = random.choice(list(colors.keys()))
    print(colors[color] + "[DEBUG] ---[" + inspect.stack()[1][3] + "+" + str(caller_info.lineno) + "]" +text + '\033[0m')
def LOG_WARN(text): #��¼������Ϣ��־����
    print('\033[31m' + "[WARN] ---[" + inspect.stack()[1][3] + "] " + text + '\033[0m')
### ��ȡ�û����������
def getInput():
    global descriptions
    global folder_name
    global num
    global _prefix
    while True:
        folder_name=input("[Tea] Ҫ�������ļ�������(�������ɵ�Json��λ�ļ�):")
        if(folder_name=="" or folder_name == None):
            folder_name = "teleports"
        try:
            os.mkdir(folder_name)  # �����ļ���
            LOG_INFO("[Tea] �Ѵ����ļ���")
            break
        except (Exception, BaseException) as e:
            LOG_WARN(f"[Tea] �����ļ���ʧ��:  {e}  ")

    while True:
        num=input("[Tea] Ҫ���ɵ�Json��λ����:")
        if num.isdigit():
            break
        LOG_WARN('[Tea] ������һ������')

    num=int(num)

    _prefix=input("[Tea] Ҫ���ɵ�Json��λ���ڲ�������Ϣǰ׺(���� TetQing- ):")
    descriptions=input("[Tea] Ҫ���ɵ�Json��λ���ڲ������Ϣ:")
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
### �����ڲ��ļ��ṹ����Ŀ���ļ�����д���ļ�
def generate():
    start = time.time()
    for i in range(1, num):  
        filename = f'{_prefix}{i}'
        x = round(random.uniform(-180, 180), 13)
        y = round(random.uniform(-90, 90), 13)
        z = round(random.uniform(-180, 180), 13)
        #json�ļ��ڲ���ʽ
        json_data = {
            "description": descriptions, #����ֶ�
            "name": filename,  #�����ֶ�
            "position": [x, y, z] #�����ֶ�
        }
        json_data = json.dumps(json_data)
        with open(f'{folder_name}/{filename}.json', 'x') as f:  
            f.write(json_data)
    end = time.time()
    return round(end-start, 2)
# �Ż���ĳ���    

_init()
getInput()
start_time = time.time() 
# �ָ�����,ÿ���̸߳���һ����
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
# �ȴ������߳����
for t in threads:
    t.join()

LOG_INFO(f'[Tea] �����ʱ: {time.time() - start_time}s')