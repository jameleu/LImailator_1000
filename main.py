from selenium import webself.driver
from selenium.webself.driver.common.keys import Keys
import csv
import re


class EmailScraper:
    def __init__(self, driver_path, keywords_path, email_templates):                
        self.email_formats = []
        with open(email_templates, 'r') as file:
            for line in file:
                self.email_formats.append(line.strip())

        # Set the path to your Webself.driver executable
        with open(driver_path, 'r') as file:
            driver_path = file.read().strip()  # Remove leading/trailing whitespaces

    def test_email(self, email):
        self.driver = webself.driver.Chrome(executable_path=self.driver_path)

    def get_emails(self, name):
        emails = []
        name = name.lower()
        first, last = name.split()
        first_i = first[0]
        last_i = last[0]
        for email_struct in self.emails_format:
            curr_email = self.emails_format.format(
                first_name=first,
                last_name=last,
                first_initial=first_i,
                last_initial=last_i
            )
            if self.test_email(curr_email):
                emails.append(curr_email)
        return emails

    def search_based_on_query(self, company, template):
        """Return list of name in query's emails"""
        # Replace "<>" with the inserted string
        final_email_list = []
        result_string = template.replace("<>", company)
        # Open Google in the browser
        self.driver.get("https://www.google.com")

        # Find the search input field using its name attribute value
        search_box = self.driver.find_element("name", "q")

        # Type your search query
        search_box.send_keys(result_string)

        # Press Enter to perform the search
        search_box.send_keys(Keys.RETURN)

        # Wait for some time to allow the search results to load
        self.driver.implicitly_wait(5)

        # Get the search results
        search_result_header = self.driver.find_element_by_css_selector('h3')  # Adjust the selector based on your needs
        name = re.match(r"^\w(?= -)", search_result_header.text)
        emails = self.get_emails(name)
        
        final_email_list.append((name, len(emails), emails))
        with open(f"{company}", 'w', newline='') as file:
            # Create a CSV writer object
            csv_writer = csv.writer(file)
            for row in final_email_list:
                csv_writer.writerow(row)
    def exit_browser(self):
        self.driver.quit()
        
        
def main():
    email_s = EmailScraper(driver_path, email_templates)
    # Read keywords from csv
    keyword_data = {}
    with open(keywords_path, 'r') as csv_file:
        csv_reader = csv.reader(csv_file)
        for row in csv_reader:
            keyword = row[0]  # col 0
            email_data = row[1]  # col 1
            keyword_data[keyword] = email_data
    for keyword, email_struct in keyword_data.items():
        pass
    email_s.exit_browser()

if __name__ == "__main__":
    main()