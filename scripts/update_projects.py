import os
import requests

USERNAME = "SaladDann"
TOKEN = os.getenv("GH_TOKEN")

headers = {"Accept": "application/vnd.github.v3+json"}
if TOKEN:
    headers["Authorization"] = f"token {TOKEN}"

LANG_BADGES = {
    "TypeScript": "https://img.shields.io/badge/TypeScript-0f172a?style=flat-square&logo=typescript&logoColor=3178C6",
    "JavaScript": "https://img.shields.io/badge/JavaScript-0f172a?style=flat-square&logo=javascript&logoColor=F7DF1E",
    "Python": "https://img.shields.io/badge/Python-0f172a?style=flat-square&logo=python&logoColor=3776AB",
    "Dart": "https://img.shields.io/badge/Dart-0f172a?style=flat-square&logo=dart&logoColor=0175C2",
    "C#": "https://img.shields.io/badge/C%23-0f172a?style=flat-square&logo=csharp&logoColor=239120",
    "Java": "https://img.shields.io/badge/Java-0f172a?style=flat-square&logo=openjdk&logoColor=ED8B00",
    "HTML": "https://img.shields.io/badge/HTML5-0f172a?style=flat-square&logo=html5&logoColor=E34F26",
    "C++": "https://img.shields.io/badge/C%2B%2B-0f172a?style=flat-square&logo=cplusplus&logoColor=00599C"
}

def get_repos():
    url = f"https://api.github.com/users/{USERNAME}/repos?sort=created&direction=desc&per_page=100"
    res = requests.get(url, headers=headers)
    if res.status_code != 200:
        raise Exception(f"Error HTTP {res.status_code}")
    return res.json()

def generate_catalog(repos):
    filtered_repos = [r for r in repos if r["name"].lower() not in [USERNAME.lower(), "my-projects"]]
    sorted_repos = sorted(filtered_repos, key=lambda x: x["created_at"], reverse=True)
    
    repos_by_year = {}
    for repo in sorted_repos:
        year = repo["created_at"].split("-")[0]
        repos_by_year.setdefault(year, []).append(repo)
    
    html = ""
    
    for year, group in repos_by_year.items():
        # Encabezado por año generado dinámicamente
        html += f'''
<div style="border-left: 3px solid #0d9488; padding-left: 12px; margin: 24px 0 16px 0;">
  <span style="font-family: 'JetBrains Mono', 'Fira Code', 'SF Mono', monospace; font-size: 0.85rem; font-weight: 600; color: #0d9488; letter-spacing: 1px;">
    // {year}
  </span>
</div>

<table width="100%" style="border-collapse: collapse;">
'''
        for i in range(0, len(group), 2):
            html += "  <tr>\n"
            for repo in group[i:i+2]:
                name = repo["name"]
                url = repo["html_url"]
                desc = repo["description"] or "Sin descripción disponible."
                lang = repo["language"] or "Code"
                created_date = repo["created_at"].split("T")[0]
                stars = repo["stargazers_count"]
                forks_count = repo["forks_count"]
                is_fork = repo["fork"]
                
                type_badge = (
                    '<img src="https://img.shields.io/badge/FORK-1e293b?style=flat-square&logo=github&logoColor=94a3b8" />' 
                    if is_fork else 
                    '<img src="https://img.shields.io/badge/ORIGINAL-0d9488?style=flat-square" />'
                )
                
                lang_badge = LANG_BADGES.get(
                    lang, 
                    f"https://img.shields.io/badge/{lang}-0f172a?style=flat-square"
                )
                
                html += f'''    <td width="50%" valign="top" style="padding: 6px;">
      <div style="padding: 14px; border: 1px solid #1e293b; border-radius: 8px; background-color: #0f172a; height: 100%;">
        <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 6px;">
          <h4 style="margin: 0; font-family: 'JetBrains Mono', monospace; font-size: 0.9rem;">
            📁 <a href="{url}" target="_blank" style="color: #f1f5f9; text-decoration: none;">{name}</a>
          </h4>
          {type_badge}
        </div>
        <p style="margin: 2px 0 8px 0;">
          <sub style="font-family: 'JetBrains Mono', monospace; color: #64748b;">📅 {created_date} &nbsp;·&nbsp; ⭐ {stars} &nbsp;·&nbsp; 🍴 {forks_count}</sub>
        </p>
        <p style="margin-bottom: 10px;"><img src="{lang_badge}" alt="{lang}" /></p>
        <p style="font-family: 'JetBrains Mono', monospace; font-size: 0.78rem; color: #94a3b8; line-height: 1.4; margin-bottom: 10px;">
          {desc}
        </p>
        <p style="margin: 0;">
          <a href="{url}" target="_blank" style="font-family: 'JetBrains Mono', monospace; font-size: 0.75rem; color: #0d9488; text-decoration: none; font-weight: 600;">
            Ver Repositorio →
          </a>
        </p>
      </div>
    </td>\n'''
            if len(group[i:i+2]) == 1:
                html += '    <td width="50%" valign="top"></td>\n'
            html += "  </tr>\n"
        html += "</table>\n"
        
    return html

def update_readme(content):
    if not os.path.exists("README.md"):
        return
        
    with open("README.md", "r", encoding="utf-8") as f:
        readme = f.read()
        
    start_tag = "<!-- CATALOG_START -->"
    end_tag = "<!-- CATALOG_END -->"
    
    s_idx = readme.find(start_tag)
    e_idx = readme.find(end_tag)
    
    if s_idx != -1 and e_idx != -1:
        new_readme = readme[:s_idx + len(start_tag)] + "\n" + content + "\n" + readme[e_idx:]
        with open("README.md", "w", encoding="utf-8") as f:
            f.write(new_readme)

if __name__ == "__main__":
    repos = get_repos()
    catalog_html = generate_catalog(repos)
    update_readme(catalog_html)
