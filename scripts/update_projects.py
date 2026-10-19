import os
import requests

USERNAME = "SaladDann"
TOKEN = os.getenv("GH_TOKEN")

headers = {"Accept": "application/vnd.github.v3+json"}
if TOKEN:
    headers["Authorization"] = f"token {TOKEN}"

LANG_BADGES = {
    "TypeScript": "https://img.shields.io/badge/TypeScript-005f73?style=flat-square&logo=typescript&logoColor=white",
    "JavaScript": "https://img.shields.io/badge/JavaScript-0a9396?style=flat-square&logo=javascript&logoColor=white",
    "Python": "https://img.shields.io/badge/Python-1e3a8a?style=flat-square&logo=python&logoColor=white",
    "Dart": "https://img.shields.io/badge/Dart-0d9488?style=flat-square&logo=dart&logoColor=white",
    "C#": "https://img.shields.io/badge/C%23-0f766e?style=flat-square&logo=c-sharp&logoColor=white",
    "Java": "https://img.shields.io/badge/Java-1e293b?style=flat-square&logo=openjdk&logoColor=white",
    "HTML": "https://img.shields.io/badge/HTML5-0a9396?style=flat-square&logo=html5&logoColor=white",
    "C++": "https://img.shields.io/badge/C%2B%2B-005f73?style=flat-square&logo=cplusplus&logoColor=white"
}

def get_repos():
    url = f"https://api.github.com/users/{USERNAME}/repos?sort=created&direction=desc&per_page=100"
    res = requests.get(url, headers=headers)
    if res.status_code != 200:
        raise Exception(f"Error HTTP {res.status_code}")
    return res.json()

def generate_catalog(repos):
    # Filtrar forks y el repo de perfil o catálogo si deseas omitirlos
    own_repos = [r for r in repos if not r["fork"] and r["name"].lower() not in [USERNAME.lower(), "my-projects"]]
    sorted_repos = sorted(own_repos, key=lambda x: x["created_at"], reverse=True)
    
    html = '<table width="100%">\n'
    for i in range(0, len(sorted_repos), 2):
        html += "  <tr>\n"
        for repo in sorted_repos[i:i+2]:
            name = repo["name"]
            url = repo["html_url"]
            desc = repo["description"] or "Proyecto desarrollado en GitHub."
            lang = repo["language"] or "Code"
            created_date = repo["created_at"].split("T")[0]
            stars = repo["stargazers_count"]
            
            badge_url = LANG_BADGES.get(
                lang, 
                f"https://img.shields.io/badge/{lang}-0d9488?style=flat-square"
            )
            
            html += f'''    <td width="50%" valign="top">
      <h4 align="left">📁 <a href="{url}">{name}</a></h4>
      <p><sub>📅 Creado: <code>{created_date}</code> | ⭐ {stars}</sub></p>
      <p><img src="{badge_url}" alt="{lang}" /></p>
      <p>{desc}</p>
      <p><a href="{url}"><b>Ver Repositorio »</b></a></p>
    </td>\n'''
        html += "  </tr>\n"
    html += "</table>\n"
    return html

def update_readme(content):
    with open("README.md", "r", encoding="utf-8") as f:
        readme = f.read()
        
    start_tag = "<!-- CATALOG_START -->"
    end_tag = "<!-- CATALOG_END -->"
    
    s_idx = readme.find(start_tag)
    e_idx = readme.find(end_tag)
    
    if s_idx != -1 and e_idx != -1:
        new_readme = readme[:s_idx + len(start_tag)] + "\n\n" + content + "\n" + readme[e_idx:]
        with open("README.md", "w", encoding="utf-8") as f:
            f.write(new_readme)

if __name__ == "__main__":
    repos = get_repos()
    catalog_html = generate_catalog(repos)
    update_readme(catalog_html)
