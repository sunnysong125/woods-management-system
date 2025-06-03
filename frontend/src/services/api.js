import axios from 'axios';

// 使用相對路徑，這樣在任何環境下都能正常工作
// 相對於當前域名的路徑 - 如果後端和前端部署在同一伺服器
const apiBaseUrl = 'https://srv.orderble.com.tw/woodsbackend/api';

// 创建一个axios实例
const apiClient = axios.create({
  baseURL: apiBaseUrl,
  timeout: 10000
  // 移除固定的Content-Type讓axios自動決定
});

// 添加请求拦截器處理請求格式
apiClient.interceptors.request.use(
  config => {
    // 對POST和PUT請求特殊處理
    if (config.method === 'post' || config.method === 'put') {
      // 如果不是FormData，轉換為FormData
      if (!(config.data instanceof FormData)) {
        const formData = new FormData();
        for (const key in config.data) {
          if (config.data[key] !== null && config.data[key] !== undefined) {
            formData.append(key, config.data[key]);
          }
        }
        config.data = formData;
      }
    }
    return config;
  },
  error => {
    return Promise.reject(error);
  }
);

// 获取树木数据
export const getTrees = async () => {
  try {
    const response = await apiClient.get('/trees/');
    return response.data;
  } catch (error) {
    console.error('获取树木数据失败:', error);
    throw error;
  }
};

// 查詢樹木數據
export const searchTrees = async (params) => {
  try {
    // 構建查詢參數
    const queryParams = new URLSearchParams();
    
    if (params.field && params.value) {
      // 嚴格檢查是否是數值型欄位，如果是則轉換為數字
      const numericFields = ['diameter', 'height', '_id'];
      const isNumericField = numericFields.includes(params.field);
      
      // 處理數值類型
      let value = params.value;
      if (isNumericField) {
        value = parseFloat(params.value);
        if (isNaN(value)) {
          throw new Error(`欄位 ${params.field} 需要數字值，但提供的值無效: ${params.value}`);
        }
      }
      
      // 根據不同的運算符，構建不同的查詢參數
      console.log(`查詢條件: ${params.field} ${params.operator} ${value}`);
      
      if (params.operator === 'eq') {
        queryParams.append(params.field, value);
      } else if (params.operator === 'gt') {
        queryParams.append(`${params.field}__gt`, value);
      } else if (params.operator === 'lt') {
        queryParams.append(`${params.field}__lt`, value);
      } else if (params.operator === 'contains') {
        queryParams.append(`${params.field}__contains`, value);
      } else if (params.operator === 'neq') {
        queryParams.append(`${params.field}__ne`, value);
      }
    }
    
    const url = `/trees/?${queryParams.toString()}`;
    console.log(`發送查詢請求: ${url}`);
    
    const response = await apiClient.get(url);
    return response.data;
  } catch (error) {
    console.error('查詢樹木數據失敗:', error);
    throw error;
  }
};

// 按ID获取树木
export const getTreeById = async (id) => {
  try {
    const response = await apiClient.get(`/trees/${id}/`);
    return response.data;
  } catch (error) {
    console.error(`获取ID为${id}的树木数据失败:`, error);
    throw error;
  }
};

// 添加树木数据
export const addTree = async (treeData) => {
  try {
    const response = await apiClient.post('/trees/', treeData);
    return response.data;
  } catch (error) {
    console.error('添加树木数据失败:', error);
    throw error;
  }
};

// 更新树木数据
export const updateTree = async (id, treeData) => {
  try {
    const response = await apiClient.put(`/trees/${id}/`, treeData);
    return response.data;
  } catch (error) {
    console.error(`更新ID为${id}的树木数据失败:`, error);
    throw error;
  }
};

// 删除树木数据
export const deleteTree = async (id) => {
  try {
    const response = await apiClient.delete(`/trees/${id}/`);
    return response.data;
  } catch (error) {
    console.error(`删除ID为${id}的树木数据失败:`, error);
    throw error;
  }
};

// 获取所有专案
export const getProjects = async () => {
  try {
    const response = await apiClient.get('/projects/');
    return response.data;
  } catch (error) {
    console.error('获取专案数据失败:', error);
    throw error;
  }
};

// 按ID获取专案
export const getProjectById = async (id) => {
  try {
    const response = await apiClient.get(`/projects/${id}/`);
    return response.data;
  } catch (error) {
    console.error(`获取ID为${id}的专案数据失败:`, error);
    throw error;
  }
};

// 添加专案
export const addProject = async (projectData) => {
  try {
    const response = await apiClient.post('/projects/', projectData);
    return response.data;
  } catch (error) {
    console.error('添加专案数据失败:', error);
    throw error;
  }
};

// 更新专案
export const updateProject = async (id, projectData) => {
  try {
    const response = await apiClient.put(`/projects/${id}/`, projectData);
    return response.data;
  } catch (error) {
    console.error(`更新ID为${id}的专案数据失败:`, error);
    throw error;
  }
};

// 删除专案
export const deleteProject = async (id) => {
  try {
    const response = await apiClient.delete(`/projects/${id}/`);
    return response.data;
  } catch (error) {
    console.error(`删除ID为${id}的专案数据失败:`, error);
    throw error;
  }
};

// ======== CSV 上傳相關API ========

/**
 * 上傳 CSV 文件並匯入樹木資料
 * @param {File} file - 要上傳的 CSV 文件
 * @param {Object} options - 額外選項
 * @param {boolean} options.validate_only - 設為 true 時只驗證不匯入 
 * @param {number} options.project_id - 指定的專案ID
 * @param {number} options.user_id - 使用者ID
 * @param {number} options.batch_id - 批次ID，應用於所有記錄
 * @returns {Promise<Object>} - 上傳結果
 */
export const uploadCsvFile = async (file, options = {}) => {
  try {
    const formData = new FormData();
    formData.append('file', file);
    
    // 添加任何額外的選項參數
    Object.keys(options).forEach(key => {
      if (options[key] !== undefined && options[key] !== null) {
        formData.append(key, options[key].toString());
      }
    });
    
    console.log('上傳選項:', options);
    
    const response = await apiClient.post('/trees/upload-csv/', formData, {
      headers: {
        'Content-Type': 'multipart/form-data'
      }
    });
    return response.data;
  } catch (error) {
    console.error('CSV 文件上傳失敗:', error);
    throw error;
  }
};

/**
 * 驗證 CSV 數據但不匯入
 * @param {File} file - 要驗證的 CSV 文件
 * @returns {Promise<Object>} - 驗證結果
 */
export const validateCsvFile = async (file) => {
  try {
    console.log('開始驗證CSV文件...');

    const formData = new FormData();
    formData.append('file', file);
    formData.append('validate_only', 'true');
    
    // 顯示請求詳情，便於調試
    console.log('驗證請求詳情:', {
      file: file.name,
      size: file.size,
      type: file.type,
      lastModified: new Date(file.lastModified).toLocaleString()
    });
    
    const response = await apiClient.post('/trees/upload-csv/', formData, {
      headers: {
        'Content-Type': 'multipart/form-data'
      }
    });
    
    console.log('驗證響應:', response.data);
    return response.data;
  } catch (error) {
    console.error('CSV驗證錯誤:', error);
    console.error('錯誤詳情:', {
      message: error.message,
      stack: error.stack,
      response: error.response ? {
        status: error.response.status,
        statusText: error.response.statusText,
        data: error.response.data
      } : '無響應數據'
    });
    
    // 重新格式化錯誤以提供更有用的信息
    throw {
      message: `CSV驗證失敗: ${error.message}`,
      response: error.response,
      originalError: error
    };
  }
};

/**
 * 獲取 CSV 匯入歷史記錄
 * @returns {Promise<Array>} - 匯入歷史記錄列表
 */
export const getCsvImportHistory = async () => {
  try {
    const response = await apiClient.get('/trees/import-history/');
    return response.data;
  } catch (error) {
    console.error('獲取CSV匯入歷史失敗:', error);
    throw error;
  }
};

/**
 * 測試 API 連接
 * @returns {Promise<Object>} - 測試結果
 */
export const testApiConnection = async () => {
  try {
    const response = await apiClient.get('/trees/test/');
    return response.data;
  } catch (error) {
    console.error('API 連接測試失敗:', error);
    throw error;
  }
}; 