# Тестовое задание Лот 37

#### Задача: Cоздание единой точки для всех каналов коммуникаций с сохранением всей истории коммуникации с клиентом компании

Ключевые задачи, которые должны быть решены в ходе реализации проекта:
- агрегация всех актов коммуникации с клиентом
- создание расширяемой системы политик, определяющих правила коммуникации: блокировка пользователя, лимиты с рамках департамента, бронирование пользователя
- создание системы фоновых задач, которые формируют очередь для отправки сообщений клиентам компании, учитывая политики коммуникации
- создание элементов BI системы: формирование статиски коммуникации в различных срезах данных

В силу ограниченности времени и условий работы над задачей (это тестовое задание) была реализована часть системы, описанной выше:
- описана модель данных в [doc/README.md](doc/README.md);
- частично реализована модель данных и созданы все основные api endpoints, описанные в постановке задачи  [backend/](backend/). Использовались Django, DRF, Postgres, JWT;
- не добавлена валидация для полей, не содаржащих списки выбора
- документация API доступна по ссылке  [https://lot37.artw.dev/api/v1/schema/swagger/#/](https://lot37.artw.dev/api/v1/schema/swagger/#/)
- реализован процесс деплоя и разворачивания приложения в кластере в [https://lot37.artw.dev/](https://lot37.artw.dev/)
- описан процесс разворачивания в k8s [.kube/README.md](.kube/README.md)


> Для обеспечения не прерывной доставки кода до конечной точки, в данном случае кластер Kubernetes. Использован система хранения кода GitLab, встроенными инструментами написан механизм доставки(пайплайн) и сборки кода, и дальнейшего передачи в кластер.
При обновлении кода в метке main(master) , происходит автоматическая сборка и доставка.
Что обеспечивает непрерывную работу приложения


### Порядок работы с API
1. Выполнить запрос POST /api/v1/sign-up/ Создание нового клиента API, заполнив данные нового клиента API
2. Выполнить запрос POST /api/v1/log-in/ Аутентификация клиента API
3. Скопировать полученный access token
4. В верху страницы сваггера нажать на кнопку Authorize вставить access token из п. 3
5. Работать с API выполняя запросы согласно кейсов