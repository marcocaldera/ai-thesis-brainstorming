import pandas as pd
from functions import set_browser


class InstaDataset:

    #     def __init__(self):
    #         self.

    def outline_user(self, user):
        browser = set_browser()
        url = "https://www.instagram.com/" + user
        print(url)
        # browser.get(url)
        # html = browser.page_source
        # soup = BeautifulSoup(html, 'html.parser')
        # body = soup.find('body')
        # script_tag = body.find('script')
        # raw_string = script_tag.text.strip().replace('window._sharedData =', '').replace(';', '')
        # load = json.loads(raw_string)
        # # with open('data.json', 'w') as f:
        # #     json.dump(load, f)
        #
        # metrics = load['entry_data']['ProfilePage'][0]['graphql']['user']
        # print(metrics)


# username_list = pd.read_csv('influencer.csv', header=None)
username_list = pd.read_csv('influencer.csv')
print(username_list)

scraping_user = InstaDataset()
for index, user in username_list.iterrows():
    # print(row[1])
    scraping_user.outline_user(user[1])
    break
