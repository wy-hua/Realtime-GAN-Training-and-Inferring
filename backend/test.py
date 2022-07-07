from PIL import Image
import time
# num=0
# while True:
#     time.sleep(10)
#     num+=1
#     str='%03d' % num
#     print(str)
#     img=Image.open(f'/data/lxq/GANsNRoses-main/output/sample/ema_A2B_{str}000.jpg')
#     print(img)

with open('measure.txt', 'r') as f:
    while True:
        j=0
        msg=[]
        while j<7:
            data=f.readline()
            j+=1
        
            msg.append(float(data))
    
        msg={"epochNum":msg[0],"metricList":msg[1:7]}
        print(msg)
                   