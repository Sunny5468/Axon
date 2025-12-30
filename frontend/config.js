// 环境配置文件
// 根据部署环境自动选择 API 地址

const CONFIG = {
    // 开发环境配置
    development: {
        apiBaseUrl: 'http://localhost:8001',
        apiEndpoint: 'http://localhost:8001/api'
    },
    
    // 生产环境配置
    production: {
        // 方案1: 使用相对路径（推荐 - API 和前端在同一域名下）
        apiBaseUrl: '',  // 空字符串表示使用当前域名
        apiEndpoint: '/api',  // Nginx 代理到后端
        
        // 方案2: 使用独立的 API 子域名
        // apiBaseUrl: 'https://api.sunnyding.cn',
        // apiEndpoint: 'https://api.sunnyding.cn'
    }
};

// 自动检测环境
function getEnvironment() {
    const hostname = window.location.hostname;
    
    // 本地开发环境
    if (hostname === 'localhost' || hostname === '127.0.0.1') {
        return 'development';
    }
    
    // 生产环境
    return 'production';
}

// 获取当前环境的配置
const ENV = getEnvironment();
const API_CONFIG = CONFIG[ENV];

// 导出配置
window.API_BASE_URL = API_CONFIG.apiBaseUrl;
window.API_ENDPOINT = API_CONFIG.apiEndpoint;

console.log(`[Environment] Running in ${ENV} mode`);
console.log(`[API Config] Base URL: ${API_CONFIG.apiBaseUrl || 'current domain'}`);
console.log(`[API Config] Endpoint: ${API_CONFIG.apiEndpoint}`);
