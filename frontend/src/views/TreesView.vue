<template>
  <div class="trees-view">
    <div class="header-container">
      <h1>樹木數據庫</h1>
      <div v-if="currentProject" class="project-info">
        <span>當前專案:</span>
        <el-tag type="success" size="large" style="background-color: #67C23A; color: #ffffff;">{{ currentProject.name }}</el-tag>
        <el-button type="primary" size="small" @click="backToProjects">
          切換專案
        </el-button>
      </div>
    </div>
    
    <div class="content-box" style="background-color: rgba(30, 30, 30, 0.4) !important;">
      <p>查看和管理Wooddb數據庫中的樹木數據</p>
      
      <TreeList ref="treeList" :project-id="projectId" />
    </div>
  </div>
</template>

<script>
import { ref, onMounted, watch, computed } from 'vue'
import { useRouter, useRoute } from 'vue-router'
import { ElMessage } from 'element-plus'
import TreeList from '@/components/TreeList.vue'
import { getProjectById } from '@/services/api'

export default {
  name: 'TreesView',
  components: {
    TreeList
  },
  props: {
    projectId: {
      type: Number,
      default: null
    }
  },
  setup(props) {
    const router = useRouter()
    const route = useRoute()
    const treeList = ref(null)
    const currentProject = ref(null)
    
    // 獲取並設定當前專案資訊
    const fetchCurrentProject = async () => {
      if (!props.projectId) {
        // 如果沒有提供專案ID，立即重定向到專案選擇頁面
        console.log('未提供專案ID，重定向到專案選擇頁面');
        router.replace({ name: 'projects' });
        return;
      }
      
      try {
        const project = await getProjectById(props.projectId);
        if (!project || !project.id) {
          // 專案不存在或無效
          ElMessage.warning('找不到指定的專案，請重新選擇');
          router.replace({ name: 'projects' });
          return;
        }
        
        currentProject.value = project;
        document.title = `${project.name} - 樹木數據庫`;
        ElMessage.success(`已載入專案 "${project.name}" 的樹木資料`);
      } catch (err) {
        console.error('獲取專案資訊失敗:', err);
        ElMessage.error('獲取專案資訊失敗，請重新選擇專案');
        router.replace({ name: 'projects' });
      }
    }
    
    // 返回專案選擇頁面
    const backToProjects = () => {
      router.push({ name: 'projects' })
    }
    
    // 當專案ID變化時重新獲取專案資訊
    watch(() => props.projectId, (newProjectId, oldProjectId) => {
      if (newProjectId !== oldProjectId) {
        fetchCurrentProject()
      }
    })
    
    // 組件掛載時獲取專案資訊
    onMounted(() => {
      fetchCurrentProject()
    })
    
    return {
      treeList,
      currentProject,
      backToProjects
    }
  }
}
</script>

<style scoped>
.trees-view {
  padding: 20px;
  padding-left: 80px;
  height: 100%;
  color: #fff;
}

.header-container {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 20px;
}

.project-info {
  display: flex;
  align-items: center;
  gap: 10px;
}

h1 {
  margin-bottom: 0;
  color: #fff !important;
  text-shadow: 0 2px 4px rgba(0, 0, 0, 0.5);
  font-weight: bold;
}

p {
  margin-bottom: 30px;
  color: #ffffff;
}

/* 添加不同透明度的功能區塊 */
.content-box {
  background-color: rgba(30, 30, 30, 0.35) !important;
}

:deep(.el-table) {
  background-color: rgba(0, 0, 0, 0.2) !important;
}

:deep(.el-table__header),
:deep(.el-table__body),
:deep(.el-table__footer) {
  margin: 0 !important;
}

:deep(.el-table__inner-wrapper),
:deep(.el-table__fixed-wrapper) {
  background-color: transparent !important;
}

:deep(.el-table__header th) {
  background-color: rgba(46, 139, 87, 0.3) !important;
  border-bottom: 1px solid rgba(255, 255, 255, 0.1);
}

:deep(.el-table__row) {
  background-color: rgba(0, 0, 0, 0.25) !important;
}

:deep(.el-table__row:hover > td) {
  background-color: rgba(46, 139, 87, 0.3) !important;
}

:deep(.el-input__wrapper) {
  background-color: rgba(255, 255, 255, 0.1) !important;
  box-shadow: 0 0 0 1px rgba(255, 255, 255, 0.2) inset !important;
}

:deep(.el-tree) {
  background-color: rgba(0, 0, 0, 0.15) !important;
  color: #fff;
}

:deep(.el-tree-node__content:hover) {
  background-color: rgba(46, 139, 87, 0.2) !important;
}

:deep(.el-tree-node:focus > .el-tree-node__content) {
  background-color: rgba(46, 139, 87, 0.3) !important;
}

:deep(.el-button) {
  margin-left: 0;
}
</style> 