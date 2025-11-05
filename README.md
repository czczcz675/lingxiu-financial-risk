# 灵嗅金融风险监测应用

这是一个基于Streamlit开发的金融风险监测应用，提供高级风险分析、预警和可视化功能。

## 功能特点

- 高级风险监测仪表盘
- 实时风险趋势图表
- 多维度预警信息展示
- 机构风险分布分析
- 人工智能风险分析
- 风险热力图展示
- 技术架构可视化

## 系统要求

- Python 3.8 或更高版本
- pip 包管理器

## 安装与运行

### 本地运行

1. 克隆或下载此仓库

2. 安装依赖
```bash
pip install -r requirements.txt
```

3. 运行应用
```bash
streamlit run 灵嗅app.py
```

### 在 iCloud 上运行

1. 将项目文件保存到 iCloud 云盘
2. 在支持 Python 的应用中打开并运行
3. 确保安装了所需的依赖包

### 在 GitHub Codespaces 上运行

1. 将项目推送到 GitHub 仓库
2. 在 GitHub 中打开仓库并创建 Codespace
3. 在 Codespace 终端中执行安装和运行命令

## 依赖项

- streamlit: Web应用框架
- pandas: 数据处理
- numpy: 数值计算
- plotly: 交互式图表
- python-dateutil: 日期时间处理

## 注意事项

- 应用使用模拟数据进行演示
- 实际部署时应连接真实数据源
- 建议定期更新依赖包以确保安全性

## 开发与扩展

应用采用面向对象设计，便于扩展新功能：
- 添加新的分析方法到 `AdvancedFinancialRiskMonitor` 类
- 使用 `@handle_errors` 装饰器增强代码健壮性
- 利用 `@st.cache_data` 提高应用性能

## 故障排除

- 如遇依赖安装问题，尝试使用虚拟环境
- 如应用运行缓慢，检查数据缓存配置
- 若出现错误，请查看日志输出进行排查