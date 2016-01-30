Title: Pyenv로 Python 환경 설정하기
Slug: Pyenv로-Python-환경-설정하기
Date: 2016-01-30
Tags: python

### 개요

전에 [Python 개발 환경 구축](http://qodot.github.io/Python-%EA%B0%9C%EB%B0%9C-%ED%99%98%EA%B2%BD-%EA%B5%AC%EC%B6%95.html)이라는 포스트에서 `vitualenv`를 이용해서 Python의 가상환경을 구축하는 방법을 설명한 적이 있었다. 그런데 `virtualenv`만으로는 다양한 Python 버전을 관리할 수가 없었고, (Ruby의 `rbenv`처럼)이 문제를 해결하기 위한 도구가 `pyenv`이다. `virtualenv`의 기능도 `pyenv`의 플러그인(`pyenv-virtualenv`)으로 똑같이 있기 때문에 `pyenv`를 안 쓸 이유가 없다.

마지막에는 환경 설정을 더 편하게 해주는 `autoenv`도 소개하겠다.

<br>
### Pyenv

사실 설치부터 사용법까지 대부분의 가이드가 개발자 [Github](https://github.com/yyuu/pyenv)에 자세하게 나와있다. 여기서는 바로 시작할 수 있도록 핵심만 간단히 다루겠다.

#### 설치

*방법 1*: `homebrew`를 통해 설치

	brew install pyenv

	# .zshrc .bashrc .bash_profile 등에 다음을 추가
	eval "$(pyenv init -)"

*방법 2*: 소스를 직접 다운로드해서 설치

	git clone https://github.com/yyuu/pyenv.git ~/.pyenv

    # .zshrc .bashrc .bash_profile 등에 다음을 추가
    export PYENV_ROOT="$HOME/.pyenv"
	export PATH="$PYENV_ROOT/bin:$PATH"
    eval "$(pyenv init -)"

#### 사용법

설치 가능한 Python 버전 확인

	pyenv install --list

Python 설치

	pyenv install <version>

shim 바이너리 리빌드 (바이너리 설치 후에 반드시 해줘야 함)[^1]

	python rehash

현재 사용중인 Python version 확인

	pyenv version
	>> 3.5.0 (set by /Users/user/.pyenv/version)

설치된 Python 버전 확인

	pyenv versions
    >> system
	* 3.5.0 (set by /Users/user/.pyenv/version)
	3.5.1

<br>
### Pyenv-virtualenv

`pyenv` 개발자가 만든 플러그인이다. 역시 [Github](https://github.com/yyuu/pyenv-virtualenv)에 설치법과 사용법이 자세히 나와 있다.

#### 설치

*방법 1*: `homebrew`를 통해 설치

    brew install pyenv-virtualenv

    # .zshrc .bashrc .bash_profile 중 하나에
    eval "$(pyenv virtualenv-init -)"

*방법 2*: 소스를 직접 다운로드해서 설치

	git clone https://github.com/yyuu/pyenv-virtualenv.git ~/.pyenv/plugins/pyenv-virtualenv

    # .zshrc .bashrc .bash_profile 중 하나에
    eval "$(pyenv virtualenv-init -)"

#### 사용법

Python 버전과 함께 새로운 가상환경 생성

	pyenv virtualenv <python_version> <virtualenv_name>

가상환경 활성화

	pyenv activate <virtualenv_name>

가상환경 해제

    pyenv deactivate

<br>
### Autoenv

#### 개요

디렉토리 기반의 환경 설정 도구. 디렉토리를 이동할 때마다 해당 디렉토리에 `.env`파일 안에 있는 스크립트를 실행한다. 자세한 내용은 [Github](https://github.com/kennethreitz/autoenv)을 참조한다.

#### 설치

	brew install autoenv

	# .zshrc .bashrc .bash_profile 중 하나에
	source /usr/local/opt/autoenv/activate.sh

#### 사용

원하는 디렉토리에 원하는 스크립트로 `.env` 파일을 작성한다. 예를 들면,

	# 디렉토리에 진입하면 특정 Python 가상환경을 활성화한다.
	pyenv activate <virtualenv_name>

<br>
#### 참조한 사이트

- [pyenv + virtualenv + autoenv 를 통한 Python 개발 환경 구축하기](https://dobest.io/how-to-set-python-dev-env/)

<br>
[^1]: rehash를 자동화하고 싶다면 다음 플러그인을 참조한다. https://github.com/yyuu/pyenv-pip-rehash
