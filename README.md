## python-flask-docker
#### Итоговый проект курса "Машинное обучение в бизнесе"

### Стек:
- DL: tensorflow, keras, PIL 
- API: flask 
- Данные: с kaggle - https://www.kaggle.com/playlist/men-women-classification


### Задача: Классификация пола человека по фото. Бинарная классификация
- Модель: предобученная модель InceptionV3
- Используемые признаки: фото человека в формате .jpeg

Файлы в репозетории подготовленны для создания образа Docker<br>
**из за большого объёма файла модели (188Мб), загрузить сам файл модели на сервис Github не удалось**

Готовый образ Docker можно скачать c http://hub.docker.com

``` $ docker pull sergeyvaganov/course_ml:latest ``` 

<hr>

 __Классификатор работает по порту 8181, имеет интенрфейсы api и web__ 



#### пример запроса api:
```
import requests
def post_qery(name):
    '''
    name - путь + имя файла для классификации
    '''
    url = '<<<http://172.17.0.2:8181>>>/api/predict'
    fp = open(name, 'rb')    
    files = {'file': fp}
    resp = requests.post(url, files=files)
    fp.close()
    return resp.text
```

```<<http://172.17.0.2:8181>>``` - необходимо указать адрес запущенного контейнера.
