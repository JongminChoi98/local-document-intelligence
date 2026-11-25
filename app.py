import streamlit as st

from rag.pipeline import ask
from ingestion.pipeline import ingest_excel
from llm.ollama import LLM_MODEL
from embeddings.ollama import EMBEDDING_MODEL
from vector_store.chroma import get_collection


st.set_page_config(
    page_title="A/S Intelligence",
    layout="wide",
)

if "messages" not in st.session_state:
    st.session_state.messages = []


def render_answer(result: dict):
    st.markdown(result["answer"])

    if result["sources"]:
        with st.expander("참조 문서"):
            for item in result["sources"]:
                st.text(
                    f"{item['reference']} "
                    f"{item['document_id']}"
                )
                st.text(f"파일: {item['source']['file']}")
                st.text(f"시트: {item['source']['sheet']}")
                st.text(f"유사도: {item['similarity']:.4f}")
                st.divider()

    st.caption(
        f"검색: {result['retrieval_seconds']:.2f}초 | "
        f"생성: {result['generation_seconds']:.2f}초 | "
        f"전체: {result['total_seconds']:.2f}초"
    )


with st.sidebar:
    st.header("A/S Intelligence")
    st.caption("Local Document Intelligence")

    st.divider()
    st.subheader("시스템 정보")

    st.caption("LLM")
    st.code(LLM_MODEL)

    st.caption("Embedding Model")
    st.code(EMBEDDING_MODEL)


    st.divider()
    st.subheader("문서 등록")

    with st.form("document_upload", clear_on_submit=True):
        uploaded_file = st.file_uploader(
            "A/S Excel 일지",
            type=["xlsx"],
        )

        st.caption("동일한 문서번호는 기존 기록을 갱신합니다.")

        submitted = st.form_submit_button("문서 등록")

    if submitted:
        if uploaded_file is None:
            st.warning("Excel 파일을 선택하세요.")
        else:
            with st.spinner("문서 분석 및 등록 중..."):
                try:
                    result = ingest_excel(
                        uploaded_file.name,
                        uploaded_file.getvalue(),
                    )

                except Exception as error:
                    st.error(
                        f"등록 실패: {type(error).__name__}"
                    )

                else:
                    st.success(
                        f"등록 완료: {result['document_id']}"
                    )

    st.metric(
        "등록된 정비 기록",
        get_collection().count(),
    )

    st.divider()

    if st.button("채팅 초기화"):
        st.session_state.messages = []

    st.caption("Local RAG Prototype v0.1.0")


st.title("A/S 정비 이력 질의응답")

st.caption(
    "등록된 차량 A/S 정비 기록을 검색하고 "
    "관련 문서를 근거로 답변합니다."
)

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        if message["role"] == "user":
            st.text(message["content"])
        else:
            render_answer(message["result"])


question = st.chat_input(
    "A/S 정비 이력에 대해 질문하세요.",
    max_chars=2000,
)

if question and question.strip():
    st.session_state.messages.append({
        "role": "user",
        "content": question,
    })

    with st.chat_message("user"):
        st.text(question)

    with st.chat_message("assistant"):
        with st.spinner("정비 기록 검색 및 답변 생성 중..."):
            try:
                result = ask(question, top_k=3)

            except Exception as error:
                st.error(
                    f"처리 중 오류가 발생했습니다: "
                    f"{type(error).__name__}"
                )

            else:
                render_answer(result)

                st.session_state.messages.append({
                    "role": "assistant",
                    "result": result,
                })
