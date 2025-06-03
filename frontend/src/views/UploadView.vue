<template>
  <div class="upload">
    <h1>上傳林木資料</h1>
    <div class="content-box">
      <div class="upload-types">
        <el-tabs v-model="activeTab">
          <el-tab-pane label="一般CSV檔案" name="general">
            <el-upload
              class="upload-demo"
              drag
              action="/api/csv/files/"
              :headers="headers"
              :on-success="handleGeneralSuccess"
              :on-error="handleError"
              :before-upload="beforeUpload"
              multiple>
              <el-icon class="el-icon--upload"><upload-filled /></el-icon>
              <div class="el-upload__text">
                拖拽文件到此處，或 <em>點擊上傳</em>
              </div>
              <template #tip>
                <div class="el-upload__tip">
                  請上傳CSV格式文件，文件大小不超過10MB
                </div>
              </template>
            </el-upload>
          </el-tab-pane>
          
          <el-tab-pane label="樹木資料CSV" name="tree">
            <div class="tree-upload-info">
              <p>請上傳包含以下列的CSV檔案：</p>
              <el-tag class="tag-id">ID</el-tag>
              <el-tag class="tag-species">species</el-tag>
              <el-tag class="tag-diameter">diameter</el-tag>
              <el-tag class="tag-height">height</el-tag>
              <el-tag class="tag-date">record_date</el-tag>
              <el-tag class="tag-project">project_id</el-tag>
              <el-tag class="tag-notes">notes</el-tag>
              
              <div class="download-template">
                <a href="/woodsfrond/tree_sample.csv" download>下載範本檔案</a>
              </div>
            </div>
            
            <!-- 添加專案選擇 -->
            <div class="project-selection">
              <p>請選擇專案：</p>
              <el-select v-model="selectedProject" placeholder="請選擇專案" style="width: 100%; margin-bottom: 20px;">
                <el-option
                  v-for="project in projects"
                  :key="project.id"
                  :label="project.name"
                  :value="project.id"
                />
              </el-select>
            </div>
            
            <!-- 修改批次ID設定區域的alert樣式 -->
            <div class="batch-id-section">
              <p>批次ID設定：</p>
              <el-input
                v-model="batchId"
                placeholder="請輸入批次ID（將應用於所有記錄）"
                style="width: 100%; margin-bottom: 10px;"
                required
              />
              <el-alert
                type="info"
                show-icon
                :closable="false"
                style="background-color: rgba(13, 35, 69, 0.8) !important; border: 1px solid #409EFF;">
                <p style="color: #ffffff !important; font-weight: 500;">若CSV檔案中已有ID欄位，此處設定將優先使用</p>
                <p style="color: #ffffff !important; font-weight: 500;">若未設定批次ID且CSV中無ID欄位，上傳將失敗</p>
              </el-alert>
            </div>
            
            <el-upload
              class="upload-demo"
              drag
              :auto-upload="false"
              :on-change="handleTreeFileChange"
              :before-upload="beforeUpload"
              multiple>
              <el-icon class="el-icon--upload"><upload-filled /></el-icon>
              <div class="el-upload__text">
                拖拽文件到此處，或 <em>點擊上傳</em>
              </div>
              <template #tip>
                <div class="el-upload__tip">
                  請上傳CSV格式文件，文件大小不超過10MB
                </div>
              </template>
            </el-upload>
            
            <!-- 修改上傳按鈕部分，簡化禁用條件 -->
            <div class="upload-actions">
              <el-button 
                type="primary" 
                @click="uploadTreeFile" 
                :disabled="!treeFile || uploading" 
                :loading="uploading">
                上傳樹木資料
              </el-button>
              <el-button 
                type="warning" 
                @click="validateTreeFile" 
                :disabled="!treeFile || validating" 
                :loading="validating">
                僅驗證CSV
              </el-button>
              <el-button type="info" @click="testApiConnection">
                測試API連接
              </el-button>
            </div>
          </el-tab-pane>
        </el-tabs>
      </div>
      
      <!-- 修改驗證結果顯示樣式 -->
      <div v-if="validateResult" class="validate-result content-box" style="margin-top: 20px; background-color: rgba(0, 0, 0, 0.6);">
        <h3 class="validate-title">CSV 驗證結果</h3>
        <el-alert
          :title="`驗證結果: ${validateResult.valid ? '數據有效' : '數據驗證失敗'}`"
          :type="validateResult.valid ? 'success' : 'error'"
          :description="validateResult.valid ? '您的CSV檔案格式正確，可以上傳' : '您的CSV檔案有格式問題，請參考下方錯誤詳情'"
          show-icon
          style="background-color: rgba(13, 35, 69, 0.8) !important; border: 1px solid #409EFF;">
          <template #title>
            <span style="color: #ffffff !important; font-weight: 600 !important;">驗證結果: {{validateResult.valid ? '數據有效' : '數據驗證失敗'}}</span>
          </template>
          <template #default>
            <span style="color: #ffffff !important; font-weight: 500 !important;">
              {{validateResult.valid ? '您的CSV檔案格式正確，可以上傳' : '您的CSV檔案有格式問題，請參考下方錯誤詳情'}}
            </span>
          </template>
        </el-alert>
        
        <div v-if="validateResult.errors && validateResult.errors.length" class="error-list">
          <h4 class="error-title">驗證錯誤:</h4>
          <ul>
            <li v-for="(error, index) in validateResult.errors" :key="index" class="error-item">
              {{ error }}
            </li>
          </ul>
        </div>
        
        <div v-if="validateResult.data && validateResult.data.length" class="preview-data">
          <h4 class="preview-title">預覽數據 (前5條):</h4>
          <el-table :data="validateResult.data.slice(0, 5)" border style="width: 100%" class="transparent-table">
            <el-table-column prop="species" label="樹種名稱" />
            <el-table-column prop="diameter" label="胸徑(公分)" />
            <el-table-column prop="height" label="樹高(公尺)" />
            <el-table-column prop="record_date" label="記錄日期" />
            <el-table-column prop="notes" label="備註" />
          </el-table>
        </div>
      </div>
    </div>

    <div v-if="uploadedFiles.length > 0" class="content-box uploaded-files">
      <div class="card-header">
        <span>上傳歷史</span>
      </div>
      <el-table :data="uploadedFiles" style="width: 100%" class="transparent-table">
        <el-table-column prop="fileName" label="文件名" width="180"></el-table-column>
        <el-table-column prop="uploadTime" label="上傳時間" width="180"></el-table-column>
        <el-table-column prop="status" label="狀態"></el-table-column>
        <el-table-column prop="type" label="類型" width="120"></el-table-column>
        <el-table-column prop="count" label="記錄數" width="100"></el-table-column>
        <el-table-column label="操作">
          <template #default="scope">
            <el-button size="small" @click="viewFile(scope.row)">查看</el-button>
            <el-button size="small" type="danger" @click="deleteFile(scope.row)">刪除</el-button>
          </template>
        </el-table-column>
      </el-table>
    </div>
    
    <!-- API 接口說明 -->
    <div class="content-box api-docs" style="margin-top: 20px;">
      <div class="card-header">
        <span>API 接口說明</span>
        <el-button type="primary" size="small" @click="showApiDocs = !showApiDocs">
          {{ showApiDocs ? '隱藏文檔' : '顯示文檔' }}
        </el-button>
      </div>
      
      <div v-if="showApiDocs">
        <p>本系統提供以下 API 接口用於 CSV 數據導入：</p>
        
        <div class="api-info">
          <h3>1. 上傳 CSV 文件並匯入</h3>
          <p><strong>URL:</strong> POST /api/trees/upload-csv/</p>
          <p><strong>Content-Type:</strong> multipart/form-data</p>
          <p><strong>參數:</strong></p>
          <ul>
            <li><code>file</code> - CSV 文件 (必須)</li>
            <li><code>validate_only</code> - 設為 "true" 僅驗證不匯入 (可選)</li>
          </ul>
          <p><strong>響應:</strong> JSON 格式匯入結果或驗證結果</p>
          
          <pre class="code-sample">
// 成功示例
{
  "success": true,
  "count": 10,
  "message": "成功導入10條樹木記錄"
}

// 錯誤示例
{
  "success": false,
  "errors": ["第3行: 樹徑不是有效的數字", "第5行: 日期格式無效"]
}
          </pre>
        </div>
        
        <div class="api-info">
          <h3>2. 獲取匯入歷史</h3>
          <p><strong>URL:</strong> GET /api/trees/import-history/</p>
          <p><strong>參數:</strong> 無</p>
          <p><strong>響應:</strong> JSON 格式的匯入歷史記錄列表</p>
          
          <pre class="code-sample">
[
  {
    "id": 1,
    "filename": "trees_20240401.csv",
    "created_at": "2024-04-01T10:30:45Z",
    "count": 25,
    "success": true,
    "user": "admin"
  },
  ...
]
          </pre>
        </div>
        
        <div class="api-info">
          <h3>3. 測試 API 連接</h3>
          <p><strong>URL:</strong> GET /api/trees/test/</p>
          <p><strong>參數:</strong> 無</p>
          <p><strong>響應:</strong> JSON 格式的測試結果</p>
          
          <pre class="code-sample">
{
  "message": "測試成功！API正常工作",
  "timestamp": "2024-04-01T12:30:45Z"
}
          </pre>
        </div>
        
        <div class="api-info">
          <h3>使用示例 (JavaScript)</h3>
          <pre class="code-sample">
// 上傳CSV文件示例 (使用fetch API)
async function uploadCSV(file) {
  const formData = new FormData();
  formData.append('file', file);
  
  const response = await fetch('/api/trees/upload-csv/', {
    method: 'POST',
    body: formData
  });
  
  return await response.json();
}

// 驗證CSV文件示例
async function validateCSV(file) {
  const formData = new FormData();
  formData.append('file', file);
  formData.append('validate_only', 'true');
  
  const response = await fetch('/api/trees/upload-csv/', {
    method: 'POST',
    body: formData
  });
  
  return await response.json();
}
          </pre>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { ref } from 'vue'
import { ElMessage } from 'element-plus'
import { useStore } from 'vuex'
import { UploadFilled } from '@element-plus/icons-vue'
import { uploadCsvFile, validateCsvFile, testApiConnection as apiTestConnection, getProjects } from '@/services/api'

export default {
  name: 'UploadView',
  components: {
    UploadFilled
  },
  setup() {
    const store = useStore()
    const uploadedFiles = ref([])
    const activeTab = ref('tree')  // 預設選擇樹木上傳
    const treeFile = ref(null)  // 保存選擇的樹木CSV文件
    const uploading = ref(false)  // 上傳狀態
    const validating = ref(false)  // 驗證狀態
    const validateResult = ref(null)  // 驗證結果
    const showApiDocs = ref(false)  // API 文檔顯示狀態
    const selectedProject = ref(null)  // 保存選擇的專案
    const projects = ref([])  // 保存所有專案
    const batchId = ref('')  // 新增：批次ID設定
    
    // 添加 baseUrl 變數，用於範本檔案下載
    const baseUrl = process.env.VUE_APP_API_URL ? process.env.VUE_APP_API_URL.replace(/\/api$/, '') : 'https://srv.orderble.com.tw/woodsbackend'
    
    const headers = {
      Authorization: `Token ${store.state.token}`
    }

    // 獲取專案列表
    const fetchProjects = async () => {
      try {
        console.log('正在獲取專案列表...')
        const projectsData = await getProjects()
        projects.value = projectsData
        console.log('獲取到的專案:', projectsData)
      } catch (error) {
        console.error('獲取專案失敗:', error)
        ElMessage.error('獲取專案列表失敗，請稍後再試')
      }
    }

    // 在組件掛載後獲取專案列表
    fetchProjects()

    const beforeUpload = (file) => {
      const isCSV = file.type === 'text/csv' || file.name.endsWith('.csv')
      const isLt10M = file.size / 1024 / 1024 < 10

      if (!isCSV) {
        ElMessage.error('請上傳CSV格式文件！')
      }
      if (!isLt10M) {
        ElMessage.error('文件大小不能超過10MB！')
      }
      return isCSV && isLt10M
    }

    const handleGeneralSuccess = (response, file) => {
      ElMessage.success('上傳成功！')
      uploadedFiles.value.push({
        fileName: file.name,
        uploadTime: new Date().toLocaleString(),
        status: '成功',
        type: '一般CSV',
        id: response.id
      })
    }
    
    // 處理樹木CSV文件選擇
    const handleTreeFileChange = (file) => {
      treeFile.value = file.raw
      // 清除之前的驗證結果
      validateResult.value = null
    }
    
    // 修改uploadTreeFile方法，放寬對批次ID的要求
    const uploadTreeFile = async () => {
      if (!treeFile.value) {
        ElMessage.warning('請先選擇要上傳的CSV文件')
        return
      }
      
      if (!selectedProject.value) {
        ElMessage.warning('請選擇專案')
        return
      }
      
      // 只在用戶未輸入批次ID時提醒，但仍允許上傳
      if (!batchId.value) {
        ElMessage.warning('未設定批次ID，僅CSV文件中包含ID欄位時才能成功上傳')
      }
      
      uploading.value = true
      
      try {
        // 獲取當前用戶ID
        const userId = store.state.user?.id || store.state.user?._id
        console.log('當前登入使用者信息:', store.state.user)
        console.log('使用者ID:', userId)
        console.log('選擇的專案ID:', selectedProject.value)
        console.log('批次ID:', batchId.value)
        
        // 使用API服務函數上傳文件
        const response = await uploadCsvFile(treeFile.value, {
          project_id: selectedProject.value,
          user_id: userId,
          batch_id: batchId.value  // 仍然傳遞批次ID參數，即使為空
        })
        
        ElMessage.success(`上傳成功！已導入${response.count}條樹木記錄`)
        
        // 如果有錯誤信息，顯示警告
        if (response.errors && response.errors.length > 0) {
          ElMessage.warning(`有${response.errors.length}行數據導入出錯，請檢查原始文件`)
          console.warn('上傳錯誤:', response.errors)
        }
        
        uploadedFiles.value.push({
          fileName: treeFile.value.name,
          uploadTime: new Date().toLocaleString(),
          status: response.errors && response.errors.length > 0 ? '部分成功' : '成功',
          type: '樹木資料',
          count: response.count,
          id: new Date().getTime()  // 使用時間戳作為唯一ID
        })
        
        // 清除選擇的文件
        treeFile.value = null
      } catch (error) {
        console.error('上傳錯誤:', error)
        // 添加更詳細的錯誤信息
        let errorMsg = error.message || '未知錯誤'
        if (error.response) {
          console.error('錯誤響應狀態:', error.response.status)
          console.error('錯誤響應數據:', error.response.data)
          errorMsg += ` (狀態碼: ${error.response.status})`
          if (error.response.data && error.response.data.error) {
            errorMsg += ` - ${error.response.data.error}`
          }
        }
        ElMessage.error(`上傳失敗，請重試！錯誤: ${errorMsg}`)
      } finally {
        uploading.value = false
      }
    }
    
    // 僅驗證CSV文件
    const validateTreeFile = async () => {
      if (!treeFile.value) {
        ElMessage.warning('請先選擇要驗證的CSV文件')
        return
      }
      
      validating.value = true
      
      try {
        console.log('開始驗證CSV文件:', treeFile.value.name)
        // 使用API服務函數驗證文件
        const response = await validateCsvFile(treeFile.value)
        console.log('CSV驗證響應:', response)
        validateResult.value = response
        
        if (response.valid) {
          ElMessage.success('CSV檔案格式正確！')
        } else {
          ElMessage.warning('CSV檔案有格式問題，請檢查詳情')
          console.warn('驗證警告:', response.errors)
        }
      } catch (error) {
        console.error('驗證錯誤:', error)
        let errorMsg = error.message || '未知錯誤'
        if (error.response) {
          console.error('錯誤響應狀態:', error.response.status)
          console.error('錯誤響應數據:', error.response.data)
          errorMsg += ` (狀態碼: ${error.response.status})`
          if (error.response.data && error.response.data.error) {
            errorMsg += ` - ${error.response.data.error}`
          }
        }
        ElMessage.error(`驗證失敗，請重試！錯誤: ${errorMsg}`)
        validateResult.value = {
          valid: false,
          errors: [errorMsg]
        }
      } finally {
        validating.value = false
      }
    }

    const handleError = (err) => {
      console.error('上傳錯誤:', err);
      ElMessage.error(`上傳失敗，請重試！錯誤: ${err.message || '未知錯誤'}`);
    }

    const viewFile = (file) => {
      // 查看文件詳情，實際開發中會跳轉到相應的頁面或API
      if (file.type === '樹木資料') {
        ElMessage.info(`查看文件：${file.fileName}，包含${file.count}條樹木記錄`)
      } else {
        ElMessage.info(`查看文件：${file.fileName}`)
      }
    }

    const deleteFile = (file) => {
      // 刪除文件，實際開發中會調用相應的API
      ElMessage.success(`文件 ${file.fileName} 已刪除`)
      const index = uploadedFiles.value.findIndex(item => item.id === file.id)
      if (index !== -1) {
        uploadedFiles.value.splice(index, 1)
      }
    }

    // 測試API連接
    const testApiConnection = async () => {
      try {
        const result = await apiTestConnection()
        ElMessage.success(`API連接測試成功: ${result.message}`)
      } catch (error) {
        console.error('API測試錯誤:', error)
        ElMessage.error(`API連接測試失敗: ${error.message || '未知錯誤'}`)
      }
    }

    return {
      uploadedFiles,
      activeTab,
      treeFile,
      uploading,
      validating,
      validateResult,
      showApiDocs,
      selectedProject,
      projects,
      headers,
      handleGeneralSuccess,
      handleTreeFileChange,
      uploadTreeFile,
      validateTreeFile,
      handleError,
      viewFile,
      deleteFile,
      beforeUpload,
      testApiConnection,
      baseUrl,
      batchId
    }
  }
}
</script>

<style scoped>
.upload {
  padding: 20px;
  padding-left: 80px;
  height: 100%;
  color: #fff;
}

h1, h2, h3, h4 {
  color: #fff !important;
  margin-bottom: 15px;
}

.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 15px;
}

.tree-upload-info {
  margin-bottom: 20px;
  padding: 15px;
  background-color: rgba(0, 0, 0, 0.2);
  border-radius: 4px;
}

.tree-upload-info p {
  margin-bottom: 10px;
}

.tree-upload-info .el-tag {
  margin-right: 10px;
  margin-bottom: 10px;
  background-color: rgba(255, 255, 255, 0.2) !important;
  border-color: rgba(255, 255, 255, 0.3) !important;
  color: #ffffff !important;
}

.upload-actions {
  margin-top: 20px;
  display: flex;
  gap: 10px;
}

.download-template {
  margin-top: 15px;
}

.download-template a {
  color: #2E8B57;
  text-decoration: none;
}

.download-template a:hover {
  text-decoration: underline;
}

.uploaded-files {
  margin-top: 20px;
}

.validate-result {
  background-color: rgba(0, 0, 0, 0.6) !important;
  padding: 15px;
  border-radius: 5px;
  border: 1px solid rgba(255, 255, 255, 0.2) !important;
}

.validate-title {
  color: #ffffff !important;
  font-size: 1.2rem;
  margin-bottom: 12px;
  text-shadow: 0 1px 2px rgba(0, 0, 0, 0.5);
}

.error-list {
  margin-top: 15px;
  padding: 15px;
  background-color: rgba(255, 100, 100, 0.15);
  border-radius: 4px;
  border: 1px solid rgba(255, 100, 100, 0.3);
}

.error-title {
  color: #ff6b6b !important;
  margin-bottom: 10px;
}

.error-item {
  color: #ffffff;
  margin-bottom: 5px;
  padding: 5px 0;
  border-bottom: 1px dashed rgba(255, 255, 255, 0.2);
}

.error-list ul {
  margin-top: 5px;
  padding-left: 20px;
}

.preview-data {
  margin-top: 20px;
  padding: 10px;
  background-color: rgba(46, 139, 87, 0.15);
  border-radius: 4px;
  border: 1px solid rgba(46, 139, 87, 0.3);
}

.preview-title {
  color: #2E8B57 !important;
  margin-bottom: 10px;
}

.api-docs {
  color: #fff;
}

.api-info {
  margin-bottom: 25px;
}

.api-info h3 {
  margin-bottom: 10px;
  color: #2E8B57 !important;
}

.api-info ul {
  margin: 10px 0;
  padding-left: 20px;
}

.code-sample {
  background-color: rgba(0, 0, 0, 0.3);
  padding: 10px;
  border-radius: 4px;
  font-family: monospace;
  white-space: pre-wrap;
  margin-top: 10px;
  color: #e0e0e0;
}

:deep(.el-upload-dragger) {
  background-color: rgba(0, 0, 0, 0.2);
  border: 1px dashed rgba(255, 255, 255, 0.3);
  width: 100%;
}

:deep(.el-upload) {
  width: 100%;
}

:deep(.el-upload__text) {
  color: #ccc;
}

:deep(.el-upload__tip) {
  color: #aaa;
}

:deep(.el-table) {
  background-color: transparent !important;
}

:deep(.el-table__inner-wrapper) {
  background-color: transparent !important;
}

:deep(.el-table__header-wrapper th.el-table__cell) {
  background-color: rgba(46, 139, 87, 0.3) !important;
  color: #fff !important;
  border-bottom: 1px solid rgba(255, 255, 255, 0.1) !important;
}

:deep(.el-table__body tr.el-table__row) {
  background-color: rgba(0, 0, 0, 0.25) !important;
}

:deep(.el-table__body tr.el-table__row:hover > td.el-table__cell) {
  background-color: rgba(46, 139, 87, 0.3) !important;
}

:deep(.el-table__body tr.el-table__row td.el-table__cell) {
  color: #fff !important;
  border-bottom: 1px solid rgba(255, 255, 255, 0.05) !important;
}

:deep(.el-alert) {
  background-color: rgba(13, 35, 69, 0.8) !important;
  border: 1px solid #409EFF !important;
}

:deep(.el-alert__title) {
  color: #ffffff !important;
  font-weight: 600 !important;
  font-size: 1rem !important;
}

:deep(.el-alert__description),
:deep(.el-alert__content p) {
  color: #ffffff !important;
  font-weight: 500 !important;
}
</style> 