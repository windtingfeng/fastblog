<template>
  <div class="content-box">
    <navbar @clickseach="clickseach" />
    <div class="frontcontainer">
      <div class="frontcontainer-box">
        <div class="container-left">
          <div class="artitem">
            <div class="artitem-title">
              <a href="javascript:;">{{ artinfo.title }}</a>
              <span class="artitem-time">{{ artinfo.timestamp }}</span>
            </div>
            <div class="artitem-cate">
              <span>类别：</span>
              <span v-for="item in artinfo.categories" :key="item.id" style="margin:0px 3px;" class="catestyle">{{ item.name }}</span>
            </div>
            <p style="margin:20px 0px 0px 0px;font-size:18px;">{{ artinfo.description }}</p>
            <!-- 文章主体 -->
            <div class="artitem-body" v-html="artinfo.body_html" />
            <div class="artitem-bottom">
              <div style="width:100%;"><span style="float:right;font-size:20px">{{ comments }}个评论</span></div>
              <div style="clear:both;" />
              <!-- 评论列表 -->
              <div class="comment-box">
                <div v-for="(item, index) in artinfo.comments" :key="index" :class="{'comment-item':true,'comment-item-bg':(index+1)%2===0}">
                  <div class="comment-item-title">
                    <span class="comment-item-index">#{{ index+1 }}</span>
                    <span class="comment-item-author">{{ item.author }}</span>
                    <span class="comment-item-time">{{ item.timestamp }}</span>
                  </div>
                  <p class="comment-item-body">{{ item.body }}</p>
                  <div class="btnreply-box"><a class="btnreply" href="javascript:;" @click="checkreply(item)">回复</a></div>
                </div>
              </div>
              <!-- 评论输入框 -->
              <div class="comment-input-title">留下你的评论</div>
              <div v-if="!islogin">
                <div class="comment-input-item">你的名字：</div>
                <div><input v-model="commentdata.author" type="text" class="form-control"></div>
                <div class="comment-input-item">电子邮箱：</div>
                <div><input v-model="commentdata.email" type="text" class="form-control"></div>
              </div>
              <div class="comment-input-item">评论：</div>
              <div><textarea v-model="commentdata.body" type="textarea" rows="5" class="form-control" /></div>
              <button type="button" class="btn btn-default" @click="checkcomment">提交</button>
            </div>
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
    <dialogcomment :artid="artid" @getartinfo="getartinfo" />
  </div>
</template>

<script>
import navbar from '@/components/navbar.vue'
import catemenu from '@/components/catemenu.vue'
import { getPostPublished } from '@/api/post'
import { createComment, createCommentAnonymous } from '@/api/comment'
import { getYear, parseTime } from '@/utils/index'
import dialogcomment from './components/dialogcomment.vue'
export default {
  name: 'Frontartinfo',
  components: {
    navbar,
    catemenu,
    dialogcomment
  },
  data() {
    return {
      artinfo: {},
      commentdata: {
        author: '',
        email: '',
        body: ''
      },
      artid: ''
    }
  },
  computed: {
    islogin() {
      if (this.$store.getters.name !== '') return true
      else return false
    },
    comments() {
      if (this.artinfo.comments !== undefined) { return this.artinfo.comments.length } else return 0
    }
  },
  created() {
    this.artid = Number(this.$route.query.id)
    this.getartinfo()
  },
  methods: {
    // 封装获取当前文章
    getartinfo() {
      getPostPublished(this.$route.query.id).then(res => {
        console.log(res)
        if (res.status === 200) {
          res.data.timestamp = getYear(res.data.timestamp)
          res.data.comments.forEach(element => {
            element.timestamp = parseTime(new Date(element.timestamp))
          })
          this.artinfo = res.data
        }
      })
    },
    // 搜索
    clickseach() {

    },
    // 提交评论
    checkcomment() {
      if (this.commentdata.body === '') return
      if (this.islogin) {
        const data = {
          post_id: this.artid,
          body: this.commentdata.body
        }
        createComment(data).then(res => {
          if (res.status === 200 || res.status === 201) {
            this.$message.success('评论成功')
            this.commentdata.body = ''
            this.getartinfo()
          }
        })
      } else {
        const data = {
          post_id: this.artid,
          body: this.commentdata.body,
          author: this.commentdata.author,
          email: this.commentdata.email
        }
        createCommentAnonymous(data).then(res => {
          if (res.status === 200 || res.status === 201) {
            this.$message.success('评论成功,请等待管理员审核')
            this.commentdata.body = ''
            this.commentdata.author = ''
            this.commentdata.email = ''
            this.getartinfo()
          }
        })
      }
    },
    // 回复
    checkreply(item) {
      this.$store.commit('user/CHANGE_ISSHOW', true)
      sessionStorage.replyinfo = item
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
                padding: 20px 20px 0px 0px;
                box-sizing: border-box;
                .artitem{
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
                        min-height: 300px;
                    }
                    .artitem-bottom{
                        a{
                            color: #007BFF;
                        }
                        .comment-box{
                            width:100%;
                            margin-top: 10px;
                            .comment-item{
                                background-color: #dedede;
                                padding: 10px;
                                .comment-item-title{
                                    font-size: 14px;
                                    .comment-item-index{
                                        color: #fff;
                                        padding: 3px 5px;
                                        background-color: #ccc;
                                        border-radius: 5px;
                                    }
                                    .comment-item-author{
                                        margin-left: 5px;
                                        color: #fff;
                                        padding: 3px 5px;
                                        background-color: #17A2B8;
                                        border-radius: 5px;
                                    }
                                    .comment-item-time{
                                        margin-left: 5px;
                                    }
                                }
                            }
                            .comment-item-bg{
                                background-color: #fff;
                            }
                            .comment-item-body{
                                padding: 5px 0px;
                            }
                            .btnreply-box{
                              width: 100%;
                              height: 35px;
                              .btnreply{
                                color: #000;
                                border-style: solid;
                                border-color: rgb(124, 124, 124) #000 #000 rgb(128, 128, 128);
                                border-width: 2px;
                                padding: 1px 5px;
                                font-size: 14px;
                                float: right;
                              }
                            }
                        }
                        .comment-input-title{
                          font-size: 20px;
                          font-weight: 300;
                        }
                        .comment-input-item{
                          font-size: 18px;
                          font-weight: 600;
                          margin: 5px 0px;
                        }
                        .btn{
                          border: 1px solid rgb(37, 37, 37);
                          margin: 10px 0px;
                        }
                        .btn:hover{
                          background-color: rgb(126, 126, 126);
                          border-color: rgb(126, 126, 126);
                          color: #fff;
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
