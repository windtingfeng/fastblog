<template>
  <div>
    <div v-show="isShow" class="dialog-box" @click="closedialog" />
    <transition name="slide-fade">
      <div v-show="isShow" class="dialog-from">
        <div class="dialog-from-title">
          <div><span>回复：</span><span>admin</span></div>
          <div><a class="" href="javascript:;" style="font-size:28px" @click="closedialog">×</a></div>
        </div>
        <div class="dialog-from-content">可以</div>
        <div class="dialog-from-reply">
          <div v-if="!islogin">
            <div class="comment-input-item">你的名字：</div>
            <div><input v-model="commentdata.author" type="text" class="form-control"></div>
            <div class="comment-input-item">电子邮箱：</div>
            <div><input v-model="commentdata.email" type="text" class="form-control"></div>
          </div>
          <div class="comment-input-item">评论：</div>
          <div><textarea v-model="commentdata.body" type="textarea" rows="5" class="form-control" /></div>
          <button type="button" class="btn btn-sm primary" @click="checksubmit">提交</button>
          <button type="button" class="btn btn-sm danger" @click="closedialog">取消</button>
        </div>
      </div>
    </transition>
  </div>
</template>

<script>
import { createComment, createCommentAnonymous } from '@/api/comment'
export default {
  props: {
    artid: {
      type: Number,
      default: null
    }
  },
  data() {
    return {
      commentdata: {
        author: '',
        email: '',
        body: ''
      }
    }
  },
  computed: {
    islogin() {
      if (this.$store.getters.name !== '') return true
      else return false
    },
    isShow() {
      return this.$store.getters.isShow
    }
  },
  created() {
    this.commentdata.author = sessionStorage.replyinfo
  },
  methods: {
    // 提交
    checksubmit() {
      if (this.islogin) {
        if (this.commentdata.body !== '') {
          const data = {
            post_id: this.artid,
            body: '@' + this.commentdata.author + ' ' + this.commentdata.body
          }
          createComment(data).then(res => {
            if (res.status === 200 || res.status === 201) {
              this.$message.success('评论成功')
              this.commentdata.body = ''
              this.$store.commit('user/CHANGE_ISSHOW', false)
              this.$emit('getartinfo')
            }
          })
        } else {
          this.$message.error('请补齐表单')
        }
      } else {
        if (this.commentdata.author !== '' && this.commentdata.email !== '' && this.commentdata.body !== '') {
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
              this.$store.commit('user/CHANGE_ISSHOW', false)
              this.$emit('getartinfo')
            }
          })
        } else {
          this.$message.error('请补齐表单')
        }
      }
    },
    // 关闭
    closedialog() {
      this.$store.commit('user/CHANGE_ISSHOW', false)
    }
  }
}
</script>

<style lang="scss" scoped>
/* 设置持续时间和动画函数 */
.slide-fade-enter-active {
  transition: all .5s ease;
}
.slide-fade-leave-active {
  transition: all .3s cubic-bezier(1.0, 0.5, 0.8, 1.0);
}
.slide-fade-enter, .slide-fade-leave-to
/* .slide-fade-leave-active for below version 2.1.8 */ {
  transform: translateY(10px);
  opacity: 0;
}
.primary{
  border: 1px solid rgb(37, 37, 37);
  margin: 10px 0px;
}
.primary:hover{
  background-color: rgb(126, 126, 126);
  border-color: rgb(126, 126, 126);
  color: #fff;
}
.danger{
  border: 1px solid red;
  margin-left: 10px;
  color: red;
}
.danger:hover{
  background-color: red;
  color: #fff;
}
.dialog-box{
    width: 100%;
    height: 100%;
    z-index: 100;
    position: fixed;
    background-color: rgba(0,0,0,.72);
    opacity: 1;
    top:0px;
}
.dialog-from{
    width: 450px;
    background-color: #fff;
    position: fixed;
    border-radius: 5px;
    top:50px;
    left: 40%;
    z-index: 1602;
    display: flex;
    flex-direction: column;
    .dialog-from-title{
        border-bottom: 1px solid #ccc;
        line-height: 20px;
        padding: 20px 20px 0px 20px;
        display: flex;
        justify-content: space-between;
    }
    .dialog-from-content{
        padding: 20px 20px 0px 20px;
    }
    .dialog-from-reply{
        padding: 20px;
        .comment-input-item{
          font-size: 18px;
          font-weight: 600;
          margin: 5px 0px;
        }
    }
}
</style>
