# Databricks LLM Playground

一個部署於 Azure VM 的 Databricks Claude 模型測試介面，支援一鍵部署。

## ⚡ 一鍵部署到 Azure

點擊下方按鈕，填入參數即可自動建立 VM 並啟動服務：

[![Deploy to Azure](https://aka.ms/deploytoazurebutton)](https://portal.azure.com/#create/Microsoft.Template/uri/https%3A%2F%2Fraw.githubusercontent.com%2Fhatsukiotowa%2Fdatabricks-playground%2Fmain%2Fazuredeploy.json)

> **部署完成後約需等待 3-5 分鐘**讓 VM 完成初始化與套件安裝。

---

## 📋 部署參數說明

| 參數 | 說明 | 預設值 |
|------|------|--------|
| `vmName` | VM 名稱 | `databricks-playground` |
| `adminUsername` | SSH 登入帳號 | `azureuser` |
| `adminPassword` | SSH 登入密碼（必填） | - |
| `githubRepoUrl` | 此 Repo 的 URL | `https://github.com/hatsukiotowa/databricks-playground` |
| `location` | 部署區域 | Resource Group 區域 |

---

## 🖥️ VM 規格

- **機型**：Standard B2as v2（2 vCPU, 8 GB RAM）
- **OS**：Ubuntu 24.04 LTS
- **磁碟**：30 GB Premium SSD
- **開放 Port**：`8080`（Playground）、`22`（SSH）

---

## 🌐 部署完成後

部署輸出 (Outputs) 會顯示：

```
playgroundUrl  →  http://<your-domain>.cloudapp.azure.com:8080
publicIP       →  xx.xx.xx.xx
sshCommand     →  ssh azureuser@xx.xx.xx.xx
```

直接開啟 `playgroundUrl` 即可使用。

---

## 🔧 本機開發

```bash
# 安裝依賴
pip3 install fastapi uvicorn httpx

# 啟動 Server（同時 serve HTML + 代理 API）
python3 databricks_server.py

# 開啟瀏覽器
open http://localhost:8080
```

---

## 📁 檔案結構

```
databricks-playground/
├── azuredeploy.json              # ARM Template（一鍵部署）
├── azuredeploy.parameters.json  # 部署參數範本
├── databricks_server.py         # FastAPI Server（HTML + Proxy）
├── databricks_playground.html   # 前端 Playground UI
├── setup.sh                     # VM 初始化腳本（參考用）
└── README.md
```

---

## ⚠️ 安全提醒

- Databricks Token 儲存於瀏覽器 `localStorage`，請勿在公用電腦使用
- 建議部署後在 Azure NSG 限制 `8080` port 只允許你的 IP 連入
- 請定期輪換 Databricks Token
