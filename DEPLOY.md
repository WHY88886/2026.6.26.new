# 部署指南

## 必须上传到GitHub的文件（共4个）

```
📁 你的仓库/
├── 📄 app_dividend_valuation.py    ← 主应用文件（必须）
├── 📄 requirements.txt              ← 依赖文件（必须）
├── 📁 .streamlit/
│   └── 📄 config.toml               ← 配置文件（必须）
└── 📄 README.md                     ← 说明文件（可选但推荐）
```

## 部署步骤

### 第一步：创建GitHub仓库
1. 登录 GitHub.com
2. 点击右上角 "+" → "New repository"
3. 仓库名称填写：`stock-valuation-system`
4. 选择 "Public"（公开）
5. 点击 "Create repository"

### 第二步：上传文件
在新建的仓库页面：
1. 点击 "uploading an existing file"
2. 将以下4个文件拖入：
   - `app_dividend_valuation.py`
   - `requirements.txt`
   - `.streamlit/config.toml`（需要先创建 .streamlit 文件夹）
   - `README.md`
3. 点击 "Commit changes"

**注意**：`.streamlit/config.toml` 的上传方式：
- 先在仓库创建 `.streamlit` 文件夹
- 然后在该文件夹中上传 `config.toml`

### 第三步：部署到Streamlit Cloud
1. 访问 https://share.streamlit.io/
2. 用GitHub账号登录
3. 点击 "New app"
4. 填写：
   - Repository: 选择你的仓库
   - Branch: main
   - Main file path: `app_dividend_valuation.py`
5. 点击 "Deploy!"

### 第四步：等待部署
- 首次部署约需1-2分钟
- 成功后会显示应用URL

## 常见问题

### Q: 报错 ModuleNotFoundError
A: 确保 `requirements.txt` 文件已上传，且内容正确

### Q: 报错 FileNotFoundError
A: 确保 `.streamlit/config.toml` 文件路径正确

### Q: 页面空白
A: 检查 `app_dividend_valuation.py` 是否完整上传
