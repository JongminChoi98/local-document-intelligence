import streamlit as st

from rag.conversation import ask_conversation
from vector_store.source_files import get_source_file
from ingestion.pipeline import ingest_excel
from llm.ollama import LLM_MODEL
from embeddings.ollama import EMBEDDING_MODEL
from vector_store.chroma import get_collection
from vector_store.management import list_documents, delete_document


st.set_page_config(
    page_title="A/S Intelligence",
    layout="wide",
)

if "messages" not in st.session_state:
    st.session_state.messages = []


def render_download(source_file: str, key: str):
    try:
        file_path = get_source_file(source_file)
        content = file_path.read_bytes()

    except (ValueError, OSError):
        st.caption("원본 파일을 사용할 수 없습니다.")
        return

    st.download_button(
        label="원본 Excel 다운로드",
        data=content,
        file_name=file_path.name,
        mime=(
            "application/vnd.openxmlformats-officedocument"
            ".spreadsheetml.sheet"
        ),
        key=key,
        on_click="ignore",
    )


def render_answer(result: dict, message_key: int):
    st.markdown(result["answer"])

    if result["sources"]:
        with st.expander("참조 문서"):
            for item in result["sources"]:
                st.text(
                    f"{item['reference']} "
                    f"{item['document_id']}"
                )
                source_file = item["source"]["file"]
                st.text(f"파일: {source_file.rsplit('/', 1)[-1]}")
                render_download(
                    source_file,
                    key=f"answer_{message_key}_{item['reference']}",
                )
                st.text(f"시트: {item['source']['sheet']}")
                st.text(f"유사도: {item['similarity']:.4f}")
                st.divider()

    rewritten = result.get("rewritten_question")

    if rewritten and rewritten != result["question"]:
        st.caption(f"재구성된 검색 질문: {rewritten}")

    st.caption(
        f"질문 재구성: {result.get('rewrite_seconds', 0):.2f}초 | "
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
    st.subheader("문서 일괄 등록")

    with st.form("document_upload", clear_on_submit=True):
        uploaded_files = st.file_uploader(
            "A/S Excel 일지",
            type=["xlsx"],
            accept_multiple_files=True,
        )

        st.caption("파일당 최대 20MB")
        st.caption("동일한 문서번호는 기존 기록을 갱신합니다.")

        submitted = st.form_submit_button("일괄 등록")

    if submitted:
        if not uploaded_files:
            st.warning("Excel 파일을 선택하세요.")
        else:
            total = len(uploaded_files)
            success_count = 0
            failed_count = 0

            progress = st.progress(0)
            status = st.empty()

            for index, uploaded_file in enumerate(
                uploaded_files, start=1
            ):
                status.text(
                    f"처리 중: {index}/{total}"
                )

                try:
                    result = ingest_excel(
                        uploaded_file.name,
                        uploaded_file.getvalue(),
                    )

                except Exception as error:
                    failed_count += 1
                    st.error(
                        f"등록 실패: {uploaded_file.name} "
                        f"({type(error).__name__})"
                    )

                else:
                    success_count += 1
                    st.success(
                        f"등록 완료: {result['document_id']}"
                    )

                progress.progress(index / total)

            status.text("일괄 등록 완료")

            st.info(
                f"전체 {total}건 | "
                f"성공 {success_count}건 | "
                f"실패 {failed_count}건"
            )

    st.metric(
        "등록된 정비 기록",
        get_collection().count(),
    )

    st.divider()


    with st.expander("등록 문서 관리"):
        notice = st.session_state.pop("delete_notice", None)

        if notice:
            st.success(notice)

        documents = list_documents()

        if not documents:
            st.info("등록된 문서가 없습니다.")

        else:
            for document in documents:
                st.text(document["document_id"])
                st.caption(document["filename"].rsplit("/", 1)[-1])
                render_download(
                    document["filename"],
                    key=f"library_{document['document_id']}",
                )
                st.divider()

            selected_id = st.selectbox(
                "삭제할 문서",
                options=[
                    document["document_id"]
                    for document in documents
                ],
                index=None,
                placeholder="문서를 선택하세요.",
            )

            if selected_id:
                confirmed = st.checkbox(
                    "검색 대상에서 삭제하는 데 동의합니다.",
                    key=f"confirm_delete_{selected_id}",
                )

                if st.button(
                    "선택 문서 삭제",
                    disabled=not confirmed,
                ):
                    try:
                        delete_document(selected_id)

                    except Exception as error:
                        st.error(
                            f"삭제 실패: {type(error).__name__}"
                        )

                    else:
                        st.session_state.delete_notice = (
                            f"삭제 완료: {selected_id}"
                        )
                        st.rerun()

    if st.button("채팅 초기화"):
        st.session_state.messages = []

    st.caption("Local RAG Prototype v0.1.0")


st.title("A/S 정비 이력 질의응답")

st.caption(
    "등록된 차량 A/S 정비 기록을 검색하고 "
    "관련 문서를 근거로 답변합니다."
)

for index, message in enumerate(st.session_state.messages):
    with st.chat_message(message["role"]):
        if message["role"] == "user":
            st.text(message["content"])
        else:
            render_answer(message["result"], index)


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
                result = ask_conversation(
                    question,
                    st.session_state.messages[:-1],
                    top_k=3,
                )

            except Exception as error:
                st.error(
                    f"처리 중 오류가 발생했습니다: "
                    f"{type(error).__name__}"
                )

            else:
                render_answer(result, len(st.session_state.messages))

                st.session_state.messages.append({
                    "role": "assistant",
                    "result": result,
                })
