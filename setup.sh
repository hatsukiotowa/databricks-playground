#!/bin/bash
# Databricks Playground - VM 自動安裝與啟動腳本
# 由 Azure ARM Template cloud-init 呼叫

set -e
exec > /var/log/databricks-playground-setup.log 2>&1

echo "=== Databricks Playground Setup Start ==="

# 1. 更新套件
apt-get update -y
apt-get install -y python3 python3-pip git

# 2. 安裝 Python 依賴
pip3 install fastapi uvicorn httpx --break-system-packages --ignore-installed typing-extensions

# 3. 建立應用目錄
mkdir -p /opt/databricks-playground
cd /opt/databricks-playground

# 4. 複製應用檔案（已由 ARM template 透過 customData 注入，或從此 repo clone）
if [ ! -f /opt/databricks-playground/databricks_server.py ]; then
  # 從 GitHub clone（部署後自動抓最新版）
  REPO_URL="${REPO_URL:-https://github.com/GITHUB_USERNAME/databricks-playground}"
  git clone "$REPO_URL" /tmp/databricks-playground-repo
  cp /tmp/databricks-playground-repo/databricks_server.py /opt/databricks-playground/
  cp /tmp/databricks-playground-repo/databricks_playground.html /opt/databricks-playground/
fi

# 5. 建立 systemd service（開機自動啟動）
cat > /etc/systemd/system/databricks-playground.service << 'EOF'
[Unit]
Description=Databricks Playground Server
After=network.target

[Service]
Type=simple
User=root
WorkingDirectory=/opt/databricks-playground
ExecStart=/usr/bin/python3 /opt/databricks-playground/databricks_server.py
Restart=always
RestartSec=5
StandardOutput=journal
StandardError=journal

[Install]
WantedBy=multi-user.target
EOF

# 6. 啟動服務
systemctl daemon-reload
systemctl enable databricks-playground
systemctl start databricks-playground

echo "=== Setup Complete ==="
echo "Service running on port 8080"
