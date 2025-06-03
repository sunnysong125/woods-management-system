<template>
  <div class="projects">
    <h1>專案選擇</h1>
    <div class="content-box">
      <div class="card-header">
        <span>選擇一個專案以查看其樹木資料</span>
        <div class="button-group">
          <el-button 
            v-if="isAuthenticated" 
            type="success" 
            size="small" 
            @click="showAddProjectDialog"
          >
            新增專案
          </el-button>
        </div>
      </div>
      
      <!-- 加載狀態 -->
      <div v-if="loading" class="loading-container">
        <el-icon class="is-loading"><loading /></el-icon>
        <p>加載中...</p>
      </div>
      
      <!-- 錯誤信息 -->
      <el-alert
        v-if="error"
        :title="error"
        type="error"
        show-icon
        @close="error = ''"
      />
      
      <!-- 專案列表 -->
      <div v-if="!loading && !error" class="project-list">
        <el-row :gutter="20">
          <el-col :span="8" v-for="project in projects" :key="project.id" class="project-card-col">
            <el-card class="project-card">
              <div class="project-card-content" @click="selectProject(project)">
                <h2>{{ project.name }}</h2>
                <p class="project-description">{{ project.description || '無描述' }}</p>
                <div class="project-dates">
                  <div v-if="project.start_date">
                    <strong>開始日期:</strong> {{ project.start_date }}
                  </div>
                  <div v-if="project.end_date">
                    <strong>結束日期:</strong> {{ project.end_date }}
                  </div>
                </div>
              </div>
              <div class="project-card-footer">
                <el-button type="primary" size="small" @click="selectProject(project)">查看樹木資料</el-button>
                <el-button 
                  v-if="canDeleteProject(project)" 
                  type="danger" 
                  size="small" 
                  @click.stop="confirmDeleteProject(project)"
                  style="margin-left: 8px;"
                >
                  刪除專案
                </el-button>
              </div>
            </el-card>
          </el-col>
        </el-row>
        
        <!-- 無數據提示 -->
        <el-empty v-if="projects.length === 0" description="暫無專案數據" />
      </div>
    </div>

    <!-- 新增專案對話框 -->
    <el-dialog
      v-model="addProjectDialogVisible"
      title="新增專案"
      width="50%"
      class="project-dialog"
    >
      <el-form 
        :model="projectForm" 
        :rules="projectFormRules" 
        ref="projectFormRef" 
        label-width="100px"
      >
        <el-form-item label="專案名稱" prop="name">
          <el-input v-model="projectForm.name" placeholder="請輸入專案名稱"></el-input>
        </el-form-item>
        <el-form-item label="專案描述" prop="description">
          <el-input
            v-model="projectForm.description"
            type="textarea"
            :rows="3"
            placeholder="請輸入專案描述"
          ></el-input>
        </el-form-item>
        <el-form-item label="開始日期" prop="start_date">
          <el-date-picker
            v-model="projectForm.start_date"
            type="date"
            placeholder="選擇開始日期"
            format="YYYY-MM-DD"
            value-format="YYYY-MM-DD"
            style="width: 100%"
          ></el-date-picker>
        </el-form-item>
        <el-form-item label="結束日期" prop="end_date">
          <el-date-picker
            v-model="projectForm.end_date"
            type="date"
            placeholder="選擇結束日期"
            format="YYYY-MM-DD"
            value-format="YYYY-MM-DD"
            style="width: 100%"
          ></el-date-picker>
        </el-form-item>
      </el-form>
      <template #footer>
        <span class="dialog-footer">
          <el-button @click="addProjectDialogVisible = false">取消</el-button>
          <el-button type="primary" @click="submitProjectForm" :loading="formLoading">確定</el-button>
        </span>
      </template>
    </el-dialog>
  </div>
</template>

<script>
import { ref, reactive, computed, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { useStore } from 'vuex'
import { ElMessage, ElMessageBox } from 'element-plus'
import { Loading } from '@element-plus/icons-vue'
import { getProjects, addProject, deleteProject } from '@/services/api'

export default {
  name: 'ProjectsView',
  components: {
    Loading
  },
  setup() {
    const router = useRouter()
    const store = useStore()
    const projects = ref([])
    const loading = ref(true)
    const error = ref('')
    const addProjectDialogVisible = ref(false)
    const formLoading = ref(false)
    const projectFormRef = ref(null)

    // 檢查用戶登入狀態和管理員權限
    const isAuthenticated = computed(() => store.getters.isAuthenticated)
    const isAdmin = computed(() => {
      const user = store.state.user
      if (!user) return false
      // 檢查是否為超級用戶、管理員或具有管理員角色
      return user.is_superuser || 
             user.is_staff || 
             user.is_admin || 
             user.role === 'ADMIN'
    })
    const currentUserId = computed(() => store.state.user?.id)

    // 檢查是否可以刪除專案（超級管理者或專案創建者）
    const canDeleteProject = (project) => {
      if (!isAuthenticated.value) return false
      // 超級管理者可以刪除任何專案
      if (isAdmin.value) return true
      // 專案創建者可以刪除自己的專案
      return project.created_by_id === currentUserId.value
    }

    // 專案表單
    const projectForm = reactive({
      name: '',
      description: '',
      start_date: '',
      end_date: ''
    })

    // 表單驗證規則
    const projectFormRules = {
      name: [
        { required: true, message: '請輸入專案名稱', trigger: 'blur' }
      ]
    }

    // 重置表單
    const resetProjectForm = () => {
      projectForm.name = ''
      projectForm.description = ''
      projectForm.start_date = ''
      projectForm.end_date = ''
    }
    
    // 獲取專案數據
    const fetchProjects = async () => {
      loading.value = true
      error.value = ''
      
      try {
        const data = await getProjects()
        projects.value = data
        console.log('獲取到的專案:', data)
      } catch (err) {
        console.error('獲取專案數據失敗:', err)
        error.value = '獲取專案數據失敗，請稍後再試'
      } finally {
        loading.value = false
      }
    }
    
    // 選擇專案並導航到樹木頁面
    const selectProject = (project) => {
      if (!project || !project.id) {
        ElMessage.warning('無效的專案')
        return
      }
      
      // 檢查是否已登入
      if (!isAuthenticated.value) {
        // 未登入時重定向到登入頁面
        ElMessage.warning('請先登入後查看專案')
        router.push('/login')
        return
      }
      
      console.log('選擇的專案:', project)
      router.push({
        name: 'trees',
        query: { projectId: project.id }
      })
    }

    // 顯示新增專案對話框
    const showAddProjectDialog = () => {
      if (!isAuthenticated.value) {
        ElMessage.warning('請先登入')
        return
      }
      
      resetProjectForm()
      addProjectDialogVisible.value = true
    }

    // 提交專案表單
    const submitProjectForm = () => {
      if (!projectFormRef.value) return
      
      projectFormRef.value.validate(async (valid) => {
        if (valid) {
          formLoading.value = true
          
          try {
            await addProject(projectForm)
            ElMessage.success('專案新增成功')
            addProjectDialogVisible.value = false
            fetchProjects() // 重新獲取專案列表
          } catch (err) {
            console.error('新增專案失敗:', err)
            ElMessage.error('新增專案失敗，請稍後再試')
          } finally {
            formLoading.value = false
          }
        }
      })
    }

    // 確認刪除專案
    const confirmDeleteProject = (project) => {
      if (!canDeleteProject(project)) {
        ElMessage.warning('您無權刪除此專案')
        return
      }

      ElMessageBox.confirm(
        `確定要刪除專案「${project.name}」嗎？此操作將同時刪除該專案下的所有樹木資料，且不可恢復。`,
        '刪除確認',
        {
          confirmButtonText: '確定刪除',
          cancelButtonText: '取消',
          type: 'warning'
        }
      ).then(async () => {
        try {
          await deleteProject(project.id)
          ElMessage.success('專案刪除成功')
          fetchProjects() // 重新獲取專案列表
        } catch (err) {
          console.error('刪除專案失敗:', err)
          ElMessage.error('刪除專案失敗，請稍後再試')
        }
      }).catch(() => {
        // 用戶取消刪除
      })
    }
    
    // 組件掛載時獲取數據
    onMounted(() => {
      fetchProjects()
    })
    
    return {
      projects,
      loading,
      error,
      selectProject,
      isAuthenticated,
      isAdmin,
      currentUserId,
      addProjectDialogVisible,
      showAddProjectDialog,
      projectForm,
      projectFormRules,
      projectFormRef,
      formLoading,
      submitProjectForm,
      confirmDeleteProject,
      canDeleteProject
    }
  }
}
</script>

<style scoped>
.projects {
  padding: 0;
  padding-left: 80px;
  padding-top: 20px;
}

h1 {
  color: #fff !important;
  margin-bottom: 20px;
}

.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 15px;
  color: #fff;
}

.button-group {
  display: flex;
  gap: 10px;
}

.loading-container {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  min-height: 200px;
  color: #fff;
}

.project-list {
  padding: 10px;
}

.project-card-col {
  margin-bottom: 20px;
}

.project-card {
  height: 100%;
  transition: all 0.3s ease;
  display: flex;
  flex-direction: column;
  justify-content: space-between;
  background-color: rgba(30, 30, 30, 0.7) !important;
  border: 1px solid rgba(255, 255, 255, 0.1) !important;
}

.project-card:hover {
  transform: translateY(-5px);
  box-shadow: 0 5px 15px rgba(0, 0, 0, 0.3);
  border-color: rgba(46, 139, 87, 0.5) !important;
}

.project-card-content {
  flex: 1;
  cursor: pointer;
  padding: 5px;
  border-radius: 4px;
  transition: background-color 0.2s ease;
}

.project-card-content:hover {
  background-color: rgba(46, 139, 87, 0.1);
}

.project-card h2 {
  color: #2E8B57 !important;
  margin-bottom: 10px;
  font-size: 18px;
}

.project-description {
  color: #ccc;
  margin-bottom: 10px;
  height: 40px;
  overflow: hidden;
  text-overflow: ellipsis;
  display: -webkit-box;
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;
}

.project-dates {
  color: #aaa;
  font-size: 12px;
  margin-bottom: 10px;
}

.project-card-footer {
  margin-top: 15px;
  display: flex;
  justify-content: flex-end;
  align-items: center;
  flex-wrap: wrap;
  gap: 8px;
}

:deep(.el-card__body) {
  padding: 15px;
  color: #fff;
}

:deep(.el-empty__description) {
  color: #fff;
}

/* 對話框樣式 */
:deep(.project-dialog .el-dialog) {
  background-color: rgba(30, 30, 30, 0.95) !important;
  border: 1px solid rgba(255, 255, 255, 0.1);
}

:deep(.project-dialog .el-dialog__header) {
  background-color: rgba(46, 139, 87, 0.8);
  border-bottom: 1px solid rgba(255, 255, 255, 0.1);
}

:deep(.project-dialog .el-dialog__title) {
  color: #fff !important;
}

:deep(.project-dialog .el-dialog__body) {
  background-color: rgba(30, 30, 30, 0.8);
  color: #fff;
}

:deep(.project-dialog .el-form-item__label) {
  color: #fff !important;
}

:deep(.project-dialog .el-input__inner) {
  background-color: rgba(50, 50, 50, 0.8) !important;
  border-color: rgba(255, 255, 255, 0.2) !important;
  color: #fff !important;
}

:deep(.project-dialog .el-textarea__inner) {
  background-color: rgba(50, 50, 50, 0.8) !important;
  border-color: rgba(255, 255, 255, 0.2) !important;
  color: #fff !important;
}

:deep(.project-dialog .el-date-editor.el-input) {
  background-color: rgba(50, 50, 50, 0.8) !important;
}

:deep(.project-dialog .el-date-editor .el-input__inner) {
  background-color: transparent !important;
}
</style> 