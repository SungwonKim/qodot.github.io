Title: SQLAlchemy Quickstart
Slug: SQLAlchemy-Quickstart
Date: 2015-11-20
Tags: sqlalchemy

SQLAlchemy를 사용하기 위한 기본적인 설정을 하는 방법을 요약해본다.

<br>
## 설치

그냥 `pip`으로 설치하면 된다.

```python
pip install sqlalchemy
```

<br>
## 설정

### 접속 설정

```python
from sqlalchemy import create_engine

URL = 'postgresql://<username>:<password@<host>:<port>/<dbname>'
engine = create_engine(URL, echo=True)
```

간단하게 `engine.execute('SELECT 1').scalar()` 같은 코드를 실행해보면 접속을 테스트해 볼 수 있다.

### 세션 팩토리 설정

데이터베이스의 커넥션을 필요할 때마다 리턴해 줄 세션 팩토리가 필요하다.

```python
from sqlalchemy.orm import sessionmaker

Session = sessionmaker(bind=engine)
```

위의 `Session`이 세션 팩토리이다.

<br>
## ORM 사용

### 선언

raw SQL만 쓸거면 SQLAlchemy를 쓸 이유가 없다. ORM을 사용하는 방법을 알아보자.

기본적으로 `Base` 클래스를 상속 받은 클래스가 테이블이 되고, 그 클래스의 필드가 컬럼이 된다.

```python
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String

Base = declarative_base()

class Table1(Base):
    __tablename__ = 'table1'
    
    column1 = Column(Integer)
    column2 = Column(Integer)
```

이건 단순히 선언했을 뿐이고, 실제로 DBMS에 스키마가 생성된건 아니다. `Base.metadata.create_all(engine)`를 실행해야 선언된 클래스가 DBMS로 반영된다.

`create_all`의 문제점은 테이블의 생성만 해준다는 것이다. 즉 컬럼의 추가나 삭제, 속성 변경 같은 것은 반영되지 않는다. 이 작업을 쉽게(Django, Rails 같이)하려면 Alembic이라는 프로젝트를 따로 사용해야 한다. 필요하면 다음 페이지를 참조한다.

- [Alembic Quickstart](https://github.com/qodot/wiki/wiki/Python-Alembic-Quickstart)

### 사용

```python
# 조회
session = Session()
table1_object = session.query(Table1).filter(Table1.column1 == ‘something’).first()
column2 = table1_object.column2
session.commit()
session.close()

# 생성
session = Session()
table1_object2 = Table1()
session.add(table1_object2)
session.commit()
session.close()

# 업데이트
session = Session()
table1_object = session.query(Table1).filter(Table1.column1 == ‘something’).first()
table1_object.column2 = 'new_value'
session.commit()
session.close()

# 삭제
session = Session()
table1_object = session.query(Table1).filter(Table1.column1 == ‘something’).first()
session.delete(table1_object)
session.commit()
session.close()
```