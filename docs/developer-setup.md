# Local Document Intelligence — Developer Setup Guide

- 기준 버전: v0.1.0
- 기준 Commit: 3b70615
- 대상 환경: Windows + WSL2 Ubuntu
- 개발 상태: MVP / Local Prototype

## 1. Overview

본 문서는 신규 개발자가 Local Document Intelligence
프로젝트를 Clone하고 독립적으로 실행하기 위한 가이드이다.

다음 작업을 포함한다.

1. WSL2 Ubuntu 개발 환경 구축
2. 기본 개발 도구 설치
3. GitHub Repository Clone
4. Ollama 및 로컬 AI 모델 구성
5. Python 개발 환경 및 의존성 설치
6. 웹 애플리케이션 실행
7. 합성 테스트 문서 생성
8. 기본 RAG 기능 확인

Open WebUI는 초기 기술 검증에 사용한 도구이며,
현재 자체 애플리케이션 실행에는 필요하지 않다.

Docker 및 별도의 데이터베이스 서버도 필요하지 않다.

## 2. Recommended Hardware

| Component | Recommended | Validated Environment |
|---|---|---|
| Host OS | Windows 11 | Windows |
| Development OS | WSL2 Ubuntu | Ubuntu 26.04 LTS |
| CPU | 8 Core | AMD Ryzen 9 8945HS |
| RAM | 32GB | 32GB |
| GPU | NVIDIA GPU | RTX 4060 Laptop |
| VRAM | 8GB | 8GB |
| Available Storage | 20GB 이상 | SSD |

위 권장 사양은 초기 개발 환경을 기준으로 제안한 값이며,
공식 최소 요구 사양은 아니다.

GPU 없이 CPU 기반 추론도 가능하지만
응답 속도가 느려질 수 있다.

## 3. Software Environment

| Software | Reference Version |
|---|---|
| Python | 3.12.16 |
| uv | 0.13.10 |
| Ollama | 0.40.17 |
| Git | Installed version |
| Generation Model | qwen3.5:4b-q4_K_M |
| Embedding Model | bge-m3:567m |

Python 라이브러리 의존성은 저장소의
pyproject.toml 및 uv.lock에서 관리한다.

Ollama 및 모델의 배포 버전은 변경될 수 있으므로
정확한 환경 재현이 필요한 경우 실제 설치 버전과
모델 ID를 함께 기록한다.

## 4. Install WSL2 Ubuntu

Windows PowerShell을 관리자 권한으로 실행한다.

```powershell
wsl --install -d Ubuntu
```

설치 후 필요한 경우 Windows를 재부팅한다.

Ubuntu를 실행하고 Linux 사용자 이름 및 비밀번호를 설정한다.

WSL 버전 및 설치 상태를 확인한다.

```powershell
wsl --update
wsl --version
wsl -l -v
```

Ubuntu의 VERSION 항목이 2인지 확인한다.

이미 WSL2 Ubuntu 환경이 구성되어 있다면
본 단계는 생략할 수 있다.

Reference:
https://learn.microsoft.com/en-us/windows/wsl/install

## 5. Configure Ubuntu Environment

이후 명령어는 WSL Ubuntu 터미널에서 실행한다.

### 5.1 Install Required Packages

```bash
sudo apt update
sudo apt install -y git curl zstd
```

### 5.2 Verify systemd

```bash
ps -p 1 -o comm=
```

Expected result:

```text
systemd
```

systemd가 활성화되어 있지 않은 경우
/etc/wsl.conf의 기존 설정을 유지하면서
다음 항목을 추가하거나 수정한다.

```ini
[boot]
systemd=true
```

Windows PowerShell에서 WSL을 재시작한다.

```powershell
wsl --shutdown
```

주의: 실행 중인 다른 WSL 배포판도 종료될 수 있다.

Ubuntu를 다시 실행하여 systemd를 확인한다.

Reference:
https://learn.microsoft.com/en-us/windows/wsl/systemd/

### 5.3 Verify GPU

NVIDIA GPU를 사용할 경우 Windows에
WSL을 지원하는 NVIDIA Driver가 설치되어 있어야 한다.

WSL Ubuntu에서 다음 명령어를 실행한다.

```bash
nvidia-smi
```

GPU 이름, Driver Version 및 GPU Memory가
정상적으로 표시되는지 확인한다.

WSL 내부에 별도의 Linux NVIDIA Display Driver를
설치하지 않는다.

GPU 인식 실패 시 Windows Driver와 WSL 상태를 확인한다.

Reference:
https://docs.nvidia.com/cuda/wsl-user-guide/

## 6. Install uv

uv는 Python 버전, 가상환경 및 프로젝트 의존성을
관리하기 위한 도구이다.

초기 검증 환경과 동일한 uv 버전을 설치한다.

```bash
curl -LsSf https://astral.sh/uv/0.13.10/install.sh | sh
```

설치 프로그램은 공식 출처 및 내용을 확인한 후 실행한다.

설치가 완료되면 터미널을 다시 열고 버전을 확인한다.

```bash
uv --version
```

Expected result:

```text
uv 0.13.10
```

이미 호환 가능한 uv가 설치되어 있다면
중복 설치할 필요는 없다.

Reference:
https://docs.astral.sh/uv/getting-started/installation/

## 7. Install Ollama

Ollama는 로컬 AI 모델을 실행하고
REST API를 제공하는 Runtime이다.

공식 Linux 설치 스크립트를 사용한다.

```bash
curl -fsSL https://ollama.com/install.sh | sh
```

설치 상태를 확인한다.

```bash
ollama --version
systemctl status ollama --no-pager
curl http://127.0.0.1:11434
```

Expected API response:

```text
Ollama is running
```

공식 설치 스크립트는 현재 배포 버전을 설치한다.
초기 검증 버전인 0.40.17과 다를 수 있다.

이미 Ollama가 실행 중인 환경이라면
중복 설치하지 않는다.

Reference:
https://docs.ollama.com/linux

## 8. Clone Repository

프로젝트를 WSL Linux 파일시스템 내부에 저장한다.

```bash
mkdir -p ~/dev
cd ~/dev

git clone https://github.com/JongminChoi98/local-document-intelligence.git

cd local-document-intelligence
```

저장소 접근 권한이 필요한 경우
Repository Owner에게 권한을 요청한다.

### 8.1 Check Repository Status

```bash
git status
git log -1 --oneline
git tag -n
```

### 8.2 Run the Latest Development Version

기본적으로 main 브랜치를 사용한다.

```bash
git switch main
git pull --ff-only
```

### 8.3 Run the Original MVP Version

v0.1.0의 정확한 소스 버전을 재현할 경우
다음 명령어를 실행한다.

```bash
git switch --detach v0.1.0
git log -1 --oneline
git describe --tags --exact-match
```

Expected result:

```text
3b70615 docs: finalize MVP architecture and development roadmap
v0.1.0
```

v0.1.0 태그는 초기 MVP 소스 버전을 의미한다.

이후 추가된 개발자용 문서들은 main 브랜치에서 관리하므로
v0.1.0 태그에는 포함되어 있지 않을 수 있다.

### 8.4 Create Development Branch

개발자가 코드를 수정할 경우
별도의 개발 브랜치를 생성한다.

```bash
git switch -c dev/local-development
```

## 9. Configure Ollama for Local Operation

프로젝트 루트에 다음 설정 파일이 존재한다.

config/ollama/override.conf

Configuration:

```ini
[Service]
Environment="OLLAMA_NO_CLOUD=1"
Environment="OLLAMA_HOST=127.0.0.1:11434"
Environment="OLLAMA_CONTEXT_LENGTH=8192"
```

| Variable | Purpose |
|---|---|
| OLLAMA_NO_CLOUD | Cloud 기능 비활성화 |
| OLLAMA_HOST | Loopback API 주소 사용 |
| OLLAMA_CONTEXT_LENGTH | 기본 Context Window 설정 |

기존 Ollama를 다른 프로젝트에서도 사용하고 있다면
기존 서비스 설정을 먼저 확인한다.

```bash
systemctl cat ollama --no-pager
```

기존 override.conf가 있다면 내용을 확인하고
필요한 설정을 병합하거나 백업한다.

신규 개발 환경에서는 저장소의 설정을 적용한다.

```bash
sudo install -D -m 644 \
    config/ollama/override.conf \
    /etc/systemd/system/ollama.service.d/override.conf

sudo systemctl daemon-reload
sudo systemctl restart ollama
```

설정 적용 여부를 확인한다.

```bash
systemctl is-active ollama
systemctl show ollama --property=Environment --no-pager
ss -ltnp | grep 11434
curl http://127.0.0.1:11434
```

Expected result:

- Ollama service: active
- API address: 127.0.0.1:11434
- OLLAMA_NO_CLOUD=1
- OLLAMA_CONTEXT_LENGTH=8192

애플리케이션의 LLM 요청은 별도의 Context Window
설정을 전달할 수 있으며 기본값은 16384이다.

Cloud 기능 비활성화 및 Loopback 주소 사용은
모든 외부 네트워크 통신 차단을 보장하지 않는다.

상세 내용은 ollama-setup.md를 참고한다.

## 10. Install Python and Project Dependencies

프로젝트 루트에서 실행한다.

```bash
uv python install 3.12.16
uv sync --locked
```

uv는 프로젝트 전용 가상환경인 .venv를 생성하고
uv.lock에 정의된 의존성을 설치한다.

설치 결과를 확인한다.

```bash
uv run python --version
uv run python -c "import openpyxl, pypdf, chromadb, streamlit; print('Dependencies OK')"
```

Expected result:

```text
Python 3.12.16
Dependencies OK
```

별도로 Python 가상환경을 생성하거나
pip install을 실행할 필요는 없다.

## 11. Download Local AI Models

### 11.1 Generation Model

```bash
ollama pull qwen3.5:4b-q4_K_M
```

Role:

- Natural Language Generation
- Document-grounded Question Answering
- Query Rewriting

초기 환경에서 관측한 다운로드 크기: 약 3.3GB.

### 11.2 Embedding Model

```bash
ollama pull bge-m3:567m
```

Role:

- Document Embedding
- Query Embedding
- Semantic Retrieval

Embedding Dimension: 1024.

초기 환경에서 관측한 다운로드 크기: 약 1.2GB.

### 11.3 Verify Installed Models

```bash
ollama list
```

두 모델이 모두 설치되어 있는지 확인한다.

```bash
ollama show qwen3.5:4b-q4_K_M
ollama show bge-m3:567m
```

모델, Python 및 패키지의 최초 다운로드에는
인터넷 연결이 필요하다.

## 12. Verify Ollama API

### 12.1 Test Embedding API

```bash
uv run python - <<'PY'
from embeddings.ollama import embed_text

vector = embed_text("테스트 차량의 전원 계통 정비 기록")

print("Embedding dimension:", len(vector))
assert len(vector) == 1024
print("Embedding API OK")
PY
```

Expected result:

```text
Embedding dimension: 1024
Embedding API OK
```

### 12.2 Test LLM API

```bash
uv run python -m llm.ollama "안녕하세요. 한국어로 간단히 답변해 주세요."
```

Model, Prompt Tokens, Completion Tokens,
Duration 및 자연어 답변이 출력되어야 한다.

GPU 사용 여부는 별도 터미널에서 확인할 수 있다.

```bash
ollama ps
nvidia-smi
```

실제 GPU 사용량은 모델, Context Window,
동시 실행 상태 및 장비 사양에 따라 달라진다.

## 13. Run Web Application

프로젝트 루트에서 실행한다.

```bash
cd ~/dev/local-document-intelligence

uv run python -m streamlit run app.py
```

Windows 브라우저에서 다음 주소에 접속한다.

http://127.0.0.1:8501

### 13.1 Default Configuration

| Parameter | Value |
|---|---|
| Ollama API | 127.0.0.1:11434 |
| Streamlit | 127.0.0.1:8501 |
| Generation Model | qwen3.5:4b-q4_K_M |
| Embedding Model | bge-m3:567m |
| Thinking | Disabled |
| Context Window | 16384 |
| Temperature | 0.1 |
| Max Output Tokens | 1024 |
| Retrieval Top-K | 3 |
| Maximum Upload Size | 20MB per file |

### 13.2 Initial Application State

최초 실행 시 등록 문서 수가 0건인 것은 정상이다.

실제 회사 A/S 문서, Vector Database 및 채팅 이력은
GitHub 저장소에 포함되어 있지 않다.

질의응답을 수행하기 전에 지원 양식의 Excel 문서를
등록해야 한다.

## 14. Generate Synthetic Test Documents

실제 회사 A/S 기록이나 개인정보를 사용하지 않고
합성 테스트 데이터를 생성하여 실행을 확인한다.

별도의 Ubuntu 터미널에서 프로젝트 루트로 이동한다.

```bash
cd ~/dev/local-document-intelligence
```

다음 코드는 현재 전처리 모듈의 FIELD_MAP 및
EXPECTED_LABELS를 이용하여 지원 양식의
Excel 테스트 문서 두 개를 생성한다.

```bash
uv run python - <<'PY'
from pathlib import Path

from openpyxl import Workbook

from preprocessors.maintenance import (
    FIELD_MAP,
    EXPECTED_LABELS,
)

output_dir = Path("storage/test_samples")
output_dir.mkdir(parents=True, exist_ok=True)

common = {
    "created_date": "2026-01-10",
    "received_date": "2026-01-09",
    "service_date": "2026-01-10",
    "location": "테스트 정비소",
    "department": "테스트 정비팀",
    "service_duration": "1h",
    "symptom_category": "전원/전기",
    "cause_category": "부품 열화",
    "action_category": "부품 교체",
    "part_category": "전원/배선",
    "prevention": "정기 점검 실시",
}

samples = [
    {
        **common,
        "document_id": "TEST-AS-001",
        "customer": "테스트 고객사 A",
        "vehicle": "테스트 차량 1호",
        "reported_symptom": "간헐적인 전원 차단",
        "observed_symptom": "릴레이 접점 불량 확인",
        "cause": "릴레이 접점 노후화 확인",
        "repair_action": "릴레이 신품 교체",
        "service_parts": "24V 100A 릴레이 1개",
    },
    {
        **common,
        "document_id": "TEST-AS-002",
        "customer": "테스트 고객사 B",
        "vehicle": "테스트 차량 2호",
        "reported_symptom": "24V 단자대 과열",
        "observed_symptom": "전원 단자대 열화 확인",
        "cause": "접촉저항 증가로 추정",
        "repair_action": "단자대 및 배선 교체",
        "service_parts": "24V 단자대 1개, 4AWG 배선 1M",
    },
]

for sample in samples:
    workbook = Workbook()
    sheet = workbook.active
    sheet.title = "AS일지_2026"

    for address, label in EXPECTED_LABELS.items():
        sheet[address] = label

    for field, address in FIELD_MAP.items():
        sheet[address] = sample.get(field)

    path = output_dir / f"{sample['document_id']}.xlsx"

    workbook.save(path)
    workbook.close()

    print(f"Created: {path}")

print("Synthetic test documents created.")
PY
```

Expected result:

```text
Created: storage/test_samples/TEST-AS-001.xlsx
Created: storage/test_samples/TEST-AS-002.xlsx
Synthetic test documents created.
```

Windows 파일 탐색기에서 테스트 문서 폴더를 연다.

```bash
explorer.exe "$(wslpath -w "$PWD/storage/test_samples")"
```

생성된 Excel은 실제 정비 기록이 아닌 합성 데이터이다.

## 15. Register Test Documents

웹 애플리케이션에 접속한다.

http://127.0.0.1:8501

Sidebar의 문서 일괄 등록 영역에서
다음 두 파일을 선택한다.

- TEST-AS-001.xlsx
- TEST-AS-002.xlsx

일괄 등록 버튼을 누른다.

Expected result:

```text
전체 2건 | 성공 2건 | 실패 0건
```

초기 데이터베이스가 비어 있는 경우
등록된 정비 기록 수는 2건이어야 한다.

동일한 문서번호의 파일을 다시 등록하면
기존 레코드를 갱신하므로 문서 수가 증가하지 않는다.

## 16. Basic Functional Verification

다음 질문으로 기본 RAG 동작을 확인한다.

### Test 01 — Single Document Question

Question:

> TEST-AS-001 문서의 고객명과 교체 부품을 알려줘.

Expected facts:

- 고객명: 테스트 고객사 A
- 교체 부품: 24V 100A 릴레이 1개
- 관련 문서번호: TEST-AS-001

### Test 02 — Multi-document Question

새 채팅을 생성한다.

Question:

> 테스트 차량 1호와 2호의 고장 원인과 조치 내용을 비교해 줘.

Expected facts:

| Vehicle | Cause | Repair Action |
|---|---|---|
| 테스트 차량 1호 | 릴레이 접점 노후화 확인 | 릴레이 신품 교체 |
| 테스트 차량 2호 | 접촉저항 증가로 추정 | 단자대 및 배선 교체 |

추정 원인과 확인된 원인을 구분해야 한다.

### Test 03 — Conversational RAG

새 채팅에서 다음 질문을 순서대로 입력한다.

First question:

> 테스트 차량 2호의 고장 원인이 뭐야?

Follow-up question:

> 그러면 어떤 부품을 사용했어?

Expected facts:

- 첫 질문: 접촉저항 증가로 추정
- 후속 질문: 24V 단자대 1개, 4AWG 배선 1M
- 후속 질문의 검색 문맥에 테스트 차량 2호가 유지되어야 함

### Test 04 — Source Download

답변의 참조 문서 영역을 펼친다.

원본 Excel 다운로드 버튼을 눌러
실제 Excel 파일이 다운로드되는지 확인한다.

### Test 05 — Chat Persistence

브라우저를 새로고침한다.

저장된 채팅 목록에서 이전 채팅을 선택하고
질문, 답변 및 참조 문서가 유지되는지 확인한다.

### Verification Scope

위 테스트는 최초 실행 여부를 확인하기 위한
기본 Smoke Test이다.

전체 기능의 정상 동작, 검색 정확도 및
답변 신뢰성을 보증하는 통합 QA는 아니다.

## 17. Supported Document Formats

| Format | Support |
|---|---|
| XLSX | 특정 A/S 양식 등록 및 검색 |
| PDF | 기본 텍스트 추출만 지원 |
| XLS | 미지원 |
| DOCX | 미지원 |
| Scanned PDF | OCR 미지원 |
| Image | 미지원 |

현재 XLSX 전처리는 AS일지_2026 시트의
특정 셀 위치와 항목명을 기준으로 동작한다.

다른 양식의 Excel은 등록에 실패할 수 있다.

이는 범용 문서 전처리가 구현되지 않은
현재 버전의 알려진 제한 사항이다.

검증 로직을 임의로 제거하거나
잘못된 셀 매핑으로 문서를 등록하지 않는다.

## 18. Runtime Data Management

| Path | Description |
|---|---|
| storage/input/ | 원본 문서 |
| storage/input/uploads/ | 웹 업로드 원본 |
| storage/processed/ | 추출 결과 |
| storage/normalized/ | 정규화 결과 |
| storage/embeddings/ | Embedding JSON |
| storage/chroma/ | Vector Database |
| storage/chat_history.db | 채팅 이력 |
| storage/test_samples/ | 합성 테스트 문서 |

storage/ 전체는 Git 관리 대상에서 제외한다.

```bash
git check-ignore storage/test_samples/TEST-AS-001.xlsx
git check-ignore storage/chat_history.db
git status --short
```

실제 회사 문서, 고객 정보, 개인정보,
Embedding 데이터 및 채팅 이력을 GitHub에 등록하지 않는다.

## 19. Troubleshooting

| Problem | Solution |
|---|---|
| uv: command not found | 터미널 재실행 및 PATH 확인 |
| ollama: command not found | Ollama 설치 확인 |
| Ollama API 연결 실패 | systemctl status ollama 확인 |
| 모델 없음 | ollama list 확인 및 필요한 모델 다운로드 |
| GPU 미인식 | Windows NVIDIA Driver 및 WSL 상태 확인 |
| Python 버전 불일치 | uv python install 3.12.16 실행 |
| 의존성 설치 실패 | uv 버전 및 uv.lock 호환 여부 확인 |
| Excel 등록 ValueError | 지원 시트명 및 셀 양식 확인 |
| 등록 문서 0건 | 합성 테스트 문서 등록 |
| Context Window 오류 | 입력 크기 및 LLM Context 설정 확인 |
| 느린 응답 | Thinking 설정, ollama ps, nvidia-smi 확인 |
| 원본 다운로드 실패 | 원본 파일 및 저장 경로 확인 |
| 8501 포트 충돌 | 기존 서버 또는 포트 사용 상태 확인 |

### 19.1 Check Ollama

```bash
systemctl status ollama --no-pager
journalctl -u ollama -n 50 --no-pager
curl http://127.0.0.1:11434
```

### 19.2 Check Port Usage

```bash
ss -ltnp | grep -E '11434|8501'
```

8501 포트가 다른 서비스에 의해 사용 중이라면
기존 서비스를 임의로 종료하지 않고
다른 로컬 포트로 실행할 수 있다.

```bash
uv run python -m streamlit run app.py --server.port 8502
```

접속 주소:

http://127.0.0.1:8502

### 19.3 Excel Data Validation Warning

openpyxl에서 다음 경고가 발생할 수 있다.

```text
Data Validation extension is not supported and will be removed
```

현재 Parser는 원본 Excel 파일을 다시 저장하지 않는다.

이 경고만으로 문서 등록에 실패했다고 판단하지 않으며
별도의 실제 오류 및 등록 결과를 확인한다.

## 20. Stop and Restart Application

### Stop

Streamlit이 실행 중인 터미널에서 Ctrl+C를 입력한다.

### Restart

```bash
cd ~/dev/local-document-intelligence

systemctl is-active ollama

uv run python -m streamlit run app.py
```

Ollama 서비스가 중지되어 있다면 시작한다.

```bash
sudo systemctl start ollama
```

원본 문서, ChromaDB 및 SQLite 데이터는
storage/에 저장되므로 일반적인 서버 재시작 시 유지된다.

storage/를 삭제하면 기존 데이터가 손실될 수 있으므로
임의로 삭제하지 않는다.

## 21. Development Workflow

개발 작업은 별도의 브랜치에서 수행한다.

```bash
git status
git switch main
git pull --ff-only
git switch -c dev/my-feature
```

코드를 변경한 후 변경 사항을 확인한다.

```bash
git status
git diff
```

개발자는 승인된 소스 코드 및 문서만 Commit한다.

실제 회사 문서와 실행 데이터는 포함하지 않는다.

기존 v0.1.0 태그를 임의로 변경하지 않는다.

## 22. Security and Deployment Limitations

현재 시스템은 단일 사용자 로컬 프로토타입이다.

다음 기능은 아직 구현 또는 검증되지 않았다.

- 사용자 인증
- Role-based Access Control
- Audit Logging
- 완전한 오프라인 동작 검증
- 외부 네트워크 통신 차단 검증
- 정량적 검색 및 답변 품질 평가
- 운영 환경 백업 및 복구
- 사내 운영 서버 배포

현재 로컬 실행 설정만으로
사내 정보보호 요구사항을 충족한다고 판단해서는 안 된다.

실제 회사 문서는 사용 승인을 받은 경우에만 처리한다.

운영 환경 배포는 별도의 검증 및 승인 후 진행한다.

## 23. Installation Checklist

- [ ] WSL2 Ubuntu installed
- [ ] systemd available
- [ ] Git and required packages installed
- [ ] GPU availability checked, if applicable
- [ ] uv installed
- [ ] Ollama installed and running
- [ ] Repository cloned
- [ ] Target Git version confirmed
- [ ] Ollama local configuration applied
- [ ] Python 3.12.16 installed
- [ ] Dependencies installed using uv.lock
- [ ] Generation model downloaded
- [ ] Embedding model downloaded
- [ ] Embedding API verified
- [ ] LLM API verified
- [ ] Streamlit application running
- [ ] Synthetic Excel documents generated
- [ ] Synthetic documents registered
- [ ] Basic RAG question answering verified
- [ ] Source download verified
- [ ] Chat persistence verified

## Related Documents

- [Project README](../README.md)
- [Developer Overview](developer-overview.md)
- [System Architecture](architecture.md)
- [Ollama Setup](ollama-setup.md)
- [Local LLM Validation](local-llm-validation.md)
- [Development Roadmap](roadmap.md)

## Official References

- https://learn.microsoft.com/en-us/windows/wsl/install
- https://learn.microsoft.com/en-us/windows/wsl/systemd/
- https://docs.nvidia.com/cuda/wsl-user-guide/
- https://docs.astral.sh/uv/
- https://docs.ollama.com/
- https://docs.streamlit.io/
- https://docs.trychroma.com/
