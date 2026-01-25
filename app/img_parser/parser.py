import requests
from bs4 import BeautifulSoup
from PIL import Image, ImageDraw, ImageFont
from svglib.svglib import svg2rlg
from reportlab.graphics import renderPM
import os
import io
from urllib.parse import urljoin
from duckduckgo_search import DDGS

from app.main import BASE_DIR
from app.img_parser.apps_list import apps_to_parse

STATIC_DIR = os.path.join(BASE_DIR, "static")
OUTPUT_DIR = os.path.join(STATIC_DIR, "images")
TARGET_SIZE = (256, 256)
FALLBACK_TARGET_SIZE_FOR_SVG_RENDER = (512, 512)
MIN_ACCEPTABLE_DIMENSION = 60
USER_AGENT = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
HEADERS = {'User-Agent': USER_AGENT}
MAX_SEARCH_RESULTS_TO_TRY = 5


def ensure_output_dir():
    if not os.path.exists(OUTPUT_DIR):
        os.makedirs(OUTPUT_DIR)
    print(f"Output directory: {os.path.abspath(OUTPUT_DIR)}")


def process_and_save_image(image_bytes, appid, original_url, is_svg=False):
    try:
        if is_svg:
            try:
                drawing = svg2rlg(io.BytesIO(image_bytes))
                if drawing:
                    dw, dh = drawing.width, drawing.height
                    if dw is None or dh is None or dw <= 0 or dh <= 0:
                        vb = drawing.getBounds()
                        dw_vb, dh_vb = vb[2] - vb[0], vb[3] - vb[1]
                        if dw_vb > 0 and dh_vb > 0:
                            dw, dh = dw_vb, dh_vb
                            print(f"INFO ({appid}): SVG from {original_url} using viewBox dimensions: {dw}x{dh}")
                        else:
                            dw, dh = FALLBACK_TARGET_SIZE_FOR_SVG_RENDER[0], FALLBACK_TARGET_SIZE_FOR_SVG_RENDER[1]
                            print(
                                f"INFO ({appid}): SVG from {original_url} has no explicit dimensions, using defaults: {dw}x{dh}")

                    scale_w = FALLBACK_TARGET_SIZE_FOR_SVG_RENDER[0] / dw if dw > 0 else 1
                    scale_h = FALLBACK_TARGET_SIZE_FOR_SVG_RENDER[1] / dh if dh > 0 else 1
                    scale = min(scale_w, scale_h)
                    if scale <= 0: scale = 1

                    drawing.width, drawing.height = dw * scale, dh * scale
                    drawing.scale(scale, scale)
                    png_bytes_from_svg = renderPM.drawToString(drawing, fmt='PNG')
                    img = Image.open(io.BytesIO(png_bytes_from_svg))
                else:
                    print(f"Error ({appid}): svg2rlg could not process SVG from {original_url}.")
                    return False
            except Exception as e_svg:
                print(f"Error ({appid}): Cant process SVG with svglib+reportlab from {original_url}. {e_svg}")
                return False
        else:
            img = Image.open(io.BytesIO(image_bytes))

        if img.mode not in ('RGBA', 'LA'):
            img = img.convert('RGBA')

        width, height = img.size
        if width < MIN_ACCEPTABLE_DIMENSION or height < MIN_ACCEPTABLE_DIMENSION:
            if not ("placeholder_generated_internally" in original_url.lower()):  # Добавил метку для плейсхолдеров
                print(f"Warning ({appid}): Original image ({width}x{height}) from {original_url} might be too small.")

        if width != height:
            max_dim = max(width, height)
            new_img_bg = Image.new('RGBA', (max_dim, max_dim), (0, 0, 0, 0))
            paste_x = (max_dim - width) // 2
            paste_y = (max_dim - height) // 2
            new_img_bg.paste(img, (paste_x, paste_y))
            img = new_img_bg

        img = img.resize(TARGET_SIZE, Image.Resampling.LANCZOS)

        output_path = os.path.join(OUTPUT_DIR, f"{appid}.png")
        img.save(output_path, 'PNG')
        print(f"Success ({appid}): Icon saved to: {output_path} (from {original_url})")
        return True
    except Exception as e:
        print(f"Error ({appid}): Cant process image (Pillow stage) from {original_url}. {e}")
        return False


def generate_placeholder_icon(appid, name):
    try:
        img = Image.new('RGBA', TARGET_SIZE, (80, 80, 150, 255))
        draw = ImageDraw.Draw(img)
        letter = name[0].upper() if name else '?'
        font_path = os.path.join(BASE_DIR, "app", "img_parser", "Montserrat-Bold.ttf")  # Уточни путь, если нужно

        try:
            font_size = int(TARGET_SIZE[0] * 0.6)
            font_file_to_try = "Montserrat-Bold.ttf"
            if os.path.exists(font_file_to_try):
                font = ImageFont.truetype(font_file_to_try, font_size)
            elif os.path.exists(font_path):  # Пробуем путь из BASE_DIR
                font = ImageFont.truetype(font_path, font_size)
            else:  # Если не найден, пробуем системный Arial
                print(f"Warning ({appid}): Montserrat-Bold.ttf not found at expected paths. Trying Arial.")
                font = ImageFont.truetype("arial.ttf", font_size)
        except IOError:
            print(f"Warning ({appid}): Specified font not found or error loading. Using default font.")
            font = ImageFont.load_default()

        if hasattr(draw, 'textbbox'):
            text_box = draw.textbbox((0, 0), letter, font=font)
            text_width = text_box[2] - text_box[0]
            text_height = text_box[3] - text_box[1]
        else:
            text_width, text_height = draw.textsize(letter, font=font)

        x = (TARGET_SIZE[0] - text_width) / 2
        y = (TARGET_SIZE[1] - text_height) / 2 - (TARGET_SIZE[1] * 0.05)
        draw.text((x, y), letter, font=font, fill=(255, 255, 255, 255))

        output_path = os.path.join(OUTPUT_DIR, f"{appid}.png")
        img.save(output_path, 'PNG')
        print(f"Info ({appid}): Created placeholder: {output_path}")
        return True
    except Exception as e:
        print(f"Error ({appid}): Cant create placeholder. {e}")
        return False


def fetch_direct_image(url, appid):
    print(f"Info ({appid}): Attempting direct download from {url}")
    try:
        response = requests.get(url, headers=HEADERS, timeout=20, stream=True)
        response.raise_for_status()
        content_type = response.headers.get('content-type', '').lower()
        image_bytes = response.content
        is_svg = 'svg' in content_type
        # Добавил webp в список поддерживаемых
        if is_svg or 'png' in content_type or 'jpeg' in content_type or 'jpg' in content_type or 'webp' in content_type:
            return process_and_save_image(image_bytes, appid, url, is_svg=is_svg)
        else:
            print(f"Warning ({appid}): Unknown or unsupported content type '{content_type}' for URL {url}")
            return False
    except requests.exceptions.RequestException as e:
        print(f"Error ({appid}): Can't download {url}. {e}")
        return False
    except Exception as e:  # Более общий обработчик
        print(f"Error ({appid}): Unexpected error during download from {url}. {e}")
        return False


def find_and_fetch_logo_on_page(page_url, app_name, appid, notes=""):
    print(f"Info ({appid}): Attempting to find logo on page: {page_url}")
    try:
        response = requests.get(page_url, headers=HEADERS, timeout=20)
        response.raise_for_status()
        soup = BeautifulSoup(response.content, 'html.parser')
        potential_image_urls = []

        # Поиск <img>
        img_tags = soup.find_all('img')
        print(f"Info ({appid}): Found {len(img_tags)} <img> tags on {page_url}")
        for img_tag in img_tags:
            src = img_tag.get('src')
            if not src: continue
            # Пропускаем data:image URI, если они не нужны или слишком длинные для лога
            if src.startswith('data:image'):
                print(f"Info ({appid}): Skipping data:image URI in <img> tag.")
                continue

            src_lower = src.lower()
            alt_lower = (img_tag.get('alt') or '').lower()
            # Добавил title в проверку
            title_lower = (img_tag.get('title') or '').lower()
            class_list = ' '.join(img_tag.get('class', [])).lower()

            app_name_first_part = app_name.split(' ')[0].lower()
            is_logo_like = any(k in src_lower for k in ['logo', 'brand', appid, app_name_first_part]) or \
                           any(k in alt_lower for k in ['logo', app_name.lower(), 'brand']) or \
                           any(k in title_lower for k in ['logo', app_name.lower(), 'brand']) or \
                           any(k in class_list for k in ['logo', 'brand-logo', 'app-icon'])

            if is_logo_like:
                full_url = urljoin(page_url, src)
                print(
                    f"Info ({appid}): Found potential logo in <img>: {full_url} (alt: '{alt_lower}', class: '{class_list}')")
                priority = 3
                if '.svg' in src_lower:
                    priority = 1
                elif '.png' in src_lower:
                    priority = 2
                potential_image_urls.append({'url': full_url, 'priority': priority})

        # Поиск <a>
        a_tags = soup.find_all('a')
        print(f"Info ({appid}): Found {len(a_tags)} <a> tags on {page_url}")
        for a_tag in a_tags:
            href = a_tag.get('href')
            if not href: continue

            href_lower = href.lower()
            # Проверяем также текст ссылки
            link_text_lower = a_tag.get_text(separator=' ', strip=True).lower()

            is_asset_link = any(k in href_lower for k in ['logo', 'brand', 'asset', 'download', 'icon']) or \
                            any(k in link_text_lower for k in ['logo', 'brand', 'download logo', 'icon'])

            if is_asset_link and any(ext in href_lower for ext in ['.svg', '.png', '.jpg', '.jpeg', '.webp', '.zip']):
                full_url = urljoin(page_url, href)
                print(f"Info ({appid}): Found potential logo in <a>: {full_url} (text: '{link_text_lower}')")
                if '.zip' in href_lower:
                    print(f"Info ({appid}): Found ZIP archive link: {full_url}. Manual extraction needed.")
                    continue
                priority = 2.1
                if '.svg' in href_lower: priority = 1.1
                potential_image_urls.append({'url': full_url, 'priority': priority})

        # Поиск <svg> тегов (упрощенный вариант - если есть <use xlink:href="...logo...">)
        # Более сложный парсинг встроенных SVG потребует больше логики
        for svg_tag in soup.find_all('svg'):
            # Проверяем наличие <use> с ссылкой на лого в атрибуте class или id самого <svg>
            svg_class = ' '.join(svg_tag.get('class', [])).lower()
            svg_id = (svg_tag.get('id') or '').lower()
            if 'logo' in svg_class or 'icon' in svg_class or 'logo' in svg_id or 'icon' in svg_id:
                # Если это встроенный SVG, его нужно сериализовать обратно в строку
                # Это может быть нетривиально, если он сложный или использует внешние ссылки
                # Для простоты, если найден такой SVG, можно вывести сообщение, что требуется ручная проверка
                print(
                    f"Info ({appid}): Found an inline <svg> tag that might be a logo. Inline SVG extraction is complex and not fully implemented here.")
                # Можно попытаться сериализовать, но это может быть не всегда корректно:
                # svg_code = str(svg_tag)
                # print(f"  SVG Code (partial): {svg_code[:200]}")
                # Здесь можно было бы добавить логику сохранения этого SVG кода как файла, если это нужно.

        if not potential_image_urls:
            print(f"Info ({appid}): No potential logo URLs found on page {page_url} after parsing.")
            return False

        potential_image_urls.sort(key=lambda x: x['priority'])

        print(f"Info ({appid}): Found {len(potential_image_urls)} potential logo URLs. Top candidates:")
        for i, item in enumerate(potential_image_urls[:3]):
            print(f"  Candidate #{i + 1}: {item['url']} (priority: {item['priority']})")

        best_match_url = potential_image_urls[0]['url']
        print(f"Info ({appid}): Selected best match: {best_match_url}")
        return fetch_direct_image(best_match_url, appid)

    except requests.exceptions.RequestException as e:
        print(f"Error ({appid}): Request failed for page {page_url}. {e}")
        return False
    except Exception as e:  # Общий обработчик
        print(f"Error ({appid}): Unexpected error while processing page {page_url}. {e}")
        # import traceback # Для детальной отладки
        # traceback.print_exc()
        return False


# --- ОБНОВЛЕННАЯ ФУНКЦИЯ ПОИСКА ИЗОБРАЖЕНИЙ ---
def search_and_download_icon(search_query, appid, app_name):
    print(f"Info ({appid}): Performing image search for: '{search_query}'")
    raw_results = []
    try:
        # Первая попытка: ищем изображения с прозрачным фоном и типом clipart/line
        print(f"Info ({appid}): Search attempt 1: type_image='transparent' or 'clipart' or 'line'")
        with DDGS(headers=HEADERS, proxies=None, timeout=25) as ddgs:  # Немного увеличил таймаут
            # Пробуем несколько вариантов type_image, которые могут дать хорошие логотипы
            for type_img_attempt in ['transparent', 'clipart', 'line', None]:  # None в конце как самый широкий
                if raw_results and len(
                    raw_results) > MAX_SEARCH_RESULTS_TO_TRY * 2: break  # Если уже достаточно набрали
                print(f"Info ({appid}): Trying with type_image='{type_img_attempt}'")
                current_attempt_results_iterator = ddgs.images(
                    keywords=search_query,
                    region='wt-wt',
                    safesearch='moderate',
                    size=None,  # Искать все размеры ('None', 'Small', 'Medium', 'Large', 'Wallpaper')
                    type_image=type_img_attempt,
                    layout='Square',  # Попробуем запросить квадратные изображения
                    license_image=None,  # Искать все лицензии
                    max_results=MAX_SEARCH_RESULTS_TO_TRY + 10  # Запросим побольше на каждую попытку
                )
                if current_attempt_results_iterator:
                    # Добавляем только уникальные URL изображений
                    for res in current_attempt_results_iterator:
                        if res.get('image') and not any(
                                existing_res.get('image') == res.get('image') for existing_res in raw_results):
                            raw_results.append(res)
                if type_img_attempt is None and not raw_results:  # Если даже полный поиск ничего не дал
                    print(f"Warning ({appid}): Search (type_image=None) also returned no results for '{search_query}'.")
                    return False

        if not raw_results:
            print(f"Warning ({appid}): All search attempts returned no results for '{search_query}'.")
            return False

        print(
            f"Info ({appid}): Found {len(raw_results)} unique raw results across attempts. Top results before filtering/scoring:")
        for i, r in enumerate(raw_results[:min(10, len(raw_results))]):  # Печать топ-10 или меньше
            print(
                f"  RawRes #{i + 1}: URL={r.get('image')}, Title={r.get('title')}, Size={r.get('width')}x{r.get('height')}, SourcePage={r.get('url')}")

        scored_results = []
        # Используем set для отслеживания уже добавленных URL, чтобы избежать дубликатов в scored_results
        processed_image_urls = set()

        for r_idx, r in enumerate(raw_results):
            score = 0
            url = r.get('image', '')
            if not url or url in processed_image_urls:  # Пропускаем результаты без URL или уже обработанные
                continue

            url_lower = url.lower()
            title_lower = r.get('title', '').lower()
            # Иногда DDGS возвращает размеры как строки, нужно преобразовать в int
            try:
                width = int(r.get('width', 0))
                height = int(r.get('height', 0))
            except ValueError:
                width, height = 0, 0

            # 1. Приоритет по типу файла
            if '.svg' in url_lower:
                score += 120  # SVG - наивысший приоритет
            elif '.png' in url_lower:
                score += 90
            elif '.webp' in url_lower:
                score += 50  # WebP может быть с прозрачностью и хорошего качества
            elif '.jpg' in url_lower or '.jpeg' in url_lower:
                score += 10
            else:
                score -= 20  # Штраф за другие/неизвестные расширения

            # 2. Ключевые слова
            # Составляем список ключевых слов, включая части имени приложения
            app_name_parts = [part for part in app_name.lower().split(' ') if
                              len(part) > 2]  # Только слова длиннее 2 символов
            keywords_to_check = ['logo', 'icon', 'official'] + app_name_parts + [appid.lower()]

            title_matches = sum(
                20 for k in keywords_to_check if k in title_lower)  # Больше очков за совпадения в заголовке
            url_matches = sum(10 for k in keywords_to_check if k in url_lower)  # Меньше, но тоже важно
            score += title_matches + url_matches

            if 'transparent' in title_lower or 'alpha' in title_lower: score += 30  # Бонус за прозрачность в названии
            if 'vector' in title_lower and '.svg' in url_lower: score += 20  # Дополнительно за вектор SVG

            # 3. Размеры и соотношение сторон
            if width > 0 and height > 0:
                if width >= MIN_ACCEPTABLE_DIMENSION and height >= MIN_ACCEPTABLE_DIMENSION:
                    score += 40  # Значительный бонус за приемлемый минимальный размер
                else:
                    score -= 150  # Очень большой штраф за слишком маленькие

                aspect_ratio = width / height
                if 0.9 <= aspect_ratio <= 1.1:  # Почти идеальный квадрат
                    score += 40
                elif 0.75 <= aspect_ratio <= 1.33:  # Хорошее соотношение
                    score += 25
                elif 0.5 <= aspect_ratio <= 2.0:  # Приемлемое соотношение
                    score += 10
                else:  # Сильно неквадратные
                    score -= 60

                # Бонус за разрешение, близкое или превышающее целевое
                if width >= TARGET_SIZE[0] and height >= TARGET_SIZE[1]: score += 30
                # Бонус за очень большие изображения (хорошо для SVG или для последующего ресайза)
                if width >= FALLBACK_TARGET_SIZE_FOR_SVG_RENDER[0] and height >= FALLBACK_TARGET_SIZE_FOR_SVG_RENDER[
                    1]: score += 15
            else:  # Если размеры не указаны (0x0), это плохой знак
                score -= 30

            # 4. Избегаем распространенных "мусорных" источников или паттернов (можно расширять)
            bad_sources = ['gallerix.asia', 'alamy.com', 'dreamstime.com', '123rf.com', 'depositphotos.com',
                           'shutterstock.com', 'stock.adobe.com', 'istockphoto.com']  # Стоки часто с вотермарками
            if any(bad_source in url_lower for bad_source in bad_sources):
                score -= 200  # Сильный штраф за стоковые сайты

            if 'favicon' in url_lower or 'ico' in url_lower:  # Фавиконки обычно не подходят
                score -= 100
            if 'avatar' in url_lower or 'profile' in url_lower:  # Аватарки тоже
                score -= 80
            if 'banner' in url_lower or 'header' in url_lower:  # Баннеры и шапки сайтов
                score -= 50

            if score > 20:  # Увеличил порог для добавления в кандидаты
                scored_results.append({
                    'url': url, 'score': score, 'title': r.get('title'),
                    'width': width, 'height': height, 'source_page': r.get('url')
                })
                processed_image_urls.add(url)  # Добавляем в обработанные

        # Сортируем по убыванию очков
        scored_results.sort(key=lambda x: x['score'], reverse=True)

        if not scored_results:
            print(f"Warning ({appid}): No images passed the scoring criteria for '{search_query}'.")
            return False

        print(
            f"Info ({appid}): Top {len(scored_results)} scored results after filtering (max {MAX_SEARCH_RESULTS_TO_TRY + 5} shown):")
        for i, res_info in enumerate(scored_results[:min(MAX_SEARCH_RESULTS_TO_TRY + 5, len(scored_results))]):
            print(
                f"  ScoredRes #{i + 1}: URL={res_info['url']}, Score={res_info['score']}, Title={res_info['title']}, Size={res_info['width']}x{res_info['height']}, Source={res_info['source_page']}")

        # Пытаемся скачать лучшие MAX_SEARCH_RESULTS_TO_TRY результатов
        for i, res_info in enumerate(scored_results[:MAX_SEARCH_RESULTS_TO_TRY]):
            print(
                f"Info ({appid}): Attempting download #{i + 1} (score: {res_info['score']}) from search: {res_info['url']}")
            if fetch_direct_image(res_info['url'], appid):
                # Сообщение об успехе уже будет в fetch_direct_image -> process_and_save_image
                return True

        print(
            f"Warning ({appid}): Could not download a suitable icon from the top {MAX_SEARCH_RESULTS_TO_TRY} scored search results for '{search_query}'.")
        return False

    except Exception as e:
        print(f"Error ({appid}): An error occurred during image search for '{search_query}': {e}")
        # import traceback # Раскомментируй для подробной отладки, если нужно
        # traceback.print_exc()
        return False


# --- КОНЕЦ ОБНОВЛЕННОЙ ФУНКЦИИ ПОИСКА ---

if __name__ == '__main__':
    ensure_output_dir()
    processed_appids = set()  # Для отслеживания уже обработанных appid

    for app_info in apps_to_parse:
        appid = app_info['appid']
        name = app_info['name']
        url_type = app_info['url_type']
        url_or_search = app_info['url']
        notes = app_info.get('notes', '')
        print(f"\n--- Processing: {name} ({appid}) ---")

        if appid in processed_appids:
            print(f"Info ({appid}): App already processed in this run. Skipping.")
            continue

        output_filepath = os.path.join(OUTPUT_DIR, f"{appid}.png")
        if os.path.exists(output_filepath):
            print(f"Info ({appid}): Icon already exists ({output_filepath}). Skipping.")
            processed_appids.add(appid)
            continue

        success = False
        if url_type in ['direct_png', 'direct_svg', 'direct_jpg']:
            success = fetch_direct_image(url_or_search, appid)
        elif url_type == 'brand_page':
            success = find_and_fetch_logo_on_page(url_or_search, name, appid, notes)
        elif url_type == 'search_fallback':
            # Убедимся, что url_or_search это строка запроса
            if not isinstance(url_or_search, str):
                print(f"Error ({appid}): Search query for search_fallback is not a string: {url_or_search}")
                url_or_search = f"{name} official app icon logo"  # Запасной запрос

            print(f"Info ({appid}): Type 'search_fallback'. Search query: '{url_or_search}'.")
            success = search_and_download_icon(url_or_search, appid, name)

        if not success:
            print(
                f"Warning ({appid}): Could not automatically find or process icon for '{name}'. Generating placeholder.")
            generate_placeholder_icon(appid, name)

        processed_appids.add(appid)  # Добавляем в обработанные в этой сессии

    print("\n--- Icon processing complete. ---")