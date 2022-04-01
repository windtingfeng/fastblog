<template>
  <div class="content-box">
    <navbar @clickseach="clickseach" />
    <div class="frontcontainer">
      <div class="frontcontainer-box">
        <div class="container-left">
          <div v-show="catename" class="cateitem"><span>当前分类：{{ catename }}</span><a class="" href="javascript:;" style="font-size:28px" @click="closecate">×</a></div>
          <!-- 文章item -->
          <div v-if="total>0">
            <div v-for="(art,index) in artdata" :key="index" class="artitem">
              <div class="artitem-title">
                <a href="javascript:;" @click="chicktitle(art.id)">{{ art.title }}</a>
                <span class="artitem-time">{{ art.timestamp }}</span>
              </div>
              <div class="artitem-cate">
                <span>类别：</span>
                <span v-for="item in art.categories" :key="item" style="margin:0px 3px;" class="catestyle">{{ item }}</span>
              </div>
              <div class="artitem-body">
                <p>{{ art.description }}</p>
              </div>
              <div class="artitem-bottom">
                <a href="javascript:;" @click="chicktitle(art.id)">继续阅读...</a>
                <a href="javascript:;">{{ art.comments }}个评论</a>
              </div>
            </div>
          </div>
          <div v-else>无文章</div>
          <div><hr></div>
          <div class="container-left-bottom">
            <a href="javascript:;" :class="seachdata.page!==1?'canclick':''" :style="seachdata.page===1?'pointer-events:none;':''" @click="clicknext(-1)">←上一页</a>
            <a href="javascript:;" :class="seachdata.page<newtotal?'canclick':''" :style="seachdata.page<newtotal?'':'pointer-events:none;'" @click="clicknext(1)">下一页→</a>
          </div>
        </div>
        <div class="container-right">
          <catemenu />
        </div>
      </div>
      <div class="footstyle">
        <span>Copyright © 2022 <a href="javascript:;"> FastAPI-Vue-Blog </a>All Rights Reserved.</span>
      </div>
    </div>
  </div>
</template>

<script>
import navbar from '@/components/navbar.vue'
import catemenu from '@/components/catemenu.vue'
import { getPostsPublished } from '@/api/post'
import { getYear } from '@/utils/index'
export default {
  name: 'Frontindex',
  components: {
    navbar,
    catemenu
  },
  data() {
    return {
      seachdata: {
        title: undefined,
        limit: 10,
        page: 1
      },
      artdata: [],
      total: 0,
      catename: ''
    }
  },
  computed: {
    newtotal() {
      return this.total / 10
    }
  },
  watch: {
    $route(to, from) {
      if (to.query.page) {
        this.getart()
      }
      if (to.query.id) {
        this.catename = sessionStorage.catename
        this.chekcate()
      }
    }
  },
  created() {
    this.getart()
  },
  methods: {
    // 封装获取文章
    getart() {
      getPostsPublished(this.seachdata).then(res => {
        if (res.status === 200) {
          const { data } = res
          data.items.forEach(element => {
            element.timestamp = getYear(element.timestamp)
          })
          this.total = data.total
          this.artdata = data.items
        }
      })
    },
    // 封装点击分类
    chekcate() {
      const data = {
        ...this.seachdata,
        category_id: this.$route.query.id
      }
      getPostsPublished(data).then(res => {
        console.log(res)
        if (res.status === 200) {
          const { data } = res
          data.items.forEach(element => {
            element.timestamp = getYear(element.timestamp)
          })
          this.total = data.total
          this.artdata = data.items
        }
      })
    },
    // 点击文章标题
    chicktitle(id) {
      this.$router.push({ path: '/artinfo', query: { id }})
    },
    // 翻页
    clicknext(num) {
      this.seachdata.page += num
      this.$router.push({ path: '/', query: { page: this.seachdata.page }})
    },
    // 搜索
    clickseach(data) {
      this.seachdata.title = data
      this.getart()
    },
    // 关闭分类
    closecate() {
      this.$router.push('/')
      this.catename = undefined
      this.getart()
    }
  }
}
</script>

<style lang="scss" scoped>
.content-box{
    width: 100%;
    .frontcontainer{
        width: 1400px;
        margin: 0 auto;
        margin-top: 20px;
        display: flex;
        flex-direction: column;
        .frontcontainer-box{
            display: flex;
            border-bottom: 1px dashed #ccc;
            .container-left{
                width: 80%;
                padding: 20px 20px 20px 0px;
                box-sizing: border-box;
                .cateitem{
                  width: 100%;
                  height: 50px;
                  border-radius: 5px;
                  background-color: #D1ECF1;
                  margin-bottom: 10px;
                  padding: 20px;
                  display: flex;
                  justify-content: space-between;
                  align-items: center;
                  color: #6FA0A9;
                }
                .artitem{
                    margin-bottom: 30px;
                    .artitem-title{
                        display: flex;
                        justify-content: space-between;
                        align-items: center;
                        a{
                          font-size: 26px;
                          font-weight: 500;
                        }
                        .artitem-time{
                          display: block;
                          height: 30px;
                          line-height: 30px;
                          padding: 0px 5px;
                          text-align: center;
                          box-sizing: border-box;
                          border: 1px solid #ccc;
                        }
                    }
                    .artitem-cate{
                        border-bottom: 1px solid #ccc;
                        padding: 5px 0px;
                        .catestyle{
                            background-color: #17A2B8;
                            padding: 4px;
                            border-radius: 5px;
                            font-size: 12px;
                            color: #fff;
                        }
                    }
                    .artitem-body{
                        padding: 20px 0px;
                    }
                    .artitem-bottom{
                        display: flex;
                        justify-content: space-between;
                        a{
                            color: #007BFF;
                        }
                    }
                }
                .container-left-bottom{
                    display: flex;
                    justify-content: space-between;
                    a{
                        padding: 5px 12px;
                        border-radius: 20px;
                        border: 1px solid #ccc;
                        color: #ccc;
                    }
                        .canclick{
                          color: #9ec9f7;
                        }
                        .canclick:hover{
                          background-color: #dedede;
                        }
                }
            }
            .container-right{
                width: 20%;
            }
        }
        .footstyle{
            margin-top: 10px;
            span{
                float: right;
                color: rgb(117, 117, 117);
                font-size: 14px;
                a{
                    color: #007BFF;
                }
            }
        }
    }
}
@media (max-width: 1600px) {
    .content-box{
        .frontcontainer{
            width: 1200px;
        }
    }
}
@media (max-width: 1400px) {
    .content-box{
        .frontcontainer{
            width: 1000px;
        }
    }
}
@media (max-width: 1200px) {
    .content-box{
        .frontcontainer{
            width: 800px;
        }
    }
}
</style>
