import requests
from bs4 import BeautifulSoup
import concurrent.futures

def find_discord_server(url):
    response = requests.get(url)
    
    if response.status_code == 200:
        soup = BeautifulSoup(response.content, 'html.parser')
        links = soup.find_all('a')
        
        for link in links:
            href = link.get('href')
            if href and 'discord.gg' in href:
                return href
    
    return None

def load_community_links(filename):
    with open(filename, 'r') as f:
        community_links = f.read().splitlines()[8881:20000]  # Ограничение на первые 10000 записей
    return community_links

def load_community_discord_links(filename):
    community_discord_links = {}
    try:
        with open(filename, 'r') as f:
            lines = f.readlines()
            for line in lines:
                parts = line.strip().split(' ')
                community = parts[0]
                discord_link = parts[1] if len(parts) > 1 else None
                community_discord_links[community] = discord_link
    except FileNotFoundError:
        # Если файл не найден, создаем пустой словарь
        community_discord_links = {}
    return community_discord_links

def main():
    communities = load_community_links('communities.txt')

    # Загрузка дополнительных ссылок на Discord серверы из файла
    community_discord_links = load_community_discord_links('discord_servers.txt')

    # Параллельный поиск ссылок на Discord серверы
    found_servers_count = 0
    with concurrent.futures.ThreadPoolExecutor() as executor:
        with open('discord_servers.txt', 'a') as f:
            # Создаем список задач для каждого сообщества
            tasks = {executor.submit(find_discord_server, f"https://www.reddit.com{community}"): community for community in communities}
            for future in concurrent.futures.as_completed(tasks):
                community = tasks[future]
                discord_server = future.result()
                
                if discord_server:
                    print(f"В сообществе {community} найден Discord сервер: {discord_server}")
                    f.write(f"{community} {discord_server}\n")
                    found_servers_count += 1
                elif community in community_discord_links:
                    print(f"Для сообщества {community} нет приглашения на Discord сервер.")
                    f.write(f"{community}\n")
                else:
                    print(f"Для сообщества {community} не найдено приглашение на Discord сервер и ссылка отсутствует в файле.")
    
    print(f"Общее количество найденных сообществ с Discord серверами: {found_servers_count}")

if __name__ == "__main__":
    main()
