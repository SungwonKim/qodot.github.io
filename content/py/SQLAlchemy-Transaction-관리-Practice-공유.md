Title: SQLAlchemy Transaction 관리 Practice 공유
Slug: SQLAlchemy-Transaction-관리-Practice-공유
Date: 2016-08-27
Tags: python, sqlalchemy



## 개요

기본적으로 `SQLAlchemy`에서는 (`autocommit=True` 옵션을 주지 않는 이상) 수동으로 트랜잭션을 관리해야 한다. 예를 들면 이런 거다.

```python
session = Session()
new_user = User(**data)
session.add(new_user)
session.commit()
```

이렇게 항상, `session.commit()` 혹은 `session.rollback()`을 붙여주어야 트랜잭션이 끝나면서 변경 내용이 반영된다. 이렇게 간단한 수준의 코드라면 별 문제 없겠지만, 만약 큰 파일을 읽어서 모든 내용을 DB에 저장하는 작업을 하나의 트랜잭션에서 관리해야 한다면?

```python
session = Session()
# very complex logic with a huge file...
# ...
# many lines...
# ...
session.commit()
```

물론 이렇게도 할 수야 있겠지만, 개발자 입장에서 현재 어떤 세션 컨텍스트 안에서 작업을 하는 중인지 헷갈릴 가능성이 높다. 게다가 롤백을 위해 예외 관리를 해야 한다면? 복잡성은 더 늘어날 것이다.

<br>

## Transaction Context 관리

이런 문제를 해결하기 위해, Python의 `with`절을 이용해 트랜잭션 관리의 가독성을 높여보자. (참고: [When do I construct a Session, when do I commit it, and when do I close it?](http://docs.sqlalchemy.org/en/latest/orm/session_basics.html#when-do-i-construct-a-session-when-do-i-commit-it-and-when-do-i-close-it))

먼저 `contextmanager`를 이용해 `with`절 문법을 사용할 수 있게 만든다.

```python
from contextlib import contextmanager

@contextmanager
def gettx():
	session = Session()
	try:
		yield session
		session.commit()
	except Exception as e:
		logger.error(e)
		session.rollback()
		raise
	finally:
		session.close()
```

그럼 이 함수를 이용해서 첫 번 째 예제를 다시 작성해보자.

```python
with gettx() as session:
    new_user = User(**data)
    session.add(new_user)
```

`with`절을 빠져 나오면서 자동으로 트랜잭션은 닫히고 커넥션 자원도 반환된다.

<br>

## 수동 Transaction을 자동으로 관리

위 방법을 이용해서 트랜잭션 관리를 편하게 할 수 있었다. 그런데 `with`을 쓰기도 귀찮다면? 큰 코드 단위를 하나의 트랜잭션으로 관리하려면 어쩔 수 없이 `with` 등을 이용해 트랜잭션을 관리해야 하겠지만, 매 쿼리마다 트랜잭션이 열리고 닫혀도 상관없는 경우도 많을 것이다.

`SQLAlchemy` 코드가 있는 부분을 service layer로 분리해서 사용할 때, `Python decorator`를 이용하면 자동으로 트랜잭션 관리도 가능하게 할 수 있다. 먼저 데코레이터 부분을 보자.

```python
def opentx(f):
	def wrap(cls, *args, session=None, **kwargs):
        if session:  # 이미 열려있는 트랜잭션을 쓰는 부분
            result = f(cls, session, *args, **kwargs)
		with gettx() as session:  # 새로운 트랜잭션을 여는 부분
			result = f(cls, session, *args, **kwargs)
            session.expunge(result)  # 트랜잭션이 닫혀도 object의 attributes에 접근 할 수 있게 함
		return result
	return wrap
```

서비스 레이어의 코드를 보자.

```python
class UserService():
    @classmethod
    @opentx
    def create(cls, session, new_user):
        session.add(new_user)
```

마지막으로 이 서비스 함수를 사용하는 코드를 보자.

```python
# 트랜잭션을 수동으로 관리하고 싶은 경우
with gettx() as session:
    new_user = User(**data)
    UserService.create(new_user, session=session)

# 트랜잭션을 자동으로 관리하고 싶은 경우
new_user = User(**data)
UserService.create(new_user)
```

이런식으로 하나의 메소드를 원하는 트랜잭션 안에서 자유롭게 사용할 수 있다.

더 좋은 방법을 아시는 분은 공유해주시면 감사하겠습니다!
