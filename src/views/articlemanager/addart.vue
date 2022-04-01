<template>
  <div class="app-container">
    <el-form
      ref="formdata"
      :model="formdata"
      :rules="rules"
      label-width="80px"
      size="small"
    >
      <el-form-item
        prop="title"
        label="标题"
      >
        <el-input v-model="formdata.title" />
      </el-form-item>
      <el-form-item
        prop="categories"
        label="类别"
      >
        <el-select v-model="formdata.categories" multiple placeholder="请选择" style="width:100%;">
          <el-option v-for="(item,index) in cate" :key="index" :value="item.id" :label="item.name">{{ item.name }}</el-option>
        </el-select>
      </el-form-item>
      <el-form-item
        prop="description"
        label="简介"
      >
        <el-input v-model="formdata.description" type="textarea" :rows="5" />
      </el-form-item>
      <el-form-item
        prop="body"
        label="主体"
      >
        <div id="main">
          <mavon-editor
            v-model="formdata.body"
            @change="changebody"
          />
        </div>
      </el-form-item>
      <el-form-item
        prop="is_published"
        label="发布"
      >
        <el-switch
          v-model="formdata.is_published"
        />
      </el-form-item>
      <el-form-item
        prop="can_comment"
        label="评论"
      >
        <el-switch
          v-model="formdata.can_comment"
        />
      </el-form-item>
      <el-form-item>
        <el-button v-if="!showcancel" size="small" type="primary" @click="createart">创建</el-button>
        <el-button v-else size="small" type="primary" @click="editart">编辑</el-button>
        <el-button v-if="!showcancel" size="small" @click="cancel">取消</el-button>
        <el-button v-else size="small" @click="cancel">返回</el-button>
      </el-form-item>
    </el-form>
  </div>
</template>

<script>
import { getCategoriesSelection } from '@/api/category'
import { createPost, getPost, updatePost } from '@/api/post'
export default {
  name: 'Addart',
  data() {
    return {
      cate: [],
      value: '',
      showcancel: false,
      formdata: {
        title: '',
        categories: [],
        description: '',
        body: '',
        body_html: '',
        is_published: false,
        can_comment: false
      },
      rules: {
        title: [{ required: true, message: '请输入标题', trigger: 'blur' }],
        categories: [{ required: true, message: '请选择类别', trigger: 'change' }],
        description: [{ required: true, message: '请输入简介', trigger: 'blur' }],
        body: [{ required: true, message: '请输入主体', trigger: 'change' }]
      }
    }
  },
  created() {
    // 获取分类
    getCategoriesSelection().then((res) => {
      if (res.status === 200) {
        this.cate = res.data
      }
    }).catch(err => {
      console.log(err)
    })
    // 判断路由是否传值
    if (Object.values(this.$route.query).length > 0 && typeof (this.$route.query.row) === 'object') {
      this.showcancel = true
      this.id = this.$route.query.row.id
      getPost(this.id).then(res => {
        this.formdata.title = res.data.title
        this.formdata.categories = res.data.categories.map((val) => {
          return val['id']
        })
        this.formdata.description = res.data.description
        this.formdata.body = res.data.body
        this.formdata.is_published = res.data.is_published
        this.formdata.can_comment = res.data.can_comment
      })
    }
    console.log(this.$route)
  },
  methods: {
    // 创建
    createart() {
      this.$refs['formdata'].validate((valid) => {
        if (valid) {
          createPost(this.formdata).then(res => {
            if (res.status === 201) {
              this.$message.success(res.statusText)
              this.$router.push('/admin/articlemanager')
            }
          }).catch(err => {
            console.error(err)
          })
        } else {
          console.log('error submit!!')
          return false
        }
      })
    },
    // 编辑
    editart() {
      this.$refs['formdata'].validate((valid) => {
        if (valid) {
          console.log(this.formdata)
          updatePost(this.id, this.formdata).then(res => {
            console.log(res)
            if (res.status === 201) {
              this.$message.success(res.statusText)
              this.$router.push('/admin/articlemanager')
            }
          }).catch(err => {
            console.error(err)
          })
        } else {
          console.log('error submit!!')
          return false
        }
      })
    },
    // 取消
    cancel() {
      this.$router.push('/admin/articlemanager')
    },
    // markdown编辑器输入转换
    changebody(value, htmlval) {
      this.formdata.body_html = htmlval
    }
  }
}
</script>

<style>

</style>
