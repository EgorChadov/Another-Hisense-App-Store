from typing import List, Optional
from pydantic import BaseModel, HttpUrl
from enum import Enum

SPECIAL_STORE_TYPE_APPS: List[str] = ['Wink', 'Билайн ТВ', 'TikTok', 'ТТК ТВ']

class Category(str, Enum):
    CINEMA = "Кино и Сериалы"
    IPTV = "IPTV"
    MUSIC = "Музыка и Радио"
    KIDS = "Детям"
    TOOLS = "Инструменты и Плееры"
    TV = "ТВ Каналы"
    OTHER = "Разное"

class App(BaseModel):
    appid: str
    name: str
    url: HttpUrl
    text: str
    category: Category = Category.OTHER
    # icon_filename: Optional[str] = None

APP_LIST: List[App] = [
    App(
        appid='lampa',
        name='Lampa',
        url='http://lampa.mx/',
        text='Lampa для Smart TV',
        category=Category.CINEMA
    ),
    App(
        appid='vokino',
        name='vokino',
        url='http://web.vokino.tv/',
        text='VoKino для Smart TV',
        category=Category.CINEMA
    ),
    App(
        appid='fxml',
        name='Media Station X',
        url='http://msx.benzac.de/foxxum.html',
        text='Создание настраиваемых мультимедийных страниц',
        category=Category.TOOLS
    ),
    App(
        appid='atodo',
        name='Atodo',
        url='http://msx.benzac.de/?start=menu:request:interaction:menu@http://atodo.fun/fun.html',
        text='Каталог приложений Atodo',
        category=Category.OTHER
    ),
    App(
        appid='moovies',
        name='Moovies',
        url='http://msx.benzac.de/?start=menu:request:interaction:init@http://moovies.uz/index.html',
        text='Приложение Moovies для MSX',
        category=Category.CINEMA
    ),
    App(
        appid='movielab',
        name='Movielab',
        url='https://msx.benzac.de/?start=menu:https://movielab.fun/msx/menu.json',
        text='Лучшие фильмы с MovieLab',
        category=Category.CINEMA
    ),
    App(
        appid='deeplex',
        name='DEEPLEX',
        url='http://smart.deeplex.cc/',
        text='Фильмы и сериалы без ограничений',
        category=Category.CINEMA
    ),
    App(
        appid='drmplay',
        name='DRM-play',
        url='http://drm-play.com/',
        text='Ott плеер DRM-play, модификация ott-play by Alex',
        category=Category.IPTV
    ),
    App(
        appid='fork',
        name='ForkPlayer',
        url='http://browser.appfxml.com/',
        text='Браузер с адаптированным просмотром сайтов',
        category=Category.TOOLS
    ),
    App(
        appid='forkbrowser',
        name='Fork Browser',
        url='http://browser.appinfo.su/',
        text='Улучшенная версия ForkPlayer',
        category=Category.TOOLS
    ),
    App(
        appid='lampalite4',
        name='Lampa lite',
        url='http://lite.lampa.mx/',
        text='Lampa Lite: облегченная версия',
        category=Category.CINEMA
    ),
    App(
        appid='twitch',
        name='Twitch',
        url='https://hisense.tv.twitch.tv/',
        text='Twitch.tv',
        category=Category.OTHER
    ),
    App(
        appid='vkvideo',
        name='VK видео',
        url='https://vk.ru/tv-app/lib?version=latest&platform=vidaa',
        text='VK Video на SmartTV',
        category=Category.OTHER
    ),
    App(
        appid='beeline',
        name='Билайн ТВ',
        url='https://smart-vidaa.beeline.tv/',
        text='Фильмы, сериалы, мультфильмы и 300 каналов от beeline.tv',
        category=Category.TV
    ),
    App(
        appid='xsmart',
        name='Xsmart',
        url='http://app.xsmart.tv/?widg=5',
        text='Многофункциональное приложение для Smart TV',
        category=Category.TOOLS
    ),
    App(
        appid='viju',
        name='Viju',
        url='https://smarttv.viju.ru/',
        text='Фильмы, сериалы и мультфильмы по подписке Viju',
        category=Category.CINEMA
    ),
    App(
        appid='tiktok',
        name='TikTok',
        url='https://tv.tiktok.com/webos',
        text='Платформа для коротких видео TikTok',
        category=Category.OTHER
    ),
    App(
        appid='m3uiptv',
        name='M3U IPTV',
        url='https://m3u-ip.tv/lg/',
        text='Загрузка плейлистов IPTV (m3u, m3u8)',
        category=Category.IPTV
    ),
    App(
        appid='kinopoisk',
        name='Кинопоиск',
        url='https://smarttv-app.ott.yandex.ru/?ott-rv=vidaa',
        text='Крупнейший русскоязычный онлайн-кинотеатр',
        category=Category.CINEMA
    ),
    App(
        appid='yandexvideo',
        name='Яндекс видео',
        url='https://yandex.ru/video/tvapp/?ui=tvapp',
        text='Телепередачи, клипы, ролики и популярное на YouTube',
        category=Category.OTHER
    ),
    App(
        appid='ott',
        name='OttPlayer',
        url='http://widget.ottplayer.tv/operatv2/index.html',
        text='Сервис для сбора IP-телевидения',
        category=Category.IPTV
    ),
    App(
        appid='ottold',
        name='OttPlayerTest',
        url='http://widget.ottplayer.tv/test/index.html',
        text='Тестовая версия OttPlayer',
        category=Category.IPTV
    ),
    App(
        appid='wink',
        name='Wink',
        url='https://production-vidaa-fhd.wink.ru/',
        text='Цифровой видеосервис от «Ростелеком»',
        category=Category.TV
    ),
    App(
        appid='kion',
        name='Кион',
        url='http://hkion.kion.ru/',
        text='Российская мультимедийная онлайн-платформа от МТС',
        category=Category.CINEMA
    ),
    App(
        appid='ssiptv',
        name='ssiptv',
        url='http://app.ss-iptv.com/',
        text='Медиасервер для просмотра фильмов и сериалов',
        category=Category.IPTV
    ),
    App(
        appid='icva',
        name='ICVA',
        url='http://icva.mx/',
        text='Новое приложение для просмотра IPTV каналов',
        category=Category.IPTV
    ),
    App(
        appid='tvap',
        name='TVap',
        url='http://tvphone.site/',
        text='Просмотр IPTV каналов на Smart TV',
        category=Category.IPTV
    ),
    App(
        appid='peers',
        name='PeersTV',
        url='http://smarttv.peers.tv/hisense/hisense-1.0.0/',
        text='Бесплатное ТВ онлайн и в записи (лайт версия)',
        category=Category.TV
    ),
    App(
        appid='bonus',
        name='Бонус ТВ',
        url='http://app.bonus-tv.ru/lg/',
        text='Телевидение онлайн на различных устройствах',
        category=Category.TV
    ),
    App(
        appid='amediateka',
        name='Aмедиатека',
        url='https://smarttv-stable.amediateka.tech/hisense/',
        text='Онлайн-сервис Амедиатека и телеканалы AMEDIA TV',
        category=Category.CINEMA
    ),
    App(
        appid='prisma',
        name='Prisma',
        url='http://prisma.ws/',
        text='Готовый к работе форк Lampa',
        category=Category.CINEMA
    ),
    App(
        appid='gets',
        name='GetsTV',
        url='https://getstv.com/app/',
        text='Приложение для просмотра ТВ, фильмов и сериалов',
        category=Category.CINEMA
    ),
    App(
        appid='ottplay_mod',
        name='OTT-Play FOSS',
        url='http://ott.prog4food.eu.org/f/',
        text='Мод IPTV плеера Ott-Play by Alex, без баннеров',
        category=Category.IPTV
    ),
    App(
        appid='kinopub',
        name='KinoPubTV',
        url='http://cdnservices.link/',
        text='Неофициальный клиент для KinoPub',
        category=Category.CINEMA
    ),
    App(
        appid='lampaun',
        name='ByLampa',
        url='http://bylampa.online/',
        text='Неофициальный форк онлайн-кинотеатра Lampa',
        category=Category.CINEMA
    ),
    App(
        appid='lampaland',
        name='Lampa.land',
        url='http://lampa.land/',
        text='Проект для тех, кто не может настроить Lampa',
        category=Category.CINEMA
    ),
    App(
        appid='oneplayer',
        name='Oneplayer',
        url='http://webos.oneplayer.me/',
        text='Интернет-плеер с широким функционалом.',
        category=Category.TOOLS
    ),
    App(
        appid='clouddy',
        name='ClouDDy',
        url='http://player.clouddy.online/',
        text='Продвинутый медиаплеер для вашего контента.',
        category=Category.TOOLS
    ),
    App(
        appid='smotreshka',
        name='Смотрешка',
        url='https://smotreshka.webapp.lfstrm.tv/loaders/vidaa/index.html',
        text='Современное интерактивное телевидение.',
        category=Category.TV
    ),
    App(
        appid='ivikids',
        name='IVI детям',
        url='http://lgkids.ivi.ru/',
        text='Приложение для детей: мультики, фильмы, сериалы.',
        category=Category.KIDS
    ),
    App(
        appid='vevo',
        name='Vevo',
        url='https://hisense.vevo.com/',
        text='Музыкальные видео',
        category=Category.MUSIC
    ),
    App(
        appid='webvideocast2',
        name='Web Video Cast',
        url='http://vewd.webvideocaster.com/',
        text='Трансляция видео с веб-сайтов на телевизор',
        category=Category.TOOLS
    ),
    App(
        appid='sweet',
        name='sweet.tv',
        url='http://foxxum240.sweet.tv/',
        text='Бесплатное онлайн ТВ в хорошем качестве, в эфире и в записи',
        category=Category.TV
    ),
    App(
        appid='stranafm',
        name='Страна FM',
        url='http://stranafm.bonus-tv.ru/stranafm/nettv/',
        text='Музыка нон-стоп',
        category=Category.MUSIC
    ),
    App(
        appid='premier',
        name='PREMIER',
        url='https://hisensesmarttv.premier.one/hisense/#/main',
        text='ТНТ Премьер: новые русские сериалы, фильмы, шоу',
        category=Category.CINEMA
    ),
    App(
        appid='mytuner',
        name='myTuner Radio',
        url='https://devices.mytuner.mobi/?utm_source=Foxxum',
        text='Более 30 000 радиостанций из 120 стран.',
        category=Category.MUSIC
    ),
    App(
        appid='zaycev',
        name='Zaycev FM',
        url='https://tv.zaycev.fm/index.html',
        text='Любимая музыка с онлайн радио Zaycev.fm.',
        category=Category.MUSIC
    ),
    App(
        appid='ctc',
        name='СТС',
        url='http://smarttv.ctc.ru/',
        text='Сериалы, программы и мультфильмы телеканала СТС.',
        category=Category.TV
    ),
    App(
        appid='siptv',
        name='Smart IPTV',
        url='http://opera.siptv.eu/',
        text='Воспроизведение IPTV потоков и видео на Smart TV.',
        category=Category.IPTV
    ),
    App(
        appid='smotrim',
        name='Смотрим',
        url='https://tv.smotrim.ru/',
        text='Новости, ток-шоу, фильмы, сериалы.',
        category=Category.TV
    ),
    App(
        appid='tvoe',
        name='TVOE',
        url='https://app.tvoe.live/?device=smart-tv&installed=vidaa',
        text='Тысячи фильмов и сериалов.',
        category=Category.CINEMA
    ),
    App(
        appid='emby',
        name='Emby',
        url='http://tv.emby.media/',
        text='Медиа-сервер и домашний кинотеатр. Каталогизация.',
        category=Category.TOOLS
    ),
    App(
        appid='stremio',
        name='Stremio',
        url='https://tv.strem.io/',
        text='Просмотр видео-контента различных онлайн-сервисов.',
        category=Category.CINEMA
    ),
    App(
        appid='tytkino',
        name='Тут Кино',
        url='http://fork-p0rtal.ru/project/',
        text='Виджет для SmartTV от fork-portal.ru на VPlay.',
        category=Category.CINEMA
    ),
    App(
        appid='impareboom',
        name='ИмперияBOOM',
        url='http://web.imboom.ru/',
        text='HD кинотеатр. Новинки кино и сериалы без рекламы.',
        category=Category.CINEMA
    ),
    App(
        appid='hdgo',
        name='HDGO',
        url='http://hdgo.me/',
        text='Готовый к работе форк Lampa Lite.',
        category=Category.CINEMA
    ),
    App(
        appid='popkorn',
        name='Попкорн',
        url='https://tv-desktop.beepopcorn.ru/',
        text='Бесплатное ТВ, фильмы, сериалы, видеоблоги, караоке.',
        category=Category.CINEMA
    ),
    App(
        appid='filmix',
        name='Filmix',
        url='http://filmix.tv/',
        text='Фильмы и сериалы с онлайн кинотеатра filmix.tv.',
        category=Category.CINEMA
    ),
    App(
        appid='akter',
        name='AKTER BLACK',
        url='http://abvidaa.ru/',
        text='Уютный онлайн кинотеатр AKTER BLACK.',
        category=Category.CINEMA
    ),
    App(
        appid='jellyfin',
        name='jellyfin',
        url='https://jellyfin-vidaa.vercel.app/',
        text='Бесплатный и свободный медиасервер.',
        category=Category.TOOLS
    ),
    App(
        appid='spotify',
        name='spotify',
        url='https://open.spotify.com/',
        text='Spotify Web App.',
        category=Category.MUSIC
    ),
]
