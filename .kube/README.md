                                    Установка в кластер Kubernetes. 

Описание проекта:

 frontend - тут располагает кодовая база frontend(vue)
 backend - тут располагается кодовая база backend(django).
    
    .kube  - тут располагаются манифесты kubernetes
    
    ./kube/ns.yml — манифест создающий отдельный namespace (x5-lot14) для приложения 

    ./kube/django.yml  манифест описывающий  контейнер backend приложения  

    ./.kube/migrate.yml - манифест описывающий миграции из backend прложения  в базу данных  postgrsql

    ./.kube/frontend.yml - манифест описывающий  контейнер frontend приложения

    ./.kube/postgresql - тут находятся манифесты для развертывания базы данных postgrsql

    ./.k ube/config_map.yml — манифест с переменными для контейнеров Postgresql, frontend, backend

    ./.kube/registry.yml - манифест для доступа к закрытому docker registry  

    ./.kube/ingress.yml — манифест описывающий ингресс контроллер 

    .gitlab-ci.yml - файл описывающий ci/cd
    
    Dockerfile.backend - Докерайл для сборки контейнера с приложением backend 

    Dockerfile.frontend - Докерайл для сборки контейнера с приложением frontend 

    nginx.conf - файл конфигурации nginx

Для работы с данным репозиторием требуется, либо один, либо 2 gitlab-runner. Если раннер один то он должен быть тегирован (tenders , docker ), если их 2 то теги будет следуюшие (docker) и (tenders). В текущий конфигурации использовалось 2 раннера, deploy раннер использовался готовый докер образ для деплоя в kubernetes.
Сборка производится в dind. в gitlab-ci.yml.
Что бы развернуть данный сервис требуется провести деплой текущей ветки.

 http://$DOMAIN/

                                    Запуск манифестов.                                       
    kubectl apply -f ns.yml

    kubectl apply -f config_map.yml

    kubectl apply -f registry.yml

    kubectl apply -f ingress.yml

    kubectl apply -f postgres.yml

    kubectl apply -f migrate.yaml

    kubectl apply -f django.yml

    kubectl apply -f frontend.yml

 
Для удаление приложения из kubernetes кластера.
 
    kubectl delete ns x5-lot14
 



