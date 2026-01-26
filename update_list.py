import requests
import re

# Configurações
BASE_URL = "https://embedflix.cv/tv/"
STREAM_SERVER = "https://dlnmh9ip6v2xcxz.cloudfont.live/"
HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
}
M3U_HEADERS = "|Referer=https://embedflix.cv/&User-Agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"

def get_channels():
    print("🔎 Buscando canais...")
    response = requests.get(BASE_URL, headers=HEADERS)
    # Procura o padrão player.php?id=nome-do-canal
    ids = re.findall(r'player\.php\?id=([a-zA-Z0-9-]+)', response.text)
    return sorted(list(set(ids)))

def create_m3u(ids):
    with open("lista.m3u", "w", encoding="utf-8") as f:
        f.write("#EXTM3U\n\n")
        for canal_id in ids:
            # Remove hífens para o link de vídeo conforme descobrimos
            slug_limpo = canal_id.replace("-", "")
            nome_bonito = canal_id.replace("-", " ").upper()
            
            link = f"{STREAM_SERVER}{slug_limpo}.m3u8{M3U_HEADERS}"
            f.write(f"#EXTINF:-1, {nome_bonito}\n{link}\n\n")
    print(f"✅ Lista gerada com {len(ids)} canais!")

if __name__ == "__main__":
    canais = get_channels()
    if canais:
        create_m3u(canais)
