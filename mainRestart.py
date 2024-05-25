import get_balloon
import time
import json

# 读取配置文件
cfg={}
with open('cfg.json', 'r') as f:
    cfg = json.load(f)
contest_id=cfg['contest_id']
# 将上一次爬取的时间写入文件，重新启动时从0开始爬取一次
with open('cnt.txt', 'w') as f:
    f.write(cfg['start_time'])


i=0
while True:
    # 每爬取8次，从第一条爬取一次，获取到爬取时正在评测的数据
    i=i+1
    if(i%8==0):
        i=i%8
        with open('cnt.txt', 'w') as f:
            f.write(f.write(cfg['start_time']))
    time.sleep(15)
    get_balloon.asr_main(contest_id)