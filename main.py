import logging
import re
import time
import requests
import csv
from bs4 import BeautifulSoup


if __name__ == '__main__':

    with open('benchmarks.csv', 'w') as benchmarks_file:
        benchmark_header = "job_title,reliability,link,team,median_salary,90th_salary,median_YoY,sample_size\n"
        benchmarks_file.write(benchmark_header)
        print(benchmark_header)

        with open('jobs.csv', 'r', encoding='utf-8-sig') as jobs_file:
            reader = csv.DictReader(jobs_file)
            jobs = list()
            for dictionary in reader:
                jobs.append(dictionary)

        for job in jobs:
            job_page = job.get("Link").strip()
            page = requests.get(job_page)
            page_text = page.text
            soup = BeautifulSoup(page_text, "html.parser")

            try:
                summary_table = soup.find("table", class_='summary')
                median_salary = summary_table.find(string=re.compile("Median annual salary")).parent.find_next("td").string.replace(",", "")
                sample_size = summary_table.find(string=re.compile("Number of salaries quoted")).parent.find_next("td").string.replace(",", "")

                # Get the 90th percentile salary (watching for a random `90` in a `fig` class cell)
                ninetieth_candidates = summary_table.findAll(string="90")
                for candidate in ninetieth_candidates:
                    if not candidate.parent.has_attr("class"):
                        ninetieth_salary = candidate.parent.find_next("td").string.replace(",", "")

                # Get the median YoY chance (watching for a missing row because of a new role)
                median_change_row = summary_table.find(string=re.compile("Median % change year-on-year"))
                if median_change_row:
                    median_change = median_change_row.parent.find_next("td").string
                else:
                    median_change = "-"

                benchmark_row = f"{job.get('Job Title')},{job.get('Reliability')},{job.get('Link')},{job.get('Team')},{median_salary},{ninetieth_salary},{median_change},{sample_size}\n"
                benchmarks_file.write(benchmark_row)
                print(benchmark_row)
            except Exception as e:
                logging.exception(e)
                catch = -1  # this row is a nice place to drop a breakpoint for debug

            time.sleep(1)

        print("</fin>")
