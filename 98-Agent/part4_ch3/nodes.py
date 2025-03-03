
import asyncio
from typing import Dict
from state import State
from tools import search_recent_news, search_news_for_subtheme

from langchain_core.messages import HumanMessage
from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI
from dotenv import load_dotenv
from models import NewsletterThemeOutput

load_dotenv()

llm = ChatOpenAI(model="gpt-4o-mini", temperature=1)
newsletter_generator = ChatOpenAI(model="gpt-4o-mini", temperature=1, max_tokens=8192)

def search_keyword_news(state: State) -> State:
    keyword = state['keyword']
    article_titles = search_recent_news(keyword)
    return {'article_titles':article_titles}

def subtheme_generator(state: State) -> State:
    article_titles = state['article_titles']
    
    structured_llm_newsletter = llm.with_structured_output(NewsletterThemeOutput)

    system = """
    You are an expert helping to create a newsletter.
    Based on a list of article titles provided, your task is to choose a single,
    specific newsletter theme framed as a clear, detailed question that grabs the reader's attention.

    In addition, generate 5 sub-themes that are highly specific, researchable news items or insights under the main theme.
    Ensure these sub-themes reflect the lastest trends in the field and frame them as compelling news topics.

    The output should be formatedd as:
    - Main theme (in question form)
    - 3-5 sub-themes (detailed and focused on emerging trends, technologies, or insights)

    The sub-themes should create a clear direction for the newsletter, avoiding broad, generic topics.
    All your output should be in English
    """

    theme_prompt = ChatPromptTemplate.from_messages(
        [
            ("system", system),
            ("human", "Article titles: \n\n {article_titles}"),
        ]
    )
    subtheme_chain = theme_prompt | structured_llm_newsletter
    newsletter_theme = subtheme_chain.invoke({"article_titles": "\n".join(article_titles)})
    newsletter_theme.sub_themes = newsletter_theme.sub_themes[:5]
    return {'newsletter_theme': newsletter_theme}


async def search_sub_theme_articles(state: State) -> State:
    subthemes = state['newsletter_theme'].sub_themes
    results = await asyncio.gather(*[search_news_for_subtheme(subtheme) for subtheme in subthemes])
    sub_theme_articles = {}
    for result in results:
        sub_theme_articles.update(result)

    if not any(sub_theme_articles.values()):
        raise ValueError("No articles found for any sub-theme. Please try a different keyword.")
    
    return {"sub_theme_articles": sub_theme_articles}
    
async def write_newsletter_section_async(state: State, sub_theme: str) -> Dict:
    articles = state['sub_theme_articles'][sub_theme]

    article_references = "\n".join(
        [f"Title: {article['title']} \nContent: {article['raw_content']}..."
        for article in articles]
    )

    prompt = f"""
    Write a newletter section for the sub-theme: "{sub_theme}".

    Use the following articles as reference and include relevant points from both their titles, images, and content:
    <article>
    {article_references}
    </article>
    Summarize the key points and trends related to this sub-theme, and ensure you reference the images where they add value to the discussion.
    Keepy the tone engaging and informative for newsletter readers. You should write in Korean.
    """

    messages = [HumanMessage(content=prompt)]
    response = await llm.ainvoke(messages)
    return {"results": {sub_theme: response.content}}

def write_newsletter_section(state: State, sub_theme: str) -> Dict:
    return asyncio.run(write_newsletter_section_async(state, sub_theme))

def aggregate_results(state: State) -> State:
    theme = state['newsletter_theme'].theme
    combined_newsletter = f"# {theme}\n\n"
    
    for sub_theme, content in state['results'].items():
        combined_newsletter += f"## {sub_theme}\n{content}\n\n"
    return {"messages": [HumanMessage(content=f"Generated Newsletter:\n\n{combined_newsletter}")]}

async def edit_newsletter(state: State) -> State:
    theme = state['newsletter_theme'].theme
    combined_newsletter = state['messages'][-1].content

    prompt = f"""
    As an expert editor, review and refine the following newsletter on the theme: {theme}

    {combined_newsletter}

    Please ensure:
    0. Title should be in question form. subtitles are free to make question or just sentence.
    1. Consistent tone and style throughout the newsletter
    2. Smooth transitions between sections
    3. Proper formatting and structure
    4. Clear and enggaging languages
    5. No gramatical or spelling errors

    Provide the edited version of the newsletter.
    """
    
    messages = [HumanMessage(content=prompt)]
    response = await newsletter_generator.ainvoke(messages)

    return {"messages": [HumanMessage(content=f"Edited Newsletter:\n\n{response.content}")]}
