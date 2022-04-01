<template>
  <div class="app-container">
    <!-- 搜索区域 -->
    <div class="seachart-box">
      <div class="sea-el-input">
        <el-input
          v-model="title"
          prefix-icon="el-icon-search"
          size="small"
        />
      </div>
      <el-button plain type="primary" icon="el-icon-search" size="small" @click="seachart">搜索</el-button>
      <el-button plain icon="el-icon-refresh" size="small" @click="resetseach">重置</el-button>
      <el-button plain type="primary" icon="el-icon-plus" size="small" @click="addart">新建</el-button>
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
        prop="title"
        label="标题"
        width="120"
      />
      <el-table-column
        prop="description"
        label="描述"
        show-overflow-tooltip
      />
      <el-table-column
        prop="timestamp"
        label="时间"
        width="180"
      />
      <el-table-column
        prop="categories"
        label="类别"
      >
        <template slot-scope="scope">
          <el-tag v-for="(item,index) in scope.row.categories" :key="index" style="margin-right:5px;" type="success">{{ item }}</el-tag>
        </template>
      </el-table-column>
      <el-table-column
        prop="comments"
        label="评论数"
        width="100"
      />
      <el-table-column
        prop="can_comment"
        label="可以评论"
        width="100"
      >
        <template slot-scope="scope">
          <el-tag v-if="scope.row.can_comment" type="success">是</el-tag>
          <el-tag v-if="!scope.row.can_comment" type="danger">否</el-tag>
        </template>
      </el-table-column>
      <el-table-column
        prop="is_published"
        label="发布状态"
        width="100"
      >
        <template slot-scope="scope">
          <el-tag v-if="scope.row.is_published" type="success">已发布</el-tag>
          <el-tag v-if="!scope.row.is_published" type="danger">未发布</el-tag>
        </template>
      </el-table-column>
      <el-table-column
        label="操作"
        width="150"
      >
        <template slot-scope="scope">
          <el-button type="text" size="small" @click="handleClick(scope.row)"><i class="el-icon-edit" />编辑</el-button>
          <span style="color:#dedede"> | </span>
          <el-dropdown>
            <el-button type="text" size="small" class="el-dropdown-link">
              更多<i class="el-icon-arrow-down el-icon--right" />
            </el-button>
            <el-dropdown-menu slot="dropdown">
              <el-dropdown-item icon="el-icon-edit-outline" @click.native="changecomment(scope.row)">切换评论</el-dropdown-item>
              <el-dropdown-item icon="el-icon-edit-outline" @click.native="changepublish(scope.row)">切换发布</el-dropdown-item>
              <el-popconfirm
                confirm-button-text="好的"
                cancel-button-text="不用了"
                icon="el-icon-info"
                icon-color="red"
                title="这是一段内容确定删除吗？"
                @onConfirm="deleteart(scope.row)"
              >
                <el-dropdown-item slot="reference" icon="el-icon-delete">删除</el-dropdown-item>
              </el-popconfirm>
            </el-dropdown-menu>
          </el-dropdown>
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
import { getPosts, updatePost, deletePost } from '@/api/post'
import { parseTime } from '@/utils/index'
export default {
  name: 'Articlemanager',
  data() {
    return {
      seachdata: {
        title: '',
        limit: 10,
        page: 1
      },
      title: '',
      tableData: [],
      total: 0
    }
  },
  created() {
    this.getart()
  },
  methods: {
    // 获取文章列表
    async getart() {
      const { data } = await getPosts(this.seachdata)
      data.items.forEach(element => {
        element.timestamp = parseTime(new Date(element.timestamp))
      })
      this.tableData = data.items
      this.total = data.total
    },
    // 搜索
    seachart() {
      this.seachdata.title = this.title
      this.getart()
    },
    // 编辑
    handleClick(row) {
      this.$router.push({ path: '/admin/addart', query: { row }})
    },
    // 新建
    addart() {
      this.$router.push('/admin/addart')
    },
    // 重置
    resetseach() {
      this.seachdata.title = ''
      this.title = ''
      this.getart()
    },
    // 切换评论
    changecomment(row) {
      updatePost(row.id, { can_comment: !row.can_comment }).then((res) => {
        this.getart()
        console.log(res)
      }).catch(err => {
        this.getart()
        console.error(err)
      })
    },
    // 切换发布
    changepublish(row) {
      updatePost(row.id, { is_published: !row.is_published }).then((res) => {
        this.getart()
        console.log(res)
      }).catch(err => {
        this.getart()
        console.error(err)
      })
    },
    // 删除
    deleteart(row) {
      deletePost(row.id).then(() => {
        this.getart()
        this.$message({
          type: 'success',
          message: '删除成功!'
        })
      }).catch(err => {
        console.log(err)
      })
    },
    // 显示数量变化
    handleSizeChange(num) {
      this.seachdata.limit = num
      this.getart()
    },
    // 页数变化
    handleCurrentChange(num) {
      this.seachdata.page = num
      this.getart()
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
