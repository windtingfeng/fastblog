<template>
  <div class="frontnavbar">
    <img src="../assets/logo.png" alt="" width="30px">
    <h3 class="left_10" style="margin-bottom:0">FastAPI Vue Blog</h3>
    <a class="left_40" href="/">文章</a>
    <a class="left_20" href="/">关于网站</a>
    <input v-model="seachdata" type="text" style="width:200px;" class="form-control form-control-sm left_10" placeholder="关键字" aria-describedby="sizing-addon2">
    <button type="button" class="btn btn-sm btn-default left_10" @click="seachart">搜索文章</button>
  </div>
</template>

<script>
export default {
  data() {
    return {
      seachdata: ''
    }
  },
  methods: {
    seachart() {
      this.$emit('clickseach', this.seachdata)
    }
  }
}
</script>
<style lang="scss" scoped>
.left_10{
    margin-left: 10px;
}
.left_20{
    margin-left: 10px;
}
.left_40{
    margin-left: 40px;
}
.frontnavbar{
    width: 100%;
    height: 60px;
    background-color: #F5F6F9;
    padding: 0% 10%;
    display: flex;
    align-items: center;
}
.btn{
    background-color: #6C757D;
    color: #fff;
}
.btn:hover{
    background-color: #5a6268;
    border-color: #545b62;
}
</style>
