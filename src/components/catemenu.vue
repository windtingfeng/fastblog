<template>
  <div class="catemenu-container">
    <div class="catemenu-title">类别</div>
    <div v-for="(item,index) in catemenulist" :key="index">
      <a class="catestyle" href="javascript:;" @click="chickcate(item)">{{ item.name }}</a><span>({{ item.posts }})</span>
    </div>
  </div>
</template>

<script>
import { getCategoriesPublished } from '@/api/category'
export default {
  data() {
    return {
      catemenulist: [],
      seachdata: {
        name: undefined,
        page: 1
      }
    }
  },
  created() {
    getCategoriesPublished(this.seachdata).then(res => {
      if (res.status === 200) {
        this.catemenulist = res.data.items
      }
    })
  },
  methods: {
    chickcate(item) {
      this.$router.push({ path: '/', query: { id: item.id }})
      sessionStorage.catename = item.name
    }
  }
}
</script>

<style lang="scss" scoped>
.catemenu-container{
    width: 100%;
    background-color: #F0F0F0;
    padding: 10px;
    .catemenu-title{
        border-bottom: 1px solid #ccc;
        margin-bottom: 10px;
    }
    .catestyle{
        background-color: #17A2B8;
        padding: 4px;
        border-radius: 5px;
        font-size: 12px;
        color: #fff;
    }
}
</style>
