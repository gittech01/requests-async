import asyncio
import aiohttp
import multiprocessing

from typing import Dict




async def session_of_requests(session, repo_name:str, func):
    result = dict()
    while True:
        async with session.post(url=url_, json=json_(repo_name, func)) as response:
            value = await response.json()
            result[repo_name] += value

    return result


def url_()-> str:
    return 'https://api.github.com/graphql'


def json_(repo_name: str,func) -> Dict:
    query: str = None
    return {'query':query, 'variables': func(repo_name)}


def vars_(repo_name: str, cursor: str = None):
    return {'name': repo_name, 'cursor': cursor}


async def process_etl_issue(page_data):
    # Realize o ETL para a página de dados aqui
    pass

async def fetch_and_process_issue_pages(start_page, end_page):
    async with aiohttp.ClientSession(trust_env=True) as session:
        tasks = []
        for page_num in range(start_page, end_page + 1):
            url = f"https://api.example.com/issues?page={page_num}"
            tasks.append(session_of_requests(session, url))

        pages_data = await asyncio.gather(*tasks)
        for page_data in pages_data:
            await process_etl_issue(page_data)

def async_worker(start_page, end_page):
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    loop.run_until_complete(fetch_and_process_issue_pages(start_page, end_page))

def main():
    num_processes = 4
    start_page = 1
    end_page = 10
    pool = multiprocessing.Pool(num_processes)
    pool.starmap(async_worker, [(start_page, end_page)] * num_processes)
    pool.close()
    pool.join()

if __name__ == "__main__":
    main()
