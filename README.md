# e-store

## Описание
**e-store** — API для онлайн магазина, позволяющий пользователям просматривать и заказывать продукты. Приложение построено с использованием FastAPI для бекенда и PostgreSQL для базы данных, а также Docker для удобства развертывания.

## Функционал
- Добавление, обновление и удаление товаров
- Создание и управление заказами

## Требования
- [Docker](https://www.docker.com/)

## Установка и запуск

### 1. Клонирование репозитория

```bash
git clone https://github.com/VictoriaFirsova/FirsovaVV.e-store.git
cd FirsovaVV.e-store
docker-compose up --build
```

### 2. После запуска приложение будет доступно по адресу:

http://localhost:8001/docs

### 3. База данных

Приложение использует PostgreSQL в качестве базы данных. Конфигурация базы данных указана в файле docker-compose.yml. Данные сохраняются в Docker volume, что позволяет сохранять их даже после перезапуска контейнера.

### 4. Реализованы автотесты для эндпойнтов с использованием pytest библиотеки. Покрытите составляет 98%.

## API представлен следующими эндпойнтами:

### Товары (Products)
#### Создать новый продукт:

POST /products
Создает новый товар.

#### Получить список продуктов:

GET /products
Возвращает список всех товаров.

#### Получить детали продукта по ID:

GET /products/{id}
Возвращает информацию о товаре по его ID.

#### Обновить товар по ID:

PUT /products/{id}
Обновляет данные товара по его ID.

#### Удалить товар по ID:

DELETE /products/{id}
Удаляет товар по его ID.

### Заказы (Orders)

#### Создать новый заказ:

POST /orders
Создает новый заказ. Можно добавлять несколько позиций товара

#### Получить список заказов:

GET /orders
Возвращает список всех заказов.

#### Получить детали заказа по ID:

GET /orders/{id}
Возвращает информацию о заказе по его ID.

#### Обновить статус заказа по ID:

PATCH /orders/{order_id}/status
Обновляет статус заказа по его ID.
