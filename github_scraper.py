import base64
import requests

def fetch_search_results(query, token):
    url = f"https://api.github.com/search/code?q={query}"
    headers = {
        "Authorization": f"token {token}",
        "Accept": "application/vnd.github.v3+json",
    }
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        return response.json()
    else:
        print(f"Failed to fetch search results: {response.status_code}")
        return None

def extract_file_info(search_results):
    file_info = []
    if "items" in search_results:
        for item in search_results["items"]:
            repo_name = item["repository"]["full_name"]
            file_path = item["path"]
            file_info.append((repo_name, file_path))
    return file_info

def download_raw_file(repo_name, file_path, token):
    url = f"https://api.github.com/repos/{repo_name}/contents/{file_path}"
    headers = {
        "Authorization": f"token {token}",
    }
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        file_content = response.json()["content"]
        decoded_content = base64.b64decode(file_content).decode('utf-8')
        filename = file_path.split("/")[-1]
        with open(temp_dir+filename, "w") as f:
            f.write(decoded_content)
        print(f"Downloaded {filename}")
    else:
        print(f"Failed to download file: {response.status_code}")


def main():
    query = "search term"
    token = "insert token here"

    search_results = fetch_search_results(query, token)
    if search_results:
        file_info = extract_file_info(search_results)
        for repo_name, file_path in file_info:
            download_raw_file(repo_name, file_path, token)


temp_dir = 'where to store files'

if __name__ == "__main__":
    main()