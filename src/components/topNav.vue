<template>

  <el-button
      :icon="Setting"
      type="primary"
      @click="settingVisiable=true"
      class="trainingSetting"
  >Parameter
  </el-button>
  <el-dialog
      v-model="settingVisiable"
      title="Parameter"
      width="30%"
  >
    <el-form
        label-position="left"
    >
      <el-form-item

          v-for="(value,parName) in parList"
          :key="parName"
          :label="parName"
      >
        <el-input v-model="parList[parName]"></el-input>
      </el-form-item>
    </el-form>
    <test-comp></test-comp>
    <template #footer>
      <span class="dialog-footer">
        <el-button @click="settingVisiable = false">Cancel</el-button>
        <el-button type="primary" @click="settingVisiable = false"
        >Confirm</el-button>
      </span>
    </template>
  </el-dialog>

  <el-button
      class="trainingSetting"
      :type="isTraining?'danger':'primary'"
      :icon="isTraining?VideoPause:VideoPlay"
      @click='handleTrainButton'
  >
    {{!isTraining?'Start':'Pause'}}
  </el-button>
  <el-button
    class="trainingSetting"
    type="primary"
    :icon="Grid"
    @click="myImageDialog.visible=true"
  >
    Structure
  </el-button>
  <el-dialog
    v-model="myImageDialog.visible"
    width="50%"
    title="Model Structure"
  >
    <el-carousel
        height="700px"
        autoplay="false"
        style="margin-top: 5px"
    >
      <el-carousel-item v-for="item in myImageDialog.urlList" :key="item">
        <h2> </h2>
        <el-image :src="item"></el-image>
      </el-carousel-item>
    </el-carousel>
  </el-dialog>
  <el-button
        type="success"
        :disabled="!myInferDialog.inferable"
        :icon="Upload"
        class="inferSetting"
        @click="myInferDialog.visible=true"
    >
    Infer
    </el-button>
  <el-dialog
      v-model="myInferDialog.visible"
      title="Infer"
      width="30%"
  >
    <el-upload
      drag
      :http-request="myInferDialog.handleRequest"
      style="align-content: center"
      thumbnail-mode
    >
      <el-icon class="el-icon--upload"><upload-filled /></el-icon>
      <div class="el-upload__text">
        Drop file here or <em>click to upload</em>
      </div>
    </el-upload>
    <span>
      <h2>Result</h2>
    </span>
    <div class="resultDiv">
      <el-image
          fit="contain"
          :src="tmpUrl"
          class="resultImage"
      ></el-image>
    </div>

  </el-dialog>

</template>

<script  setup>
import {ref,inject,unref,reactive} from 'vue'
import {
  Setting,
    VideoPause,
    VideoPlay,
    Upload,
    UploadFilled,
    Grid
}from '@element-plus/icons-vue'
const  socket=inject("socket")
const handleStart=(e)=>{
  console.log("start the training");
  isTraining.value=true;
  socket.emit('sendPara',unref(parList))
}
const  handlePause=(e)=>{
  console.log("pause the training")
  isTraining.value=false;
  socket.emit('stopTraining')
}
const handleTrainButton=function (){
  if(isTraining.value)
    handlePause()
  else
    handleStart()
}
const isTraining=ref(false)
const parList=ref({
  iter:300000,
  batch:4,
  n_sample:64,
  size:256,
  r1:10,
  lambda_cycle:1,
  path_regularize:2,
  d_reg_every:16,
  g_reg_every:4,
  mixing:0.9,
  lr:2e-3,
})
const settingVisiable=ref(false)
class InferDialog{
  constructor() {
    this.visiable=false
    this.inferable=true
  }
  handleRequest(data){
      socket.emit('InferRequest',data,(...args)=>{
        console.log('Receive Infer Result:',args)
        const blob = new Blob([args[0]["image_data"]], { type: "image/png" });
        const iUrl = (window.URL || window.webkitURL).createObjectURL(blob);
        console.log("Refer result  iUrl is",iUrl)
        this.resultUrl=ref(iUrl)
        tmpUrl.value=iUrl
        console.log("resultUrl is ",this.resultUrl)
      })
  }
}
const myInferDialog=ref(new InferDialog())

const tmpUrl=ref('')
class ImageDialog{
  constructor() {
    this.urlList=[require('@/assets/img/discriminator.png'),require('@/assets/img/generator.png')]
    this.imageName=['Discriminator','Generator']
    this.visiable=false
  }
}
const myImageDialog=ref(new ImageDialog())
</script>
<style scoped>
.trainingSetting{
  float: left;
  margin-right: 10px;
}
.inferSetting{
  float: right;
  margin: 0 10px;
}
.resultDiv{
  width: 100%;
  height: 100%;
}
.resultImage{
  width: 100%;
  height: 100%;
}
</style>