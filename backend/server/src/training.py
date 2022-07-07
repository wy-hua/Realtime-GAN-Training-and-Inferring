import os
import  time
#在本文件中修改socketio也会反映在app文件中
class Train:
    def __init__(self,socketio):
        self.socketio=socketio
        self.isTraining=False

        #调用listen 开始监听前端发来的开始/暂停训练的请求
    def Listen(self):
        self.GetPara()
        self.StopTraining()
        self.ListenInferRequest()
    def TrainFuc(self):
        self.isTraining = True
        preLocalTime=time.localtime(time.time())
        epochN=5
        while (self.isTraining):
            localtime = time.localtime(time.time())
            localtime2 = time.asctime(time.localtime(time.time()))
            if (localtime.tm_sec % 3 == 0 and preLocalTime!=localtime):
                print(localtime2)
                self.socketio.emit("sendResult", localtime2)
            if(localtime.tm_sec % 10 == 0 and preLocalTime!=localtime):
                #因为是在app.py函数中被调用所以 相对路径是相对于app.py的
                nameList,urlList=[],[]
                for m in range(4):
                    name=str(m+1)+"_real_A.png"
                    imageurl = 'src/assets/images/'+name
                    nameList.append(name)
                    urlList.append(imageurl)
                self.sendImage(nameList,urlList)
                epochN+=1
                self.sendMetric({"epochNum":epochN,"metricList":[1,2,3,4,5,6]})
            preLocalTime=localtime
        print("Training is stopped")

    #等待获取前端发来的参数   接受到之后输出参数  并开始训练
    def GetPara(self):
        @self.socketio.on('sendPara')
        def handle_trainingPara(json):
            #发过来 <class 'dict'>类型的参数
            print("received json:" + str(json))
            #定时
            num=0
            i=0
            self.isTraining=True
            with open('/data/lxq/GANsNRoses-main/measure.txt', 'r') as f:
                while self.isTraining:
                    time.sleep(6)
                    img_path='%03d' % num
                    # 需要修改为服务器端的文件路径
                    # self.sendImage(['A2B','B2A'],[f'/data/lxq/GANsNRoses-main/output/sample/ema_A2B_{img_path}000.jpg',f'/data/lxq/GANsNRoses-main/output/sample/ema_B2A_{img_path}000.jpg'])
                    num+=1
                #发送指标
                    j=0
                    msg=[j,2,3,4,5,6,7,8,9]
                    j+=1
                    # while j<7:
                    #     data=f.readline()
                    #     j+=1
                    #     msg.append(float(data))
                    msg={"epochNum":msg[0],"metricList":msg[1:7]}
                    self.sendMetric(msg)
                    print("1")
                
           
    #等待前端发来的暂停训练的请求  接到请求后令isTraining为false来暂停训练
    def StopTraining(self):
        @self.socketio.on('stopTraining')
        def handle_stop():
            print("stop training")
            self.isTraining = False

    #发送指标   结构为 {"epochNum":10,"metricList":[1,2,3,4,5,6]}
    def sendMetric(self,msg):
        self.socketio.emit('MetricMsg',msg)

    #发送图片   参数分别为图片名的列表  图片本地路径的列表  图片格式限于png  路径必须将对于实例化对象的程序
    def sendImage(self,imageNameList:list,imageUrlList:list):
        dictList=[]
        for i in range(len(imageUrlList)):
            with open(imageUrlList[i], 'rb') as f:
                image_data = f.read()
                dictList.append({'image_name':imageNameList[i],'image_data': image_data})
        self.socketio.emit('ImageMsg', dictList)

    def ListenInferRequest(self):
        @self.socketio.on('InferRequest')
        def handle(data):
            print(data.keys())
            with open('src/assets/images/1.png', 'wb') as f:
                f.write(data['file'])
            self.run_python()
            with open('/data/lxq/GANsNRoses-main/server/test.png', 'rb') as f:
                image_data = f.read()
                return {'image_name':'test.png','image_data': image_data}
            # imageName=''
            # imageUrl=''
            # with open(imageUrl, 'rb') as f:
            #     image_data = f.read()
            #     self.socketio.send({'image_name': imageName, 'image_data': image_data})


    #运行训练或者推理
    def run_python(self):
        os.environ['MKL_THREADING_LAYER'] = 'GNU' 
                                                                             
        
        os.system('python /data/lxq/GANsNRoses-main/test_infer.py')

