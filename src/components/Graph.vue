<template>
  <div class="MiddleImage">
    <span class="graphTitle">Image during training</span>
    <el-carousel
        height="650px"
        autoplay="false"
        style="margin-top: 5px"
    >
      <el-carousel-item >
        <el-image
            fit="fill"
            :src="url1"></el-image>
      </el-carousel-item>
      <el-carousel-item >
        <el-image
            fit="contain"
            :src="url2"></el-image>
      </el-carousel-item>
    </el-carousel>

  </div>

  <div class="secondPart">
    <el-row :gutter="5" style="height: 300px">
      <el-col
          :span="4"
          v-for="item in 6"
          :key="item"
      >
        <div class="echartGraph"></div>
      </el-col>

    </el-row>
  </div>
</template>

<script setup>
import * as echarts from 'echarts'
import {ref, watch, watchEffect, nextTick, inject} from "vue";
const  socket=inject("socket")
const myUrl=ref('')
class EchartGraph{
  constructor() {
    this.epochList=[]
    this.metricList=[[],[],[],[],[],[]]
    this.chartList=[]
    this.InitEchart()
    this.ListenFuc()
  }
  //将echart和Dom元素进行绑定  并且在对象初试化的时候就进行调用
  async InitEchart(){
    await nextTick()
    var graphDoms=document.getElementsByClassName("echartGraph");
    for(let i=0;i<graphDoms.length;i++)
      this.chartList.push(echarts.init(graphDoms[i]))
  }

  //利用对象里的属性更新echart表格
  async UpdateEchart(){
    const metricNameList=['D_adv_loss_val','lpips','G_adv_loss_val','G_cycle_loss_val','G_con_loss_val','G_style_loss']
    await nextTick()
    for(let i=0;i<this.chartList.length;i++){
      let seriesList=[]
      for(let j=0;j<this.epochList.length;j++)
        seriesList.push([this.epochList[j],this.metricList[i][j]])
      let myOption={
        title: {
          text: metricNameList[i]
        },
        xAxis: {
          type:'value',
          // data: this.epochList,
        },
        yAxis: {
          type:'value'
        },
        series: [
          {
            name: '销量',
            type: 'line',
            data: seriesList,
            label:{
              // show:true
            }
          }
        ]
      }
      this.chartList[i].clear()
      this.chartList[i].setOption(myOption)
      window.onresize = ()=>{
        this.chartList[i].resize();
      };
    }
  }
  ListenFuc(){
    socket.on('MetricMsg',(...args)=>{
      // console.log('Para is received')
      // console.log(args)
      this.epochList.push(parseInt(args[0].epochNum))
      for(let i=0;i<this.metricList.length;i++)
        this.metricList[i].push(parseFloat(args[0].metricList[i]))
      this.UpdateEchart()
    })
  }
}
class TrainingGraph{
  constructor() {
    this.urlList=[]
    this.ListenFuc()
  }
  ListenFuc(){
    socket.on('ImageMsg',(...args)=>{
      console.log('ObjList is',args[0])
      //清空数组  准备接收新到来的两张图片
      // this.urlList.value=[]
      //发过来的image_data是
      for(let i=0;i<args[0].length;i++){
        const blob = new Blob([args[0][i]["image_data"]], { type: "image/png" });
        const iUrl = (window.URL || window.webkitURL).createObjectURL(blob);
        // this.urlList.push(iUrl)
        if(i==0)
          url1.value=iUrl
        else
          url2.value=iUrl
        // console.log('iUrl is',iUrl)
        // console.log(this.urlList)
      }
    })
  }
}
let myEcharts=new EchartGraph()
let myTrainingGraph=ref(new TrainingGraph())
let url1=ref('')
let url2=ref('')
</script>

<style scoped>
.graphTitle{
  size: 2em;
  font-size: 1.5em;
}
.MiddleImage{
  width: 80%;
  margin: 5px auto;
  text-align: center;
}
.secondPart{
  width: 100%;
  height: 25%;
}
.echartGraph{
  display: inline-block;
  width: 90%;
  height: 100%;
  /*border:#9C1A1C 1px solid;*/
}
</style>