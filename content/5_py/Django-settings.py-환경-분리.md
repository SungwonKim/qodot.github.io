Title: Django settings.py 환경 분리
Slug: Django-settings.py-환경-분리
Date: 2015-07-29
Tags: django

### 개요

애플리케이션을 배포하게 되면, 장비에 따라 필요한 라이브러리, 데이터베이스 정보 등 설정 정보를 다르게 가져가야 한다. Django 프로젝트를 생성하면 기본적으로 1개의 `settings.py`가 있는데, 설정 정보를 따로 가져가기 위해서는 파일을 분리할 필요가 있다.

그래서! 기존의 패키지 구조

    myproject/
        myproject/
            settings.py

를

    myproject/
        myproject/
            settings/
                __init__.py
                base.py
                local.py
                development.py
                production.py

로 분리하는 작업을 진행해보자.

<br>
### 설정 파일 분리

일단 모든 환경에 필요한 공통된 설정 정보를 저장할 `base.py`에 기존 `settings.py`의 정보를 모두 복사하고, 다음 `local.py`, `development.py`, `production.py`에 다음과 같이 `base.py`를 import 한다.

	from myproject.settings.base import *

이제 환경마다 다르게 가져갈 설정 정보들을 분리해보자.

    # local.py
    from myproject.settings.base import *

    # local 환경이니까 디버그 모드를 켜야지!
    DEBUG = true

    # local 데이터베이스의 정보를 입력한다.
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.postgresql_psycopg2',
            'NAME': 'LOCAL_DB_NAME',
            'USER': 'LOCAL_DB_USER',
            'PASSWORD': 'LOCAL_DB_PASSWORD',
            'HOST': 'LOCAL_DB_HOST',
            'PORT': 'LOCAL_DB_PORT',
        }
    }

위와 같이 분리할 정보를 `base.py`에서 지우고 환경에 맞는 파일에 넣어주면 된다.

이제 애플리케이션이 구동될 때, 변경된 설정 파일을 읽도록 설정해주어야 한다. 프로젝트의 `wsgi.py` 파일을 열면 기본 설정 파일을 지정하는 코드가 있다.

    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "myproject.settings")

본인 기본 설정을 `local`로 지정할 것이다.

    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "myproject.settings.local")

그러나 이런 하드코딩 방법 말고, 애플리케이션을 구동할 때 다른 설정을 주입할 수 있어야 할 것이다. 두 가지 방법이 있다.

첫 번째는 위에서 봤던 `DJANGO_SETTINGS_MODULE`을 `.bashrc`, `.bash_profile`, `.zshrc`에 환경 변수로 등록하는 방법이다.

    export DJANGO_SETTINGS_MODULE=myproject.settings.local

두 번째는 서버를 띄울 때 설정을 주입하는 방법이다.

    python manage.py runserver --settings=myproject.settings.local

<br>
#### 참고한 페이지

- [Django settings for multiple enviroments](http://morion4000.com/django-settings-for-multiple-environments/)
- [How to manage local vs production settings in Django?](http://stackoverflow.com/questions/1626326/how-to-manage-local-vs-production-settings-in-django)
