Title: Django 설정을 환경 변수로 관리하기
Slug: Django-설정을-환경-변수로-관리하기
Date: 2015-07-30
Tags: django

### 개요
설정 정보를 다루다 보면 코드에 그대로 적어서는 안되는 정보들이 있다. 예를 들어 Github의 public 계정을 사용할 경우, 불특정 다수가 서비스의 상용 데이터베이스의 접속 정보를 알아서는 안될 것이다.

그래서, 간단하게 django 설정 정보를 환경 변수로 등록해서 repository에 노출되지 않도록 해보자. (SECRET_KEY를 예로 들겠음) 만약 virtualenv를 쓰고 있지 않다면 상당히 간단하다.

<br>
### Virtualenv를 사용하지 않는 경우

`.bashrc`, `.bash_profile`, `.zshrc`에 환경 변수를 등록한다.

	export SECRET_KEY='my_secret_key'

Django의 설정 변수를 다음과 같이 바꾼다.

    import os
    SECRET_KEY = os.environ.get('SECRET_KEY')

끝!

<br>
### Virtualenv를 사용하는 경우

해당 프로젝트가 이용하는 가상환경 디렉토리로 이동한다.

    cd ~/.virtualenvs/myproject/

`bin` 디렉터리로 이동해서 `postactivate` 파일을 편집기로 연다.

    cd bin
    vi postactivate
    # postactivate : 가상환경이 실행되고 바로 다음에 실행할 shell script

등록할 환경 변수를 입력한다.

    export SECRET_KEY='my_secret_key'

`postdeactivate` 파일을 편집기로 연다.

    vi postdeactivate
    # postdeactivate : 가상환경에서 빠져 나오고 바로 다음에 실행할 shell script

앞에서 등록했던 환경변수를 해제한다.

    unset SECRET_KEY

Django의 설정 변수를 다음과 같이 바꾼다.

    import os
    SECRET_KEY = os.environ.get('SECRET_KEY')

끝!

<br>
##### PS
전에 작성했던 Django 환경 설정 분리에서 `DJANGO_SETTINGS_MODULE`를 사용했었다. 이 값도 `postactivate`와 `postdeactivate`에 등록해서 관리가 가능하다.

<br>
##### 참고한 페이지
- [Where to store secret keys DJANGO](http://stackoverflow.com/questions/15209978/where-to-store-secret-keys-django)
