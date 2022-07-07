<template>
  <div id="app">
    <el-container>
      <el-header
          class="header"
      >
        <top-nav></top-nav>
      </el-header>
      <el-main class="main">
        <graph></graph>
      </el-main>
      <el-footer style="text-align: center;">
        Visulization for Training and Inferring GANs N’Roses
      </el-footer>
    </el-container>
  </div>


</template>

<script>

import TopNav from "./components/topNav";
import Graph from "./components/Graph";
export default {
  name: "App",
  components: {
    Graph,
    TopNav
  }
};
</script>

<style>
body{
  margin: 0;
  padding: 0;
}
#app {
  height: 100%;
  width: 100%;
}

.el-container{
  height: 100%;
}
.header{
  border-bottom: #DCDFE6 1px solid;
  margin-top: 10px;
}
.main{
  height:85% ;
  width: 100%;
}

</style>
