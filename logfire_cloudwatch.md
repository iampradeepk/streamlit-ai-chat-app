# Docker-compatible Logfire + CloudWatch Integration Template

## Folder Structure:

```
logfire-cloudwatch-app/
├── Dockerfile
├── cloudwatch-config.json
├── log_config.py
├── app.py
├── requirements.txt
└── .dockerignore
```

---

### ✅ `Dockerfile`
```Dockerfile
FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD ["python", "app.py"]
```

---

### ✅ `requirements.txt`
```text
logfire
```

---

### ✅ `log_config.py`
```python
import logging
from logfire import configure

# Configure Logfire to log locally only
configure(exporter="console")  # or omit to disable exporting entirely

# Set up local file logging
logger = logging.getLogger("app")
logger.setLevel(logging.INFO)
file_handler = logging.FileHandler("/var/log/app.log")
file_handler.setFormatter(logging.Formatter('%(message)s'))
logger.addHandler(file_handler)
```

---

### ✅ `app.py`
```python
import logging
from log_config import logger
import time

if __name__ == '__main__':
    for i in range(10):
        logger.info(f"Running log event #{i}")
        time.sleep(2)
```

---

### ✅ `cloudwatch-config.json`
```json
{
  "logs": {
    "logs_collected": {
      "files": {
        "collect_list": [
          {
            "file_path": "/var/log/app.log",
            "log_group_name": "logfire-docker-log-group",
            "log_stream_name": "docker-app-stream",
            "timestamp_format": "%Y-%m-%d %H:%M:%S"
          }
        ]
      }
    }
  }
}
```

---

### ✅ `.dockerignore`
```text
__pycache__
*.pyc
*.pyo
*.log
```

---

## 🚀 How to Run in Docker and Connect to CloudWatch

### 1. **Build the Docker image**
```bash
docker build -t logfire-cloudwatch .
```

### 2. **Run the container and mount volume**
```bash
docker run -d \
  --name logfire-app \
  -v $(pwd)/logs:/var/log \
  logfire-cloudwatch
```

Ensure `/var/log/app.log` inside container is accessible and visible to CloudWatch agent.

### 3. **Install CloudWatch Agent on Host (or ECS/EC2)**
```bash
sudo yum install amazon-cloudwatch-agent -y  # Or apt for Debian/Ubuntu
```

### 4. **Apply CloudWatch Config**
```bash
sudo /opt/aws/amazon-cloudwatch-agent/bin/amazon-cloudwatch-agent-ctl \
  -a fetch-config \
  -m ec2 \
  -c file:/path/to/cloudwatch-config.json \
  -s
```

You’ll see logs from the Docker app appear in your AWS CloudWatch Logs console under the specified log group.

---

Let me know if you want this set up for ECS or EKS workloads next!
