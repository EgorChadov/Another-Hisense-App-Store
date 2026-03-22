# Another Hisense App Store

Кастомный магазин приложений для Hisense Vidaa OS.

## Запуск сервера

Открыть PowerShell в корне проекта и выполнить:

```powershell
py -m app.web
```

Сервер стартует на порту **443** (HTTPS). Сертификат `cert.pem` и ключ `key.pem` генерируются автоматически при первом запуске, если отсутствуют.

## Настройка DNS (AdGuard Home)

Чтобы телевизор и устройства обращались к локальному серверу:

- **Filters → DNS Rewrites**: добавить правило `vidaahub.com` → IP компьютера (например `192.168.1.X`)

## Порт занят

Если при запуске ошибка `Address already in use`:

```powershell
# Найти процесс
netstat -ano | findstr :443
# Завершить (заменить PID)
taskkill /PID <PID> /F
```

## API

- `GET /apps` — список приложений (используется телевизором)
- `GET /` — веб-интерфейс магазина
