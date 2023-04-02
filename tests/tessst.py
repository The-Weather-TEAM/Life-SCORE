
import requests
import time




def get_download_size(url):
    response = requests.head(url, allow_redirects=True)
    content_length = response.headers.get('Content-Length')
    if content_length is None:
        return None
    else:
        return int(content_length)


url = 'https://github.com/The-Weather-TEAM/Life-SCORE/raw/main/test.zip'
download_size = get_download_size(url)
if download_size is not None:
    print(f"La taille du téléchargement est de {download_size} bits.")
else:
    print("Impossible de récupérer la taille du téléchargement.")









def download_file(url, filename):
    response = requests.get(url, stream=True)
    chunk_size = 1024
    bytes_downloaded = 0
    start_time = time.time()
    with open(filename, 'wb') as f:
        for chunk in response.iter_content(chunk_size=chunk_size):
            if chunk:
                f.write(chunk)
                bytes_downloaded += len(chunk)
                current_time = time.time()
                time_elapsed = current_time - start_time
                if time_elapsed != 0 :
                    download_speed = bytes_downloaded / time_elapsed
                #print(f"Téléchargé : {bytes_downloaded} bits ({download_speed:.2f} bits/s)")
                pourcentage = bytes_downloaded / download_size * 100
                print(pourcentage)
                
                
url = 'https://github.com/The-Weather-TEAM/Life-SCORE/raw/main/test.zip'
filename = 'file.zip'
download_file(url, filename)
