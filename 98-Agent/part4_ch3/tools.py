import asyncio
from typing import Dict, List, TypedDict, Annotated
from tavily import AsyncTavilyClient

async_tavily_client = AsyncTavilyClient(api_key="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")

from tavily import TavilyClient
import os
from langchain_core.tools import tool

tavily_client = TavilyClient()

def search_recent_news(keyword):
    """
    This tool interacts with the Tavily AI API to search for recent news articles related to a given keyword.

    Args:
        keyword (str): The keyword or phrase to search for in the news articles.
    
    Returns:
        list:
            A list of titles, each containing up to 10 of the most recent news articles related to the keyword.
            If the content of news articles smilar with others, replace it with new article.
            - 'title' (str): The title of the news article.
    
    Example:
        response = search_news("OpenAI")
        # Returns a list of news articles published in the last day related to OpenAI.
    """
    article_info = []

    response = tavily_client.search(
        query=keyword,
        max_results=10,
        topic="news",
        days=7
    )

    title_list = [i['title'] for i in response['results']]
    return title_list

async def search_news_for_subtheme(subtheme):

    async_tavily_client = AsyncTavilyClient()
    
    search_params = {
        "query" : subtheme,
        "max_result" : 5,
        "topic" : "news",
        "days" : 3,
        "include_images" : True,
        "include_raw_content" : True,
    }

    try:
        with st.statu(label=f"'{subtheme}'와 관련된 뉴스 검색중...", expanded=True) as status:
            st.markdown(f"'{subtheme}'와 관련된 뉴스를 검색하고 있습니다.")
            response = await async_tavily_client.search(**search_params)
            images = response.get('images', [])
            results = response.get('results', [])

            article_info = []
            for i, result in enumerate(results):
                article_info.append({
                    'title': result['title'],
                    'image_url': images[i] if i < len(images) else "",
                    'raw_content': result.get('raw_content', '')
                })
            
            status.update(
                label=f"'{subtheme}'와 관련된 {len(article_info)}개의 기사를 찾았습니다.",
                state='complete',
                expanded=False,
            )
            return {subtheme: article_info}
    except Exception as e:
        st.error(f"뉴스 검색 중 오류가 발생했습니다: {e}")
        return {subtheme: []}

    article_info = []
    for i, result in enumerate(results):
        article_info.append({
            'title': result['title'],
            'image_url': images[i],
            'raw_content': result['raw_content']
        })
    
    return {subtheme: article_info}

async def search_news_by_subthemes(subthemes):
    # asyncio.gather에서 지속적으로 exception이 일어남
    # results = await asyncio.gather(*[search_news_for_subtheme(subtheme) for subtheme in subthemes])
    search_results = {}
    # for result in results:
    for subtheme in subthemes:
        result = await search_news_for_subtheme(subtheme)
        search_results.update(result)
    
    return search_results