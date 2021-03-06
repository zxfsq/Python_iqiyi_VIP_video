import requests
from bs4 import BeautifulSoup
import threading


def video_search_iqiyi(name):
    r = requests.get("https://so.iqiyi.com/so/q_" + name)
    r.encoding = r.apparent_encoding
    # print(r.text)
    soup = BeautifulSoup(r.text, 'html.parser')
    target = soup.find_all("div", class_="qy-search-result-item vertical-pic")
    video_inf = []
    try:
        for div in target:
            video_site = div.find('em', class_='player-name')
            if '爱奇艺' in video_site:
                video_img = div.find('img').attrs['src']
                video_type = div.find('span', class_='item-type').get_text()
                video_name = div.find('a', class_='main-tit').attrs['title']
                video_list = []
                ul_list = div.find_all('ul', style="display:none;")
                for ul in ul_list:
                    li_list = ul.find_all('li')
                    for li in li_list:
                        video_list.append('https:' + li.a.attrs['href'])
                if len(video_list) == 0:
                    video_list.append('https:' + div.find('a', class_='qy-search-result-btn').attrs['href'])
                video_inf.append([video_img, video_type, video_name, video_list])
    except Exception as error:
        print(error)
    print("查找完毕")
    print("结果如下：")
    for inf in video_inf:
        print(inf[0])
        print(inf[1])
        print(inf[2])
        i = 1
        for temp in inf[3]:
            print("第" + str(i) + "集:" + temp)
            i = i + 1
        print()
    return video_inf


if __name__ == "__main__":
    search_name = input("输入电影或电视剧：")
    t_search = threading.Thread(target=video_search_iqiyi, args=(search_name,))
    t_search.start()
