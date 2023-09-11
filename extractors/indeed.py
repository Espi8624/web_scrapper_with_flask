
from bs4 import BeautifulSoup
from selenium import webdriver

# def get_page_count(keyword):
#     base_url = "https://kr.indeed.com/jobs"

#     browser = webdriver.Chrome()
#     browser.get(f"{base_url}?q={keyword}")

#     soup = BeautifulSoup(browser.page_source, "html.parser")
#     pagination = soup.find("nav", class_="ecydgvn0")

#     if pagination == None:
#         return 1
#     pages = pagination.find_all("div", recursive=False)
#     count = len(pages)
#     if count >= 5:
#         return 5
#     else:
#         return count
    
def get_page_count(keyword):
    browser = webdriver.Chrome()
    base_url = "https://jp.indeed.com/jobs"
    
    count = 0
    front_checker = ""
    back_checker = ""
    is_run = True
    while is_run:
        front_checker = back_checker
        final_url = f"{base_url}?q={keyword}&start={count}"
        browser.get(final_url)
        soup = BeautifulSoup(browser.page_source, "html.parser")
        pagination = soup.find("nav", class_="ecydgvn0")
        back_checker = pagination
        if count == 0:
            count = 10
        # limit page 10
        else:
            count +=10
            if front_checker == back_checker or count == 100:
                is_run = False
    return int(count/10) + 1

def extract_indeed_jobs(keyword):
    browser = webdriver.Chrome()
    results = []

    pages = get_page_count(keyword)
    print("Found", pages, "pages")
    for page in range(pages):
        base_url = "https://jp.indeed.com/jobs"
        final_url = f"{base_url}?q={keyword}&start={page*10}"
        print("Requesting", final_url)
        browser.get(final_url)
        soup = BeautifulSoup(browser.page_source, "html.parser")
        job_list = soup.find("ul",class_="css-zu9cdh")
        # print("job_list? ",job_list)
        jobs = job_list.find_all('li', recursive=False)

        for job in jobs:
            zone = job.find("div", class_="mosaic-zone")
            if zone == None:
                anchor = job.select_one("h2 a")
                title = anchor['aria-label']
                link = anchor['href']
                company = job.find("span", class_="companyName")
                region = job.find("div", class_="companyLocation")
                job_data = {
                    'link':f"https://jp.indeed.com{link}",
                    'company':company.string,
                    'region':region.string,
                    'position':title,
                }
                results.append(job_data)
            
    return results