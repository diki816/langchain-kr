import streamlit as st
import asyncio
from graph import create_newsletter_graph


st.title("AI Newsletter Generator")

keyword = st.text_input("Enter a keyword for the newsletter:")
if keyword.strip() =="":
    st.warning("Please enter a valid keyword")
    st.stop()

async def run_graph(inputs):
    graph = create_newsletter_graph()

    status_container = st.container()

    with status_container:
        col1, col2 = st.columns([2,1])
        with col1:
            status_text = st.empty()
        with col2:
            progress_bar = st.progress(0)

        with st.expander("Detailed Progress", expanded=True):
            search_status = st.empty()
            theme_status = st.empty()
            subtheme_status = st.empty()
            write_status = st.empty()
            aggregate_status = st.empty()
            edit_status = st.empty()
    step = 0
    total_steps = 10
    try:
        async for output in graph.astream(inputs):
            for key, value in output.items():
                step += 1
                progress_bar.progress(step / len(total_steps))
                status_text.text(f"Current step: {key}")
                
                if key == "search_news":
                    search_status.success("Article Search completed")
                elif key == "generate_theme":
                    theme_status.success("Theme generation completed")
                elif key == "search_sub_themes":
                    subtheme_status.success("Sub-theme search completed")
                elif key == "write_section":
                    write_status.success("Section {key[-1]} writing completed")
                elif key == "aggregate":
                    aggregate_status.success("Newsletter aggregation completed")
                    with st.expander("Draft Newsletter", expanded=False):
                        st.markdown(value['messages'][0].content)
                elif key == "editor":
                    edit_status.success("Final editing completed")
                    st.markdown("## Final Newsletter")
                    st.markdown(value['messages'][0].content)
            status_text.success("Newsletter generation completed!")
    except Exception as e:
        status_text.error(f"Newsletter generation failed.")
        with st.expander("Error Details"):
            st.error(f"An error occured: {str(e)}")
            import traceback
            st.code(traceback.format_exc())
if st.button("Generate Newsletter"):
    inputs = {"keyword":keyword}
    asyncio.run(run_graph(inputs))