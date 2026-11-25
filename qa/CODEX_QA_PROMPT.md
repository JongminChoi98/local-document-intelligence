# Local Document Intelligence — Codex QA Prompt

- 최초 검증 대상: v0.1.0
- Baseline Commit: 3b70615
- 목적: 독립적인 기능 검증 및 결함 발견
- 작업 유형: QA / Integration Test / Regression Test

---

## 1. 작업 목적

현재 개발된 Local Document Intelligence 시스템의
전체 기능을 독립적인 QA 관점에서 검증해 줘.

단순한 소스 코드 검토에 그치지 않고 실제 애플리케이션,
Ollama API, 데이터베이스 및 웹 인터페이스를 실행하여
기능이 정상적으로 동작하는지 확인해야 한다.

이번 작업의 목적은 다음과 같다.

- 신규 개발 환경에서의 실행 가능 여부 확인
- 구현된 기능의 정상 동작 검증
- 기능 간 연동 오류 발견
- 검색 결과 및 AI 답변 정확성 확인
- 예외 처리 및 데이터 무결성 확인
- 기본적인 보안 설정 확인
- 응답 시간 및 시스템 자원 사용량 측정
- 발견된 결함 및 개선 사항 보고

새로운 기능 개발이나 리팩토링은 수행하지 않는다.

## 2. 프로젝트 정보

| Item | Value |
|---|---|
| Repository | https://github.com/JongminChoi98/local-document-intelligence |
| Initial Version | v0.1.0 |
| Baseline Commit | 3b70615 |
| Default Branch | main |
| Language | Python 3.12.16 |
| Package Manager | uv |
| LLM Runtime | Ollama |
| Generation Model | qwen3.5:4b-q4_K_M |
| Embedding Model | bge-m3:567m |
| Embedding Dimension | 1024 |
| Vector Database | ChromaDB |
| Chat Database | SQLite |
| Web Framework | Streamlit |
| Default API Address | 127.0.0.1:11434 |
| Default Web Address | 127.0.0.1:8501 |

현재 열린 프로젝트의 실제 버전 및 Commit을 확인한다.

v0.1.0 이후의 버전을 검증하는 경우
실제 소스 코드와 문서를 기준으로 테스트 범위를 갱신한다.

기존 브랜치나 버전을 임의로 변경하지 않는다.

## 3. 작업 원칙

1. README.md 및 관련 개발자 문서를 먼저 확인한다.
2. 실제 구현 코드와 문서에 명시된 기능을 대조한다.
3. 가능하면 별도의 Git Worktree 또는 임시 Clone에서 검증한다.
4. 기존 프로젝트의 storage/를 테스트에 사용하지 않는다.
5. 실제 회사 문서 및 개인정보를 사용하지 않는다.
6. 합성 테스트 데이터만 사용한다.
7. 기존 데이터베이스를 초기화하거나 삭제하지 않는다.
8. 기존 실행 중인 서비스를 임의로 종료하지 않는다.
9. 기존 애플리케이션 소스 코드를 수정하지 않는다.
10. 테스트 코드, Fixture 및 보고서만 별도로 생성할 수 있다.
11. 오류가 발생해도 가능한 나머지 테스트는 계속 진행한다.
12. 실제 실행하지 않은 기능을 PASS로 판정하지 않는다.
13. Mock 테스트와 실제 연동 테스트를 구분한다.
14. Git Commit, Push, Tag 변경 및 Release 생성은 수행하지 않는다.
15. 외부 API에 테스트 문서나 회사 자료를 전송하지 않는다.
16. 사용자 동의 없이 대용량 모델을 추가 다운로드하지 않는다.
17. 시스템 설정 변경이나 관리자 권한이 필요한 작업은 임의로 수행하지 않는다.
18. 테스트를 실제로 실행하고 결과를 보고한다.

현재 구현되지 않은 기능은 알려진 제한 사항으로 분류한다.

테스트 과정에서 발견된 결함을 자동으로 수정하지 말고
재현 절차 및 수정 권장 사항을 기록한다.

## 4. 사전 분석

다음 문서와 모듈을 확인한다.

### Documentation

- README.md
- docs/developer-overview.md
- docs/developer-setup.md
- docs/architecture.md
- docs/roadmap.md

### Application Modules

- app.py
- chat_store.py
- parsers/
- preprocessors/
- embeddings/
- vector_store/
- retrieval/
- llm/
- rag/
- ingestion/
- config/
- .streamlit/config.toml
- pyproject.toml
- uv.lock
- .gitignore

문서에 작성된 내용과 실제 구현이 다른 경우
해당 차이를 기록한다.

실제 코드를 기준으로 테스트 케이스를 구체화한다.

## 5. 테스트 환경 구성

### 5.1 Environment Verification

다음 항목을 확인한다.

- OS 및 WSL 환경
- Git 버전
- 현재 Branch 및 Commit
- Working Tree 상태
- Python 버전
- uv 버전
- 의존성 설치 상태
- uv.lock 일치 여부
- Ollama 버전 및 실행 상태
- 설치된 AI 모델 및 모델 ID
- GPU 인식 여부
- GPU VRAM
- 시스템 RAM
- 저장 공간
- Streamlit 설정
- 사용 중인 네트워크 포트

### 5.2 Isolation

별도의 테스트 작업공간을 구성한다.

테스트 작업공간에는 기존 storage/ 데이터를 복사하지 않는다.

테스트용 애플리케이션, 합성 문서,
ChromaDB 및 SQLite를 독립적으로 관리한다.

기존 Streamlit 서버와 포트 충돌이 발생하면
8502 등 사용 가능한 별도의 Loopback 포트를 사용한다.

Ollama는 기존 로컬 서비스를 사용할 수 있지만
서비스의 설정이나 설치 모델을 임의로 변경하지 않는다.

테스트 종료 시 QA 과정에서 시작한 프로세스만 종료한다.

### 5.3 Installation Verification

가능한 범위에서 다음을 실제로 검증한다.

- Repository Clone 또는 Worktree 생성
- uv sync --locked
- Python 모듈 Import
- Python 소스 문법 검사
- Ollama API 연결
- Embedding 생성
- LLM 답변 생성
- Streamlit 서버 실행

신규 PC에 WSL이나 Ollama를 처음 설치하는 과정까지
검증할 수 없다면 해당 항목을 NOT TESTED로 기록한다.

## 6. Synthetic Test Data

### 6.1 Normal Test Documents

현재 preprocessors/maintenance.py의
FIELD_MAP 및 EXPECTED_LABELS를 확인한다.

지원하는 시트명과 셀 배치를 정확히 재현한
합성 XLSX 문서를 최소 5개 생성한다.

| Document ID | Vehicle | Symptom | Cause | Repair |
|---|---|---|---|---|
| TEST-AS-001 | 테스트 차량 1호 | 간헐적 전원 차단 | 릴레이 접점 노후화 확인 | 24V 100A 릴레이 교체 |
| TEST-AS-002 | 테스트 차량 2호 | 전원단자대 과열 | 접촉저항 증가로 추정 | 단자대 및 4AWG 배선 교체 |
| TEST-AS-003 | 테스트 차량 3호 | 카메라 영상 끊김 | 커넥터 접촉 불량 | 커넥터 재체결 |
| TEST-AS-004 | 테스트 차량 4호 | 차량 내부 누수 | 실링 부위 손상 | 실링 보강 |
| TEST-AS-005 | 테스트 차량 5호 | 제동 시 소음 | 브레이크 패드 마모 | 브레이크 패드 교체 |

각 문서에는 구분 가능한 다음 정보를 포함한다.

- 문서번호
- 작성일
- 접수일
- 조치일
- 고객명
- 위치
- 차량
- 담당 부서
- 작업 시간
- 고장 유형
- 원인 유형
- 조치 유형
- 부품 유형
- 고객 접수 내용
- 현장 확인 내용
- 발생 원인
- 조치 내용
- 조치 부품
- 재발 방지 내용

기대 정답 및 원본 데이터를 JSON으로 별도 저장한다.

실제 고객사 이름, 실제 차량 번호 및 개인정보는
사용하지 않는다.

### 6.2 Exceptional Test Documents

다음 예외 테스트 데이터를 추가 생성한다.

- 잘못된 시트명
- 잘못된 셀 배치
- 문서번호 누락
- 일부 선택 필드 누락
- 동일 문서번호를 가진 수정본
- 다른 시트에 검색 방해용 데이터가 있는 Excel
- 손상된 XLSX
- 허용하지 않는 파일 확장자
- 최대 업로드 크기를 초과하는 테스트 입력
- 텍스트 기반 PDF
- 추출 가능한 텍스트가 없는 PDF

파일 크기 제한 테스트는 불필요하게
대량의 파일을 생성하지 않는 방식으로 수행한다.

## 7. Functional Test Matrix

### Group A — Document Parsing

| ID | Test |
|---|---|
| A-01 | 정상 XLSX 파일 열기 |
| A-02 | 지정된 정비 기록 시트 선택 |
| A-03 | 셀 주소 및 값 추출 |
| A-04 | 빈 셀 처리 |
| A-05 | 다른 시트의 데이터 제외 |
| A-06 | 지원하지 않는 시트 처리 |
| A-07 | 손상된 XLSX 처리 |
| A-08 | PDF 페이지별 텍스트 추출 |
| A-09 | 텍스트 없는 PDF 처리 |

PDF는 현재 텍스트 추출 기능만 검증한다.

PDF를 Vector DB에 등록하거나 RAG 검색에 사용하는
기능은 현재 구현 범위를 확인하여 판정한다.

### Group B — Data Normalization

| ID | Test |
|---|---|
| B-01 | 19개 정비 필드 매핑 |
| B-02 | 고객명 및 차량 정보 정확성 |
| B-03 | 고객 접수 내용과 현장 확인 내용 구분 |
| B-04 | 발생 원인과 조치 내용 구분 |
| B-05 | 선택 필드 누락 처리 |
| B-06 | 문서번호 누락 처리 |
| B-07 | 지원하지 않는 양식 거부 |
| B-08 | 원본 파일 및 셀 주소 보존 |

고정 양식이 아닌 문서를 정상적으로 거부하는 경우
해당 예외 처리 테스트는 PASS로 판정한다.

범용 전처리 미구현 자체는 알려진 제한 사항이다.

### Group C — Embedding

| ID | Test |
|---|---|
| C-01 | Ollama Embedding API 연결 |
| C-02 | 단일 텍스트 Embedding |
| C-03 | 다중 텍스트 Embedding |
| C-04 | 1024차원 벡터 확인 |
| C-05 | 문서 Serialization |
| C-06 | 빈 입력 처리 |
| C-07 | 비정상 API 응답 처리 |
| C-08 | Ollama 연결 실패 처리 |

API 예외 테스트는 기존 Ollama 서비스를 종료하지 않고
Mock 또는 독립적인 테스트 설정을 사용한다.

### Group D — ChromaDB

| ID | Test |
|---|---|
| D-01 | Vector DB 초기화 |
| D-02 | Collection 생성 |
| D-03 | 단일 문서 등록 |
| D-04 | 다중 문서 등록 |
| D-05 | 동일 문서번호 Upsert |
| D-06 | 중복 등록 시 문서 수 유지 |
| D-07 | Metadata 저장 및 조회 |
| D-08 | 등록 문서 삭제 |
| D-09 | 삭제된 문서의 검색 제외 |
| D-10 | 프로세스 재실행 후 데이터 유지 |

테스트용 Vector DB에서만 삭제 테스트를 수행한다.

문서 삭제와 원본 파일 삭제는 구분한다.

현재 구현에서 원본 파일 보존이 의도된 동작이라면
원본 파일이 남아 있는 것을 결함으로 판단하지 않는다.

### Group E — Retrieval

| ID | Test |
|---|---|
| E-01 | Dense Search |
| E-02 | Keyword Score 계산 |
| E-03 | Hybrid Search |
| E-04 | RRF 계산 |
| E-05 | 정확한 문서번호 우선 검색 |
| E-06 | Top-K 제한 |
| E-07 | 빈 Vector DB 검색 |
| E-08 | 등록 문서보다 큰 Top-K |
| E-09 | 한국어 의미 기반 검색 |
| E-10 | 부품명 및 부품 사양 검색 |
| E-11 | 다중 문서 관련성 검색 |
| E-12 | 존재하지 않는 문서번호 검색 |
| E-13 | 무관한 질문 검색 결과 분석 |

Dense Search와 Hybrid Search의 결과를 비교한다.

가능하면 다음 지표를 계산한다.

- Hit@1
- Recall@3
- MRR

정답 문서 집합은 테스트 실행 전에 정의한다.

코사인 유사도와 RRF 점수를 구분한다.

정확한 문서번호 우선순위 기능과
정확한 문서번호 필터링을 혼동하지 않는다.

현재 Top-K 방식은 관련성이 낮은 문서도
반환할 수 있으므로 그 영향을 분석한다.

### Group F — LLM and RAG

| ID | Test |
|---|---|
| F-01 | Ollama Chat API 연결 |
| F-02 | 한국어 답변 생성 |
| F-03 | 단일 문서 기반 질의응답 |
| F-04 | 다중 문서 비교 분석 |
| F-05 | 고객명 정확성 |
| F-06 | 차량 정보 정확성 |
| F-07 | 부품 정보 정확성 |
| F-08 | 추정 원인과 확정 원인 구분 |
| F-09 | 원본에 없는 정보에 대한 답변 |
| F-10 | 참조 문서와 답변의 일치 |
| F-11 | 다른 차량 정보 혼합 여부 |
| F-12 | 출력 토큰 제한 처리 |
| F-13 | 응답 시간 및 토큰 수 확인 |

다음 질문을 대표 사례로 활용한다.

1. TEST-AS-001 문서의 고객명과 교체 부품을 알려줘.
2. 테스트 차량 2호의 발생 원인은 확정된 사실인가?
3. 전원 관련 고장 사례를 비교해 줘.
4. 브레이크 패드를 교체한 차량은 무엇인가?
5. 카메라 영상 끊김을 해결하기 위해 어떤 조치를 했어?
6. TEST-AS-001 문서의 정비 비용은 얼마인가?
7. 등록되어 있지 않은 테스트 차량 99호의 정비 이력을 알려줘.

답변은 문자열 완전 일치로 평가하지 않는다.

핵심 사실, 원본 근거, 참조 문서,
정보 혼합 및 Hallucination 여부를 확인한다.

정비 비용 등 원본에 없는 정보를
임의로 생성하면 FAIL로 판정한다.

검색 문서가 존재하더라도 질문과 무관한 정보라면
관련 기록을 확인할 수 없다고 답변해야 한다.

### Group G — Conversational RAG

| ID | Test |
|---|---|
| G-01 | 첫 질문의 Query Rewriting 생략 |
| G-02 | 후속 질문의 이전 차량 정보 유지 |
| G-03 | 이전 문서번호 활용 |
| G-04 | 명시적인 차량 변경 처리 |
| G-05 | 제한된 대화 이력 활용 |
| G-06 | 질문 재구성 실패 처리 |
| G-07 | 재구성 과정의 새로운 사실 생성 여부 |

다음 질문을 동일한 채팅에서 순차적으로 실행한다.

First question:

테스트 차량 2호의 고장 원인이 뭐야?

Follow-up question:

그러면 어떤 부품을 사용했어?

Topic change:

이번에는 테스트 차량 3호의 조치 내용을 알려줘.

재구성된 질문, 검색 결과 및 답변을 함께 비교한다.

이전 차량의 정보가 새로운 차량에 혼합되는지 확인한다.

### Group H — Web Application

| ID | Test |
|---|---|
| H-01 | Streamlit 서버 실행 |
| H-02 | 실제 브라우저 접속 |
| H-03 | 단일 Excel 업로드 |
| H-04 | 다중 Excel 일괄 등록 |
| H-05 | 정상 및 오류 파일 혼합 등록 |
| H-06 | 등록 성공 및 실패 건수 표시 |
| H-07 | 등록 문서 수 갱신 |
| H-08 | 웹 채팅 질의응답 |
| H-09 | Markdown 및 표 출력 |
| H-10 | 참조 문서 표시 |
| H-11 | 원본 Excel 다운로드 |
| H-12 | 다운로드 파일 SHA-256 일치 |
| H-13 | 등록 문서 목록 조회 |
| H-14 | 문서 삭제 확인 |
| H-15 | 삭제 후 문서 수 갱신 |
| H-16 | 삭제된 문서의 검색 제외 |

가능하면 실제 브라우저를 통해 검증한다.

브라우저 접근이 불가능하면
Streamlit AppTest 등 대체 방법을 검토한다.

대체 테스트만으로 확인할 수 없는 브라우저 동작은
NOT TESTED 또는 BLOCKED로 판정한다.

### Group I — Chat History

| ID | Test |
|---|---|
| I-01 | SQLite 초기화 |
| I-02 | 새 채팅 생성 |
| I-03 | 질문 및 답변 저장 |
| I-04 | 첫 질문 기반 제목 생성 |
| I-05 | 이전 채팅 불러오기 |
| I-06 | 브라우저 새로고침 후 채팅 유지 |
| I-07 | 서버 재실행 후 채팅 유지 |
| I-08 | 채팅 제목 변경 |
| I-09 | 채팅 삭제 |
| I-10 | 삭제된 채팅의 메시지 제거 |
| I-11 | 채팅 간 문맥 격리 |
| I-12 | 참조 문서 및 답변 Metadata 보존 |

테스트용 SQLite DB에서만 삭제 테스트를 수행한다.

### Group J — LLM Settings

| ID | Test |
|---|---|
| J-01 | 설치된 모델 목록 조회 |
| J-02 | 생성 모델 및 Embedding 모델 구분 |
| J-03 | 기본 생성 모델 선택 |
| J-04 | Cloud 모델 제외 |
| J-05 | Thinking 설정 전달 |
| J-06 | Context Window 설정 전달 |
| J-07 | Temperature 설정 전달 |
| J-08 | Max Output Tokens 설정 전달 |
| J-09 | 선택된 모델의 답변 생성 |
| J-10 | Query Rewriting 설정 전달 |
| J-11 | 호환되지 않는 설정 처리 |
| J-12 | 실제 모델 전환 |

실제 API 요청 Payload가 설정값과 일치하는지 확인한다.

API 요청값 전달과 모델의 실제 동작을 구분한다.

추가 생성 모델이 설치되어 있지 않다면
Mock을 사용하여 모델 선택 로직을 검증할 수 있다.

실제 다른 모델을 실행하지 않았다면
J-12는 NOT TESTED로 기록한다.

### Group K — Security and Error Handling

| ID | Test |
|---|---|
| K-01 | storage/의 Git 제외 |
| K-02 | 비밀정보 파일의 Git 제외 |
| K-03 | 원본 파일 접근 경로 검증 |
| K-04 | Path Traversal 방지 |
| K-05 | 허용되지 않는 확장자 처리 |
| K-06 | 업로드 파일 크기 제한 |
| K-07 | 원본 Excel 데이터 보존 |
| K-08 | 등록 실패 시 잔여 파일 확인 |
| K-09 | Ollama 연결 오류 처리 |
| K-10 | 없는 원본 파일 처리 |
| K-11 | 문서 내부 Prompt Injection 대응 |
| K-12 | Loopback 주소 바인딩 |
| K-13 | Ollama Cloud 비활성화 설정 |
| K-14 | 가능한 범위의 외부 네트워크 통신 확인 |

보안 테스트는 격리된 테스트 환경에서만 수행한다.

Prompt Injection 테스트에는
무해한 합성 문자열만 사용한다.

실제 외부 전송을 유발하거나
민감정보 접근을 시도하지 않는다.

기존 네트워크 설정이나 방화벽을
임의로 변경하지 않는다.

완전한 오프라인 동작을 확인하지 못한 경우
외부 통신이 없다고 단정하지 않는다.

인증, RBAC 및 Audit Logging이 현재 미구현이라면
알려진 제한 사항으로 기록한다.

## 8. Performance Measurement

다음 항목을 가능한 범위에서 실제 측정한다.

| Metric | Description |
|---|---|
| Parsing Time | 문서 추출 시간 |
| Normalization Time | 데이터 구조화 시간 |
| Embedding Time | 문서 및 질문 벡터 생성 시간 |
| Ingestion Time | 전체 문서 등록 시간 |
| Retrieval Time | 검색 처리 시간 |
| Query Rewrite Time | 질문 재구성 시간 |
| Generation Time | LLM 답변 생성 시간 |
| Total Response Time | 전체 질의응답 시간 |
| Prompt Tokens | 입력 토큰 수 |
| Completion Tokens | 출력 토큰 수 |
| GPU Memory | GPU VRAM 사용량 |
| System Memory | 시스템 RAM 사용량 |

대표 측정 시나리오:

- 단일 문서 등록
- 다중 문서 일괄 등록
- 단일 문서 질의응답
- 다중 문서 비교 질문
- 대화 문맥 기반 후속 질문

가능하면 Cold Start와 Warm Start를 구분한다.

측정에 사용한 모델, 장비, Context Window,
Thinking 및 Temperature 설정을 함께 기록한다.

측정 가능한 항목만 기록하고
측정하지 않은 수치를 임의로 추정하지 않는다.

불필요하게 동일한 테스트를 반복하지 않는다.

성능 기준이 사전에 정의되지 않았다면
응답 시간은 관측값으로 보고하고
임의의 기준을 설정하여 FAIL로 처리하지 않는다.

## 9. Test Result Classification

| Status | Definition |
|---|---|
| PASS | 기대 결과를 실제 실행으로 확인 |
| FAIL | 실제 결과가 기대 결과와 불일치 |
| BLOCKED | 환경 또는 선행 조건으로 수행 불가 |
| NOT TESTED | 실제 검증하지 않음 |
| N/A | 현재 구현 범위에 해당하지 않음 |

모든 테스트에 실제 판정 근거를 기록한다.

다음 검증 방법을 구분하여 기록한다.

- Static Inspection
- Unit Test
- Mock Test
- Integration Test
- Browser E2E Test

Static Inspection만 수행한 항목을
실제 실행 테스트 PASS로 판정하지 않는다.

Mock Test가 성공했더라도 실제 외부 연동은
검증되지 않았을 수 있음을 명시한다.

PASS Rate를 보고할 경우 분모를 명시한다.

실행 테스트 성공률:

PASS / (PASS + FAIL)

전체 테스트 실행 범위:

(PASS + FAIL) / (전체 테스트 - N/A)

BLOCKED와 NOT TESTED를 숨기거나
PASS로 포함하지 않는다.

## 10. Defect Severity

| Severity | Definition |
|---|---|
| Critical | 데이터 손실, 심각한 보안 문제, 전체 시스템 실행 불가 |
| High | 핵심 기능 실패, 업무 판단을 왜곡하는 잘못된 답변 |
| Medium | 일부 기능 오류 또는 사용성 저하 |
| Low | 경미한 UI, 로그 또는 편의성 문제 |

FAIL이 발생하면 재현 가능 여부를 확인한다.

결함마다 다음 항목을 기록한다.

- Defect ID
- 관련 Test ID
- Severity
- 발생 환경
- 재현 절차
- 기대 결과
- 실제 결과
- 발생 빈도
- 관련 파일 및 코드 위치
- 추정 원인
- 수정 권장 사항
- 재검증 필요 여부

추정 원인은 확인된 사실과 구분한다.

동일한 원인으로 여러 테스트가 실패한 경우
하나의 결함으로 연결할 수 있다.

## 11. QA Deliverables

격리된 테스트 작업공간에 다음 결과물을 생성한다.

qa_results/
    QA_TEST_REPORT.md
    QA_TEST_RESULTS.csv
    QA_DEFECT_LIST.md
    environment/
    fixtures/
    scripts/
    evidence/

실제 저장 경로를 최종 보고에 포함한다.

### 11.1 QA_TEST_REPORT.md

다음 내용을 포함한다.

1. Executive Summary
2. 검증 대상 버전 및 Commit
3. 실제 테스트 환경
4. 테스트 범위 및 제외 범위
5. 테스트 데이터 구성
6. 전체 테스트 결과
7. 그룹별 결과
8. 검색 정확도 분석
9. 답변 정확도 분석
10. 성능 측정 결과
11. 발견된 결함
12. 알려진 제한 사항
13. 개선 우선순위
14. 미검증 항목
15. 실제 사내 적용 가능 여부
16. 최종 결론

### 11.2 QA_TEST_RESULTS.csv

다음 컬럼을 포함한다.

Test ID
Category
Description
Expected Result
Actual Result
Status
Verification Method
Duration Seconds
Evidence
Defect ID
Notes

테스트 케이스마다 한 행을 작성한다.

CSV는 UTF-8 형식으로 저장한다.

### 11.3 QA_DEFECT_LIST.md

발견된 결함을 심각도별로 정리한다.

- Critical
- High
- Medium
- Low

실제 결함과 알려진 제한 사항을 분리한다.

결함이 없다면 발견되지 않았다고 기록하되
검증 범위를 벗어난 결함까지 없다고 단정하지 않는다.

### 11.4 Evidence

가능한 범위에서 다음 자료를 보존한다.

- 실제 실행 명령어
- 실행 로그
- 테스트 스크립트
- 합성 테스트 문서
- 기대 정답 데이터
- API 테스트 결과
- 검색 결과
- 모델 답변
- 브라우저 스크린샷
- 파일 해시 검증 결과
- 성능 측정 결과

실제 회사 데이터 및 개인정보는 포함하지 않는다.

## 12. Completion Criteria

다음 조건을 기준으로 작업을 마무리한다.

- 구현된 기능의 실제 실행 테스트 수행
- 기능별 결과 판정 및 증거 기록
- 실패 항목에 대한 재현 절차 작성
- 알려진 제한 사항과 결함 분리
- 미검증 항목 명시
- 테스트 결과 보고서 생성
- 테스트용 프로세스 정리
- 기존 소스 및 사용자 데이터 변경 여부 확인

모든 테스트가 PASS일 필요는 없다.

실패 결과를 숨기거나 테스트 기대값을
실제 결과에 맞추어 변경하지 않는다.

환경 제약으로 진행할 수 없는 테스트는
BLOCKED 또는 NOT TESTED로 기록한다.

기존 운영 데이터의 무결성을 직접 확인하지 못했다면
확인하지 못했다고 명시한다.

## 13. Final Response

최종 결과를 한국어로 보고한다.

다음 내용을 포함한다.

1. 검증 대상 버전 및 Commit
2. 전체 테스트 결과 및 실행 범위
3. 주요 정상 동작 기능
4. Critical 및 High 결함
5. Medium 및 Low 결함
6. 검색 및 답변 정확도 평가
7. 성능 측정 결과
8. 알려진 제한 사항
9. 검증하지 못한 항목
10. 수정 권장 우선순위
11. 실제 사내 적용 가능 여부
12. 생성한 QA 결과물의 실제 경로
13. 기존 소스 및 사용자 데이터 변경 여부

단순히 코드가 정상적으로 보인다는 평가가 아니라
실제 테스트 결과를 근거로 결론을 작성한다.

이제 현재 프로젝트와 실행 환경을 확인한 후
독립적인 통합 QA 검증을 시작해 줘.
