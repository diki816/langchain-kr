def create_newsletter_graph():
    # logger.info("Creating newsletter graph")
    workflow = StateGraph(State)
    workflow.add_node("editor", edit_newsletter)
    workflow.add_node("search_news", search_keyword_news)
    workflow.add_node("generate_theme", generate_newsletter_theme)
    workflow.add_node("search_sub_themes", search_sub_theme_articles)
    workflow.add_node("aggregate", aggregate_results)

    for i in range(5):
        node_name = f"write_section_{i}"
        workflow.add_node(node_name, lambda s, i=1: write_newsletter_section(s, s['newsletter_theme'].sub_themes[i]))

    workflow.add_edge(START, "search_news")
    workflow.add_edge("search_news", "generate_theme")
    workflow.add_edge("generate_theme", "search_sub_themes")

    for i in range(5):
        workflow.add_edge("search_sub_themes", f"write_section_{i}")
        workflow.add_edge(f"write_section_{i}", "aggregate")

    workflow.add_edge("aggregate", "editor")
    workflow.add_edge("editor", END)
    # logger.info("Newsletter graph is created successfully")

    return workflow.compile()