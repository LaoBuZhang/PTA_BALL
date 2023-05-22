# 使用说明

1. 第一次运行运行main.py：`python -u main.py`
   - 会做出两个动作
     1. 将时间戳（cnt.txt）设置为比赛开始的时间
     2. 将存储过题情况的字典（dict.pkl）清空
   - 然后就会开始爬取pta榜单
2. 后边中断的话，运行restartMain.py重新开始运行：`python -u restartMain.py`
   - 这次只重置时间戳，字典不在清空