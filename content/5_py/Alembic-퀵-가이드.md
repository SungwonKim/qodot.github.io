Title: Alembic 퀵 가이드
Slug: Alembic-퀵-가이드
Date: 2015-11-25
Tags: alembic, sqlalchemy

## 개요

Rails나 Django 같은 모던 웹 프레임워크의 ORM에서는, 반복되는 DB 스키마 변경을 수월하게 진행 할 수 있도록 전용 마이그레이션 툴이 ORM에 내장되어 있다. 그러나 SQLAlchemy에서는 기본적으로 테이블의 생성은 가능하나, 생성된 테이블의 스키마 변경은 지원하지 않는데, 이를 수월하게 만들어 주는 툴이 바로 Alembic이다.

<br>
## Alembic 환경 생성
원하는 디렉토리에서

``` bash
alembic init alembic
```

을 실행하면 아래와 같은 디렉토리 구조가 생긴다.

```
yourproject/
    alembic/
        env.py
        README
        script.py.mako
        versions/
            3512b954651e_add_account.py
            2b1ae634e5cd_add_order_id.py
            3adcc9a56557_rename_username_field.py
```

- yourproject: root 디렉토리
- env.py: alembic이 실행될 때 환경을 설정하기 위해 먼저 실행되는 설정용 python script
- versions: 실제 revision[^1]가 순차적으로 쌓이는 디렉토리
- alembic.ini: 설정 변수들이 저장되는 파일. env.py에서 이 파일을 읽어서 설정값을 채운다.

<br>
## 기본 환경 설정

`alembic.ini` 파일을 열어서 `sqlalchemy.url` 변수에 원하는 데이터베이스의 URL을 입력한다. 만약 development, production 등의 환경 분리가 필요하다면 아예 ini 파일을 따로 만들어서 alembic 명령어를 `-c` 옵션과 함께 줄 수 있다.

``` bash
alembic -c development.ini upgrade head
```	

혹은 하나의 파일 내부에 대괄호를 이용해서 grouping 할 수 도 있다.

``` bash
[development]
sqlalchemy.url = dev_db_url
[production]
sqlalchemy.url = prod_db_url

# 커맨드 사용
alembic --name development upgrade head
```

<br>
## Migration Script 생성

적용을 원하는 Alembic 환경의 root 디렉토리로 이동하고, revision의 이름을 지정하여 생성한다.

``` bash
alembic revision -m 'create some table'
```

versions 디렉토리에 생성된 스크립트를 보면 `upgrade`와 `downgrade` 메소드가 있는데, 이곳에 원하는 로직을 채워 넣으면 된다.[^2] SQLAlchemy 문법을 써서 할 수도 있어서 편하다.

``` python
def upgrade():
    op.create_table(
        'account',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('name', sa.String(50), nullable=False),
        sa.Column('description', sa.Unicode(200)),
    )

def downgrade():
    op.drop_table('account')
```

물론 raw SQL을 직접 작성해서 할 수도 있다.

<br>
## 생성된 Migration Script 적용

적용을 원하는 Alembic 환경의 root 디렉토리로 이동하고, 명령어를 입력한다.

``` bash
# 가장 최신의 마이그레이션 스크립트까지 순차 적용한다
alembic upgrade head

# 현재 마이그레이션 버전으로 부터 한단계 상위의 스크립트만 적용한다
alembic upgrade +1

# 반대로 하면 원하는 버전으로 롤백 가능
alembic downgrade -1
```

<br>
## Migrations Script 자동생성

`upgrade`, `downgrade` 메소드를 직접 구현하지 않고, 변경한 SQLAlchemy 모델을 자동으로 감지하여 마이그레이션 스크립트를 생성 할 수 있다.

``` bash
alembic revision --autogenerate -m 'some messages'
```

이 기능을 이용하려면 `env.py` 파일을 이용하여, Alembic이 SQLAlchemy의 변경 사항을 자동으로 감지할 수 있도록 설정해 주어야 한다.

`env.py` 파일을 열고 다음과 같이 입력 혹은 수정한다.

``` python
# SQLAlchemy의 모델 메타데이터를 가져오는 부분
from app.database import Base
target_metadata = Base.metadata

def run_migrations_online():
    engine = engine_from_config(
        config.get_section(
            config.config_ini_section,
            prefix='sqlalchemy.',
            poolclass=pool.NullPool
        )
    )

    with engine.connect() as connection:
        context.configure(
            connection=connection,
            # 가져온 메타데이터를 넣는 부분
            target_metadata=target_metadata
        )

        with context.begin_transaction():
            context.run_migrations()
```

`--autogenerate` 옵션이 모든 변화를 전부 감지 할 수 있는 것은 아니다. 자세한 내용은 공식 문서([What Does Autogenerate Detec](http://alembic.readthedocs.org/en/latest/autogenerate.html#what-does-autogenerate-detect-and-what-does-it-not-detect))를 참조하길 바란다.

<br>
[^1]: 각각의 Migration script를 의미한다.
[^2]: `upgrade`에는 현재 변화를 원하는 로직을, `downgrade`에는 롤백용 로직을 넣으면 된다.
