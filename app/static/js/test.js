/**
 * Deobfuscated Script for Hisense VIDAA App Management Utility
 *
 * Original script likely managed apps, handled unlocking via key sequences,
 * offered debugging tools, and theme customization on Hisense TVs.
 *
 * Requires: jQuery library, Hisense specific APIs (Hisense_*, omi_platform, HiBrowser)
 */

// --- Initial Definitions & Configuration ---
var N_DECRYPT_OFFSET = 111; // Offset used in Hisense_Decrypt fallback key generation
var DATE_KEY_APP_INDEX = 3; // 1-based index of the app requiring the Date/MAP key sequence (Lampa)

// List of applications to display
var APP_LIST = [
    { appid: 'anb_lampa', name: 'Lampa', url: 'http://lampa.mx/', text: 'Новое полностью бесплатное приложение для Smart TV' },
    { appid: 'anb_vokino', name: 'vokino', url: 'http://web.vokino.tv/', text: 'Смотреть зарубежные фильмы и сериалы в хорошем качестве' },
    { appid: 'anb_atodo', name: 'Atodo', url: 'http://msx.benzac.de/?start=menu:request:interaction:menu@http://atodo.fun/fun.html', text: 'АТОDO' },
    { appid: 'anb_fxml', name: 'Media Station X', url: 'http://msx.benzac.de/foxxum.html', text: 'Приложение для создания настраиваемых мультимедийных страниц (видео, аудио и пр.)' },
    { appid: 'anb_moovies', name: 'Moovies', url: 'http://msx.benzac.de/?start=menu:request:interaction:init@http://moovies.uz/index.html', text: 'Moovies for MSX' },
    { appid: 'anb_movielab', name: 'Movielab', url: 'https://msx.benzac.de/?start=menu:https://movielab.fun/msx/menu.json', text: 'Наслаждайтесь просмотром лучших фильмов с MovieLab' },
    { appid: 'anb_deeplex', name: 'DEEPLEX', url: 'http://smart.deeplex.cc', text: 'Фильмы, сериалы и многое другое без ограничений.Инструкция -> http://deeplex.cc/#/instructions' },
    { appid: 'anb_drmplay', name: 'DRM-play', url: 'http://drm-play.com', text: 'Ott плеер drm-play, mod плеера ott-play by Alex ' },
    { appid: 'anb_fork', name: 'ForkPlayer', url: 'http://browser.appfxml.com/', text: 'ForkPlayer — это браузер с адаптированным под ваше устройство просмотром сайтов' },
    { appid: 'anb_forkbrowser', name: 'Fork Browser', url: 'http://browser.appinfo.su/', text: 'Новая, улучшенная версия ForkPlayer' },
    { appid: 'anb_lampalite4', name: 'Lampa lite', url: 'http://lite.lampa.mx/', text: 'Lampa Lite, облегченная версия приложения для онлайн просмотра.' },
    { appid: 'anb_twitch', name: 'twitch', url: 'https://hisense.tv.twitch.tv/', text: 'Видеостриминговый сервис, специализирующийся на тематике компьютерных игр.' },
    { appid: 'anb_vkvideo', name: 'VK видео', url: 'https://vk.ru/tv-app/lib?version=latest&platform=vidaa', text: 'Смотрите видеозаписи ВКонтакте на большом экране SmartTV. ' },
    { appid: 'anb_beeline', name: 'Билайн ТВ', url: 'https://smart-vidaa.beeline.tv/', text: 'Тысячи фильмов, сериалов и мультфильмов. 300 каналов и доступ к онлайн-кинотеатру beeline.tv.' },
    { appid: 'anb_xsmart', name: 'Xsmart', url: 'http://app.xsmart.tv/?widg=5', text: 'Приложение для Smart TV, которое объединяет в себе различные функции.' },
    { appid: 'anb_viju', name: 'Viju', url: 'https://smarttv.viju.ru', text: 'Viju – это лучшие фильмы, сериалы и мультфильмы по подписке' },
    { appid: 'anb_tiktok', name: 'TikTok', url: 'https://tv.tiktok.com/webos', text: 'Ведущая видеоплатформа для коротких видео' },
    { appid: 'anb_m3uiptv', name: 'M3U IPTV', url: 'https://m3u-ip.tv/lg/', text: 'Просто загрузите свой плейлист IPTV по URL-адресу (в виде файла m3u или m3u8) и вперед' },
    { appid: 'anb_kinopoisk', name: 'Кинопоиск', url: 'https://smarttv-app.ott.yandex.ru/?ott-rv=vidaa', text: 'Крупнейший русскоязычный онлайн-кинотеатр.' },
    { appid: 'anb_yandexvideo', name: 'Яндекс видео', url: 'https://yandex.ru/video/tvapp/?ui=tvapp', text: 'Cмотреть телепередачи, музыкальные клипы, игровые ролики и популярное на YouTube' },
    { appid: 'anb_ott', name: 'OttPlayer', url: 'http://widget.ottplayer.tv/operatv2/index.html', text: 'Cервис, который позволяет вам собрать всё ваше IP-телевидение в одном плейлисте.' },
    { appid: 'anb_ottold', name: 'OttPlayerTest', url: 'http://widget.ottplayer.tv/test/index.html', text: 'OttPlayer, более новая(тестовая версия приложения)' },
    { appid: 'anb_wink', name: 'Wink', url: 'https://production-vidaa-fhd.wink.ru/', text: 'Цифровой видеосервис компании «Ростелеком»' },
    { appid: 'anb_kion', name: 'Кион', url: 'http://hkion.kion.ru/', text: 'Российская мультимедийная онлайн-платформа, созданная компанией МТС' },
    { appid: 'anb_ssiptv', name: 'ssiptv', url: 'http://app.ss-iptv.com', text: 'Медиа сервер для просмотра фильмов, сериалов, мультфильмов и пр.' },
    { appid: 'anb_icva', name: 'ICVA', url: 'http://icva.mx/', text: 'ICVA - новое приложение для просмотра IPTV каналов' },
    { appid: 'anb_tvap', name: 'TVap', url: 'http://tvphone.site/', text: 'TVap - просмотр IPTV каналов на Smart TV' },
    { appid: 'anb_peers', name: 'PeersTV', url: 'http://smarttv.peers.tv/hisense/hisense-1.0.0/', text: 'Бесплатное приложение для просмотра ТВ онлайн и в записи. Лайт версия без рекламы' },
    { appid: 'anb_bonus', name: 'Бонус ТВ', url: 'http://app.bonus-tv.ru/lg/', text: 'Телевидение онлайн на смартфоне, планшете, Smart-телевизоре или ТВ-приставке.' },
    { appid: 'anb_amediateka', name: 'Aмедиатека', url: 'https://smarttv-stable.amediateka.tech/hisense/', text: 'Онлайн-сервис Амедиатека и телеканалы AMEDIA TV. Лучшие сериалы планеты' },
    { appid: 'anb_prisma', name: 'Prisma', url: 'http://prisma.ws/', text: 'Полностью готовый к работе форк Lampa.' },
    { appid: 'anb_gets', name: 'GetsTV', url: 'https://getstv.com/app/', text: 'Приложение для просмотра ТВ, фильмов и сериалов.' },
    { appid: 'anb_ottplay_mod', name: 'OTT-Play FOSS', url: 'http://ott.prog4food.eu.org/f/', text: ' Moд iptv плеера Ott-Play by Alex. Отсутствие баннеров и блокировки каналов.' },
    { appid: 'anb_kinopub', name: 'KinoPubTV', url: 'http://cdnservices.link', text: 'Неофициальный клиент для популярного онлайн-кинотеатра' },
    { appid: 'anb_lampaun', name: 'ByLampa', url: 'http://bylampa.online/', text: 'Неофициальный форк онлайн-кинотеатра Lampa' },
    { appid: 'anb_lampaland', name: 'Lampa.land', url: 'http://lampa.land', text: 'Проект, созданный для тех, кто не может самостоятельно настроить приложение Lampa' },
    { appid: 'anb_iptvportal', name: 'IPTVPORTAL', url: 'http://go.iptvportal.ru/?screen=1280x720&user-agent=lg', text: 'Просмотр IPTV из сетей провайдеров, подключенных к платформе IPTVPORTAL' },
    { appid: 'anb_oneplayer', name: 'Oneplayer', url: 'http://webos.oneplayer.me/', text: 'Интернет-плеер с широким функционалом' },
    { appid: 'anb_clouddy', name: 'ClouDDy', url: 'http://player.clouddy.online/', text: 'Продвинутый и удобный медиаплеер для воспроизведения вашего любимого медиаконтента.' },
    { appid: 'anb_smotreshka', name: 'Смотрешка', url: 'https://smotreshka.webapp.lfstrm.tv/loaders/vidaa/index.html', text: 'Современное интерактивное телевидение' },
    { appid: 'anb_ivikids', name: 'IVI детям', url: 'http://lgkids.ivi.ru', text: 'Приложение, сделанное специально для детей! Мультики, фильмы и сериалы' },
    { appid: 'anb_viloud', name: 'Viloud', url: 'https://app.viloud.tv//smarttv//v2//?associate=fox-a5f1&app=ef2b1dd758eb0fcc065561e1275e4af6#viloud', text: 'Самая Простая и Доступная Онлайн-Видеоплатформа' },
    { appid: 'anb_vevo', name: 'Vevo', url: 'https://hisense.vevo.com', text: 'Музыкальное видео от крупнейших звукозаписывающих корпораций' },
    { appid: 'anb_webvideocast2', name: 'Web Video Cast', url: 'http://vewd.webvideocaster.com/', text: 'Позволяет вам транслировать любое видео, найденное на веб-сайтах, на ваш телевизор.' },
    { appid: 'anb_sweet', name: 'sweet.tv', url: 'http://foxxum240.sweet.tv', text: 'Бесплатное онлайн телевидение в хорошем качестве. Телеканалы в прямом эфире и в записи!' },
    { appid: 'anb_stranafm', name: 'Страна FM', url: 'http://stranafm.bonus-tv.ru/stranafm/nettv/', text: 'Страна FM — российский коммерческий развлекательный телеканал. Музыка нон стоп' },
    { appid: 'anb_premier', name: 'PREMIER', url: 'https://hisensesmarttv.premier.one/hisense/#/main', text: 'ТНТ премьер. Новые русские сериалы, фильмы и шоу.' },
    { appid: 'anb_mytuner', name: 'myTuner Radio', url: 'https://devices.mytuner.mobi/?utm_source=Foxxum', text: 'Удобное прослушивание более 30 000 популярных радиостанций 120 стран мира' },
    { appid: 'anb_zaycev', name: 'Zaycev FM', url: 'https://tv.zaycev.fm/index.html', text: 'Любимая музыка теперь всегда будет с вами вместе с онлайн радио Zaycev.fm!' },
    { appid: 'anb_ctc', name: 'СТС', url: 'http://smarttv.ctc.ru', text: 'Все самые интересные сериалы, популярные программы и мультфильмы телеканала СТС' },
    { appid: 'anb_siptv', name: 'Smart IPTV', url: 'http://opera.siptv.eu', text: 'Play IPTV streams, videos on your Smart TV' },
    { appid: 'anb_ttktv', name: 'ТТК ТВ', url: 'http://eltex-web.ls.tv.ttk.ru', text: 'Приложение для просмотра любимых фильмов, сериалов, мультфильмов и телевизионных программ' },
    { appid: 'anb_sibseti', name: 'Tв Сибсети', url: 'http://smarty.nsk.211.ru', text: 'IPTV для абонентов Сибсети. Создай свой личный медиацентр с нашим приложением!' },
    { appid: 'anb_zefirtv', name: 'Зефир ТВ', url: 'http://webkit.zt.platform24.tv/', text: 'ТВ-каналы, фильмы, сериалы, спорт' },
    { appid: 'anb_smotrim', name: 'Смотрим', url: 'https://tv.smotrim.ru/', text: 'Новости, ток-шоу, документальные и художественные фильмы, телесериалы и пр.' },
    { appid: 'anb_moovi', name: 'moovi', url: 'http://base.portal.moovi-iptv.ru/ui/1280/index.html?rand=0.3412177627522204', text: 'Кабельное Телевидение Moovi. Современный формат цифрового телевидения.' },
    { appid: 'anb_tvoe', name: 'TVOE', url: 'https://app.tvoe.live?device=smart-tv&installed=vidaa', text: 'Тысячи фильмов и сериалов' },
    { appid: 'anb_emby', name: 'Emby', url: 'http://tv.emby.media/', text: 'Медиа-сервер и домашний кинотеатр. Позволяет скачивать фильмы, сериалы и добавлять их в каталог.' },
    { appid: 'anb_24_1', name: '24tv', url: 'http://webkit.24h.tv', text: '24ТВ Всё ТВ и кинотеатры в одном приложении' },
    { appid: 'anb_IDC', name: 'IDC Smart TV', url: 'https://smart.iptv.idc.md', text: 'Приложение от крупнейшего телекоммуникационного оператора на территории Приднестровья' },
    { appid: 'anb_stremio', name: 'Stremio', url: 'https://tv.strem.io', text: 'Stremio – программа для просмотра видео-контента различных известных онлайн-сервисов' },
    { appid: 'anb_tytkino', name: 'Тут Кино', url: 'http://fork-p0rtal.ru/project/', text: 'Виджет для SmartTV от fork-portal.ru на движке VPlay.' },
    { appid: 'anb_impareboom', name: 'ИмперияBOOM', url: 'http://web.imboom.ru/', text: 'Твой HD кинотеатр. Новинки кино и сериалы без навязчивой рекламы' },
    { appid: 'anb_djin', name: 'HDGO', url: 'http://hdgo.me/', text: 'Полностью готовый к работе форк Lampa Lite' },
    { appid: 'anb_popkorn', name: 'Попкорн', url: 'https://tv-desktop.beepopcorn.ru', text: 'Бесплатное ТВ, фильмы, сериалы, видеоблоги и караоке' },
    { appid: 'anb_filmix', name: 'Filmix', url: 'http://filmix.tv', text: 'Приложение для просмотра фильмов и сериалов с популярного онлайн кинотеатра filmix.tv' },
    { appid: 'anb_akter', name: 'AKTER BLACK', url: 'http://abvidaa.ru', text: 'Уютное киноубежище - онлайн кинотеатр AKTER BLACK' },
    { appid: 'anb_movix', name: 'Movix', url: 'http://cdn.smarttv.domru.ru/hisense/', text: 'Устройте онлайн-кинотеатр у себя дома вместе с Movix!' },
    { appid: 'anb_jellyfin', name: 'jellyfin', url: 'https://jellyfin-vidaa.vercel.app', text: 'Бесплатный и свободный медиасервер' },
    { appid: 'anb_farlinetv', name: 'Фарлайн ТВ', url: 'http://tv.farline.net', text: 'Смотрите наше интерактивное телевидение онлайн в любое удобное для вас время! Фильмы, мультфильмы, шоу и новости.' },
    { appid: 'anb_sevstartv', name: 'Севстар Tв', url: 'http://tvs.sevstar.net', text: 'Приложение для просмотра пакетов Цифрового телевидения от компании Севстар' },
    { appid: 'anb_focustv', name: 'Фокус Лайф', url: 'http://tv.focus.life/', text: 'Приложение для просмотра пакетов Цифрового телевидения от компании Фокус Лайф' },
];

// Encrypted data string (likely contains pre-calculated key or device info)
var ENCRYPTED_DATA_HD = '696aa22fc375afab73c223bf8c049f38f7cb8a48cebf3cc26b4204898386d1bfdb9b125c8eb848af60b9005e79377e4db85f8ee66e198881396f63835c5971aebcc7d09c42f22021ad8f9cb112caafa5d159aa25dab91ad8e60dee1c12e09a14a9eeca1ca2e7d3b93fc86a8b88551214c403c880e298212f39e564b46973a5a0';
var MAC_KEY_OFFSET = 0; // Offset for MAC address key generation (SMAP)
var UI_IMAGE_BASE_URL = 'https://vidaa.surge.sh/images_ui/'; // Base URL for UI images/icons
var THUMBNAIL_BASE_URL = 'http://195.58.50.236/'; // Base URL for thumbnails
var COLOR_WHITE = '#fafafa'; // Color White
var COLOR_BLACK = '#0f0f0f'; // Color Black
// Mapping array: ASCII codes for digits '0' through '9' - used for key generation
var DIGIT_MAP = ['48', '49', '50', '51', '52', '53', '54', '55', '56', '57'];
var LOG_SEPARATOR_STRING = '==========> '; // Separator string used in logging/key generation
var currentThemePreference = 0; // Theme preference (0 = text/icons hidden, 1 = visible) - Default

// --- Removed Obfuscator Setup ---
// The original script had complex IIFEs for array shuffling and anti-debugging.
// All string lookups (`_0x58e4(0x...)`) have been replaced with the actual strings below.

// --- Console Log Override ---
var originalConsoleLog = function() {};
if (typeof console !== 'undefined' && typeof console['log'] !== 'undefined') {
    originalConsoleLog = console['log'];
}

// Override console.log to also append messages to the #console div in the HTML
console['log'] = function(message) {
    originalConsoleLog(message); // Call original console.log
    var messageString = '';
    if (typeof message === 'object') {
        // Try to stringify objects for display
        try {
            messageString = JSON && JSON['stringify'] ? JSON['stringify'](message) : Object.prototype.toString.call(message);
        } catch (e) {
            messageString = '[Unstringifiable Object]';
        }
    } else {
        messageString = message;
    }
    // Append to the HTML element #console (assuming jQuery is present)
    try {
        var $consoleDiv = $('#console');
        $consoleDiv.append('<div>' + messageString + '</div>').animate({
            'scrollTop': $consoleDiv.prop('scrollHeight')
        }, 700);
    } catch (e) {
        // Fallback if jQuery or #console isn't available
        originalConsoleLog("Error appending to #console:", e);
    }
};

// Redirect other console methods to the overridden console.log
console['warn'] = console['error'] = console['info'] = console['trace'] = console['log'];

// --- Global Variables and Key Generation ---
var macAddress;
var macAddressBytesDecimal; // Array of MAC address bytes as decimal numbers
var macAddressStringDecimal; // String of joined decimal MAC bytes
var masterKeySequence; // Master Key sequence derived from MAC address (SMAP in original)
var logStringPart1, logStringPart2, logStringPart3; // Strings derived from MAC for logging (arm1, arm2, arm3)
var dateKeySequence; // Date Key sequence derived from HD decryption or Date (MAP in original)
var dateKeyLogString1, dateKeyLogString2; // Strings related to date key generation for logging (arr, arr2)
var isUnlocked = true; // Flag indicating if the interface is unlocked

// Helper function to generate key component strings for logging (uses MAC bytes)
function generateMacLogStringComponent(separator, index1, index2) {
    // Replicates: ' ' + DIGIT_MAP[macAddressStringDecimal[MAC_KEY_OFFSET+index1]] + separator + DIGIT_MAP[macAddressStringDecimal[MAC_KEY_OFFSET+index2]] + '> '
    let val1 = DIGIT_MAP[macAddressStringDecimal[MAC_KEY_OFFSET + index1]];
    let val2 = DIGIT_MAP[macAddressStringDecimal[MAC_KEY_OFFSET + index2]];
    return ' ' + val1 + separator + val2 + '> ';
}
function generateMacLogStringComponent3(index1, index2) {
     let val1 = DIGIT_MAP[macAddressStringDecimal[MAC_KEY_OFFSET + index1]];
     let val2 = DIGIT_MAP[macAddressStringDecimal[MAC_KEY_OFFSET + index2]];
    return ' ' + val1 + '> MAC ' + val2 + '> ';
}

try {
    // 1. Attempt to get MAC Address and generate Master Key (SMAP)
    macAddress = Hisense_GetMacAddress();
    var macPartsHex = macAddress.split(':');
    macAddressBytesDecimal = macPartsHex.map(hex => parseInt(hex, 16));
    macAddressStringDecimal = macAddressBytesDecimal.join(''); // Concatenated decimal values as a string

    // Generate Master Key sequence (SMAP) using MAC bytes and DIGIT_MAP
    masterKeySequence = [
        DIGIT_MAP[macAddressStringDecimal[MAC_KEY_OFFSET + 0]],
        DIGIT_MAP[macAddressStringDecimal[MAC_KEY_OFFSET + 1]],
        DIGIT_MAP[macAddressStringDecimal[MAC_KEY_OFFSET + 2]],
        DIGIT_MAP[macAddressStringDecimal[MAC_KEY_OFFSET + 3]],
        DIGIT_MAP[macAddressStringDecimal[MAC_KEY_OFFSET + 4]],
        DIGIT_MAP[macAddressStringDecimal[MAC_KEY_OFFSET + 5]]
    ];

    // Generate logging strings based on MAC (arm1, arm2, arm3)
    logStringPart1 = generateMacLogStringComponent('> ', 0, 1);
    logStringPart2 = generateMacLogStringComponent('> DNS ', 2, 3);
    logStringPart3 = generateMacLogStringComponent3(4,5);

} catch (macError) {
    console.log("NO GetMacAddress API, ERROR !!");
    masterKeySequence = []; // Set to empty if MAC unavailable
    logStringPart1 = logStringPart2 = logStringPart3 = "N/A";
}

try {
    // 2. Attempt to decrypt ENCRYPTED_DATA_HD to get Date Key sequence (MAP)
    var decryptedData = Hisense_Decrypt(ENCRYPTED_DATA_HD); // Assuming returns array/object
    // Generate Date Key sequence (MAP) using decrypted data and DIGIT_MAP
    dateKeySequence = [
        DIGIT_MAP[decryptedData[N_DECRYPT_OFFSET + 0]],
        DIGIT_MAP[decryptedData[N_DECRYPT_OFFSET + 1]],
        DIGIT_MAP[decryptedData[N_DECRYPT_OFFSET + 2]],
        DIGIT_MAP[decryptedData[N_DECRYPT_OFFSET + 3]]
    ];
    dateKeyLogString1 = dateKeyLogString2 = '||++++'; // Placeholder logs if decryption works
} catch (decryptError) {
    // 3. Fallback: Generate Date Key sequence (MAP) based on current Date if decryption fails
    var currentDate = new Date();
    var dayOfMonth = currentDate.getUTCDate();
    var jsDayOfWeek = currentDate.getUTCDay(); // 0=Sun, 6=Sat
    var mappedDayOfWeek = [7, 1, 2, 3, 4, 5, 6][jsDayOfWeek]; // Map to 1-7 (Mon=1, Sun=7)
    var weekOfMonth = Math.floor(dayOfMonth / 7) + 1; // Calculate week number (1-based)
    var dayDigits = dayOfMonth.toString().split('');

    // Get DIGIT_MAP-mapped digits for the day (handle single digit days)
    var mappedDigit1 = DIGIT_MAP[dayDigits[0]];
    var mappedDigit2 = (dayDigits.length > 1) ? DIGIT_MAP[dayDigits[1]] : DIGIT_MAP[0]; // Use DIGIT_MAP[0] ('48') if single digit day
    if (dayOfMonth < 10) { // If day is single digit (1-9)
        mappedDigit2 = mappedDigit1; // Second mapped digit is same as first
        mappedDigit1 = DIGIT_MAP[0]; // First mapped digit is '48'
    }

    // Generate Date Key sequence (MAP) using date components and DIGIT_MAP
    dateKeySequence = [mappedDigit1, DIGIT_MAP[mappedDayOfWeek], DIGIT_MAP[weekOfMonth], mappedDigit2];

    // Generate logging strings for date key (arr, arr2) using '=' repeats
    let separator = ' ';
    let equalsDay = '='.repeat(mappedDayOfWeek);
    let equalsDayComplement = '='.repeat(Math.max(0, 10 - mappedDayOfWeek)); // Ensure repeat count isn't negative
    dateKeyLogString1 = '||' + equalsDay + separator + equalsDayComplement;

    let equalsWeek = '='.repeat(weekOfMonth);
    let equalsWeekComplement = '='.repeat(Math.max(0, 10 - weekOfMonth)); // Ensure repeat count isn't negative
    dateKeyLogString2 = '||' + equalsWeek + separator + equalsWeekComplement;
}

// --- jQuery Document Ready ---
$(document).ready(function() {
    // Check unlock status from localStorage
    if (localStorage.getItem('key') !== null) {
        isUnlocked = true;
        // Hide elements intended only for the locked state
        $('.nokey').removeClass('hide'); // Original used removeClass, implies .nokey elements are hidden by default
    } else {
        isUnlocked = false;
    }

    // Load theme preference from localStorage, default to 0 if not set
    currentThemePreference = localStorage.getItem('tp') !== null ? parseInt(localStorage.getItem('tp'), 10) : 0;
    localStorage.setItem('tp', currentThemePreference); // Ensure it's stored

    // Check if Hisense install API exists and initialize UI
    if (typeof Hisense_installApp !== 'undefined') {
        $('.CBGbtn').removeClass('hide'); // Show general install-related buttons/elements
        displayTvInfo(); // Display basic TV info
        // Iterate over the APP_LIST and add tiles for each app
        $.each(APP_LIST, function(index, appData) {
            addAppTile(appData); // Renamed function
        });
    } else {
        // $('#nosupport').removeClass('hide'); // Show unsupported message
        // $('.CBGbtn').removeClass('hide');
    }
});

// --- OS Version Detection and Image Path Determination ---
var imageFolderPrefix = 'images/'; // Default image folder ('img/' or 'images/')
try {
    var osVersionString = Hisense_GetOSVersion();
    // Determine image folder prefix based on OS version substrings
    if (osVersionString.includes('U6') || osVersionString.includes('U06') ||
        osVersionString.includes('U07') || osVersionString.includes('U7') ||
        osVersionString.includes('U08') || osVersionString.includes('U8')) {
        imageFolderPrefix = 'img/';
    } else if (osVersionString.includes('U04') || osVersionString.includes('U4')) {
        imageFolderPrefix = 'images/';
        // isUnlocked = true; // Original set key=4 for U4 OS, maybe implies auto-unlock? Simplified to just set path.
    }
} catch (osVersionError) {
    console.log("Could not determine OS version, using default image path.");
    imageFolderPrefix = 'images/'; // Default on error
}

// --- Get List of Already Installed "Debug" Apps ---
var installedDebugApps = []; // Array to hold info about installed 'debug' apps
try {
    // Use Hisense API to get all installed apps
    var installedAppsJson = getInstalledAppJsonObj();
    if (installedAppsJson && installedAppsJson.AppInfo) {
        for (let i = 0; i < installedAppsJson.AppInfo.length; i++) {
            let appInfo = installedAppsJson.AppInfo[i];
            // Filter for apps whose ID contains 'debug'
            if (appInfo && appInfo.Id && appInfo.Id.includes('debug')) {
                installedDebugApps.push(appInfo);
            }
        }
    }
} catch (getInstalledAppsError) {
    console.warn("getInstalledAppJsonObj fail!");
}

// --- Check for OMI Platform (Alternative Hisense Environment?) ---
if (!!window['omi_platform']) {
    $('#shop, .CBGbtn').css({ 'transform': 'translateY(-615px)' }); // Apply specific style
    // isUnlocked = true; // Original set key=3 for OMI, maybe auto-unlock? Simplified.
    imageFolderPrefix = 'img/'; // Use 'img/' path for OMI environment
}

// --- Function to Add Application Tiles to the UI ---
function addAppTile(appData) { // Renamed from addTile
    // Construct paths/IDs
    var thumbnailUrl = THUMBNAIL_BASE_URL + imageFolderPrefix + appData.appid + '.png';
    var iconUrl = UI_IMAGE_BASE_URL + appData.appid + '.png'; // For the main icon element
    var appIdDebug = appData.name + 'debug'; // ID used for install/uninstall actions
    var $container = $('#container');
    var $tileTemplate = $('#empty_tile');

    // Clone the template tile (ensure template exists in HTML)
    if (!$tileTemplate.length) {
        console.error("HTML template '#empty_tile' not found!");
        return;
    }
    var $newTile = $tileTemplate.clone();
    $newTile.removeAttr('id'); // Remove ID from clone to avoid duplicates

    // Populate the cloned tile with app data (Update selectors based on actual HTML structure)
    $newTile.find('.icon img').attr('src', iconUrl).on('error', function() { $(this).hide(); }); // Set icon, hide on error
    $newTile.find('.name').html(appData.name);      // Main name display
    $newTile.find('.ticon').html(appData.name);     // Icon text overlay?
    $newTile.find('.text').html(appData.text);      // App description text

    // Set up the install overlay/button content (adjust HTML structure as needed)
    var $installOverlay = $newTile.find('.install');
    $installOverlay.html(
        '<div class="name">' + appData.name + '</div>' +
        '<div class="text">' + appData.text + '</div>' +
        '<div class="nam" >нажмите OK для установки</div>' // "press OK to install" prompt
    );
    $installOverlay.attr('data-appid', appData.appid); // Store original appid maybe? Original stored on overlay.

    $newTile.removeClass('hide'); // Make the tile visible
    $container.append($newTile); // Add the tile to the container

    // Determine the 'startAppType' for installation ('store' or 'sraf_ext')
    var startAppType = 'store'; // Default type
    var specialTypeApps = ['Wink', 'Билайн ТВ', 'TikTok', 'ТТК ТВ'];
    if (specialTypeApps.includes(appData.name)) {
        startAppType = 'sraf_ext';
    }

    // Apply the current color theme to the new tile elements
    applyColorThemeToElement($newTile); // Apply theme to the tile itself and its children

    // --- Theme Preference Application ---
    // Hide icons/text if theme preference is 0 (adjust selectors as needed)
    if (currentThemePreference === 0) {
        $newTile.find('.icon, .text').addClass('hide');
    }

    // --- App Index and Locking Logic ---
    var appIndex = APP_LIST.findIndex(item => item.name === appData.name);
    var requiresDateKeyUnlock = (appIndex + 1 === DATE_KEY_APP_INDEX); // Check if this app needs the Date Key

    // Determine if the app is restricted in DEMO mode (locked if not unlocked)
    // Indices 0-11 (1-12) and 30-35 (31-36) seem available in demo. Others are locked.
    var isDemoLocked = !(appIndex < 12 || (appIndex > 29 && appIndex < 36));

    // --- Tile Hover Logic ---
    var scrollState = 0; // Scroll state variable (0=top, 1=middle, 2=bottom) - specific to this tile closure
    $newTile.on('mouseenter', function() {
        // Update status display (e.g., "3 / 80") - requires an element like #appStatusDisplay
        $('#appStatusDisplay').text((appIndex + 1) + ' / ' + APP_LIST.length);

        // Show/Hide status on hover (add/remove 'hide' class)
        $newTile.on('mouseover', function() { $('#appStatusDisplay').removeClass('hide'); });
        $newTile.on('mouseout', function() { $('#appStatusDisplay').addClass('hide'); });

        // Adjust container scroll position based on hovered item index (3 rows assumed)
        var currentTransform = $container.css('transform'); // Get current transform state if needed for smoother logic

        if (appIndex + 1 > 24 && scrollState === 0) { // Past row 1, scroll down
            $container.css('transform', 'translateY(-336px)'); // Scroll to row 2
            scrollState = 1;
        } else if (appIndex + 1 < 25 && scrollState === 1) { // Back into row 1 from row 2
            $container.css('transform', 'translateY(0px)');   // Scroll to top
            scrollState = 0;
        } else if (appIndex + 1 > 48 && scrollState === 1) { // Past row 2, scroll down
            $container.css('transform', 'translateY(-615px)'); // Scroll to row 3
            scrollState = 2;
        } else if (appIndex + 1 < 49 && scrollState === 2) { // Back into row 2 from row 3
            $container.css('transform', 'translateY(-336px)'); // Scroll to row 2
            scrollState = 1;
        }

        // Set global flag indicating if the hovered app requires the Date Key sequence
        appRequiresDateKeyFlag = requiresDateKeyUnlock ? 1 : 0;
    });

    // --- Click Logic (Install/Uninstall) ---

    // Handle DEMO locked apps if the interface is NOT unlocked
    if (isDemoLocked && !isUnlocked) {
        var $lockOverlay = $newTile.find('.lock-overlay'); // Assuming a dedicated overlay element
        if ($lockOverlay.length) {
            $lockOverlay.html('<b>' + appData.name + ' ─</b><br><br>Недоступно в DЕMO версии'); // "Unavailable in DEMO version"
            $lockOverlay.removeClass('hide');
            $installOverlay.addClass('hide'); // Hide the regular install overlay
        } else {
            // Fallback: show message in description area if no dedicated overlay
            $newTile.find('.text').html('<b>' + appData.name + ' ─</b><br><br>Недоступно в DЕMO версии').removeClass('hide');
             $installOverlay.addClass('hide');
        }
    } else {
        // If unlocked OR app is not demo-locked, enable install action
        $installOverlay.on('click', function() {
            console.log("Attempting to install:", appIdDebug);
            // Call Hisense API to install the app
            Hisense_installApp(
                appIdDebug,       // Use the 'debug' version of the ID
                appData.name,     // App Name
                thumbnailUrl,     // Thumbnail URL (repeated 3 times in original?)
                thumbnailUrl,
                thumbnailUrl,
                appData.url,      // The actual URL of the app to install
                startAppType,     // 'store' or 'sraf_ext'
                function(installError) { // Callback function
                    if (installError) {
                        logGroupedMessage('Install Error', '-', "INSTALLATION FAILED for " + appData.name, '-', installError);
                    } else {
                        logGroupedMessage('Install Success', '-', appData.name + " app INSTALLATION COMPLETED !", '-');
                        // Visual feedback: hide install button, show uninstall button
                        $installOverlay.slideUp(500);
                        $newTile.find('.uninstall').removeClass('hide'); // Show the uninstall element
                        refreshAppsOnHisenseUI(appIdDebug); // Notify the TV UI about the change
                    }
                }
            );
        });
    }

    // --- Uninstall Button Setup ---
    var $uninstallButton = $newTile.find('.uninstall'); // Assuming .uninstall is the container/button
    // Add uninstall button text/content (adjust based on HTML)
    $uninstallButton.html('<div class="button">УДАЛИТЬ</div>' + appData.name); // "DELETE" + app name

    // Add uninstall click handler
    $uninstallButton.on('click', function() {
        console.log("Attempting to uninstall:", appIdDebug);
        // Call Hisense API to uninstall
        Hisense_uninstallApp(appIdDebug, function(uninstallError) { // Callback
            if (!uninstallError) { // Assuming 0 or falsy means success
                 logGroupedMessage('Uninstall Success', '-', appData.name + " app uninstalled success !", '-');
                 // Visual feedback: show install button, hide uninstall
                 $installOverlay.slideDown(500);
                 $uninstallButton.addClass('hide');
                 refreshAppsOnHisenseUI(appIdDebug); // Notify UI
            } else {
                console.log("Error uninstall app:", uninstallError);
            }
        });
    });

    // --- Initial State based on installedDebugApps list ---
    // Check if this app (by name) is already in the list of installed debug apps
    var isAlreadyInstalled = installedDebugApps.some(installedApp => installedApp && installedApp.appName === appData.name);

    if (isAlreadyInstalled) {
        // If installed, hide install overlay, show uninstall button initially
        $installOverlay.addClass('hide');
        $uninstallButton.removeClass('hide');
    } else {
         // If not installed, ensure install overlay is visible and uninstall is hidden
         $installOverlay.removeClass('hide'); // Might already be visible, but ensure it
         $uninstallButton.addClass('hide');
    }

} // end addAppTile function

// --- Global Variables for UI State ---
var themeToggleCounter = 0; // Counter for theme cycling (tt)
var logViewerToggleCounter = 0; // Counter for log viewer toggle (cg)
var debugEditorToggleCounter = 0; // Counter for debug editor toggle (cr)
var isLogViewerActive = false; // Flag if log viewer is currently shown (don)
var appRequiresDateKeyFlag = 0; // Flag indicating if the currently hovered app requires the DATE key sequence (ky)

// --- Global Keydown Event Listener ---
document.addEventListener('keydown', function(event) {
    var keyCode = event.keyCode;

    // --- Unlock Key Sequence Input Handling ---
    var dateKeyInputSequence = []; // Store user input for date key
    var masterKeyInputSequence = []; // Store user input for master key

    // 1. Date Key Sequence Check (MAP)
    // Active only if NOT unlocked AND the currently hovered app requires it (appRequiresDateKeyFlag=1)
    if (!isUnlocked && appRequiresDateKeyFlag === 1 && dateKeySequence && dateKeySequence.length > 0) {
        dateKeyInputSequence = window._dateKeyBuffer || []; // Retrieve or initialize buffer
        dateKeyInputSequence.push(keyCode.toString()); // Store key code as string

        // Keep buffer length same as target sequence length (rolling input)
        if (dateKeyInputSequence.length > dateKeySequence.length) {
            dateKeyInputSequence.shift();
        }
        window._dateKeyBuffer = dateKeyInputSequence; // Store buffer globally (or use closure)

        // Check for match only when the buffer length is correct
        if (dateKeyInputSequence.length === dateKeySequence.length &&
            dateKeyInputSequence.join('') === dateKeySequence.join('')) {
            isUnlocked = true; // Unlock!
            localStorage.setItem('key', '1'); // Store unlocked state
            logGroupedMessage("Unlock Success", '-', "Unlocked ! Your Date Key: " + dateKeySequence.join(','), '-');
            $('.nokey').addClass('hide'); // Hide DEMO restrictions
            $('.CBRbtn').removeClass('hide'); // Show Red button functions (debug/log related)
            window._dateKeyBuffer = []; // Reset input buffer
            appRequiresDateKeyFlag = 0; // Reset flag after successful unlock
        }
    }

    // 2. Master Key Sequence Check (SMAP)
    // Always checked if not unlocked
    if (!isUnlocked && masterKeySequence && masterKeySequence.length > 0) {
        masterKeyInputSequence = window._masterKeyBuffer || [];
        masterKeyInputSequence.push(keyCode.toString());

        if (masterKeyInputSequence.length > masterKeySequence.length) {
            masterKeyInputSequence.shift();
        }
        window._masterKeyBuffer = masterKeyInputSequence;

        // Check for match only when the buffer length is correct
        if (masterKeyInputSequence.length === masterKeySequence.length &&
            masterKeyInputSequence.join('') === masterKeySequence.join('')) {
            isUnlocked = true; // Unlock!
            localStorage.setItem('key', '1');
            logGroupedMessage("Unlock Success", '-', "Master Key Unlock !", '-');
            $('.nokey').addClass('hide');
            $('.CBRbtn').removeClass('hide');
            window._masterKeyBuffer = []; // Reset buffer
        }
    }

    // --- Handle Specific Key Presses (Remote Control Codes) ---
    switch (keyCode) {
        case 8: // Backspace Key / BACK button
            try { window.close(); } catch (e) { console.log("window.close() failed."); }
            break;
        case 404: // Red button -> Toggle Log Viewer
            toggleLogViewer();
            break;
        case 405: // Green button -> Cycle Theme
            if (isUnlocked) cycleColorTheme();
            break;
        case 403: // Yellow button -> Toggle Debug App Editor
             if (isUnlocked) toggleDebugEditor(); // Only allow if unlocked
            break;
        case 406: // Blue button -> Lock Interface
            if (isUnlocked) {
                isUnlocked = false; // Set state to locked
                localStorage.removeItem('key');
                $('.CBRbtn').addClass('hide'); // Hide Red button functions
                $('.nokey').removeClass('hide'); // Show DEMO restrictions
                // Potentially refresh UI to re-apply demo locks visually
                console.log("Interface locked.");
            }
            break;
    }
    event.preventDefault(); // Prevent default browser action for the key
}, false); // Use bubbling phase

// --- Function to Toggle Log Information Viewer ---
function toggleLogViewer() {
    logViewerToggleCounter++;
    // Only toggle if Debug Editor isn't active
    if (debugEditorToggleCounter % 2 === 0) { // Check if editor is hidden (cr=0 or cr=2, etc.)
        if (logViewerToggleCounter % 2 !== 0) { // If showing (cg is odd)
            // Show log viewer (animate or display block)
            $('#logViewerPanel').removeClass('hide'); // Assuming a panel with ID #logViewerPanel
            // Animate: $('.debug').css('transform', 'scale(1.4) translate(315px, 130px)'); // Original animation target?
            $('#container, .CBRbtn').addClass('hide'); // Hide main app container and Red buttons
            $('#debugStatusDisplay').text('Off Log'); // Update status display (e.g., #debugon button)
            isLogViewerActive = true; // Set state flag

            // Gather and display TV Information
            displayLogInfo();

        } else { // Hiding (cg is even)
            $('#logViewerPanel').addClass('hide'); // Hide the log viewer panel
            displayTvInfo(); // Refresh basic TV info display (e.g., in #debugStatusDisplay)
            isLogViewerActive = false; // Reset state flag
            $('#container').removeClass('hide'); // Show main container
            $('#debugStatusDisplay').html("Get Log"); // Reset status display text
             if (isUnlocked) { $('.CBRbtn').removeClass('hide'); } // Show Red buttons if unlocked
        }
    } else {
         logViewerToggleCounter = 0; // Reset counter if editor is active
         console.log("Log viewer cannot be opened while Debug Editor is active.");
    }
}

// --- Function to Display Log Information ---
function displayLogInfo() {
    var installedAppsInfo = "error";
    try { installedAppsInfo = Hisense_getInstalledApps() || "N/A"; } catch (e) { /* ignore */ }
    var installApiStatus = "error";
    try { if (typeof Hisense_installApp !== 'undefined') installApiStatus = 'OK'; } catch (e) { /* ignore */ }
    var dnsInfo = "error";
    try { dnsInfo = Hisense_GetDNS() || "N/A"; } catch (e) { /* ignore */ }
    var macInfo = "error";
    try { macInfo = Hisense_GetMacAddress() || "N/A"; } catch (e) { /* ignore */ }
    var netTypeInfo = "error";
    try { netTypeInfo = Hisense_GetNetType() || "N/A"; } catch (e) { /* ignore */ }

    // Log collected info using the custom console group function
    logGroupedMessage(
        "API LOG",
        "|| Hisense_installApp " + LOG_SEPARATOR_STRING + installApiStatus,
        "|| getInstalledApps " + LOG_SEPARATOR_STRING + installedAppsInfo,
        "|| Date " + LOG_SEPARATOR_STRING + new Date()
    );

    if (!isUnlocked) { // If locked, show masked/obfuscated key info
        logGroupedMessage(
            "KEY",
            dateKeyLogString1, // Date-based key info string 1
            '|| NET ' + logStringPart1 + netTypeInfo + ' ' + logStringPart2 + dnsInfo + logStringPart3 + macInfo, // Network/MAC info
            dateKeyLogString2 // Date-based key info string 2
        );
    } else { // If unlocked, show master key hint
         logGroupedMessage(
            "API LOG", // Reused group name
            LOG_SEPARATOR_STRING.slice(0, 9), // "========="
            "Your master key: " + LOG_SEPARATOR_STRING + (macAddressStringDecimal ? macAddressStringDecimal.slice(0, 6) : "N/A"), // Show first 6 MAC digits
            LOG_SEPARATOR_STRING.slice(0, 9) // "========="
        );
    }
}

// --- Function to Apply Color Theme ---
function applyColorTheme(backgroundColor, foregroundColor) {
    // Apply colors using jQuery's css() method to various elements selectors combined
    var elementsToColor1 = '.CBGbtn, .CBYbtn, .CBRbtn, .text:not(.static), .tile:hover .text:not(.static), .APP, .di, #console, #save, #comb, #appName, #appUrl, #thumbnail';
    var elementsToBorder1 = '.ticon, .btn-danger, .btn-info, .nokey, input, #save, select, .debimg';
    var elementsToBorder2 = '.CBRbtn, .CBYbtn'; // Uses 2px border
    var elementsToInvert = 'body, .debug, .ticon, .btn-info, .text.static, .nokey, #debugStatusDisplay, #appName, #comb'; // Example static text selector
    var elementsToColorText = 'input, #save, select';
    var elementsToShadow1 = '.V'; // Uninstall icon?
    var elementsToShadow2 = '.CBRbtn, .CBYbtn'; // Main buttons?
    var elementsToHover = '.btn-info, .btn-danger, .nokey';

    try {
        $(elementsToColor1).css({ 'background-color': backgroundColor, 'color': foregroundColor });
        $(elementsToBorder1).css('border', '1px solid' + backgroundColor);
        $(elementsToBorder2).css('border', '2px solid' + backgroundColor);
        $(elementsToInvert).css({ 'background-color': foregroundColor, 'color': backgroundColor });
        $(elementsToColorText).css({ 'color': backgroundColor });
        $(elementsToShadow1).css({ 'box-shadow': '0px 0px 0px 2px' + foregroundColor });
        $(elementsToShadow2).css({ 'box-shadow': '0 0 17px 17px' + foregroundColor });

        // Apply hover effect
        $(elementsToHover).off('mouseenter mouseleave').hover( // Remove previous handlers first
            function() { $(this).css({ 'background-color': backgroundColor, 'color': foregroundColor }); },
            function() { $(this).css({ 'background-color': 'transparent', 'color': backgroundColor }); }
        );

        // Store the applied colors in localStorage
        localStorage.setItem('bc', backgroundColor);
        localStorage.setItem('c', foregroundColor);
    } catch(e) {
        console.error("Error applying color theme:", e);
    }
}

// Helper function to apply theme to a specific dynamically added element (like a tile)
function applyColorThemeToElement($element) {
    var bgColor = localStorage.getItem('bc') || COLOR_WHITE; // Default to white if not set
    var fgColor = localStorage.getItem('c') || COLOR_BLACK; // Default to black if not set

    // Apply basic coloring - adapt selectors as needed for elements within the tile
    $element.find('.someSelector').css({ 'background-color': bgColor, 'color': fgColor });
    $element.find('.anotherSelector').css({ 'background-color': fgColor, 'color': bgColor });
    // Add specific border/shadow rules if necessary
}


// --- Function to Cycle Through Themes ---
function cycleColorTheme() {
    themeToggleCounter++;
    // Only cycle if Log viewer and Debug Editor are not active
    if (!isLogViewerActive && (debugEditorToggleCounter % 2 === 0)) {
        switch (themeToggleCounter % 4) { // Use modulo 4 for cycling
            case 1: // State 1: White on Black, Text/Icons visible
                $('.icon, .text').removeClass('hide');
                currentThemePreference = 1;
                localStorage.setItem('tp', currentThemePreference);
                applyColorTheme(COLOR_WHITE, COLOR_BLACK);
                break;
            case 2: // State 2: White on Black, Text/Icons hidden
                $('.icon, .text').addClass('hide');
                currentThemePreference = 0;
                localStorage.setItem('tp', currentThemePreference);
                // applyColorTheme(COLOR_WHITE, COLOR_BLACK); // Color already set
                break;
            case 3: // State 3: Black on White, Text/Icons visible
                 $('.icon, .text').removeClass('hide');
                currentThemePreference = 1;
                localStorage.setItem('tp', currentThemePreference);
                applyColorTheme(COLOR_BLACK, COLOR_WHITE);
                break;
            case 0: // State 0 (was 4): Black on White, Text/Icons hidden
                $('.icon, .text').addClass('hide');
                currentThemePreference = 0;
                themeToggleCounter = 0; // Reset counter
                localStorage.setItem('tp', currentThemePreference);
                // applyColorTheme(COLOR_BLACK, COLOR_WHITE); // Color already set
                break;
        }
        console.log("Theme changed to state:", themeToggleCounter % 4, " Text/Icons visible:", currentThemePreference === 1);
    } else {
        // If Log or Debugger is active, just toggle between the two main color pairs
        if (themeToggleCounter % 2 !== 0) {
            applyColorTheme(COLOR_WHITE, COLOR_BLACK); // White/Black
        } else {
            applyColorTheme(COLOR_BLACK, COLOR_WHITE); // Black/White
        }
         console.log("Theme toggled (Debug/Log active):", themeToggleCounter % 2 !== 0 ? "W/B" : "B/W");
    }
}


// --- Helper to Group Console Logs ---
function logGroupedMessage(groupName, separator1, message1, separator2, message2) {
    // Uses the overridden console.log which also appends to #console div
    console.log('--- ' + groupName + ' ---');
    if (separator1 !== null) console.log(separator1);
    if (message1 !== null) console.log(message1);
    if (separator2 !== null) console.log(separator2);
    if (message2 !== undefined && message2 !== null) {
        console.log(message2);
    }
    console.log('--------------------');
}


// --- Function to Notify Hisense UI about App Changes ---
function refreshAppsOnHisenseUI(appId) {
    var messagePayload = {
        param: 'updateAppState',
        MsgType: 'APPMessage',
        action: 'appControl',
        key: 'startAppType', // Seems constant, purpose maybe internal to Hisense handler
        type: 2,
        data: {
            event: 'AllAppsUpdate',
            SubModuleName: 'AllApps',
            startFrom: '',
            appInfo: appId // The ID of the app that changed (e.g., 'AppNameDebug')
        }
    };

    try {
        // Send message using the appropriate Hisense platform API
        if (!!window['omi_platform']) {
            omi_platform.sendPlatformMessage(JSON.stringify(messagePayload));
        } else if (!!window['opera_omi']) { // Fallback?
            opera_omi.sendPlatformMessage(JSON.stringify(messagePayload));
        } else {
             console.log("No OMI platform found to refresh Hisense UI.");
        }
    } catch (e) {
        console.error("Error sending platform message to refresh UI:", e);
    }
}

// --- Function to Display Basic TV Info ---
// Target element assumed to be #debugStatusDisplay (was #debugon)
function displayTvInfo() {
    var infoHtml = '- Debug Page -';
    try {
        // Use Hisense APIs to get details
        infoHtml += Hisense_GetBrand() + ' vidaa ' + Hisense_GetOSVersion() + ' TV detected' + '<br>' +
                   'Model name : ' + Hisense_GetModelName() + ' || Country_Code ' + // Country code API might not exist
                   ' || FirmWare Version : ' + Hisense_GetFirmWareVersion();
        $('#debugStatusDisplay').html(infoHtml);
    } catch (aboutTvError) {
        logGroupedMessage('TV Info Error', '==', 'TV API not detected or failed', '==', aboutTvError);
        $('#debugStatusDisplay').html(infoHtml + "<br>TV API not detected.");
    }
}

// --- Debug App Editor Logic ---
function toggleDebugEditor() {
    // Check if unlocked and Log viewer isn't active
    if (isUnlocked && !isLogViewerActive) {
        debugEditorToggleCounter++;
        if (debugEditorToggleCounter % 2 !== 0) { // If showing (cr is odd)
            // Show editor
            $('#appInstallArea').addClass('hide'); // Hide normal install elements? Needs selector.
            $('#debugEditorPanel').removeClass('hide'); // Show the editor panel (assuming #debugEditorPanel)
            $('#debugStatusDisplay').html("Debug Off"); // Update status display
            loadDebugEditorContent(); // Load the editor content
        } else { // Hiding (cr is even)
            $('#appInstallArea').removeClass('hide'); // Show normal install elements?
            $('#debugEditorPanel').addClass('hide'); // Hide the editor panel
            displayTvInfo(); // Restore basic TV info in status display
        }
    } else if (!isUnlocked) {
        console.log("Debug Editor requires unlock.");
    } else if (isLogViewerActive) {
        console.log("Debug Editor cannot be opened while Log Viewer is active.");
        debugEditorToggleCounter = 0; // Reset counter if log viewer is active
    }
}

// --- Load Content for the Debug App Editor ---
// Target element assumed to be #debugEditorPanel (was #debugon)
function loadDebugEditorContent() {
    var editorHtml =
        '<div class="di"><p>Installed (' + installedDebugApps.length + ') <select id="debugAppSelect" onchange="changeDebugEditorSelection()"></select></p></div>' +
        '<div class="di"><p>App Name <input id="debugAppName" type="text"></p></div>' +
        '<div class="di"><p>Thumbnail <input type="text" id="debugThumbnailUrl"></p></div>' +
        '<div class="di"><p>App Url <input type="text" id="debugAppUrl"></p></div>' +
        '<button id="debugSaveButton" onclick="saveDebugAppChanges()">INSTALL/UPDATE</button>' +
        '<div class="debimg"> <img id="debugThumbnailPreview" src="" alt="Thumbnail Preview"/> </div>' + // Added ID and alt text
        // Add buttons for Debug Port and Get Log if needed
        '<button onclick="triggerDebugPortOn()">Debug Port ON</button>' +
        '<button onclick="triggerDebugPortOff()">Debug Port OFF</button>' +
        '<button id="getTvLogButton" onclick="triggerGetTvLog()">Get TV Log</button>';

    $('#debugEditorPanel').html(editorHtml);

    // If installed debug apps exist, populate dropdown and fill fields with the first app's data
    if (installedDebugApps.length > 0) {
        fillDebugEditorFields(installedDebugApps[0]); // Fill inputs with data from the first app
        // Populate the dropdown menu
        var appSelect = document.getElementById('debugAppSelect');
        installedDebugApps.forEach(function(app, index) {
            if (app && app.appName) { // Basic check
                appSelect.options.add(new Option(app.appName, index)); // Display appName, Value = index
            }
        });
    } else {
        $('#debugAppSelect').append('<option>No debug apps installed</option>').prop('disabled', true);
    }

    // Re-apply the current color theme to the newly added editor elements
    applyColorThemeToElement($('#debugEditorPanel')); // Apply theme to the panel and children
}

// --- Fill Debug Editor Fields with App Data ---
function fillDebugEditorFields(appObject) {
    if (!appObject) return; // Exit if no app object provided

    $('#debugAppName').val(appObject.appName || '');
    $('#debugThumbnailUrl').val(appObject.Thumb || '');
    $('#debugAppUrl').val(appObject.URL || '');

    // Display the thumbnail image preview
    var imageUrl = '';
    var thumbUrl = appObject.Thumb;
    if (thumbUrl) {
        if (thumbUrl.startsWith('https://')) {
            // Construct URL using vidaa.do.am if it's a known pattern (seems specific)
            try {
                var filename = thumbUrl.substring(thumbUrl.lastIndexOf('/') + 1);
                imageUrl = 'https://vidaa.do.am/images/' + filename;
            } catch (e) { imageUrl = thumbUrl; } // Fallback to original URL on error
        } else {
            // Assume relative path or needs prefix - needs clarification
            imageUrl = thumbUrl; // Might need THUMBNAIL_BASE_URL + imageFolderPrefix + thumbUrl
        }
    }
    $('#debugThumbnailPreview').attr('src', imageUrl).on('error', function() { $(this).hide(); }).show();
}

// --- Save/Install Function for Debug Editor ---
function saveDebugAppChanges() {
    var appName = $('#debugAppName').val().trim();
    var thumbnailUrl = $('#debugThumbnailUrl').val().trim();
    var appUrl = $('#debugAppUrl').val().trim();
    var appType = 'store'; // Type seems fixed to 'store' for edited apps
    var appId = appName + 'debug'; // Create debug ID

    // --- Validation ---
    if (appName === '' || appUrl === '') {
        logGroupedMessage("Validation Error", "-", "App Name and App Url could not be null !", "-");
        return;
    }
    if (!appUrl.startsWith('http')) {
         logGroupedMessage("Validation Error", "-", "App Url must start with http or https", "-");
         return;
    }

    // Check if an app with the same URL but different name is already installed (potential conflict)
    var conflict = installedDebugApps.find(installedApp => installedApp.URL === appUrl && installedApp.appName !== appName);
    if (conflict) {
        // Append error message directly to the #console div
        $('#console').append('<div>' + 'Conflict: You have installed "' + conflict.appName + '" with the same URL ' + appUrl + '. Please use a unique URL or match the name.' + '</div>');
        return; // Stop if conflict found
    }

    // Default thumbnail if none provided
    if (thumbnailUrl === '') {
        thumbnailUrl = THUMBNAIL_BASE_URL + imageFolderPrefix + 'anb_icon.png'; // Default icon
    }

    // --- Installation Call ---
    logGroupedMessage("Install/Update", "-", "Attempting action for: " + appName, "- URL: " + appUrl);
    Hisense_installApp(
        appId,
        appName,
        thumbnailUrl, // Repeated 3 times
        thumbnailUrl,
        thumbnailUrl,
        appUrl,
        appType, // 'store'
        function(installError) { // Callback
            if (installError) {
                logGroupedMessage('Install Error', '-', "INSTALLATION FAILED for " + appName, '-', installError);
            } else {
                logGroupedMessage('Install Success', '-', appName + " app INSTALLATION COMPLETED/UPDATED !", '-');
                // Update the displayed thumbnail preview
                $('#debugThumbnailPreview').attr('src', thumbnailUrl);
                refreshAppsOnHisenseUI(appId); // Notify UI

                // TODO: Update the installedDebugApps array and the dropdown list after success
                // This requires fetching the updated list or modifying the local array.
            }
        }
    );
}

// --- Trigger Functions for Debug Port/Log Buttons ---
function triggerDebugPortOn() {
    console.log("Triggering Debug Port ON");
    try {
        var result = HiBrowser.File.openDebugPort();
        $('#console').append('<div>' + (result === 0 ? "OpenDebugPort successed, please reboot TV" : "OpenDebugPort failed! Check TV memory.") + '</div>');
    } catch (e) {
        console.error("HiBrowser.File.openDebugPort API not available or failed.", e);
        $('#console').append('<div>ERROR: Debug Port API unavailable.</div>');
    }
}

function triggerDebugPortOff() {
    console.log("Triggering Debug Port OFF");
     try {
        var result = HiBrowser.File.closeDebugPort();
        $('#console').append('<div>' + (result === 0 ? "CloseDebugPort successed, please reboot TV" : "CloseDebugPort failed! Check TV memory.") + '</div>');
     } catch(e) {
         console.error("HiBrowser.File.closeDebugPort API not available or failed.", e);
         $('#console').append('<div>ERROR: Debug Port API unavailable.</div>');
     }
}

function triggerGetTvLog() {
    console.log("Triggering Get TV Log");
    var $getLogButton = $('#getTvLogButton');
    var $consoleDiv = $('#console');
    try {
        $getLogButton.prop('disabled', true);
        $consoleDiv.append('<div>' + "getting log from TV...Please wait..." + '</div>');

        var fetchLogData = function() {
            try {
                var logData = HiBrowser.File.getLog();
                $consoleDiv.append('<div><pre>' + (logData || "No log data received.") + '</pre></div>'); // Use <pre> for formatting
                $getLogButton.prop('disabled', false);
            } catch (e) {
                 console.error("HiBrowser.File.getLog API call failed.", e);
                 $consoleDiv.append('<div>ERROR fetching log.</div>');
                 $getLogButton.prop('disabled', false);
            }
        };
        // Fetch log after a delay
        setTimeout(fetchLogData, 1000);
    } catch (e) {
         console.error("HiBrowser.File.getLog API not available or initial access failed.", e);
         $consoleDiv.append('<div>ERROR: Get Log API unavailable.</div>');
         $getLogButton.prop('disabled', false); // Re-enable button on initial error too
    }
}

// --- Dropdown Change Handler for Debug Editor ---
function changeDebugEditorSelection() {
    var selectedIndex = $('#debugAppSelect').prop('selectedIndex');
    if (selectedIndex >= 0 && selectedIndex < installedDebugApps.length) {
        var selectedApp = installedDebugApps[selectedIndex];
        fillDebugEditorFields(selectedApp); // Fill the editor fields with selected app's data
    }
}