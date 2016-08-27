Title: SQLAlchemy-PostgreSQL에서의 JSON 타입 업데이트
Slug: SQLAlchemy-PostgreSQL에서의-JSON-타입-업데이트
Date: 2016-08-26
Tags: python, sqlalchemy, postgresql

`PostgreSQL 9.3` 과 `SQLAlchemy`를 이용해서 JSON 타입의 컬럼을 업데이트 하려고 했는데 되질 않았다. 찾다보니 한 아티클[Updating PostgreSQL JSON fields via SQLAlchemy](https://bashelton.com/2014/03/updating-postgresql-json-fields-via-sqlalchemy/)을 찾게 되어 내용을 정리해본다.

<br>
## 기본적인 업데이트 방법

아마 다들 알다시피, `SQLAlchemy`에서는 다음과 같은 방법으로 간단하게 update 쿼리를 날릴 수 있다.

```python
session = Session()
user = session.query(User).filter(User.id == user_id).first()
user.name = 'new_name'
session.commit()
```

그런데 만약 업데이트 하려는 컬럼이 JSON 타입이라면?

```python
session = Session()
user = session.query(User).filter(User.id == user_id).first()
user.json_field['key'] = 'value'  # 이렇게?
user.json_field2 = {'key2': 'value2'}  # 아님 이렇게?
session.commit()
```

안된다.

왜? `PostgreSQL` 9.3을 `SQLAlchemy`로 이용할 때 생기는 문제라고 한다. 9.5에서는 JSONB 타입 컬럼의 경우 자동으로 업데이트가 되도록 변경 되었지만, 여전히 JSON 타입 컬럼에 대해서는 지원하지 않는다고 한다.

<br>
## 그럼 어떻게 하지?

```python
from sqlalchemy.orm.attributes import flag_modified

user = session.query(User).filter(User.id == user_id).first()
user.json_field['key'] = 'value'
flag_modified(user, 'json_field')
session.commit()
```

된다. 강제로 해당 컬럼을 업데이트 하겠다는 신호를 주는 듯 하다.

직접적으로 세션을 이용하는 방법도 있다.

```python
session.query(User).filter(User.id == user_id).update({'json_field': {'key': 'value'}})
session.commit()
```
