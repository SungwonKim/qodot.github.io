Title: Python으로 텔레그램 봇 만들기
Slug: Python으로-텔레그램-봇-만들기
Date: 2016-03-06
Tags: python, telegrambot

## 개요 및 기획

회사에 있는 하루 중 가장 힘든 시간은 바로 점심을 뭘 먹을지 결정하는 순간이다. 사실 누구든 아무거나 먹어도 상관 없는데 아무도 결정하지 못하는 상황을 자주 마주치게 된다. 그래서 나는 우리 대신 빠른 결정을 내려줄 무언가가 필요하다고 생각했다.

식당을 등록/제거하고, 등록된 식당을 조회하고, 등록된 식당 중에 하나를 랜덤으로 뽑아줄 기능이 필요했다. 그런데 이렇게 간단한 기능을 웹서비스로 구현하는 것은 불필요하게 큰 작업이라는 생각이 들었고, 마침 평소에 궁금해 했던 텔레그램 봇 API를 이용해서 만들면 적절하겠다라는 생각을 했다.

<br>
## Bot Token 얻기

텔레그램을 pc나 스마트 기기에 설치하고, 친구 검색창에 `@BotFather`를 입력해서 봇 파더와 대화를 시작한다. 봇 파더에게 `/start`, `/newbot` 명령어를 차례로 입력하고, 프로젝트 이름과 봇의 이름을 입력하면 access token을 준다. 이것을 잘 저장해놓고 있자.

<br>
## Telepot 설치

[텔레그램의 공식 봇 API 문서](https://core.telegram.org/bots/api)를 봐도 되지만, 더 간단한 방법이 있다. 봇 API를 wrapping한 telepot([github](https://github.com/nickoala/telepot))을 쓰면 된다.

적절히 python 환경을 구성한 뒤, telepot을 설치한다.

    pip install telepot

기본적인 사용법은 telepot github 페이지에 잘 정리되어 있다. 그 중에서도 더 기본적인 기능만 소개해보면,

    # 봇 생성
    bot = telepot.Bot(YOUR_ACCESS_TOKEN)

    # 메세지 수신 대기 (busy waiting)
    import time
    bot.notifyOnMessage(callback_function_to_handle_message)
    while True:
        time.sleep(10)

    # 메세지 발신
    bot.sendMessage(target, sending_message)

메세지 발신시의 `target`은 수신 메세지에 들어있는 `chat_id`이다. (수신된 메세지를 출력해 보면 구조를 자세히 알 수 있다.)

이를 잘 조합해서 간단하게 필요한 기능을 구현할 수 있다. 커스텀 키보드를 유저에게 노출시켜서 편리한 UX을 제공할 수도 있으니, 이용해 보면 좋을 것 같다.

<br>
## SQLAlchemy

### 설치

등록한 음식점을 데이터베이스에 저장해 놓아야 다음에 다시 등록하는 일 없이 사용할 수 있기 때문에, `sqlalchemy`와 `sqlite`를 이용해서 간단하게 데이터베이스를 구현해 보자.

`sqlalchemy`에 대한 기본적인 소개와 튜토리얼은 [Haruair님의 SQLAlchemy 시작하기](http://haruair.com/blog/1682)에 잘 정리되어 있으니 참고바란다.

다음 명령어로 설치한다.

    pip install sqlalchemy

### Scheme 생성

다음은 데이터베이스 연결을 수행하고, 식당의 테이블 정보를 담고있는 `sqlalchemy` 모델 정보가 담겨있는 `db.py` 파일이다.

    from datetime import datetime

    from sqlalchemy import create_engine
    from sqlalchemy import Column, Integer, String, DateTime
    from sqlalchemy.orm import sessionmaker
    from sqlalchemy.ext.declarative import declarative_base


    # 데이터베이스 연결 및 세션 취득
    engine = create_engine('sqlite:///db.sqlite3', echo=True)
    session = sessionmaker(bind=engine)() #
    Base = declarative_base()


    # 식당 테이블
    class Restaurant(Base):
        __tablename__ = 'restaurants'

        id = Column(Integer, primary_key=True)
        name = Column(String)
        created_at = Column(DateTime, default=datetime.now)
        updated_at = Column(DateTime, default=datetime.now, onupdate=datetime.now)

위의 `session` 변수를 통해 데이터베이스에 접속해서 쿼리를 실행할 수 있다.

### Migration

이제 저 python class를 이용해  실제 데이터베이스의 테이블로 만들어줘야 하는데, 여러가지 방법이 있다.

1. 직접 데이터베이스에 접속해서 `create table` 쿼리를 날린다.
2. sqlalchemy의 `Base.metadata.create_all(engine)`를 이용해서 자동으로 테이블을 생성한다.
3. `alembic`을 이용해서 마이그레이션 한다.

1번은 너무 귀찮고, 2번의 경우 테이블 생성은 되지만 테이블 변경은 자동으로 되지 않는 문제가 있어서(프로젝트가 단순해서 변경할 일이 없다면 문제 없겠지만) 3번을 선택했다. `alembic`은 `sqlalchemy`를 위한 마이그레이션 툴이고, 이전에 작성했던 [Alembic 퀵 가이드](http://qodot.github.io/Alembic-%ED%80%B5-%EA%B0%80%EC%9D%B4%EB%93%9C.html)에서 간단하게 소개한 적이 있다. 참고하길 바란다.

### 사용

1, 2, 3번 중 하나를 선택해서 테이블 스키마를 생성했다면, 이제 데이터베이스에 접속해서 쿼리를 날려볼 차례인데, 여기서는 이 프로젝트에서 사용한 기본적인 `select`, `insert`, `delete` 동작의 예시를 소개해 본다.

    # 식당 테이블의 모든 row 조회
    restaurants = session.query(Restaurant).all()

    # 식당 테이블의 모든 row 갯수 조회
    restaurants_count = session.query(Restaurant).count()

    # 새 식당 등록
    restaurant = Restaurant(name=name)
    session.add(restaurant)
    session.commit()

    # 특정 이름을 가진 식당 하나를 제거
    restaurant = session.query(Restaurant).filter(Restaurant.name==name).first()
    session.delete(restaurant)
    session.commit()

<br>
## 개선점

`telepot`과 `sqlalchemy`를 이용해서 텔레그램 봇을 만들 수 있다. 그런데 실제로 봇을 운영하려면 python 스크립트를 리눅스 데몬이나 서비스로 띄우는 방법에 대한 고려가 되어야 한다. 그리고 이벤트 listen을 담당하는 부분이 busy waiting 방식으로 구현되어 있는데 `asyncio`를 이용한 비동기 방식으로 구현하는 것이 더 좋을 것이다. 특히 두 번 째 부분은 공부가 많이 필요한 부분이라... 따로 포스트를 작성하면서 정리해야 겠다.
