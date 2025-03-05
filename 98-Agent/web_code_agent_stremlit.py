from dotenv import load_dotenv
import streamlit as st
from langchain_core.messages import AIMessage, HumanMessage

from web_code_agent_graph import graph

load_dotenv()

st.title("깃헙 통합 검색 에이전트")
st.markdown("#### Intelligent Research Assistant")

if "messages" not in st.session_state:
    st.session_state["messages"] = [
        AIMessage(content="안녕하세요! 코드 작성을 도와드리는 AI 어시스턴드 입니다.")
    ]

for msg in st.session_state.messages:
    if isinstance(msg, AIMessage):
        st.chat_message("assistant").write(msg.content)
    if isinstance(msg, HumanMessage):
        st.chat_message("user").write(msg.content)

if prompt := st.chat_input():
    st.session_state.messages.append(HumanMessage(content=prompt))
    st.chat_message("user").write(prompt)

    with st.chat_message("assistant"):
        initial_state = {
            "question": prompt,
            "ceretainty_score": 0,
            "search_results": [],
            "web_score": "",
            "repo_name": "",
            "generation": ""
        }

        try:
            for step in graph.stream( initial_state,
                config={
                    "recursion_limit": 100,
                }):
                for node_name, state in step.items():
                    # 확실성 점수
                    if 'certainty_score' in state:
                        with st.status("제가 스스로 답할 수 있는지 고민 중입니다.", expanded=True) as status:
                            st.write(f"LLM의 확신 정도: {state['certainty_score']}")
                            if state['certainty_score'] == 100:
                                status.update(label="이건 확실히 알곘네요! 제가 답변해볼게요!", status="complete", expanded=False)
                            else:
                                status.update(label="이건 제가 잘 모르는 겁니다. 웹검색을 시작합니다.", status="complete", expanded=False)
                    if 'web_score' in state:
                        if state['web_score'] == "yes":
                            with st.status("웹에서 검색해볼게요.", expanded=True) as status:
                                status.update(label="오! 웹 검색 결과 유용한 정보가 있었어요.", status="complete", expanded=False)
                            with st.expander("웹 검색결과"):
                                for i, results in enumerate(state['search_results'], 1):
                                    st.write(f"출처 {i}: URL: {results['url']}")
                                    # st.write(results['text'])
                        else:
                            with st.status("웹 검색으로 해결 가능한지 확인 중...", expanded=False) as status:
                                status.update(label="이건 제가 잘 모르는 겁니다. 웹검색을 시작합니다.", status="complete", expanded=False)
                    if 'repo_name' in state:
                        with st.expander("GitHub 검색 결과"):
                            st.write(f"참고한 GitHub 저장소: {state['repo_name']}")
                            
                    if 'generation' in state:
                        st.session_state.messages.append(AIMessage(cntent=state['generation']))
                        st.markdown(state['generation'])
                    
        except Exception as e:
            st.error(f"오류가 발생했습니다: {str(e)}")

if st.sidebar.button("대화 기록 지우기"):
    st.session_state.messages = [
        AIMessage(content="안녕하세요! 코드 작성을 도와드리는 AI 어시스턴드 입니다.")
    ]
    st.rerun()
