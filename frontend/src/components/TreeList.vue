<template>
  <div class="tree-list">
    <div class="header-container">
      <h2>樹木列表</h2>
      <div class="stats-container" v-if="trees.length > 0">
        <div class="stat-item">
          <span class="stat-label">平均胸徑：</span>
          <span class="stat-value">{{ averageDiameter }} 公分</span>
        </div>
        <div class="stat-item">
          <span class="stat-label">平均樹高：</span>
          <span class="stat-value">{{ averageHeight }} 公尺</span>
        </div>
        <div class="stat-item">
          <span class="stat-label">最新記錄：</span>
          <span class="stat-value">{{ latestRecordDate }}</span>
        </div>
      </div>
    </div>
    
    <!-- 今日新增資料區 -->
    <div v-if="hasTodayRecords" class="content-box today-records-box">
      <div class="card-header">
        <span>
          <el-tag type="primary" size="small" style="background-color: #409EFF; color: #ffffff; font-weight: bold; margin-right: 10px">今日新增</el-tag>
          樹木資料 ({{ todayRecords.length }} 筆)
        </span>
      </div>
      
      <el-table
        :data="todayRecords"
        style="width: 100%"
        border
        stripe
        class="transparent-table today-table"
      >
        <el-table-column prop="_id" label="ID" width="80" />
        <el-table-column prop="species" label="樹種名稱" width="150" />
        <el-table-column prop="diameter" label="胸徑(公分)" width="120" />
        <el-table-column prop="height" label="樹高(公尺)" width="120" />
        <el-table-column prop="record_date" label="記錄日期" width="120" />
        <el-table-column prop="project_name" label="專案" width="150" />
        <el-table-column prop="created_by_name" label="創建者" width="120">
          <template #default="scope">
            {{ scope.row.created_by_name || '未知' }}
          </template>
        </el-table-column>
        <el-table-column prop="notes" label="備註" min-width="200" :show-overflow-tooltip="true" />
      </el-table>
    </div>
    
    <div class="content-box tree-list-box">
      <div class="card-header">
        <span>
          <template v-if="projectId">
            專案樹木數據
          </template>
          <template v-else>
            樹木數據列表
          </template>
          <el-tag v-if="!isAdmin" type="success" size="small" style="margin-left: 10px">
            僅顯示您創建的樹木
          </el-tag>
          <el-tag v-else type="primary" size="small" style="margin-left: 10px; background-color: #409EFF; color: #ffffff;">
            顯示所有樹木
          </el-tag>
          <el-tag v-if="projectId" type="info" size="small" style="margin-left: 10px; background-color: #909399; color: #ffffff;">
            專案 ID: {{ projectId }}
          </el-tag>
        </span>
        <div class="button-group">
          <el-button type="primary" size="small" @click="refreshData">刷新數據</el-button>
          <el-button 
            v-if="isAuthenticated" 
            type="success" 
            size="small" 
            @click="showAddDialog"
          >
            新增樹木
          </el-button>
          <el-button 
            v-if="isAdmin" 
            type="warning" 
            size="small" 
            @click="showQRCodeDialog"
          >
            生成QR碼
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
      
      <!-- 數據表格 -->
      <el-table
        v-if="!loading && !error && trees.length > 0"
        :data="trees"
        style="width: 100%"
        border
        stripe
        max-height="450"
        class="transparent-table"
        @selection-change="handleSelectionChange"
      >
        <el-table-column type="selection" width="55" />
        <el-table-column prop="_id" label="ID" width="80" />
        <el-table-column prop="species" label="樹種名稱" width="150" />
        <el-table-column prop="diameter" label="胸徑(公分)" width="120" />
        <el-table-column prop="height" label="樹高(公尺)" width="120" />
        <el-table-column prop="record_date" label="記錄日期" width="120" />
        <el-table-column prop="project_name" label="專案" width="150" />
        <el-table-column prop="created_by_name" label="創建者" width="120">
          <template #default="scope">
            {{ scope.row.created_by_name || '未知' }}
          </template>
        </el-table-column>
        <el-table-column prop="notes" label="備註" min-width="200" :show-overflow-tooltip="true" />
        
        <el-table-column fixed="right" label="操作" width="180">
          <template #default="scope">
            <el-button 
              type="text" 
              size="small" 
              @click="viewTreeDetails(scope.row)"
            >
              查看
            </el-button>
            <template v-if="isAuthenticated">
              <el-button 
                type="text" 
                size="small" 
                @click="showEditDialog(scope.row)"
              >
                修改
              </el-button>
              <el-button 
                type="text" 
                size="small" 
                @click="confirmDelete(scope.row)"
                class="delete-btn"
              >
                刪除
              </el-button>
            </template>
          </template>
        </el-table-column>
      </el-table>
      
      <!-- 無數據提示 -->
      <el-empty 
        v-if="!loading && !error && trees.length === 0" 
        description="暫無樹木數據" 
      />
    </div>
    
    <!-- 樹木詳情對話框 -->
    <el-dialog
      v-model="dialogVisible"
      title="樹木詳情"
      width="50%"
      class="tree-dialog"
    >
      <div v-if="selectedTree">
        <div class="tree-detail-section">
          <h3>當前資料</h3>
          <div class="tree-detail-item">
            <strong>ID: </strong>
            <span>{{ selectedTree._id }}</span>
          </div>
          <div class="tree-detail-item">
            <strong>樹種名稱: </strong>
            <span>{{ selectedTree.species }}</span>
          </div>
          <div class="tree-detail-item">
            <strong>胸徑(公分): </strong>
            <span>{{ selectedTree.diameter }}</span>
          </div>
          <div class="tree-detail-item">
            <strong>樹高(公尺): </strong>
            <span>{{ selectedTree.height }}</span>
          </div>
          <div class="tree-detail-item">
            <strong>記錄日期: </strong>
            <span>{{ selectedTree.record_date }}</span>
          </div>
          <div class="tree-detail-item">
            <strong>專案名稱: </strong>
            <span>{{ selectedTree.project_name || '無' }}</span>
          </div>
          <div class="tree-detail-item">
            <strong>創建者: </strong>
            <span>{{ selectedTree.created_by_name || '未知' }}</span>
          </div>
          <div class="tree-detail-item">
            <strong>備註: </strong>
            <span>{{ selectedTree.notes || '無' }}</span>
          </div>
          <div class="tree-detail-item">
            <strong>建立時間: </strong>
            <span>{{ new Date(selectedTree.created_at).toLocaleString() }}</span>
          </div>
          <div class="tree-detail-item">
            <strong>更新時間: </strong>
            <span>{{ new Date(selectedTree.updated_at).toLocaleString() }}</span>
          </div>
        </div>

        <!-- 添加歷史記錄部分 -->
        <div class="tree-history-section">
          <h3>歷史記錄</h3>
          <el-timeline v-if="treeHistory.length > 0">
            <el-timeline-item
              v-for="history in treeHistory"
              :key="history.id"
              :timestamp="new Date(history.created_at).toLocaleString()"
              :type="history.action === 'DELETE' ? 'danger' : 'primary'"
            >
              <h4>{{ history.action === 'DELETE' ? '刪除' : '更新' }}</h4>
              <p>樹種名稱: {{ history.species }}</p>
              <p>胸徑: {{ history.diameter }} 公分</p>
              <p>樹高: {{ history.height }} 公尺</p>
              <p>記錄日期: {{ history.record_date }}</p>
              <p>專案: {{ history.project_name || '無' }}</p>
              <p>備註: {{ history.notes || '無' }}</p>
            </el-timeline-item>
          </el-timeline>
          <el-empty v-else description="暫無歷史記錄" />
        </div>
      </div>
      <template #footer>
        <span class="dialog-footer">
          <el-button @click="dialogVisible = false">關閉</el-button>
        </span>
      </template>
    </el-dialog>
    
    <!-- 新增/編輯樹木對話框 -->
    <el-dialog
      v-model="formDialogVisible"
      :title="dialogType === 'add' ? '新增樹木' : '編輯樹木'"
      width="50%"
      class="tree-dialog"
    >
      <el-form 
        :model="treeForm" 
        :rules="formRules" 
        ref="treeFormRef" 
        label-width="100px"
      >
        <el-form-item label="樹種名稱" prop="species">
          <el-input v-model="treeForm.species" placeholder="請輸入樹種名稱"></el-input>
        </el-form-item>
        <el-form-item label="胸徑(公分)" prop="diameter">
          <el-input-number v-model="treeForm.diameter" :min="0" :precision="2" :step="0.1" style="width: 100%"></el-input-number>
        </el-form-item>
        <el-form-item label="樹高(公尺)" prop="height">
          <el-input-number v-model="treeForm.height" :min="0" :precision="2" :step="0.1" style="width: 100%"></el-input-number>
        </el-form-item>
        <el-form-item label="記錄日期" prop="record_date">
        <el-date-picker
          v-model="treeForm.record_date"
          type="date"
          placeholder="選擇日期"
          format="YYYY-MM-DD"
          value-format="YYYY-MM-DD"
          style="width: 100%"
        ></el-date-picker>
      </el-form-item>
        <el-form-item label="專案" prop="project_id">
          <el-select v-model="treeForm.project_id" placeholder="請選擇專案" style="width: 100%">
            <el-option
              v-for="project in projects"
              :key="project.id"
              :label="project.name"
              :value="project.id"
            ></el-option>
          </el-select>
        </el-form-item>
        <el-form-item label="備註" prop="notes">
          <el-input
            v-model="treeForm.notes"
            type="textarea"
            :rows="3"
            placeholder="請輸入備註"
          ></el-input>
        </el-form-item>
      </el-form>
      <template #footer>
        <span class="dialog-footer">
          <el-button @click="formDialogVisible = false">取消</el-button>
          <el-button type="primary" @click="submitTreeForm" :loading="formLoading">確定</el-button>
        </span>
      </template>
    </el-dialog>
    
    <!-- QR Code 生成對話框 -->
    <el-dialog
      v-model="qrCodeDialogVisible"
      title="生成QR碼"
      width="50%"
      class="qr-code-dialog"
    >
      <div class="qr-code-options">
        <el-radio-group v-model="qrCodeOption">
          <el-radio label="all">生成所有樹木的QR碼</el-radio>
          <el-radio label="selected">生成選中樹木的QR碼</el-radio>
        </el-radio-group>
        <div v-if="qrCodeOption === 'selected'" class="selection-tip">
          <el-alert
            type="info"
            show-icon
            :closable="false"
            style="background-color: rgba(13, 35, 69, 0.8) !important; border: 1px solid #409EFF; margin-top: 10px;">
            <p style="color: #ffffff !important; font-weight: 500;">請先在樹木數據表格中勾選您需要生成QR碼的樹木</p>
          </el-alert>
        </div>
      </div>
      
      <div v-if="qrCodeOption === 'selected'" class="selected-trees">
        <p>已選擇 {{ selectedTrees.length }} 棵樹木</p>
        <div v-if="selectedTrees.length > 0" class="selected-trees-list">
          <el-table
            :data="selectedTrees"
            style="width: 100%"
            border
            stripe
            height="200"
            class="transparent-table"
          >
            <el-table-column prop="_id" label="ID" width="80" />
            <el-table-column prop="species" label="樹種名稱" width="150" />
            <el-table-column prop="diameter" label="胸徑(公分)" width="120" />
            <el-table-column prop="height" label="樹高(公尺)" width="120" />
          </el-table>
        </div>
      </div>
      
      <template #footer>
        <span class="dialog-footer">
          <el-button @click="qrCodeDialogVisible = false">關閉</el-button>
          <el-button 
            type="primary" 
            @click="generateQRCodes" 
            :loading="generatingQRCodes"
            :disabled="qrCodeOption === 'selected' && selectedTrees.length === 0"
          >
            生成QR碼
          </el-button>
        </span>
      </template>
    </el-dialog>
  </div>
</template>

<script>
import { ref, reactive, computed, onMounted, watch } from 'vue';
import { useStore } from 'vuex';
import { getTrees, addTree, updateTree, deleteTree, getProjects } from '@/services/api';
import axios from 'axios';
import { Loading } from '@element-plus/icons-vue';
import { ElMessage, ElMessageBox } from 'element-plus';

export default {
  name: 'TreeList',
  components: {
    Loading
  },
  props: {
    projectId: {
      type: Number,
      default: null
    }
  },
  setup(props) {
    const store = useStore();
    const treeFormRef = ref(null);
    const allTrees = ref([]); // 存儲所有樹木數據
    const trees = computed(() => {
      if (!isAuthenticated.value) return [];
      
      // 首先按照用戶權限過濾樹木
      let filteredTrees = isAdmin.value ? 
        allTrees.value : 
        allTrees.value.filter(tree => tree.created_by_id === (store.state.user?._id || store.state.user?.id));
      
      // 如果指定了專案ID，僅顯示該專案的樹木
      if (props.projectId) {
        filteredTrees = filteredTrees.filter(tree => tree.project_id === props.projectId);
      } else {
        // 沒有專案ID時，顯示所有有專案ID的樹木，不顯示無專案的樹木
        // 如果想顯示所有樹木（包括無專案的），則移除此行
        filteredTrees = filteredTrees.filter(tree => tree.project_id);
      }
      
      // 按照ID排序
      return filteredTrees.sort((a, b) => {
        return (parseInt(a._id) || 0) - (parseInt(b._id) || 0);
      });
    });
    const projects = ref([]);
    const loading = ref(true);
    const error = ref('');
    const dialogVisible = ref(false);
    const formDialogVisible = ref(false);
    const formLoading = ref(false);
    const selectedTree = ref(null);
    const dialogType = ref('add'); // 'add' 或 'edit'
    const qrCodeDialogVisible = ref(false);
    const qrCodeOption = ref('all');
    const selectedTrees = ref([]);
    const generatedQRCodes = ref([]);
    const generatingQRCodes = ref(false);
    const isAdmin = computed(() => store.state.user?.is_admin || store.state.user?.role === 'ADMIN');
    const treeHistory = ref([]);
    
    // 檢查是否已登錄
    const isAuthenticated = computed(() => store.state.isAuthenticated);
    
    // 樹木表單
    const treeForm = reactive({
      species: '',
      diameter: null,
      height: null,
      record_date: '',
      project_id: null,
      notes: ''
    });
    
    // 表單驗證規則
    const formRules = {
      species: [
        { required: true, message: '請輸入樹種名稱', trigger: 'blur' }
      ]
    };
    
    // 獲取樹木數據
    const fetchTrees = async () => {
      loading.value = true;
      error.value = '';
      
      try {
        const data = await getTrees();
        allTrees.value = data;
      } catch (err) {
        error.value = '獲取樹木數據失敗，請稍後再試';
        console.error(err);
      } finally {
        loading.value = false;
      }
    };
    
    // 獲取專案數據
    const fetchProjects = async () => {
      try {
        const data = await getProjects();
        projects.value = data;
        console.log('獲取到的專案數據:', data); // 調試用
      } catch (err) {
        console.error('獲取專案數據失敗:', err);
        ElMessage.error('獲取專案數據失敗');
      }
    };
    
    // 刷新數據
    const refreshData = () => {
      fetchTrees();
    };
    
    // 查看樹木詳情
    const viewTreeDetails = async (tree) => {
      selectedTree.value = tree;
      dialogVisible.value = true;
      await fetchTreeHistory(tree._id);
    };
    
    // 顯示新增對話框
    const showAddDialog = () => {
      if (!isAuthenticated.value) {
        ElMessage.warning('請先登錄');
        return;
      }
      
      dialogType.value = 'add';
      resetForm();
      
      // 如果有專案ID，自動選擇該專案
      if (props.projectId) {
        treeForm.project_id = props.projectId;
      }
      
      formDialogVisible.value = true;
    };
    
    // 顯示編輯對話框
    const showEditDialog = (tree) => {
      if (!isAuthenticated.value) {
        ElMessage.warning('請先登錄');
        return;
      }
      
      dialogType.value = 'edit';
      resetForm();
      
      // 填充表單數據
      Object.keys(treeForm).forEach(key => {
        if (key in tree) {
          treeForm[key] = tree[key];
        }
      });
      
      // 確保記錄ID被正確設置
      treeForm.id = tree._id || tree.id;
      formDialogVisible.value = true;
      
      console.log('編輯數據:', JSON.stringify(treeForm)); // 調試用
    };
    
    // 重置表單
    const resetForm = () => {
      if (treeFormRef.value) {
        treeFormRef.value.resetFields();
      }
      
      treeForm.species = '';
      treeForm.diameter = null;
      treeForm.height = null;
      treeForm.record_date = '';
      treeForm.project_id = null;
      treeForm.notes = '';
      delete treeForm.id;
    };
    
    // 提交表單
    const submitTreeForm = () => {
      if (!treeFormRef.value) return;
      
      treeFormRef.value.validate(async (valid) => {
        if (valid) {
          formLoading.value = true;
          
          try {
            // 創建一個新對象，避免修改原始表單數據
            const formData = { ...treeForm };
            
            // 數據處理 - 確保數字字段是數字類型
            if (formData.diameter) formData.diameter = Number(formData.diameter);
            if (formData.height) formData.height = Number(formData.height);
            
            // 移除可能導致問題的空值或undefined值
            Object.keys(formData).forEach(key => {
              if (formData[key] === null || formData[key] === undefined || formData[key] === '') {
                delete formData[key];
              }
            });
            
            console.log('處理後的提交數據:', formData); // 調試用
            
            if (dialogType.value === 'add') {
              await addTree(formData);
              ElMessage.success('新增樹木成功');
            } else {
              const id = formData.id || formData._id;
              delete formData.id; // 刪除id字段，避免與URL參數衝突
              delete formData._id; // 刪除_id字段，避免與URL參數衝突
              await updateTree(id, formData);
              ElMessage.success('更新樹木成功');
            }
            
            formDialogVisible.value = false;
            fetchTrees();
          } catch (err) {
            console.error('提交樹木數據失敗:', err);
            ElMessage.error(`提交失敗: ${err.message || '請稍後再試'}`);
          } finally {
            formLoading.value = false;
          }
        }
      });
    };
    
    // 確認刪除
    const confirmDelete = (tree) => {
      if (!isAuthenticated.value) {
        ElMessage.warning('請先登錄');
        return;
      }
      
      // 處理樹種名稱為空的情況
      const speciesName = tree.species ? `樹種「${tree.species}」` : '無樹種名稱';
      
      ElMessageBox.confirm(
        `確定要刪除${speciesName}的記錄嗎？此操作不可恢復。`,
        '刪除確認',
        {
          confirmButtonText: '確定',
          cancelButtonText: '取消',
          type: 'warning'
        }
      ).then(async () => {
        try {
          const id = tree._id || tree.id;
          await deleteTree(id);
          ElMessage.success('刪除成功');
          fetchTrees();
        } catch (err) {
          console.error('刪除樹木數據失敗:', err);
          ElMessage.error('刪除失敗，請稍後再試');
        }
      }).catch(() => {
        // 用戶取消刪除
      });
    };
    
    // 組件掛載時獲取數據
    onMounted(() => {
      fetchTrees();
      fetchProjects();
      checkAdminStatus();
    });
    
    // 監聽登錄狀態變化
    watch(() => store.state.isAuthenticated, (newValue) => {
      if (!newValue && formDialogVisible.value) {
        formDialogVisible.value = false;
      }
      if (newValue) {
        fetchTrees();
        fetchProjects();
      }
    });
    
    // 監聽專案 ID 變化
    watch(() => props.projectId, (newValue) => {
      console.log('TreeList: 專案 ID 已變更為', newValue);
      // 專案變更時可以重新獲取數據
      fetchTrees();
    });
    
    const checkAdminStatus = async () => {
      try {
        console.log('正在检查管理员状态...')
        const response = await axios.get('/api/users/current-user/')
        console.log('获取到的用户数据:', response.data)
        // 检查response.data中是否有is_admin字段
        console.log('API返回的is_admin字段:', response.data.is_admin)
        // 如果没有is_admin字段，尝试从role字段推断
        if (response.data.is_admin === undefined && response.data.role === 'ADMIN') {
          isAdmin.value = true
          console.log('根据role=ADMIN设置isAdmin为true')
        } else {
          isAdmin.value = response.data.is_admin || false
        }
        console.log('isAdmin设置为:', isAdmin.value)
      } catch (error) {
        console.error('Error checking admin status:', error)
        isAdmin.value = false
      }
    };
    
    const showQRCodeDialog = () => {
      qrCodeDialogVisible.value = true
      generatedQRCodes.value = []
    };
    
    const generateQRCodes = async () => {
      generatingQRCodes.value = true
      try {
        let treeIds = []
        if (qrCodeOption.value === 'selected') {
          treeIds = selectedTrees.value.map(tree => tree._id)
        } else {
          treeIds = trees.value.map(tree => tree._id)
        }
        
        console.log('準備生成QR碼，樹木ID:', treeIds)
        const response = await axios.post('/api/trees/generate-bulk-qr/', {
          tree_ids: treeIds
        }, {
          responseType: 'blob',  // 指定響應類型為 blob
          headers: {
            'Content-Type': 'application/json'
          }
        })
        
        // 創建下載連結
        const url = window.URL.createObjectURL(new Blob([response.data]))
        const link = document.createElement('a')
        link.href = url
        link.setAttribute('download', 'tree_qrcodes.zip')
        document.body.appendChild(link)
        link.click()
        link.remove()
        window.URL.revokeObjectURL(url)
        
        ElMessage.success('QR碼已生成並開始下載！')
      } catch (error) {
        console.error('生成QR碼時發生錯誤:', error)
        if (error.response) {
          console.error('錯誤響應:', error.response.status, error.response.data)
        }
        ElMessage.error('生成QR碼時發生錯誤')
      } finally {
        generatingQRCodes.value = false
      }
    };
    
    // 添加獲取歷史記錄的方法
    const fetchTreeHistory = async (treeId) => {
      try {
        const response = await axios.get(`/api/trees/history/${treeId}/`);
        treeHistory.value = response.data;
      } catch (error) {
        console.error('獲取歷史記錄失敗:', error);
        ElMessage.error('獲取歷史記錄失敗');
      }
    };
    
    // 計算平均胸徑
    const averageDiameter = computed(() => {
      if (!trees.value || trees.value.length === 0) return '0.00';
      const sum = trees.value.reduce((acc, tree) => acc + (Number(tree.diameter) || 0), 0);
      return (sum / trees.value.length).toFixed(2);
    });

    // 計算平均樹高
    const averageHeight = computed(() => {
      if (!trees.value || trees.value.length === 0) return '0.00';
      const sum = trees.value.reduce((acc, tree) => acc + (Number(tree.height) || 0), 0);
      return (sum / trees.value.length).toFixed(2);
    });

    // 獲取最新記錄日期
    const latestRecordDate = computed(() => {
      if (!trees.value || trees.value.length === 0) return '無';
      const dates = trees.value
        .map(tree => tree.record_date)
        .filter(date => date)
        .sort((a, b) => new Date(b) - new Date(a));
      return dates[0] || '無';
    });
    
    // 修改todayRecords計算邏輯，使用更新時間代替創建時間並按ID排序
    const todayRecords = computed(() => {
      if (!trees.value || trees.value.length === 0) return [];
      
      const today = new Date();
      today.setHours(0, 0, 0, 0);
      
      // 獲取當前用戶ID
      const currentUserId = store.state.user?._id || store.state.user?.id;
      
      const filteredRecords = trees.value.filter(tree => {
        // 檢查更新日期是否為今天
        const updatedDate = new Date(tree.updated_at || tree.created_at);
        updatedDate.setHours(0, 0, 0, 0);
        const isToday = updatedDate.getTime() === today.getTime();
        
        // 如果是管理員，顯示所有今日更新的資料；否則只顯示當前用戶的資料
        return isToday && (isAdmin.value ? true : tree.created_by_id === currentUserId);
      });
      
      // 按照ID排序
      return filteredRecords.sort((a, b) => {
        return (parseInt(a._id) || 0) - (parseInt(b._id) || 0);
      });
    });
    
    // 判斷今日是否有新增資料
    const hasTodayRecords = computed(() => {
      return todayRecords.value.length > 0;
    });
    
    // 添加處理表格選擇變化的方法
    const handleSelectionChange = (selection) => {
      selectedTrees.value = selection;
      console.log('選擇的樹木:', selection);
    };
    
    return {
      trees,
      projects,
      loading,
      error,
      dialogVisible,
      formDialogVisible,
      formLoading,
      selectedTree,
      dialogType,
      treeForm,
      treeFormRef,
      formRules,
      isAuthenticated,
      isAdmin,
      refreshData,
      viewTreeDetails,
      showAddDialog,
      showEditDialog,
      submitTreeForm,
      confirmDelete,
      qrCodeDialogVisible,
      qrCodeOption,
      selectedTrees,
      generatedQRCodes,
      generatingQRCodes,
      showQRCodeDialog,
      generateQRCodes,
      treeHistory,
      averageDiameter,
      averageHeight,
      latestRecordDate,
      todayRecords,
      hasTodayRecords,
      handleSelectionChange,
    };
  }
};
</script>

<style scoped>
.tree-list {
  padding: 0;
}

h2 {
  margin-bottom: 20px;
  color: #fff !important;
}

.stats-container {
  display: flex;
  gap: 20px;
}

.stat-item {
  background-color: rgba(46, 139, 87, 0.2);
  padding: 8px 15px;
  border-radius: 6px;
  color: #fff;
}

.stat-label {
  font-weight: 500;
  margin-right: 5px;
}

.stat-value {
  color: #2E8B57;
  font-weight: bold;
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

.tree-list-box {
  margin-top: 20px;
}

.today-records-box {
  margin-top: 20px;
  margin-bottom: 20px;
  background-color: rgba(67, 142, 73, 0.15) !important;
  border: 1px solid rgba(103, 194, 58, 0.3);
  border-radius: 5px;
}

:deep(.today-table .el-table__header th.el-table__cell) {
  background-color: rgba(103, 194, 58, 0.3) !important;
}

:deep(.today-table .el-table__row:hover > td.el-table__cell) {
  background-color: rgba(103, 194, 58, 0.3) !important;
}

.header-container {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 20px;
}

.tree-detail-section {
  margin-bottom: 20px;
  padding-bottom: 20px;
  border-bottom: 1px solid rgba(255, 255, 255, 0.1);
}

.tree-history-section {
  margin-top: 20px;
}

.tree-detail-item {
  margin-bottom: 10px;
  padding-bottom: 10px;
  border-bottom: 1px solid rgba(255, 255, 255, 0.1);
  color: #fff;
}

.tree-list-box {
  background: transparent !important;
}

:deep(.el-table) {
  --el-table-tr-bg-color: transparent !important;
  --el-table-bg-color: transparent !important;
  --el-table-row-hover-bg-color: rgba(46, 139, 87, 0.3) !important;
  background-color: transparent !important;
}

:deep(.el-table__inner-wrapper),
:deep(.el-table__header),
:deep(.el-table__body),
:deep(.el-table__footer) {
  background-color: transparent !important;
}

:deep(.el-table__cell) {
  background-color: transparent !important;
}

:deep(.el-table__header-wrapper th.el-table__cell) {
  background-color: rgba(46, 139, 87, 0.3) !important;
  color: #fff !important;
  border-bottom: 1px solid rgba(255, 255, 255, 0.1) !important;
}

:deep(.el-table__body tr.el-table__row) {
  background-color: transparent !important;
}

:deep(.el-table__body tr.el-table__row td.el-table__cell) {
  background-color: transparent !important;
  color: #fff !important;
  border-bottom: 1px solid rgba(255, 255, 255, 0.05) !important;
}

:deep(.el-table__body tr.el-table__row:hover > td.el-table__cell) {
  background-color: rgba(46, 139, 87, 0.3) !important;
}

:deep(.el-button--text) {
  color: #2E8B57 !important;
}

:deep(.el-button--text:hover) {
  color: #fff !important;
}

:deep(.delete-btn) {
  color: #f56c6c !important;
}

:deep(.delete-btn:hover) {
  color: #ff4d4f !important;
}

:deep(.el-dialog__header) {
  background-color: rgba(46, 139, 87, 0.4) !important;
  color: #fff !important;
  padding: 15px 20px !important;
  border-bottom: 1px solid rgba(255, 255, 255, 0.1) !important;
}

:deep(.el-dialog__title) {
  color: #fff !important;
}

:deep(.el-dialog__body) {
  background-color: rgba(30, 30, 30, 0.8) !important;
  color: #fff !important;
  padding: 20px !important;
}

:deep(.el-dialog__footer) {
  background-color: rgba(30, 30, 30, 0.8) !important;
  border-top: 1px solid rgba(255, 255, 255, 0.1) !important;
  padding: 15px 20px !important;
}

:deep(.el-form-item__label) {
  color: #fff !important;
}

:deep(.el-input__wrapper) {
  background-color: rgba(0, 0, 0, 0.3) !important;
  box-shadow: 0 0 0 1px rgba(255, 255, 255, 0.2) inset !important;
}

:deep(.el-input__inner),
:deep(.el-textarea__inner) {
  color: #fff !important;
}

:deep(.el-date-editor), 
:deep(.el-select) {
  width: 100% !important;
}

.qr-code-dialog .qr-code-options {
  margin-bottom: 20px;
}
  
.qr-code-dialog .selected-trees {
  margin: 10px 0;
  padding: 10px;
  background-color: rgba(0, 0, 0, 0.1);
  border-radius: 4px;
}

:deep(.el-timeline-item__content) {
  color: #fff;
}

:deep(.el-timeline-item__timestamp) {
  color: rgba(255, 255, 255, 0.7);
}

.selected-trees-list {
  margin-top: 10px;
  max-height: 200px;
  overflow-y: auto;
  border: 1px solid rgba(255, 255, 255, 0.2);
  border-radius: 4px;
}

:deep(.el-table__body tr.el-table__row.selected) {
  background-color: rgba(46, 139, 87, 0.5) !important;
}

.selection-tip {
  margin-top: 10px;
}
</style> 