Title: Python 개발 환경 구축
Slug: Python-개발-환경-구축
Date: 2015-07-27
Tags: python

### Python
OS X에는 python 2가 기본으로 설치되어 있다. 터미널에서 아무데서나 Python 명령어를 입력해서 대화형 인터프리터가 뜨면 설치 확인할 수 있다.

<br>
### Pip
Python 전용 패키지 매니저이다.[^1] `brew`나 `easy_install`로 설치할 수도 있는 것 같은데, 혹시 모를 귀찮은 문제를 피하기 위해 기왕이면 설치 공식 문서에 나와있는대로 설치하자.

<br>
### Virtualenv 개요
Python의 수많은 라이브러리들을 가상환경으로 분리하여 관리할 수 있도록 도와준다. 하나의 개발 장비 안에 여러개의 Python 프로젝트가 존재 할 경우, 각각의 프로젝트들을 독립된 환경에서 개발할 수 있다.

<br>
### Virtualenv 설치
다음과 같은 명령어를 입력하면, `virtualenv`와 `virtualenvwrapper`가 같이 설치된다.

    sudo pip install virtualenvwrapper
    # sudo pip install virtualenv 로 따로 설치도 가능

가상환경을 저장할 디렉토리를 생성한다.

    mkdir ~/.virtualenvs

`.bashrc` (혹은 `.bash_profile`) 혹은 `.zshrc`에 아래와 같이 환경 변수를 등록한다.

    export WORKON_HOME=~/.virtualenvs
    source /usr/local/bin/virtualenvwrapper.sh
    # 보통 /usr/local/bin 에 설치되지만, 혹시 아닐 수도 있으니 확인 필요

아래 명령으로 가상환경을 생성해보자.

    mkvirtualenv myenvname

생성이 완료되면 터미널 프롬프트에 `(myenvname)`이 생긴 것을 볼 수 있다. 지금부터 `pip`으로 설치하는 모든 라이브러리는 `~/.virtualenvs`의 지정한 이름(`myenvname`)의 가상환경 디렉토리안에 놓일 것이다.

가상환경 활성화 비활성화 명령어는 다음과 같다.

    workon myenvname # 활성화
    deactivate # 비활성화

끝!

<br>
[^1]: OS X의 brew, Ubuntu의 apt-get과 비슷한 역할이라고 보면 된다.