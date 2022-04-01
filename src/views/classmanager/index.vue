<template>
  <div class="app-container">
    <!-- 搜索区域 -->
    <div class="seachart-box">
      <div class="sea-el-input">
        <el-input
          v-model="seachname"
          prefix-icon="el-icon-search"
          size="small"
        />
      </div>
      <el-button plain type="primary" icon="el-icon-search" size="small" @click="seachclass">搜索</el-button>
      <el-button plain icon="el-icon-refresh" size="small" @click="resetseach">重置</el-button>
      <el-button plain type="primary" icon="el-icon-plus" size="small" @click="addclass">新建</el-button>
    </div>
    <!-- 表格区域 -->
    <el-table
      ref="multipleTable"
      :data="tableData"
      tooltip-effect="dark"
      style="width: 100%"
      stripe
    >
      <el-table-column
        type="selection"
        width="55"
      />
      <el-table-column
        prop="id"
        label="ID"
        width="50"
      />
      <el-table-column
        prop="name"
        label="名称"
      />
      <el-table-column
        prop="posts"
        label="文章数"
      />
      <el-table-column
        label="操作"
        width="150"
      >
        <template slot-scope="scope">
          <el-button type="text" size="small" @click="handleClick(scope.row)"><i class="el-icon-edit" />编辑</el-button>
          <span style="color:#dedede"> | </span>
          <el-popconfirm
            confirm-button-text="好的"
            cancel-button-text="不用了"
            icon="el-icon-info"
            icon-color="red"
            title="这是一段内容确定删除吗？"
            @onConfirm="handledel(scope.row)"
          >
            <el-button slot="reference" type="text" size="small"><i class="el-icon-delete" /> 删除</el-button>
          </el-popconfirm>
        </template>
      </el-table-column>
    </el-table>
    <!-- 分页 -->
    <el-pagination
      style="margin-top:20px;"
      :current-page="seachdata.page"
      background
      :page-sizes="[5, 10, 15, 20]"
      :page-size="seachdata.limit"
      layout="total, sizes, prev, pager, next, jumper"
      :total="total"
      @size-change="handleSizeChange"
      @current-change="handleCurrentChange"
    />
    <!-- 新建和编辑dialog -->
    <el-dialog :title="dialogtitle" :visible.sync="dialogFormVisible" width="500px">
      <el-form :model="dialogform" :rules="rules">
        <el-form-item label="名称" prop="name">
          <el-input v-model="dialogform.name" size="small" autocomplete="off" />
        </el-form-item>
      </el-form>
      <div slot="footer" class="dialog-footer">
        <el-button type="primary" size="small" @click="dialogsubmit">确 认</el-button>
        <el-button size="small" @click="dialogFormVisible = false">取 消</el-button>
      </div>
    </el-dialog>
  </div>
</template>

<script>
import { getAllCategories, deleteCategory, createCategory, updateCategory } from '@/api/category'
export default {
  name: 'Classmanager',
  data() {
    return {
      seachdata: {
        name: undefined,
        page: 1,
        limit: 10,
        unlimit: false
      },
      seachname: '',
      tableData: [],
      total: 0,
      isnew: true,
      dialogtitle: '创建类别',
      dialogFormVisible: false,
      currentCategory: undefined,
      dialogform: {
        name: ''
      },
      rules: {
        name: [{ required: true, message: '请输入标题', trigger: 'blur' }]
      }
    }
  },
  created() {
    this.getclass()
  },
  methods: {
    // 封装获取分类
    getclass() {
      getAllCategories(this.seachdata).then(res => {
        console.log(res)
        if (res.status === 200) {
          this.tableData = res.data.items
          this.total = res.data.total
        }
      })
    },
    // 搜索
    seachclass() {
      this.seachdata.name = this.seachname
      this.getclass()
    },
    // 重置
    resetseach() {
      this.seachdata.name = undefined
      this.name = ''
      this.getclass()
    },
    // 新建
    addclass() {
      this.dialogtitle = '新建类别'
      this.dialogform.name = ''
      this.isnew = true
      this.dialogFormVisible = true
    },
    // 编辑
    handleClick(row) {
      this.dialogtitle = '修改类别'
      this.currentCategory = row
      this.isnew = false
      this.dialogform.name = row.name
      this.dialogFormVisible = true
    },
    // 删除
    handledel(row) {
      console.log(row)
      deleteCategory(row.id).then(res => {
        if (res.status === 200) {
          this.$message.success('删除成功')
          this.getclass()
        }
      })
    },
    // 每页数量变化
    handleSizeChange(num) {
      this.seachdata.limit = num
      this.getclass()
    },
    // 页数变化
    handleCurrentChange(num) {
      this.seachdata.page = num
      this.getclass()
    },
    // dialog确认
    dialogsubmit() {
      if (this.isnew) {
        createCategory(this.dialogform).then(res => {
          if (res.status === 201) {
            this.$message.success('创建成功')
            this.dialogFormVisible = false
            this.getclass()
          }
        })
      } else {
        console.log(this.currentCategory)
        updateCategory(this.currentCategory.id, this.dialogform).then(res => {
          console.log(res)
          if (res.status === 200) {
            this.$message.success('修改成功')
            this.dialogFormVisible = false
            this.getclass()
          }
        })
      }
    }
  }
}
</script>

<style lang="scss" scoped>
.seachart-box{
        display: flex;
        .sea-el-input{
            width: 250px;
            margin-right: 10px;
        }
    }
</style>
