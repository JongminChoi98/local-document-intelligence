# AGENTS.md

## 1. Project Identity

Project: Local Document Intelligence

본 프로젝트는 사내 문서를 기반으로 자연어 검색,
질의응답 및 분석을 수행하는 Local RAG 애플리케이션이다.

첫 번째 적용 대상은 차량 A/S 정비 이력이다.

초기 MVP 기준 버전은 v0.1.0이며,
현재 구현 상태는 실제 소스 코드와 Git 이력을 기준으로 판단한다.

## 2. Repository Documentation

작업 목적에 따라 다음 문서를 참고한다.

| Document | Purpose |
|---|---|
| README.md | 프로젝트 소개 및 진입점 |
| docs/developer-overview.md | 기술 설명 및 설계 근거 |
| docs/developer-setup.md | 개발 환경 구축 및 실행 |
| docs/architecture.md | 시스템 아키텍처 |
| docs/roadmap.md | 향후 개발 계획 |
| prompts/PROJECT_ONBOARDING.md | 프로젝트 인수 및 환경 분석 |
| qa/CODEX_QA_PROMPT.md | 통합 기능 검증 |
| docs/archive/ | 초기 기술 검증 기록 |

Archive 문서는 과거 개발 기록이며
현재 구현 상태를 보증하지 않는다.

문서와 실제 구현이 다르면 차이를 보고한다.

## 3. Technical Context

초기 프로젝트의 주요 기술 구성은 다음과 같다.

- Python 및 uv
- Ollama Local LLM Runtime
- Qwen3.5 Generation Model
- BGE-M3 Embedding Model
- ChromaDB Vector Database
- SQLite Chat History
- openpyxl 및 pypdf
- Dense Search, Keyword Search 및 RRF
- Traditional RAG 및 Conversational RAG
- Streamlit Web Application

현재 버전, 모델 및 의존성은 실제 코드,
pyproject.toml, uv.lock 및 실행 환경에서 확인한다.

기존 개발자의 PC 경로나 하드웨어 사양을
새로운 개발자의 환경에 그대로 적용하지 않는다.

## 4. Working Principles

- 작업 시작 전 프로젝트 루트와 Git 상태를 확인한다.
- 기존 아키텍처와 모듈별 역할을 존중한다.
- 사용자가 요청한 범위에서만 작업한다.
- 확인된 사실과 추정 내용을 구분한다.
- 실제 실행하지 않은 테스트를 PASS로 보고하지 않는다.
- 불필요한 리팩토링과 의존성 추가를 피한다.
- 기존 사용자 변경 사항을 임의로 되돌리지 않는다.
- 환경 설정, 관리자 권한 작업 및 대용량 모델 다운로드는
  사용자 승인 없이 수행하지 않는다.
- Git Commit, Push, Tag 변경 및 Release 생성은
  별도 사용자 승인 없이 수행하지 않는다.

## 5. Development Conventions

- Python 기반의 모듈화된 구조를 유지한다.
- 문서 처리, 검색, LLM 및 UI의 책임을 분리한다.
- 기존 코드 스타일 및 명명 규칙을 따른다.
- 의존성은 uv 및 uv.lock으로 관리한다.
- 소스 코드의 식별자와 Git Commit 메시지는 영어를 사용한다.
- 개발자 보고 및 설명은 기본적으로 한국어를 사용한다.
- 코드 변경 시 관련 문서와 테스트 영향도를 확인한다.

## 6. Data Security

실제 회사 문서 및 사용자 데이터는
테스트용 데이터와 분리해야 한다.

다음 항목을 Git에 포함하거나
승인되지 않은 외부 서비스에 전달하지 않는다.

- 실제 회사 문서
- 개인정보 및 고객 정보
- 사용자 계정 및 비밀번호
- 환경 변수 파일 및 인증정보
- 원본 문서와 Embedding 데이터
- Vector Database 및 SQLite 채팅 이력

프로젝트 분석에는 실제 업무 문서의 내용이 필요하지 않다.

storage/ 및 기타 민감정보 저장 경로의
데이터를 임의로 읽거나 수정하거나 삭제하지 않는다.

기능 검증에는 합성 테스트 데이터를 우선 사용한다.

로컬 실행 설정만으로 완전한 오프라인 동작이나
정보보호 요구사항 충족을 주장하지 않는다.

## 7. Task Workflows

### Project Onboarding

프로젝트를 처음 인수하거나 현재 상태를 파악하는 경우
prompts/PROJECT_ONBOARDING.md를 따른다.

이 단계는 읽기 전용 분석 및 보고를 수행한다.

### Environment Setup

개발 환경을 구축하는 경우
docs/developer-setup.md를 참고한다.

현재 환경과 기존 설치 상태를 먼저 확인하고
필요한 변경 사항을 사용자에게 설명한다.

### Integration QA

전체 기능을 검증하는 경우
qa/CODEX_QA_PROMPT.md를 따른다.

기존 운영 데이터와 분리된 환경에서
합성 테스트 데이터를 이용하여 검증한다.

QA 단계에서는 애플리케이션 결함을 발견하더라도
사용자 승인 없이 수정하지 않는다.

### Feature Development

신규 기능을 개발하거나 기존 기능을 수정하는 경우
관련 소스 코드와 docs/roadmap.md를 확인한다.

변경 범위와 검증 방법을 정리한 후
사용자가 요청한 작업을 수행한다.

## 8. Completion Reporting

작업 완료 후 다음 사항을 보고한다.

- 수행한 작업
- 변경된 파일
- 실제 검증 결과
- 발견된 문제
- 미검증 사항 및 제한 사항
- 다음 권장 작업

작업 범위를 벗어난 후속 작업을 자동으로 시작하지 않는다.
