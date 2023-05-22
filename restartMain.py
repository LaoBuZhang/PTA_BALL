import get_balloon
import time


with open('cnt.txt', 'w') as f:
    f.write("2023/05/21 09:00:00")
contest_id="1659939214638964736"

i=0
while True:
    i=i+1
    if(i%8==0):
        i=i%8
        with open('cnt.txt', 'w') as f:
            f.write("2023/05/21 09:00:00")
    time.sleep(15)
    get_balloon.asr_main(contest_id)