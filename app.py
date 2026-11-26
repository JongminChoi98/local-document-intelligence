import streamlit as st

from chat_store import (
    init_db,
    create_chat,
    list_chats,
    load_messages,
    append_message,
    rename_chat,
    delete_chat,
)

from rag.conversation import ask_conversation
from vector_store.source_files import get_source_file
from ingestion.pipeline import ingest_excel
from llm.settings import (
    DEFAULT_MODEL,
    GenerationSettings,
    list_generation_models,
)
from embeddings.ollama import EMBEDDING_MODEL
from vector_store.chroma import get_collection
from vector_store.management import list_documents, delete_document


st.set_page_config(
    page_title="A/S Intelligence",
    layout="wide",
)

init_db()

chats = list_chats()
chat_ids = [chat["id"] for chat in chats]

if st.session_state.get("chat_id") not in chat_ids:
    st.session_state.chat_id = (
        chat_ids[0] if chat_ids else create_chat()
    )

st.session_state.messages = load_messages(
    st.session_state.chat_id
)


def select_chat():
    st.session_state.chat_id = st.session_state.chat_picker


def render_chat_manager():
    if st.button("새 채팅"):
        st.session_state.chat_id = create_chat()
        st.rerun()

    chats = list_chats()
    titles = {chat["id"]: chat["title"] for chat in chats}

    chat_id = st.session_state.chat_id
    st.session_state.chat_picker = chat_id

    st.selectbox(
        "채팅 목록",
        options=list(titles),
        format_func=lambda value: titles[value],
        key="chat_picker",
        on_change=select_chat,
    )

    with st.expander("현재 채팅 관리"):
        title = st.text_input(
            "채팅 제목",
            value=titles[chat_id],
            key=f"title_{chat_id}_{titles[chat_id]}",
        )

        if st.button("제목 변경"):
            if title.strip():
                rename_chat(chat_id, title)
                st.rerun()
            else:
                st.warning("제목을 입력하세요.")

        confirmed = st.checkbox(
            "현재 채팅 삭제에 동의합니다.",
            key=f"delete_chat_{chat_id}",
        )

        if st.button("채팅 삭제", disabled=not confirmed):
            delete_chat(chat_id)

            remaining = list_chats()
            st.session_state.chat_id = (
                remaining[0]["id"]
                if remaining else create_chat()
            )

            st.rerun()


@st.cache_data(ttl=30)
def available_models():
    return list_generation_models()


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

    if result.get("model"):
        st.caption(f"Model: {result['model']}")

    if result.get("done_reason") == "length":
        st.warning("생성 길이 제한에 도달했습니다.")

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

    if result.get("rewrite_status") == "fallback_original":
        st.caption(
            "질문 재구성 실패로 원래 질문의 문서번호를 사용했습니다."
        )

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
    st.subheader("채팅 관리")
    render_chat_manager()

    st.divider()
    st.subheader("시스템 정보")

    st.subheader("LLM 설정")

    try:
        models = available_models()
    except Exception:
        st.error("Ollama 모델 목록을 조회할 수 없습니다.")
        st.stop()

    if not models:
        st.error("사용 가능한 생성 모델이 없습니다.")
        st.stop()

    names = list(models)

    selected_model = st.selectbox(
        "생성 모델",
        options=names,
        index=(
            names.index(DEFAULT_MODEL)
            if DEFAULT_MODEL in names else 0
        ),
    )

    think = None

    if "thinking" in models[selected_model]:
        if selected_model == DEFAULT_MODEL:
            think = st.checkbox(
                "Thinking 활성화", value=False
            )
        else:
            think = st.selectbox(
                "Thinking",
                options=[None, False, True],
                format_func=lambda value: {
                    None: "모델 기본값",
                    False: "OFF",
                    True: "ON",
                }[value],
                key=f"thinking_{selected_model}",
            )

    with st.expander("고급 추론 설정"):
        num_ctx = st.selectbox(
            "Context Window",
            options=[4096, 8192, 16384],
            index=2,
        )

        temperature = st.slider(
            "Temperature",
            min_value=0.0,
            max_value=1.0,
            value=0.1,
            step=0.1,
        )

        num_predict = st.selectbox(
            "Max Output Tokens",
            options=[512, 1024, 2048],
            index=1,
        )

    generation_settings = GenerationSettings(
        model=selected_model,
        think=think,
        num_ctx=num_ctx,
        temperature=temperature,
        num_predict=num_predict,
    )

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
    user_message = {
        "role": "user",
        "content": question,
    }

    append_message(
        st.session_state.chat_id,
        user_message,
    )

    st.session_state.messages.append(user_message)

    with st.chat_message("user"):
        st.text(question)

    with st.chat_message("assistant"):
        with st.spinner("정비 기록 검색 및 답변 생성 중..."):
            try:
                result = ask_conversation(
                    question,
                    st.session_state.messages[:-1],
                    top_k=3,
                    settings=generation_settings,
                )

            except Exception as error:
                st.error(
                    f"처리 중 오류가 발생했습니다: "
                    f"{type(error).__name__}"
                )

            else:
                render_answer(result, len(st.session_state.messages))

                assistant_message = {
                    "role": "assistant",
                    "result": result,
                }

                append_message(
                    st.session_state.chat_id,
                    assistant_message,
                )

                st.session_state.messages.append(
                    assistant_message
                )

                st.rerun()
