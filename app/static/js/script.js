// Функция для вывода отладочных сообщений на экран
function logToScreen(message) {
    const logContainer = document.getElementById('debug-log');
    if (logContainer) {
        const entry = document.createElement('p');
        // Добавляем время для наглядности
        const time = new Date().toLocaleTimeString();
        entry.textContent = `[${time}] ${message}`;
        // Новые сообщения добавляются сверху
        logContainer.prepend(entry);
    }
}
// ===== Helpers =====
function createTile(app, isInstalled) {
    const container = document.getElementById("app-grid");
    const tile = document.createElement("div");
    tile.className = "app-tile";
    if (isInstalled) tile.classList.add("installed");

    // иконка
    const iconWrapper = document.createElement("div");
    iconWrapper.className = "app-icon-placeholder";
    const icon = document.createElement("img");
    icon.src = app.thumbnail_url || "";
    icon.alt = app.name;
    icon.onerror = () => { icon.style.display = "none"; };
    iconWrapper.appendChild(icon);

    // название
    const title = document.createElement("div");
    title.className = "app-title";
    title.textContent = app.name;

    // описание
    const desc = document.createElement("div");
    desc.className = "app-text";
    desc.textContent = app.text || "";

    // кнопка
    const button = document.createElement("button");
    button.className = "install-button";
    if (isInstalled) {
        button.textContent = "Uninstall";
        button.onclick = () => handleUninstall(app, button, tile);
    } else {
        button.textContent = "Install";
        button.onclick = () => handleInstall(app, button, tile);
    }

    // сборка
    tile.appendChild(iconWrapper);
    tile.appendChild(title);
    tile.appendChild(desc);
    tile.appendChild(button);
    container.appendChild(tile);

    return tile;
}

// ===== Core API wrappers =====
function installApp(app, onSuccess, onError) {
    try {
        if (typeof Hisense_installApp === "function") {
            Hisense_installApp(
                app.install_app_id,
                app.name,
                app.thumbnail_url,
                app.thumbnail_url,
                app.thumbnail_url,
                app.url,
                app.store_type,
                function (res) {
                    if (!res || res === 0 || res === "0" || res === true) {
                        onSuccess && onSuccess();
                    } else {
                        onError && onError(res);
                    }
                }
            );
        } else {
            throw new Error("Hisense_installApp API недоступен");
        }
    } catch (e) {
        console.error("installApp error:", e);
        onError && onError(e);
    }
}

function uninstallApp(app, onSuccess, onError) {
    try {
        if (typeof Hisense_uninstallApp === "function") {
            Hisense_uninstallApp(app.install_app_id, function (res) {
                if (!res || res === 0 || res === "0" || res === true) {
                    onSuccess && onSuccess();
                } else {
                    onError && onError(res);
                }
            });
        } else {
            throw new Error("Hisense_uninstallApp API недоступен");
        }
    } catch (e) {
        console.error("uninstallApp error:", e);
        onError && onError(e);
    }
}

// ===== Handlers =====
function handleInstall(app, button, tile) {
    console.log("Installing:", app.name);
    button.textContent = "Installing...";
    button.disabled = true;

    installApp(
        app,
        () => {
            console.log(`Application '${app.name}' installed successfully.`);
            tile.classList.add("installed");
            button.textContent = "Uninstall";
            button.disabled = false;
            button.onclick = () => handleUninstall(app, button, tile);
        },
        (err) => {
            console.error("Install error:", err);
            button.textContent = "Install";
            button.disabled = false;
        }
    );
}

function handleUninstall(app, button, tile) {
    console.log("Uninstalling:", app.name);
    button.textContent = "Uninstalling...";
    button.disabled = true;

    uninstallApp(
        app,
        () => {
            console.log(`Application '${app.name}' uninstalled successfully.`);
            tile.classList.remove("installed");
            button.textContent = "Install";
            button.disabled = false;
            button.onclick = () => handleInstall(app, button, tile);
        },
        (err) => {
            console.error("Uninstall error:", err);
            button.textContent = "Uninstall";
            button.disabled = false;
        }
    );
}

// ===== Init =====
async function loadApps() {
    try {
        const resp = await fetch("/apps");
        const apps = await resp.json();

        let installedIds = [];
        try {
            if (typeof Hisense_getInstalledApps === "function") {
                Hisense_getInstalledApps(function (res) {
                    if (res && res.AppInfo) {
                        installedIds = res.AppInfo.map((a) => ({
                            id: (a.Id || a.appId || "").toLowerCase(),
                            name: (a.AppName || "").toLowerCase(),
                            url: (a.URL || "").toLowerCase()
                        }));
                    }
                    renderApps(apps, installedIds);
                });
                return; // ждём коллбэк
            }
        } catch (e) {
            console.warn("Hisense_getInstalledApps error:", e);
        }

        renderApps(apps, installedIds);
    } catch (e) {
        console.error("Ошибка загрузки списка приложений:", e);
    }
}
// ===== Версия loadApps с экранным логгером =====
// async function loadApps() {
//     logToScreen("1. Функция loadApps ЗАПУЩЕНА.");
//     try {
//         logToScreen("2. Создаем промис для Hisense API и ждем его...");
//
//         const installedIds = await new Promise((resolve, reject) => {
//             try {
//                 if (typeof Hisense_getInstalledApps === "function") {
//
//                     const timeoutId = setTimeout(() => {
//                         logToScreen("!!! Hisense_getInstalledApps не ответила за 5 секунд! Продолжаем с пустым списком.");
//                         resolve([]);
//                     }, 5000);
//
//                     Hisense_getInstalledApps(function (res) {
//                         clearTimeout(timeoutId);
//                         logToScreen("3. Коллбэк от Hisense_getInstalledApps СРАБОТАЛ!");
//
//                         if (res && res.AppInfo) {
//                             const ids = res.AppInfo.map((a) => ({
//                                 id: (a.Id || a.appId || "").toLowerCase(),
//                                 name: (a.appName || "").toLowerCase(),
//                                 url: (a.URL || "").toLowerCase(),
//                             }));
//                             resolve(ids);
//                         } else {
//                             resolve([]);
//                         }
//                     });
//                 } else {
//                     logToScreen("Hisense_getInstalledApps is not available.");
//                     resolve([]);
//                 }
//             } catch (e) {
//                 logToScreen(`!!! Ошибка внутри промиса Hisense: ${e.message}`);
//                 reject(e);
//             }
//         });
//
//         logToScreen("4. Промис от Hisense API ЗАВЕРШИЛСЯ. Сейчас будет fetch.");
//
//         const resp = await fetch("/apps");
//         logToScreen("5. Запрос fetch УСПЕШНО отправлен и получен ответ.");
//         const apps = await resp.json();
//
//         renderApps(apps, installedIds);
//         logToScreen("6. Приложения отрисованы.");
//
//     } catch (e) {
//         logToScreen(`!!! ВНЕШНИЙ CATCH. Ошибка в loadApps: ${e.message}`);
//     }
// }

function renderApps(apps, installedIds) {
    const container = document.getElementById("app-grid");
    container.innerHTML = "";
    apps.forEach((app) => {
        const isInstalled = installedIds.some(inst =>
            inst.id === app.install_app_id.toLowerCase() ||
            inst.name === app.name.toLowerCase() ||
            (app.url && inst.url === app.url.toLowerCase())
        );
        // logToScreen(`Inst: ${installedIds.name} App: ${app.name}`);
        // logToScreen(`${installedIds.name}`)
        // logToScreen(${app.name})
        logToScreen("!!!!!!!!");
        createTile(app, isInstalled);
    });
}

window.addEventListener("DOMContentLoaded", loadApps);
