import requests
import re

# Configurações
BASE_URL = "https://embedflix.cv/tv/"
STREAM_SERVER = "https://dlnmh9ip6v2xcxz.cloudfont.live/"
HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
}

def get_channels():
    print("🔎 Buscando canais...")
    try:
        response = requests.get(BASE_URL, headers=HEADERS, timeout=15)
        # Procura o padrão player.php?id=nome-do-canal
        ids = re.findall(r'player\.php\?id=([a-zA-Z0-9-]+)', response.text)
        return sorted(list(set(ids)))
    except Exception as e:
        print(f"❌ Erro ao buscar canais: {e}")
        return []

def create_m3u(ids):
    with open("lista.m3u", "w", encoding="utf-8") as f:
        f.write("#EXTM3U\n\n")
        for canal_id in ids:
            # Remove hífens para o link de vídeo conforme descobrimos (ex: globo-sp -> globosp)
            slug_limpo = canal_id.replace("-", "")
            nome_bonito = canal_id.replace("-", " ").upper()
            
            link_base = f"{STREAM_SERVER}{slug_limpo}.m3u8"
            
            # Escreve no formato compatível com VLC, XCIPTV e OTT Navigator
            f.write(f"#EXTINF:-1, {nome_bonito}\n")
            # Tags de cabeçalho para o player
            f.write(f"#EXTVLCOPT:http-referrer=https://embedflix.cv/\n")
            f.write(f"#EXTVLCOPT:http-user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64)\n")
            # A URL do vídeo deve vir logo abaixo das opções
            f.write(f"{link_base}\n\n")
            
    print(f"✅ Lista universal gerada com {len(ids)} canais!")

if __name__ == "__main__":
    canais = get_channels()
    if canais:
        create_m3u(canais)
    else:
        print("⚠️ Nenhum ID encontrado. Verifique se o site mudou a estrutura.")
