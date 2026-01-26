from typing import List, Optional
from pydantic import BaseModel, HttpUrl

SPECIAL_STORE_TYPE_APPS: List[str] = ['Wink', 'Билайн ТВ', 'TikTok', 'ТТК ТВ']

class App(BaseModel):
    appid: str
    name: str
    url: HttpUrl
    text: str
    # icon_filename: Optional[str] = None

APP_LIST: List[App] = [
    App(
        appid='lampa',
        name='Lampa',
        url='http://lampa.mx/',
        text='Lampa для Smart TV'
    ),
    App(
        appid='vokino',
        name='vokino',
        url='http://web.vokino.tv/',
        text='VoKino для Smart TV'
    ),
    App(
        appid='fxml',
        name='Media Station X',
        url='http://msx.benzac.de/foxxum.html',
        text='Создание настраиваемых мультимедийных страниц'
    ),
    App(
        appid='atodo',
        name='Atodo',
        url='http://msx.benzac.de/?start=menu:request:interaction:menu@http://atodo.fun/fun.html',
        text='Каталог приложений Atodo'
    ),
    App(
        appid='moovies',
        name='Moovies',
        url='http://msx.benzac.de/?start=menu:request:interaction:init@http://moovies.uz/index.html',
        text='Приложение Moovies для MSX'
    ),
    App(
        appid='movielab',
        name='Movielab',
        url='https://msx.benzac.de/?start=menu:https://movielab.fun/msx/menu.json',
        text='Лучшие фильмы с MovieLab'
    ),
    App(
        appid='deeplex',
        name='DEEPLEX',
        url='http://smart.deeplex.cc/',
        text='Фильмы и сериалы без ограничений'
    ),
    App(
        appid='drmplay',
        name='DRM-play',
        url='http://drm-play.com/',
        text='Ott плеер DRM-play, модификация ott-play by Alex'
    ),
    App(
        appid='fork',
        name='ForkPlayer',
        url='http://browser.appfxml.com/',
        text='Браузер с адаптированным просмотром сайтов'
    ),
    App(
        appid='forkbrowser',
        name='Fork Browser',
        url='http://browser.appinfo.su/',
        text='Улучшенная версия ForkPlayer'
    ),
    App(
        appid='lampalite4',
        name='Lampa lite',
        url='http://lite.lampa.mx/',
        text='Lampa Lite: облегченная версия'
    ),
    App(
        appid='twitch',
        name='Twitch',
        url='https://hisense.tv.twitch.tv/',
        text='Twitch.tv'
    ),
    App(
        appid='vkvideo',
        name='VK видео',
        url='https://vk.ru/tv-app/lib?version=latest&platform=vidaa',
        text='VK Video на SmartTV'
    ),
    App(
        appid='beeline',
        name='Билайн ТВ',
        url='https://smart-vidaa.beeline.tv/',
        text='Фильмы, сериалы, мультфильмы и 300 каналов от beeline.tv'
    ),
    App(
        appid='xsmart',
        name='Xsmart',
        url='http://app.xsmart.tv/?widg=5',
        text='Многофункциональное приложение для Smart TV'
    ),
    App(
        appid='viju',
        name='Viju',
        url='https://smarttv.viju.ru/',
        text='Фильмы, сериалы и мультфильмы по подписке Viju'
    ),
    App(
        appid='tiktok',
        name='TikTok',
        url='https://tv.tiktok.com/webos',
        text='Платформа для коротких видео TikTok'
    ),
    App(
        appid='m3uiptv',
        name='M3U IPTV',
        url='https://m3u-ip.tv/lg/',
        text='Загрузка плейлистов IPTV (m3u, m3u8)'
    ),
    App(
        appid='kinopoisk',
        name='Кинопоиск',
        url='https://smarttv-app.ott.yandex.ru/?ott-rv=vidaa',
        text='Крупнейший русскоязычный онлайн-кинотеатр'
    ),
    App(
        appid='yandexvideo',
        name='Яндекс видео',
        url='https://yandex.ru/video/tvapp/?ui=tvapp',
        text='Телепередачи, клипы, ролики и популярное на YouTube'
    ),
    App(
        appid='ott',
        name='OttPlayer',
        url='http://widget.ottplayer.tv/operatv2/index.html',
        text='Сервис для сбора IP-телевидения'
    ),
    App(
        appid='ottold',
        name='OttPlayerTest',
        url='http://widget.ottplayer.tv/test/index.html',
        text='Тестовая версия OttPlayer'
    ),
    App(
        appid='wink',
        name='Wink',
        url='https://production-vidaa-fhd.wink.ru/',
        text='Цифровой видеосервис от «Ростелеком»'
    ),
    App(
        appid='kion',
        name='Кион',
        url='http://hkion.kion.ru/',
        text='Российская мультимедийная онлайн-платформа от МТС'
    ),
    App(
        appid='ssiptv',
        name='ssiptv',
        url='http://app.ss-iptv.com/',
        text='Медиасервер для просмотра фильмов и сериалов'
    ),
    App(
        appid='icva',
        name='ICVA',
        url='http://icva.mx/',
        text='Новое приложение для просмотра IPTV каналов'
    ),
    App(
        appid='tvap',
        name='TVap',
        url='http://tvphone.site/',
        text='Просмотр IPTV каналов на Smart TV'
    ),
    App(
        appid='peers',
        name='PeersTV',
        url='http://smarttv.peers.tv/hisense/hisense-1.0.0/',
        text='Бесплатное ТВ онлайн и в записи (лайт версия)'
    ),
    App(
        appid='bonus',
        name='Бонус ТВ',
        url='http://app.bonus-tv.ru/lg/',
        text='Телевидение онлайн на различных устройствах'
    ),
    App(
        appid='amediateka',
        name='Aмедиатека',
        url='https://smarttv-stable.amediateka.tech/hisense/',
        text='Онлайн-сервис Амедиатека и телеканалы AMEDIA TV'
    ),
    App(
        appid='prisma',
        name='Prisma',
        url='http://prisma.ws/',
        text='Готовый к работе форк Lampa'
    ),
    App(
        appid='gets',
        name='GetsTV',
        url='https://getstv.com/app/',
        text='Приложение для просмотра ТВ, фильмов и сериалов'
    ),
    App(
        appid='ottplay_mod',
        name='OTT-Play FOSS',
        url='http://ott.prog4food.eu.org/f/',
        text='Мод IPTV плеера Ott-Play by Alex, без баннеров'
    ),
    App(
        appid='kinopub',
        name='KinoPubTV',
        url='http://cdnservices.link/',
        text='Неофициальный клиент для KinoPub'
    ),
    App(
        appid='lampaun',
        name='ByLampa',
        url='http://bylampa.online/',
        text='Неофициальный форк онлайн-кинотеатра Lampa'
    ),
    App(
        appid='lampaland',
        name='Lampa.land',
        url='http://lampa.land/',
        text='Проект для тех, кто не может настроить Lampa'
    ),
    App(
        appid='oneplayer',
        name='Oneplayer',
        url='http://webos.oneplayer.me/',
        text='Интернет-плеер с широким функционалом.'
    ),
    App(
        appid='clouddy',
        name='ClouDDy',
        url='http://player.clouddy.online/',
        text='Продвинутый медиаплеер для вашего контента.'
    ),
    App(
        appid='smotreshka',
        name='Смотрешка',
        url='https://smotreshka.webapp.lfstrm.tv/loaders/vidaa/index.html',
        text='Современное интерактивное телевидение.'
    ),
    App(
        appid='ivikids',
        name='IVI детям',
        url='http://lgkids.ivi.ru/',
        text='Приложение для детей: мультики, фильмы, сериалы.'
    ),
    App(
        appid='vevo',
        name='Vevo',
        url='https://hisense.vevo.com/',
        text='Музыкальные видео'
    ),
    App(
        appid='webvideocast2',
        name='Web Video Cast',
        url='http://vewd.webvideocaster.com/',
        text='Трансляция видео с веб-сайтов на телевизор'
    ),
    App(
        appid='sweet',
        name='sweet.tv',
        url='http://foxxum240.sweet.tv/',
        text='Бесплатное онлайн ТВ в хорошем качестве, в эфире и в записи'
    ),
    App(
        appid='stranafm',
        name='Страна FM',
        url='http://stranafm.bonus-tv.ru/stranafm/nettv/',
        text='Музыка нон-стоп'
    ),
    App(
        appid='premier',
        name='PREMIER',
        url='https://hisensesmarttv.premier.one/hisense/#/main',
        text='ТНТ Премьер: новые русские сериалы, фильмы, шоу'
    ),
    App(
        appid='mytuner',
        name='myTuner Radio',
        url='https://devices.mytuner.mobi/?utm_source=Foxxum',
        text='Более 30 000 радиостанций из 120 стран.'
    ),
    App(
        appid='zaycev',
        name='Zaycev FM',
        url='https://tv.zaycev.fm/index.html',
        text='Любимая музыка с онлайн радио Zaycev.fm.'
    ),
    App(
        appid='ctc',
        name='СТС',
        url='http://smarttv.ctc.ru/',
        text='Сериалы, программы и мультфильмы телеканала СТС.'
    ),
    App(
        appid='siptv',
        name='Smart IPTV',
        url='http://opera.siptv.eu/',
        text='Воспроизведение IPTV потоков и видео на Smart TV.'
    ),
    App(
        appid='smotrim',
        name='Смотрим',
        url='https://tv.smotrim.ru/',
        text='Новости, ток-шоу, фильмы, сериалы.'
    ),
    App(
        appid='tvoe',
        name='TVOE',
        url='https://app.tvoe.live/?device=smart-tv&installed=vidaa',
        text='Тысячи фильмов и сериалов.'
    ),
    App(
        appid='emby',
        name='Emby',
        url='http://tv.emby.media/',
        text='Медиа-сервер и домашний кинотеатр. Каталогизация.'
    ),
    App(
        appid='stremio',
        name='Stremio',
        url='https://tv.strem.io/',
        text='Просмотр видео-контента различных онлайн-сервисов.'
    ),
    App(
        appid='tytkino',
        name='Тут Кино',
        url='http://fork-p0rtal.ru/project/',
        text='Виджет для SmartTV от fork-portal.ru на VPlay.'
    ),
    App(
        appid='impareboom',
        name='ИмперияBOOM',
        url='http://web.imboom.ru/',
        text='HD кинотеатр. Новинки кино и сериалы без рекламы.'
    ),
    App(
        appid='hdgo',
        name='HDGO',
        url='http://hdgo.me/',
        text='Готовый к работе форк Lampa Lite.'
    ),
    App(
        appid='popkorn',
        name='Попкорн',
        url='https://tv-desktop.beepopcorn.ru/',
        text='Бесплатное ТВ, фильмы, сериалы, видеоблоги, караоке.'
    ),
    App(
        appid='filmix',
        name='Filmix',
        url='http://filmix.tv/',
        text='Фильмы и сериалы с онлайн кинотеатра filmix.tv.'
    ),
    App(
        appid='akter',
        name='AKTER BLACK',
        url='http://abvidaa.ru/',
        text='Уютный онлайн кинотеатр AKTER BLACK.'
    ),
    App(
        appid='jellyfin',
        name='jellyfin',
        url='https://jellyfin-vidaa.vercel.app/',
        text='Бесплатный и свободный медиасервер.'
    ),
    App(
        appid='spotify',
        name='spotify',
        url='https://open.spotify.com/',
        text='Spotify Web App.'
    ),
]
