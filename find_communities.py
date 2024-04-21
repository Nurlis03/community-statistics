import requests
from bs4 import BeautifulSoup

def find_community_links(url, num_communities):
    community_links = []
    count = 0
    page = 1
    
    while count < num_communities:
        response = requests.get(f"{url}{page}/")
        
        if response.status_code == 200:
            soup = BeautifulSoup(response.content, 'html.parser')
            links = soup.find_all('a')
            
            for link in links:
                href = link.get('href')
                if href and '/r/' in href and '/comments/' not in href:
                    community_links.append(href)
                    count += 1
                    if count >= num_communities:
                        break
            
            page += 1
        else:
            print("Ошибка при получении данных.")
            break
    
    return community_links

def save_links_to_file(links, filename):
    with open(filename, 'w') as f:
        for link in links:
            f.write(link + '\n')

def main():
    base_url = 'https://www.reddit.com/best/communities/'
    num_communities = 100000

    # Получение ссылок на сообщества Reddit
    community_links = find_community_links(base_url, num_communities)

    # Сохранение найденных ссылок в файл
    save_links_to_file(community_links, 'communities.txt')
    print("Ссылки на сообщества Reddit сохранены в файл 'communities.txt'.")

if __name__ == "__main__":
    main()
