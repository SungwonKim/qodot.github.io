Title: Python/Django에서 Celery로 Task Queue 구축
Slug: Python/Django에서-Celery로-Task-Queue-구축
Date: 2016-04-05
Tags: python, django, celery

## 개요

서비스를 만들다보면 유저에게 특정 요청이 들어오면 이메일을 보내야 할 때가 있다. 그런데 이 때, 메일 서버의 상태가 좀 이상하다면? 혹은 서버에 이미 보내야 할 메일이 산더미처럼 쌓여있다면? 이메일 전송이 지연되면 유저의 요청도 지연되고, 유저는 기다리다 지쳐 서비스 이용을 관두게 된다 ㅜㅜ 그럼 어떡하지?

일단 유저에게는 요청이 완료되었다는 응답을 보내고, 이메일을 보내는 과정은 서버가 알아서 기다리고 알아서 처리하게 하는 방법이 있다. 실제로 우리도 어떤 서비스를 가입하면 가입 환영 메일을 받는데, 가입하자마자 오는 경우도 있지만 시간이 꽤 지난 후에 메일을 받는 경우도 많다.

태스크 큐`task queue`를 이용하면 이런 비동기 작업을 수월하게 할 수 있다. 이메일을 보내라는 요청이 들어오면 일단 큐에 이메일을 보내는 작업`task`을 넣어놓고, 결과에 상관없이 유저에게는 응답을 보낸다. python에서는 [`celery`](http://www.celeryproject.org/)라는 아주 인기 높은 분산 태스크 큐가 있다. `celery`와 함께라면 당신도 억울하게 유저를 잃지 않을 수 있다. 추가로 `celery`의 작업들을 모니터링 할 수 있는 `flower`까지 알아보자.

<br>
## Message Broker

`celery`에서 실제로 작업을 처리하는 프로세스를 워커`worker`라고 하는데, 이 워커가 일을 하려면 작업을 전달해주는 메세지 브로커`message broker`가 필요하다. 그리고 이 메세지 브로커는 `celery` 내부에 있는 것이 아니고 따로 설치를 해줘야 한다.

대표적으로 `rabbitmq`와 `redis`가 있는데, 데이터베이스를 쓸 수도 있고 다른 프로그램을 쓸 수도 있지만, (공식적으로도) [추천하지 않는다](http://docs.celeryproject.org/en/latest/getting-started/brokers/index.html). 그냥 `rabbitmq`를 쓰자.

### RabbitMQ 설치

[공식 문서](https://www.rabbitmq.com/download.html)를 참조하는게 좋다. 내가 쓰는 OS만 대표적으로 옮겨 놓겠다.

#### OS X

``` bash
brew update
brew install rabbitmq
```

#### RHEL

무슨 이유인지는 모르겠는데 `erlang`, `rabbitmq` 둘 다 `yum`에 기본적으로 등록이 안 되어있다.

``` bash
# install erlang
wget http://packages.erlang-solutions.com/erlang-solutions-1.0-1.noarch.rpm
rpm -Uvh erlang-solutions-1.0-1.noarch.rpm
yum install erlang

# install rabbitmq-server
wget http://www.rabbitmq.com/releases/rabbitmq-server/v3.6.0/rabbitmq-server-3.6.0-1.noarch.rpm
rpm -Uvh rabbitmq-server-3.6.0-1.noarch.rpm
```

### RabbitMQ 실행

``` bash
rabbitmq-server
```

브로커가 떴다!

<br>
## Celery Worker

실제로 워커를 띄우기 위해 `celery`를 적용해보자. 본 포스트에서는 `django`와 연동하는 예제([공식 문서](http://docs.celeryproject.org/en/latest/django/first-steps-with-django.html)도 같이 참조하면 좋다)을 보여주겠다.[^1]

### Celery 설치

``` bash
pip install celery
```

### Celery 설정

`celery` 애플리케이션을 설정하고 생성하기 위해서 `django`의 설정 디렉토리(최초 `settings.py`가 있는 디렉토리)에 `celery.py` 파일을 만들고 다음 코드를 작성한다.

``` python
from __future__ import absolute_import

import os

from celery import Celery
from django.conf import settings

# celery 앱에 django의 settings 값을 주입한다.
os.environ.setdefault(
    'DJANGO_SETTINGS_MODULE', os.environ.get('DJANGO_SETTINGS_MODULE')
)

app = Celery('your_django_app_name')
```

같은 디렉토리의 `__init__.py`에 다음과 같이 입력한다.

``` python
from your_django_app_name.celery import app as celery_app
```

`django`의 `settings.py`에 `celery`가 `rabbitmq`와 연결할 수 있도록 다음과 같은 설정을 추가한다.

``` python
# rabbitmq의 기본 유저, 기본 호스트, 기본포트(5672)로 연결한다.
BROKER_URL = 'amqp://guest:guest@localhost//'
```

이제 `django`가 구동되면서 `celery`를 생성하게 되고, 사용할 수 있다.

### Celery Task 작성

서두에 말했던 것과 같이 이메일을 보내는 간단한 작업을 작성해보자. 간단하게 `django`의 `send_mail` 메소드를 이용하자.

``` python
from celery import shared_task
from django.core.mail import send_mail

# shared_task는 하나의 프로젝트에서 여러개의 celery 인스턴스를 생성할 경우, 인스턴스에서 공유가 가능한 작업을 뜻한다
@shared_task
def send_email(title, content, fromm, to, html_content=None):
    send_mail(title, content, fromm, to, html_message=html_content)
```

WOW! 엄청 간단하다. 그럼 이제 실제로 이 작업을 사용해보자.

### Django View 작성

`@shared_task`로 선언된 함수를 실행할 때, `delay()`를 통해 실행하면[^2] 자동으로 메세지 브로커를 통해 작업이 워커로 날아간다! 너무 편하다!

``` python
from your_tasks_path import send_email
def some_controller_method(request):
    ...
	send_email.delay('my_title', 'my_content', 'noreply@email.com', ['target@email.com'])
    ...
```

### Celery Worker 프로세스 구동

`django`의 루트 디렉토리로 이동한 후, 다음 명령어로 메세지 브로커를 통해 받은 작업을 처리할 워커를 띄운다.

``` bash
celery worker -A your_django_app_name -l info
```

콘솔에 이런저런 로그가 뜨면서 `rabbitmq`와 연결되었다는 메세지를 확인하면 성공이다.

<br>
## Flower를 통한 Celery 모니터링

유저의 HTTP 요청은 이메일 전송 성공 여부에 상관없이 성공 응답(200)을 뱉는다. 그럼 실제로 이메일 전송 작업이 성공했는지는 어떻게 알지? 걱정마라. `celery`를 모니터링 할 수 있는 오픈소스인 [`flower`](http://flower.readthedocs.org/en/latest/)가 있다.

### Flower 설치

``` bash
pip install flower
```

### Flower 실행

`django`의 루트 디렉토리로 이동한 후, 다음 명령어로 `flower` 웹 인스턴스를 띄운다.

``` bash
# 기본 포트는 5555이다
flower -A your_django_app_name
```

`rabbitmq`와 `celery` 워커가 실행되어 있다면 정상적으로 인스턴스가 구동된다. `localhost:5555`로 접속하면 [멋진 화면](http://flower.readthedocs.org/en/latest/screenshots.html)을 볼 수 있다. 이렇게 간단하게 괜찮은 모니터링 툴을 이용할 수 있다니 ㅜㅜ

<br>
[^1]: `django`와 상관없이 python에서는 모두 사용 가능하다.
[^2]: `delay()`를 안 붙이면 그냥 평범한 함수처럼 실행된다.
