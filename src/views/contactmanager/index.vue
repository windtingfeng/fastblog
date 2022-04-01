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
      <el-button plain type="primary" icon="el-icon-search" size="small" @click="seachcontact">查询</el-button>
      <el-button plain icon="el-icon-refresh" size="small" @click="resetseach">重置</el-button>
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
        prop="author"
        label="作者"
      />
      <el-table-column
        prop="email"
        label="邮箱"
      />
      <el-table-column
        prop="body"
        label="内容"
      />
      <el-table-column
        prop="post"
        label="文章"
      >
        <template slot-scope="scope">
          <a :href="'/index?postid=' + scope.row.post.id">{{ scope.row.post.title }}</a>
        </template>
      </el-table-column>
      <el-table-column
        prop="timestamp"
        label="日期"
      />
      <el-table-column
        prop="reviewed"
        label="审核通过"
      >
        <template slot-scope="scope">
          <el-tag v-if="!scope.row.reviewed" type="danger">否</el-tag>
          <el-tag v-if="scope.row.reviewed" type="success">是</el-tag>
        </template>
      </el-table-column>
      <el-table-column
        label="操作"
        width="150"
      >
        <template slot-scope="scope">
          <el-button type="text" size="small" @click="handleClick(scope.row)"><i class="el-icon-edit" />通过审核</el-button>
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
  </div>
</template>

<script>
import { getComments, deleteComment, updateComment } from '@/api/comment'
import { parseTime } from '@/utils/index'
export default {
  name: 'Contactmanager',
  data() {
    return {
      seachdata: {
        page: 1,
        limit: 10,
        unlimit: false
      },
      seachname: '',
      tableData: [],
      total: 0
    }
  },
  created() {
    this.getcomment()
  },
  methods: {
    // 封装获取评论
    getcomment() {
      getComments(this.seachdata).then(res => {
        if (res.status === 200) {
          res.data.items.forEach(element => {
            element.timestamp = parseTime(new Date(element.timestamp))
          })
          this.tableData = res.data.items
          this.total = res.data.total
        }
      })
    },
    // 查询
    seachcontact() {
      this.getcomment()
    },
    // 重置
    resetseach() {
      this.seachname = ''
      this.getcomment()
    },
    // 通过审核
    handleClick(row) {
      updateComment(row.id, { reviewed: true }).then(res => {
        if (res.status === 200) {
          this.$message.success('审核成功')
          this.getcomment()
        }
        this.getcomment()
      })
    },
    // 删除
    handledel(row) {
      deleteComment(row.id).then(res => {
        if (res.status === 200) {
          this.$message.success('删除成功')
          this.getcomment()
        }
      })
    },
    // 每页数量变化
    handleSizeChange(num) {
      this.seachdata.limit = num
      this.getcomment()
    },
    // 页数变化
    handleCurrentChange(num) {
      this.seachdata.page = num
      this.getcomment()
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
