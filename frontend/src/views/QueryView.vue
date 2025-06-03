<template>
  <div class="query">
    <h1>查詢樹木資料</h1>
    <div class="content-box query-form-box" style="background-color: rgba(30, 30, 30, 0.45) !important;">
      <el-form :model="queryForm" label-width="120px">
        <el-form-item label="選擇數據源">
          <el-select v-model="queryForm.fileId" placeholder="請選擇數據源" style="width: 100%;">
            <el-option
              v-for="file in files"
              :key="file.id"
              :label="file.name"
              :value="file.id">
            </el-option>
          </el-select>
        </el-form-item>
        <el-form-item label="搜索條件">
          <el-select v-model="queryForm.field" placeholder="請選擇字段" style="margin-right: 10px;">
            <el-option
              v-for="field in fields"
              :key="field"
              :label="field"
              :value="field">
            </el-option>
          </el-select>
          <el-select v-model="queryForm.operator" placeholder="運算符" style="margin-right: 10px;">
            <el-option label="等於" value="eq"></el-option>
            <el-option label="不等於" value="neq"></el-option>
            <el-option label="大於" value="gt"></el-option>
            <el-option label="小於" value="lt"></el-option>
            <el-option label="包含" value="contains"></el-option>
          </el-select>
          <el-input v-model="queryForm.value" placeholder="搜索值"></el-input>
        </el-form-item>
        <el-form-item>
          <el-button type="primary" @click="submitQuery" :loading="loading">查詢</el-button>
          <el-button @click="resetForm">重置</el-button>
        </el-form-item>
      </el-form>
    </div>

    <div v-if="queryResults.length > 0" class="content-box query-results" style="background-color: rgba(30, 30, 30, 0.3) !important;">
      <div class="card-header">
        <span>查詢結果 (共 {{ totalItems }} 條)</span>
        <el-button size="small" @click="exportData">導出結果</el-button>
      </div>
      <el-table 
        :data="queryResults" 
        style="width: 100%; background-color: rgba(0, 0, 0, 0.25) !important;" 
        height="400" 
        border 
        class="custom-table"
        v-loading="loading">
        <el-table-column
          v-for="column in tableColumns"
          :key="column"
          :prop="column"
          :label="column"
          :min-width="100">
        </el-table-column>
      </el-table>
      <div class="pagination-container">
        <el-pagination
          :current-page="currentPage"
          :page-sizes="[10, 20, 50, 100]"
          :page-size="pageSize"
          layout="total, sizes, prev, pager, next, jumper"
          :total="totalItems"
          @size-change="handleSizeChange"
          @current-change="handleCurrentChange">
        </el-pagination>
      </div>
    </div>
    
    <div v-if="loading && queryResults.length === 0" class="content-box loading-box" style="background-color: rgba(30, 30, 30, 0.3) !important;">
      <div class="loading-container">
        <el-icon class="is-loading"><loading /></el-icon>
        <p>正在查詢中...</p>
      </div>
    </div>
  </div>
</template>

<script>
import { ref, reactive } from 'vue'
import { ElMessage } from 'element-plus'
import { searchTrees } from '@/services/api'
import { Loading } from '@element-plus/icons-vue'

export default {
  name: 'QueryView',
  components: {
    Loading
  },
  setup() {
    // 定義欄位映射表
    const fieldMappings = {
      '樹種名稱': 'species',
      '胸徑': 'diameter',
      '樹高': 'height',
      '記錄日期': 'record_date',
      '專案': 'project__name',
      '創建者': 'created_by__username',
      '備註': 'notes',
      'ID': '_id',
    };

    // 定義欄位映射表（反向，從後端到前端的顯示）
    const reverseFieldMappings = {
      'species': '樹種名稱',
      'diameter': '胸徑',
      'height': '樹高',
      'record_date': '記錄日期',
      'project': '專案',
      'created_by': '創建者',
      'created_by_name': '創建者',
      'notes': '備註',
      '_id': 'ID',
      'project_name': '專案',
    };
    
    // 現在使用樹木相關的欄位
    const fields = ref(Object.keys(fieldMappings));
    
    const queryForm = reactive({
      fileId: 1, // 預設選擇第一個檔案（樹木主表）
      field: '',
      operator: '',
      value: ''
    });
    
    const queryResults = ref([]);
    const tableColumns = ref([]);
    const currentPage = ref(1);
    const pageSize = ref(10);
    const totalItems = ref(0);
    const loading = ref(false);
    
    // 模擬文件列表
    const files = ref([
      { id: 1, name: '樹木主表.csv' },
      { id: 2, name: '樹木歷史記錄.csv' },
      { id: 3, name: '林地調查資料.csv' }
    ]);
    
    // 實際查詢提交
    const submitQuery = async () => {
      if (!queryForm.field || !queryForm.operator || !queryForm.value) {
        ElMessage.warning('請完整填寫搜索條件');
        return;
      }
      
      // 驗證數值欄位的輸入
      const backendField = fieldMappings[queryForm.field] || queryForm.field;
      const numericFields = ['diameter', 'height', '_id'];
      if (numericFields.includes(backendField)) {
        const num = parseFloat(queryForm.value);
        if (isNaN(num)) {
          ElMessage.error(`${queryForm.field} 必須是有效的數字`);
          return;
        }
      }
      
      loading.value = true;
      try {
        // 使用API進行查詢
        console.log(`映射前端欄位 "${queryForm.field}" 到後端欄位 "${backendField}"`);
        
        const results = await searchTrees({
          field: backendField,
          operator: queryForm.operator,
          value: queryForm.value
        });
        
        // 處理結果
        if (results && results.length > 0) {
          // 提取所有可能的欄位
          const firstItem = results[0];
          tableColumns.value = Object.keys(firstItem)
            .filter(key => key !== 'images' && key !== 'url') // 排除一些不需要顯示的欄位
            .map(key => {
              // 轉換欄位名稱為顯示用名稱
              return reverseFieldMappings[key] || key;
            });
          
          // 格式化數據以供表格顯示
          queryResults.value = results.map(item => {
            const formattedItem = {};
            Object.keys(item).forEach(key => {
              if (key !== 'images' && key !== 'url') {
                const displayKey = reverseFieldMappings[key] || key;
                formattedItem[displayKey] = item[key];
              }
            });
            return formattedItem;
          });
          
          totalItems.value = results.length;
          ElMessage.success(`查詢成功，找到 ${results.length} 條記錄`);
        } else {
          queryResults.value = [];
          totalItems.value = 0;
          ElMessage.info('沒有符合條件的記錄');
        }
      } catch (error) {
        console.error('查詢失敗:', error);
        ElMessage.error(`查詢失敗: ${error.message || '請稍後再試'}`);
        queryResults.value = [];
      } finally {
        loading.value = false;
      }
    };
    
    const resetForm = () => {
      queryForm.field = '';
      queryForm.operator = '';
      queryForm.value = '';
      queryResults.value = [];
      totalItems.value = 0;
    };
    
    const handleSizeChange = (size) => {
      pageSize.value = size;
      // 在實際開發中，這裡應該重新調用查詢API
    };
    
    const handleCurrentChange = (page) => {
      currentPage.value = page;
      // 在實際開發中，這裡應該重新調用查詢API
    };
    
    const exportData = () => {
      if (queryResults.value.length === 0) {
        ElMessage.warning('沒有數據可匯出');
        return;
      }
      
      try {
        // 將結果轉換為CSV
        const headers = tableColumns.value;
        const rows = queryResults.value.map(item => {
          return headers.map(header => {
            return item[header] !== undefined && item[header] !== null ? 
              item[header].toString() : '';
          });
        });
        
        // 創建CSV內容
        let csvContent = "data:text/csv;charset=utf-8,";
        csvContent += headers.join(",") + "\n";
        rows.forEach(row => {
          csvContent += row.join(",") + "\n";
        });
        
        // 創建下載連結
        const encodedUri = encodeURI(csvContent);
        const link = document.createElement("a");
        link.setAttribute("href", encodedUri);
        link.setAttribute("download", "查詢結果.csv");
        document.body.appendChild(link);
        link.click();
        document.body.removeChild(link);
        
        ElMessage.success('數據導出成功');
      } catch (error) {
        console.error('數據導出失敗:', error);
        ElMessage.error('數據導出失敗');
      }
    };
    
    return {
      files,
      fields,
      queryForm,
      queryResults,
      tableColumns,
      currentPage,
      pageSize,
      totalItems,
      loading,
      submitQuery,
      resetForm,
      handleSizeChange,
      handleCurrentChange,
      exportData
    };
  }
}
</script>

<style scoped>
.query {
  padding: 20px;
  padding-left: 80px;
  height: 100%;
  overflow-y: auto;
  color: #fff;
}

.query-results {
  margin-top: 20px;
}

.query-form-box {
  background-color: rgba(30, 30, 30, 0.45) !important;
}

h1 {
  color: #fff !important;
  text-shadow: 0 2px 4px rgba(0, 0, 0, 0.5);
  margin-bottom: 20px;
  font-weight: bold;
}

.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  font-size: 18px;
  font-weight: bold;
  color: #ffffff;
  margin-bottom: 15px;
}

.pagination-container {
  margin-top: 20px;
  display: flex;
  justify-content: center;
}

.el-form-item__label {
  color: #fff !important;
}

.el-select .el-input__inner,
.el-input__inner {
  color: #fff !important;
  background-color: rgba(30, 30, 30, 0.8) !important;
}

.el-input__wrapper {
  background-color: rgba(30, 30, 30, 0.8) !important;
  box-shadow: 0 0 0 1px rgba(255, 255, 255, 0.2) inset !important;
}

.el-select .el-input .el-select__caret {
  color: #fff;
}

/* 下拉菜單樣式 */
.el-select__popper.el-popper,
.el-select-dropdown {
  background-color: rgba(45, 45, 45, 0.95) !important;
  border-color: rgba(255, 255, 255, 0.2) !important;
}

.el-select-dropdown__item {
  color: #fff !important;
}

.el-select-dropdown__item.hover,
.el-select-dropdown__item:hover {
  background-color: rgba(46, 139, 87, 0.3) !important;
}

.el-pagination {
  --el-pagination-button-color: #fff;
  --el-pagination-text-color: #fff;
}

.el-pagination .el-select .el-input .el-input__inner {
  color: #000;
}

/* 自定義表格樣式 */
.custom-table {
  --el-table-header-bg-color: rgba(46, 139, 87, 0.3) !important;
  --el-table-tr-bg-color: rgba(0, 0, 0, 0.25) !important;
  --el-table-border-color: rgba(255, 255, 255, 0.1) !important;
  --el-table-text-color: #fff !important;
  background-color: transparent !important;
}

.custom-table .el-table__inner-wrapper,
.custom-table .el-scrollbar__wrap,
.custom-table .el-table__body,
.custom-table .el-table__header {
  background-color: transparent !important;
}

.custom-table th.el-table__cell {
  background-color: rgba(46, 139, 87, 0.3) !important;
  border-bottom: 1px solid rgba(255, 255, 255, 0.1) !important;
  color: #fff !important;
}

.custom-table tr.el-table__row {
  background-color: rgba(0, 0, 0, 0.25) !important;
}

.custom-table tr.el-table__row td.el-table__cell {
  background-color: transparent !important;
  color: #fff !important;
  border-bottom: 1px solid rgba(255, 255, 255, 0.05) !important;
}

.el-table__body tr.el-table__row.hover-row > td.el-table__cell,
.el-table__body tr.el-table__row:hover > td.el-table__cell {
  background-color: rgba(46, 139, 87, 0.3) !important;
}

.el-table__header-wrapper,
.el-table__body-wrapper,
.el-table__footer-wrapper {
  background-color: transparent !important;
}

.el-table__empty-block {
  background-color: rgba(0, 0, 0, 0.2) !important;
}

/* 額外強制覆蓋元素 */
.el-table--enable-row-hover .el-table__body tr:hover > td {
  background-color: rgba(46, 139, 87, 0.3) !important;
}

.el-table__body,
.el-table__header,
.el-table__footer,
.el-table__fixed-body-wrapper,
.el-table__fixed-header-wrapper,
.el-table__fixed-footer-wrapper {
  background-color: transparent !important;
}

/* 確保表格背景是透明的 */
.el-table::before {
  display: none !important;
}

.el-table, 
.el-table__header,
.el-table__body,
.el-table__footer {
  background-color: transparent !important;
}

/* 按鈕樣式調整 */
.el-button {
  color: #ffffff !important;
  border-color: rgba(255, 255, 255, 0.2) !important;
}

.el-button:not(.el-button--primary) {
  background-color: rgba(70, 70, 70, 0.8) !important;
}

.el-button:not(.el-button--primary):hover {
  background-color: rgba(90, 90, 90, 0.9) !important;
}
</style> 