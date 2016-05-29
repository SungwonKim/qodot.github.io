Title: Python asyncio 2: 비동기 처리
Slug: Python-asyncio-2-비동기-처리
Date: 2016-03-27
Tags: python

## 이어서

[지난 포스트](http://qodot.github.io/Python-asyncio.html)에서 python의 제네레이터`generator`에 대해서 알아봤다. 제네레이터를 이용하면 두개의 함수가 서로 메세지를 주고 받으면서 코루틴`coroutine`으로서 동작할 수 있다는 것을 확인했다. 이것에 이어서, `asyncio`가 이 제네레이터와 코루틴 개념을 이용해서 이벤트 드리븐`event-driven`으로 비동기 작업을 처리할 수 있는지 알아보자.

<br>
## Event Loop & Message Queue

코드가 이벤트 드리븐으로 동작하려면 이벤트를 받아줄 이벤트 루프`event loop`와 메세지 큐`message queue`가 필요하다. python의 `asyncio`에서 바로 이 부분을 제공해준다. 이벤트 루프를 만들고, 원하는 코루틴을 메세지 큐에 넣어 스케쥴링 하는 코드를 살펴보자.

``` python
import asyncio

@asyncio.coroutine
def some_coroutine():
    ...

loop = asyncio.get_event_loop().run_until_complete(some_coroutine())
```

`@asyncio.coroutine` 데코레이터는 이 함수가 코루틴임을 알려준다. 코루틴은 그냥 제네레이터라고 봐도 거의 무방하다. 일반 제네레이터는 함수를 실행하면 제네레이터 객채가 생성되고 수동으로 `next()`를 호출해줘야 시작되는데, 이것을 자동화하여 함수를 실행하면 바로 내부 로직이 실행될 수 있도록 해준다.

`some_coroutine`은 메세지 큐에 잘 넣었지만, `some_coroutine` 내부에서도 다른 코루틴을 메세지 큐에 계속해서 넣고 싶을 수 있다. 이럴 때 `yield from` 문법과 `asyncio`의 `Task` 클래스를 이용한다.

``` python
@asyncio.coroutine
def another_coroutine():
    ...

@asyncio.coroutine
def some_coroutine():
    ...
    yield from asyncio.Task(another_coroutine())
    ...
```

이런 식으로 간단하게 코루틴을 스케쥴링 할 수 있다.

<br>
## 비동기 처리

메세지 큐에 넣은 코루틴은 이벤트 루프에 의해 백그라운드에서 실행될 것이다. 이 실행 결과를 받을 수 있어야 비로소 비동기 처리를 한다고 말할 수 있을 것이다. 콜백 패턴에서는 비동기 작업의 실행 결과를 얻기 위해서 콜백 함수를 등록했다. `asyncio`에서는 다음과 같이 처리한다.

``` python
result = yield from asyncio.Task(another_coroutine())
if not result.name:
    ...
...
```

**오잉? 뭐야 이거 비동기 맞아?** 네 맞습니다. **그냥 평범한 synchronous 코드 같은데?** 네 그래서 좋은겁니다. `yield from`은 쉽게 말하면 '이 작업이 끝날 때 까지 기다린다'의 의미입니다. **그럼 비동기가 아니지 않나?** 그 기다리는 시간동안 다른 작업을 처리할 수 있습니다.

<br>
## 결론

`asyncio`를 이용하면 callback/promise 패턴 같은 스타일이 아닌, 평범하게 절차적/동기적 스타일로 코드를 작성하면서, (thread 같은 방법에 비해서) 리소스 대비 성능이 뛰어난 이벤트 드리븐 방식으로 비동기 작업을 처리할 수 있다.

javascript에서도 제네레이터를 비롯하여 python의 `asyncio`가 제공하는 기능을 거의 동일하게(진짜 똑같다 ㅋㅋ) 제공하고 있다. 이런 추세로 봐서, 제네레이터와 코루틴 개념을 이용한 비동기 처리는 지금도 그렇지만 앞으로는 더욱 일반적이고 중요한 개념이 될 것 같다.

<br>
## 참고한 사이트

- http://stackoverflow.com/questions/27076577/yield-from-coroutine-vs-yield-from-task
- http://stackoverflow.com/questions/29819151/what-should-i-decorate-with-asyncio-coroutine-for-async-operations
