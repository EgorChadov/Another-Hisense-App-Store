import requests
import os
import io
from PIL import Image, ImageOps  # ImageOps может понадобиться для более качественного ресайза или padding

# --- Константы из JavaScript ---
HISENSE_APP_LIST = [
    {'appid': 'anb_lampa', 'name': 'Lampa', 'url': 'http://lampa.mx/',
     'text': 'Новое полностью бесплатное приложение для Smart TV'},
    {'appid': 'anb_vokino', 'name': 'vokino', 'url': 'http://web.vokino.tv/',
     'text': 'Смотреть зарубежные фильмы и сериалы в хорошем качестве'},
    {'appid': 'anb_atodo', 'name': 'Atodo',
     'url': 'http://msx.benzac.de/?start=menu:request:interaction:menu@http://atodo.fun/fun.html', 'text': 'АТОDO'},
    {'appid': 'anb_fxml', 'name': 'Media Station X', 'url': 'http://msx.benzac.de/foxxum.html',
     'text': 'Приложение для создания настраиваемых мультимедийных страниц (видео, аудио и пр.)'},
    {'appid': 'anb_moovies', 'name': 'Moovies',
     'url': 'http://msx.benzac.de/?start=menu:request:interaction:init@http://moovies.uz/index.html',
     'text': 'Moovies for MSX'},
    {'appid': 'anb_movielab', 'name': 'Movielab',
     'url': 'https://msx.benzac.de/?start=menu:https://movielab.fun/msx/menu.json',
     'text': 'Наслаждайтесь просмотром лучших фильмов с MovieLab'},
    {'appid': 'anb_deeplex', 'name': 'DEEPLEX', 'url': 'http://smart.deeplex.cc',
     'text': 'Фильмы, сериалы и многое другое без ограничений.Инструкция -> http://deeplex.cc/#/instructions'},
    {'appid': 'anb_drmplay', 'name': 'DRM-play', 'url': 'http://drm-play.com',
     'text': 'Ott плеер drm-play, mod плеера ott-play by Alex '},
    {'appid': 'anb_fork', 'name': 'ForkPlayer', 'url': 'http://browser.appfxml.com/',
     'text': 'ForkPlayer — это браузер с адаптированным под ваше устройство просмотром сайтов'},
    {'appid': 'anb_forkbrowser', 'name': 'Fork Browser', 'url': 'http://browser.appinfo.su/',
     'text': 'Новая, улучшенная версия ForkPlayer'},
    {'appid': 'anb_lampalite4', 'name': 'Lampa lite', 'url': 'http://lite.lampa.mx/',
     'text': 'Lampa Lite, облегченная версия приложения для онлайн просмотра.'},
    {'appid': 'anb_twitch', 'name': 'twitch', 'url': 'https://hisense.tv.twitch.tv/',
     'text': 'Видеостриминговый сервис, специализирующийся на тематике компьютерных игр.'},
    {'appid': 'anb_vkvideo', 'name': 'VK видео', 'url': 'https://vk.ru/tv-app/lib?version=latest&platform=vidaa',
     'text': 'Смотрите видеозаписи ВКонтакте на большом экране SmartTV. '},
    {'appid': 'anb_beeline', 'name': 'Билайн ТВ', 'url': 'https://smart-vidaa.beeline.tv/',
     'text': 'Тысячи фильмов, сериалов и мультфильмов. 300 каналов и доступ к онлайн-кинотеатру beeline.tv.'},
    {'appid': 'anb_xsmart', 'name': 'Xsmart', 'url': 'http://app.xsmart.tv/?widg=5',
     'text': 'Приложение для Smart TV, которое объединяет в себе различные функции.'},
    {'appid': 'anb_viju', 'name': 'Viju', 'url': 'https://smarttv.viju.ru',
     'text': 'Viju – это лучшие фильмы, сериалы и мультфильмы по подписке'},
    {'appid': 'anb_tiktok', 'name': 'TikTok', 'url': 'https://tv.tiktok.com/webos',
     'text': 'Ведущая видеоплатформа для коротких видео'},
    {'appid': 'anb_m3uiptv', 'name': 'M3U IPTV', 'url': 'https://m3u-ip.tv/lg/',
     'text': 'Просто загрузите свой плейлист IPTV по URL-адресу (в виде файла m3u или m3u8) и вперед'},
    {'appid': 'anb_kinopoisk', 'name': 'Кинопоиск', 'url': 'https://smarttv-app.ott.yandex.ru/?ott-rv=vidaa',
     'text': 'Крупнейший русскоязычный онлайн-кинотеатр.'},
    {'appid': 'anb_yandexvideo', 'name': 'Яндекс видео', 'url': 'https://yandex.ru/video/tvapp/?ui=tvapp',
     'text': 'Cмотреть телепередачи, музыкальные клипы, игровые ролики и популярное на YouTube'},
    {'appid': 'anb_ott', 'name': 'OttPlayer', 'url': 'http://widget.ottplayer.tv/operatv2/index.html',
     'text': 'Cервис, который позволяет вам собрать всё ваше IP-телевидение в одном плейлисте.'},
    {'appid': 'anb_ottold', 'name': 'OttPlayerTest', 'url': 'http://widget.ottplayer.tv/test/index.html',
     'text': 'OttPlayer, более новая(тестовая версия приложения)'},
    {'appid': 'anb_wink', 'name': 'Wink', 'url': 'https://production-vidaa-fhd.wink.ru/',
     'text': 'Цифровой видеосервис компании «Ростелеком»'},
    {'appid': 'anb_kion', 'name': 'Кион', 'url': 'http://hkion.kion.ru/',
     'text': 'Российская мультимедийная онлайн-платформа, созданная компанией МТС'},
    {'appid': 'anb_ssiptv', 'name': 'ssiptv', 'url': 'http://app.ss-iptv.com',
     'text': 'Медиа сервер для просмотра фильмов, сериалов, мультфильмов и пр.'},
    {'appid': 'anb_icva', 'name': 'ICVA', 'url': 'http://icva.mx/',
     'text': 'ICVA - новое приложение для просмотра IPTV каналов'},
    {'appid': 'anb_tvap', 'name': 'TVap', 'url': 'http://tvphone.site/',
     'text': 'TVap - просмотр IPTV каналов на Smart TV'},
    {'appid': 'anb_peers', 'name': 'PeersTV', 'url': 'http://smarttv.peers.tv/hisense/hisense-1.0.0/',
     'text': 'Бесплатное приложение для просмотра ТВ онлайн и в записи. Лайт версия без рекламы'},
    {'appid': 'anb_bonus', 'name': 'Бонус ТВ', 'url': 'http://app.bonus-tv.ru/lg/',
     'text': 'Телевидение онлайн на смартфоне, планшете, Smart-телевизоре или ТВ-приставке.'},
    {'appid': 'anb_amediateka', 'name': 'Aмедиатека', 'url': 'https://smarttv-stable.amediateka.tech/hisense/',
     'text': 'Онлайн-сервис Амедиатека и телеканалы AMEDIA TV. Лучшие сериалы планеты'},
    {'appid': 'anb_prisma', 'name': 'Prisma', 'url': 'http://prisma.ws/',
     'text': 'Полностью готовый к работе форк Lampa.'},
    {'appid': 'anb_gets', 'name': 'GetsTV', 'url': 'https://getstv.com/app/',
     'text': 'Приложение для просмотра ТВ, фильмов и сериалов.'},
    {'appid': 'anb_ottplay_mod', 'name': 'OTT-Play FOSS', 'url': 'http://ott.prog4food.eu.org/f/',
     'text': ' Moд iptv плеера Ott-Play by Alex. Отсутствие баннеров и блокировки каналов.'},
    {'appid': 'anb_kinopub', 'name': 'KinoPubTV', 'url': 'http://cdnservices.link',
     'text': 'Неофициальный клиент для популярного онлайн-кинотеатра'},
    {'appid': 'anb_lampaun', 'name': 'ByLampa', 'url': 'http://bylampa.online/',
     'text': 'Неофициальный форк онлайн-кинотеатра Lampa'},
    {'appid': 'anb_lampaland', 'name': 'Lampa.land', 'url': 'http://lampa.land',
     'text': 'Проект, созданный для тех, кто не может самостоятельно настроить приложение Lampa'},
    {'appid': 'anb_iptvportal', 'name': 'IPTVPORTAL', 'url': 'http://go.iptvportal.ru/?screen=1280x720&user-agent=lg',
     'text': 'Просмотр IPTV из сетей провайдеров, подключенных к платформе IPTVPORTAL'},
    {'appid': 'anb_oneplayer', 'name': 'Oneplayer', 'url': 'http://webos.oneplayer.me/',
     'text': 'Интернет-плеер с широким функционалом'},
    {'appid': 'anb_clouddy', 'name': 'ClouDDy', 'url': 'http://player.clouddy.online/',
     'text': 'Продвинутый и удобный медиаплеер для воспроизведения вашего любимого медиаконтента.'},
    {'appid': 'anb_smotreshka', 'name': 'Смотрешка',
     'url': 'https://smotreshka.webapp.lfstrm.tv/loaders/vidaa/index.html',
     'text': 'Современное интерактивное телевидение'},
    {'appid': 'anb_ivikids', 'name': 'IVI детям', 'url': 'http://lgkids.ivi.ru',
     'text': 'Приложение, сделанное специально для детей! Мультики, фильмы и сериалы'},
    {'appid': 'anb_viloud', 'name': 'Viloud',
     'url': 'https://app.viloud.tv//smarttv//v2//?associate=fox-a5f1&app=ef2b1dd758eb0fcc065561e1275e4af6#viloud',
     'text': 'Самая Простая и Доступная Онлайн-Видеоплатформа'},
    {'appid': 'anb_vevo', 'name': 'Vevo', 'url': 'https://hisense.vevo.com',
     'text': 'Музыкальное видео от крупнейших звукозаписывающих корпораций'},
    {'appid': 'anb_webvideocast2', 'name': 'Web Video Cast', 'url': 'http://vewd.webvideocaster.com/',
     'text': 'Позволяет вам транслировать любое видео, найденное на веб-сайтах, на ваш телевизор.'},
    {'appid': 'anb_sweet', 'name': 'sweet.tv', 'url': 'http://foxxum240.sweet.tv',
     'text': 'Бесплатное онлайн телевидение в хорошем качестве. Телеканалы в прямом эфире и в записи!'},
    {'appid': 'anb_stranafm', 'name': 'Страна FM', 'url': 'http://stranafm.bonus-tv.ru/stranafm/nettv/',
     'text': 'Страна FM — российский коммерческий развлекательный телеканал. Музыка нон стоп'},
    {'appid': 'anb_premier', 'name': 'PREMIER', 'url': 'https://hisensesmarttv.premier.one/hisense/#/main',
     'text': 'ТНТ премьер. Новые русские сериалы, фильмы и шоу.'},
    {'appid': 'anb_mytuner', 'name': 'myTuner Radio', 'url': 'https://devices.mytuner.mobi/?utm_source=Foxxum',
     'text': 'Удобное прослушивание более 30 000 популярных радиостанций 120 стран мира'},
    {'appid': 'anb_zaycev', 'name': 'Zaycev FM', 'url': 'https://tv.zaycev.fm/index.html',
     'text': 'Любимая музыка теперь всегда будет с вами вместе с онлайн радио Zaycev.fm!'},
    {'appid': 'anb_ctc', 'name': 'СТС', 'url': 'http://smarttv.ctc.ru',
     'text': 'Все самые интересные сериалы, популярные программы и мультфильмы телеканала СТС'},
    {'appid': 'anb_siptv', 'name': 'Smart IPTV', 'url': 'http://opera.siptv.eu',
     'text': 'Play IPTV streams, videos on your Smart TV'},
    {'appid': 'anb_ttktv', 'name': 'ТТК ТВ', 'url': 'http://eltex-web.ls.tv.ttk.ru',
     'text': 'Приложение для просмотра любимых фильмов, сериалов, мультфильмов и телевизионных программ'},
    {'appid': 'anb_sibseti', 'name': 'Tв Сибсети', 'url': 'http://smarty.nsk.211.ru',
     'text': 'IPTV для абонентов Сибсети. Создай свой личный медиацентр с нашим приложением!'},
    {'appid': 'anb_zefirtv', 'name': 'Зефир ТВ', 'url': 'http://webkit.zt.platform24.tv/',
     'text': 'ТВ-каналы, фильмы, сериалы, спорт'},
    {'appid': 'anb_smotrim', 'name': 'Смотрим', 'url': 'https://tv.smotrim.ru/',
     'text': 'Новости, ток-шоу, документальные и художественные фильмы, телесериалы и пр.'},
    {'appid': 'anb_moovi', 'name': 'moovi',
     'url': 'http://base.portal.moovi-iptv.ru/ui/1280/index.html?rand=0.3412177627522204',
     'text': 'Кабельное Телевидение Moovi. Современный формат цифрового телевидения.'},
    {'appid': 'anb_tvoe', 'name': 'TVOE', 'url': 'https://app.tvoe.live?device=smart-tv&installed=vidaa',
     'text': 'Тысячи фильмов и сериалов'},
    {'appid': 'anb_emby', 'name': 'Emby', 'url': 'http://tv.emby.media/',
     'text': 'Медиа-сервер и домашний кинотеатр. Позволяет скачивать фильмы, сериалы и добавлять их в каталог.'},
    {'appid': 'anb_24_1', 'name': '24tv', 'url': 'http://webkit.24h.tv',
     'text': '24ТВ Всё ТВ и кинотеатры в одном приложении'},
    {'appid': 'anb_IDC', 'name': 'IDC Smart TV', 'url': 'https://smart.iptv.idc.md',
     'text': 'Приложение от крупнейшего телекоммуникационного оператора на территории Приднестровья'},
    {'appid': 'anb_stremio', 'name': 'Stremio', 'url': 'https://tv.strem.io',
     'text': 'Stremio – программа для просмотра видео-контента различных известных онлайн-сервисов'},
    {'appid': 'anb_tytkino', 'name': 'Тут Кино', 'url': 'http://fork-p0rtal.ru/project/',
     'text': 'Виджет для SmartTV от fork-portal.ru на движке VPlay.'},
    {'appid': 'anb_impareboom', 'name': 'ИмперияBOOM', 'url': 'http://web.imboom.ru/',
     'text': 'Твой HD кинотеатр. Новинки кино и сериалы без навязчивой рекламы'},
    {'appid': 'anb_djin', 'name': 'HDGO', 'url': 'http://hdgo.me/',
     'text': 'Полностью готовый к работе форк Lampa Lite'},
    {'appid': 'anb_popkorn', 'name': 'Попкорн', 'url': 'https://tv-desktop.beepopcorn.ru',
     'text': 'Бесплатное ТВ, фильмы, сериалы, видеоблоги и караоке'},
    {'appid': 'anb_filmix', 'name': 'Filmix', 'url': 'http://filmix.tv',
     'text': 'Приложение для просмотра фильмов и сериалов с популярного онлайн кинотеатра filmix.tv'},
    {'appid': 'anb_akter', 'name': 'AKTER BLACK', 'url': 'http://abvidaa.ru',
     'text': 'Уютное киноубежище - онлайн кинотеатр AKTER BLACK'},
    {'appid': 'anb_movix', 'name': 'Movix', 'url': 'http://cdn.smarttv.domru.ru/hisense/',
     'text': 'Устройте онлайн-кинотеатр у себя дома вместе с Movix!'},
    {'appid': 'anb_jellyfin', 'name': 'jellyfin', 'url': 'https://jellyfin-vidaa.vercel.app',
     'text': 'Бесплатный и свободный медиасервер'},
    {'appid': 'anb_farlinetv', 'name': 'Фарлайн ТВ', 'url': 'http://tv.farline.net',
     'text': 'Смотрите наше интерактивное телевидение онлайн в любое удобное для вас время! Фильмы, мультфильмы, шоу и новости.'},
    {'appid': 'anb_sevstartv', 'name': 'Севстар Tв', 'url': 'http://tvs.sevstar.net',
     'text': 'Приложение для просмотра пакетов Цифрового телевидения от компании Севстар'},
    {'appid': 'anb_focustv', 'name': 'Фокус Лайф', 'url': 'http://tv.focus.life/',
     'text': 'Приложение для просмотра пакетов Цифрового телевидения от компании Фокус Лайф'},
    {'appid': 'spotify', 'name': 'Spotify', 'url': 'https://open.spotify.com/',
     'text': 'Spotify'},
]  # Конец HISENSE_APP_LIST

UI_IMAGE_BASE_URL = 'https://vidaa.surge.sh/images_ui/'
THUMBNAIL_BASE_URL = 'http://195.58.50.236/'
IMAGE_FOLDER_PREFIXES = ['images/', 'img/']

from app.main import BASE_DIR

STATIC_DIR = os.path.join(BASE_DIR, "static")
IMAGES_DIR = os.path.join(STATIC_DIR, "images")
# --- Конфигурация для нового скрипта ---
OUTPUT_DIR_BASE = os.path.join(IMAGES_DIR, "hisense_icons_collection_v4")
OUTPUT_DIR_UI = os.path.join(OUTPUT_DIR_BASE, 'ui_icons')
OUTPUT_DIR_THUMBNAILS = os.path.join(OUTPUT_DIR_BASE, 'thumbnail_icons')

TARGET_SIZE_HISENSE = (512, 512)
USER_AGENT_HISENSE = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
HEADERS_HISENSE = {'User-Agent': USER_AGENT_HISENSE}


def ensure_output_directories():
    for path_dir in [OUTPUT_DIR_UI, OUTPUT_DIR_THUMBNAILS]:
        if not os.path.exists(path_dir):
            os.makedirs(path_dir)
    print(f"Иконки UI будут сохранены в: {os.path.abspath(OUTPUT_DIR_UI)}")
    print(f"Иконки Thumbnail будут сохранены в: {os.path.abspath(OUTPUT_DIR_THUMBNAILS)}")


def enhance_and_save_image(image_bytes, final_filepath, appid_for_log):
    """
    Обрабатывает скачанные байты изображения (Pillow) и сохраняет.
    Включает обрезку, приведение к квадрату, изменение размера и увеличение резкости.
    """
    try:
        img = Image.open(io.BytesIO(image_bytes))

        if img.mode not in ('RGBA', 'LA'):  # Обеспечиваем RGBA для прозрачности
            img = img.convert('RGBA')
        else:
            # Если уже RGBA или LA (Luminance + Alpha), убедимся, что альфа-канал используется правильно
            # Иногда PNG могут быть в режиме 'P' с палитрой и маской прозрачности. img.convert('RGBA') это учтет.
            pass

        # 1. Автоматическая обрезка лишней прозрачности
        if img.mode == 'RGBA':
            try:
                bbox = img.getbbox()  # Получаем (left, upper, right, lower) для непрозрачной части
                if bbox:
                    print(f"Инфо ({appid_for_log}): Обнаружен bbox для обрезки: {bbox} для {final_filepath}")
                    img = img.crop(bbox)
                else:
                    # Это может случиться, если изображение полностью прозрачное
                    print(
                        f"Предупреждение ({appid_for_log}): Изображение полностью прозрачное или bbox не найден для {final_filepath}. Обрезка пропущена.")
            except Exception as e_crop:
                print(
                    f"Предупреждение ({appid_for_log}): Ошибка при попытке обрезки изображения {final_filepath}: {e_crop}")

        width, height = img.size
        if width == 0 or height == 0:  # После обрезки полностью прозрачного изображения
            print(
                f"Ошибка ({appid_for_log}): Размеры изображения нулевые после обрезки для {final_filepath}. Сохранение невозможно.")
            return False

        # 2. Приведение к квадратному виду (с прозрачным фоном)
        if width != height:
            max_dim = max(width, height)
            new_img_square = Image.new('RGBA', (max_dim, max_dim), (0, 0, 0, 0))  # Прозрачный фон
            paste_x = (max_dim - width) // 2
            paste_y = (max_dim - height) // 2
            # При вставке RGBA на RGBA, маска используется автоматически из альфа-канала img
            new_img_square.paste(img, (paste_x, paste_y), img if img.mode == 'RGBA' else None)
            img = new_img_square

        # 3. Изменение размера
        img = img.resize(TARGET_SIZE_HISENSE, Image.Resampling.LANCZOS)

        # 4. Увеличение резкости (опционально, но может улучшить вид)
        try:
            img = img.filter(ImageFilter.SHARPEN)
        except Exception as e_sharpen:
            print(
                f"Предупреждение ({appid_for_log}): Не удалось применить фильтр резкости для {final_filepath}: {e_sharpen}")

        img.save(final_filepath, 'PNG')
        print(f"Успех ({appid_for_log}): Иконка обработана и сохранена: {final_filepath}")
        return True

    except Exception as e_pil:
        print(
            f"Ошибка ({appid_for_log}): Ошибка Pillow при обработке для {final_filepath}: {e_pil}. Попытка сохранить 'как есть', если это PNG.")
        # Попытка сохранить "сырые" байты, если URL указывал на PNG
        # и обработка Pillow не удалась на раннем этапе (до save).
        # В данной функции это менее вероятно, т.к. img.save() является частью try.
        # Эта логика больше подходила для download_hisense_image_attempt
        # Если Image.open(io.BytesIO(image_bytes)) не удался, мы сюда не дойдем.
        # Если URL не PNG, то сохранять сырые байты как PNG не стоит.
        # Для простоты, если основная обработка не удалась, считаем это ошибкой.
        return False


def download_and_process_hisense_image(url, output_dir, filename_base, appid_for_log, source_suffix_for_filename):
    """
    Скачивает изображение, формирует полный путь и вызывает enhance_and_save_image.
    """
    final_filename = f"{filename_base}_{source_suffix_for_filename}.png"
    final_filepath = os.path.join(output_dir, final_filename)

    if os.path.exists(final_filepath):
        print(f"Инфо ({appid_for_log}): Файл {final_filepath} уже существует. Пропуск ({source_suffix_for_filename}).")
        return True  # Считаем успехом, так как файл уже есть

    print(f"Инфо ({appid_for_log}): Попытка загрузки ({source_suffix_for_filename}): {url}")
    try:
        response = requests.get(url, headers=HEADERS_HISENSE, timeout=20, stream=True)  # Увеличил таймаут
        if response.status_code == 200:
            image_bytes = response.content
            if not image_bytes:
                print(
                    f"Предупреждение ({appid_for_log}): Получен пустой ответ от {url} для {source_suffix_for_filename}.")
                return False

            # Проверяем Content-Type, чтобы убедиться, что это изображение, прежде чем передавать в Pillow
            content_type = response.headers.get('content-type', '').lower()
            if not content_type.startswith('image/'):
                print(
                    f"Предупреждение ({appid_for_log}): Content-Type '{content_type}' не является изображением для URL {url}. Пропуск.")
                return False

            return enhance_and_save_image(image_bytes, final_filepath, appid_for_log)
        elif response.status_code == 404:
            print(f"Инфо ({appid_for_log}): Файл не найден (404) по URL ({source_suffix_for_filename}): {url}")
            return False
        else:
            print(
                f"Ошибка ({appid_for_log}): Не удалось скачать ({source_suffix_for_filename}) {url} (статус: {response.status_code})")
            return False
    except requests.exceptions.Timeout:
        print(f"Ошибка ({appid_for_log}): Таймаут при загрузке ({source_suffix_for_filename}) {url}.")
        return False
    except requests.exceptions.RequestException as e:
        print(f"Ошибка ({appid_for_log}): Ошибка сети при загрузке ({source_suffix_for_filename}) {url}. {e}")
        return False
    except Exception as e_general:
        print(
            f"Ошибка ({appid_for_log}): Непредвиденная ошибка при работе с ({source_suffix_for_filename}) {url}. {e_general}")
        return False


def fetch_all_hisense_icons():
    ensure_output_directories()  # Создаем обе папки вывода

    total_apps = len(HISENSE_APP_LIST)
    print(f"Начинаем обработку {total_apps} приложений из списка Hisense...")

    successful_saves_count = 0

    for i, app_data in enumerate(HISENSE_APP_LIST):
        js_appid = app_data.get('appid')
        app_name = app_data.get('name', 'UnknownApp')

        if not js_appid:
            print(f"Предупреждение: Пропуск записи #{i + 1} из-за отсутствия 'appid': {app_data}")
            continue

        print(f"\n--- Обработка [{i + 1}/{total_apps}]: {app_name} ({js_appid}) ---")

        # 1. UI Icon (источник 'ui') -> папка OUTPUT_DIR_UI
        ui_icon_url = f"{UI_IMAGE_BASE_URL}{js_appid}.png"
        if download_and_process_hisense_image(ui_icon_url, OUTPUT_DIR_UI, js_appid, appid_for_log=js_appid,
                                              source_suffix_for_filename="ui"):
            successful_saves_count += 1

        # 2. Thumbnail Icons -> папка OUTPUT_DIR_THUMBNAILS
        for prefix_folder in IMAGE_FOLDER_PREFIXES:
            thumb_type_suffix = prefix_folder.replace('/', '')  # 'images' или 'img'
            thumb_url = f"{THUMBNAIL_BASE_URL}{prefix_folder}{js_appid}.png"
            if download_and_process_hisense_image(thumb_url, OUTPUT_DIR_THUMBNAILS, js_appid, appid_for_log=js_appid,
                                                  source_suffix_for_filename=f"thumb_{thumb_type_suffix}"):
                successful_saves_count += 1

    print(
        f"\n--- Загрузка иконок Hisense завершена. Всего успешно сохранено/обновлено файлов: {successful_saves_count} ---")
    print(f"Проверьте папки: \n  {os.path.abspath(OUTPUT_DIR_UI)} \n  {os.path.abspath(OUTPUT_DIR_THUMBNAILS)}")


if __name__ == '__main__':
    # Установка зависимостей: pip install requests Pillow
    # Убедись, что список HISENSE_APP_LIST в начале скрипта заполнен!

    fetch_all_hisense_icons()