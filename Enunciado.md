# SystemInfo: Servidor HTTP para exportação de informação do sistema  
## Laboratório de Sistemas Operacionais (CC) – Trabalho Prático

---

### 1. Objetivos

- Compreender a construção e personalização de sistemas Linux embarcados.
- Desenvolver uma aplicação que acessa informações do sistema através dos diretórios `/proc` e `/sys`.
- Criar e expor um serviço REST simples no ambiente gerado com Buildroot.
- Trabalhar com conceitos de processos, uso de recursos, dispositivos e interfaces do sistema operacional.

---

### 2. Descrição

Neste trabalho, você deve utilizar o **Buildroot** para gerar uma imagem Linux embarcada contendo uma aplicação em **Python 3** que será executada automaticamente após o boot. Esta aplicação deve criar um **servidor REST** escutando na porta **8080**:

```
GET /status
```

Esse endpoint deve retornar, em **formato JSON**, as informações do sistema descritas abaixo. **Todas as informações devem ser obtidas dinamicamente** a cada requisição e exclusivamente por meio de arquivos em `/proc` e `/sys`.

---

### ⚠️ Requisitos obrigatórios

- O **servidor Python deve estar incluído na imagem final da distribuição Linux gerada pelo Buildroot**.
- O programa `linuxstatus.py` deve ser **executado automaticamente na inicialização do sistema**.
- A aplicação deve escutar na **porta 8080** e retornar os dados em **JSON**.
- **Não é permitido o uso de bibliotecas externas**. Utilize apenas a **Python Standard Library**.

---

### 3. Informações a serem exibidas no JSON

A resposta ao acessar `/status` deve conter as seguintes chaves:

- `datetime`: Data e hora atual do sistema.
- `uptime_seconds`: Tempo desde o último boot (em segundos).
- `cpu`:  
  - `model`: Modelo do processador.  
  - `speed_mhz`: Frequência.  
  - `usage_percent`: Uso atual da CPU em porcentagem.
- `memory`:  
  - `total_mb`: Memória total.  
  - `used_mb`: Memória usada.
- `os_version`: Versão do sistema operacional.
- `processes`: Lista de processos com `pid` e `name`.
- `disks`: Lista de dispositivos de armazenamento com `device` e `size_mb`.
- `usb_devices`: Lista de dispositivos USB com `port` e `description`.
- `network_adapters`: Lista de interfaces de rede com `interface` e `ip_address`.

---

### 4. Exemplo de retorno esperado

```json
{
  "datetime": "2025-04-02 14:33:10",
  "uptime_seconds": 123456,
  "cpu": {
    "model": "ARMv7 Processor rev 4 (v7l)",
    "speed_mhz": 1200,
    "usage_percent": 17.5
  },
  "memory": {
    "total_mb": 512,
    "used_mb": 230
  },
  "os_version": "Linux version 5.15.0 (buildroot@host) #1 SMP Wed Mar 27",
  "processes": [
    { "pid": 1, "name": "init" },
    { "pid": 2, "name": "kthreadd" }
  ],
  "disks": [
    { "device": "/dev/mmcblk0", "size_mb": 8192 }
  ],
  "usb_devices": [
    { "port": "1-1", "description": "SanDisk Corp. Cruzer Blade" }
  ],
  "network_adapters": [
    { "interface": "eth0", "ip_address": "192.168.0.100" }
  ]
}
```

---

### 5. Código base (a ser completado pelo aluno)

```python
#!/usr/bin/env python3

import json
import time
from http.server import BaseHTTPRequestHandler, HTTPServer
from datetime import datetime

# --- Alunos devem implementar as funções abaixo --- #

def get_datetime():
    return 0

def get_uptime():
    return 0  # TODO

def get_cpu_info():
    return {
        "model": "TODO",
        "speed_mhz": 0,
        "usage_percent": 0.0
    }

def get_memory_info():
    return {
        "total_mb": 0,
        "used_mb": 0
    }

def get_os_version():
    return "TODO"

def get_process_list():
    return []  # lista de { "pid": int, "name": str }

def get_disks():
    return []  # lista de { "device": str, "size_mb": int }

def get_usb_devices():
    return []  # lista de { "port": str, "description": str }

def get_network_adapters():
    return []  # lista de { "interface": str, "ip_address": str }

# --- Servidor HTTP --- #

class StatusHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path != "/status":
            self.send_response(404)
            self.end_headers()
            self.wfile.write(b"Not Found")
            return

        response = {
            "datetime": get_datetime(),
            "uptime_seconds": get_uptime(),
            "cpu": get_cpu_info(),
            "memory": get_memory_info(),
            "os_version": get_os_version(),
            "processes": get_process_list(),
            "disks": get_disks(),
            "usb_devices": get_usb_devices(),
            "network_adapters": get_network_adapters()
        }

        data = json.dumps(response, indent=2).encode()
        self.send_response(200)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(data)))
        self.end_headers()
        self.wfile.write(data)

def run_server(port=8080):
    print(f"Servidor disponível em http://0.0.0.0:{port}/status")
    server = HTTPServer(("0.0.0.0", port), StatusHandler)
    server.serve_forever()

if __name__ == "__main__":
    run_server()
```

---

### 6. Entrega

* **Código-fonte completo**: arquivo `systeminfo.py` com todas as funções implementadas.
* **Arquivo de configuração**: `.config` localizado na raiz do projeto **Buildroot**.
* **Manual do programa**: arquivo `README.md` contendo:
  * Descrição do funcionamento básico do programa.
  * Capturas de tela (screenshots) das respostas obtidas pelo endpoint `/status`.
  * Explicação de como cada informação exibida é obtida a partir de `/proc` e `/sys`.