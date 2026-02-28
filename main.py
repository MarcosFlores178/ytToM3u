import yt_dlp
import os

# Configuración de archivos
INPUT_FILE = 'youtube_channel_info.txt'
OUTPUT_FILE = 'lista_canales.m3u'

def get_live_link(youtube_url):
    """Extrae el enlace m3u8 real usando yt-dlp."""
    ydl_opts = {
        'quiet': True,
        'no_warnings': True,
        'format': 'best',
        'force_generic_extractor': False,
    }
    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(youtube_url, download=False)
            return info.get('url')
    except Exception:
        return None

def generate_m3u():
    if not os.path.exists(INPUT_FILE):
        print(f"Error: No se encuentra el archivo {INPUT_FILE}")
        return

    with open(OUTPUT_FILE, 'w', encoding='utf-8') as out:
        # Cabecera del archivo M3U
        out.write('#EXTM3U x-tvg-url="https://github.com/botallen/epg/releases/download/latest/epg.xml"\n')
        
        print("Procesando canales...")
        
        with open(INPUT_FILE, 'r', encoding='utf-8') as f:
            for line in f:
                line = line.strip()
                if not line or line.startswith('~~'):
                    continue
                
                # Si la línea no es una URL, es la info del canal
                if not line.startswith('https:'):
                    parts = [p.strip() for p in line.split('|')]
                    if len(parts) >= 4:
                        ch_name, grp_title, tvg_logo, tvg_id = parts
                        # Guardamos temporalmente la info del encabezado
                        header = f'\n#EXTINF:-1 group-title="{grp_title}" tvg-logo="{tvg_logo}" tvg-id="{tvg_id}", {ch_name}\n'
                else:
                    # La línea es la URL, procedemos a extraer el m3u8
                    print(f"Extrayendo link para: {ch_name}...", end=" ", flush=True)
                    m3u8_link = get_live_link(line)
                    
                    if m3u8_link:
                        out.write(header)
                        out.write(m3u8_link + '\n')
                        print("✅")
                    else:
                        print("❌ Falló")

    print(f"\n¡Listo! Lista guardada en: {OUTPUT_FILE}")

if __name__ == "__main__":
    generate_m3u()