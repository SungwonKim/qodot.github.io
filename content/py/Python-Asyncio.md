Title: Python Asyncio
Slug: Python-Asyncio
Date: 2016-03-27
Tags: python, asyncio

## 개요

파이썬 3.3에 추가된 `asyncio`는, 동시성 문제를 코루틴`coroutine` 기반으로 처리하는 비동기 IO 라이브러리다. 동시성 문제를 처리하는 방법은 대표적으로 쓰레드와 콜백 패턴이 있다.

### Thread

가장 대표적인 방법이다. 대중적인 방법이므로 이해도 쉽고 적용도 쉽다. 그런데 쓰레드에는 다음과 같은 문제가 있다.

1. 쓰레드를 생성하는데 드는 오버헤드
2. 쓰레드를 만들 때마다 추가되는 메모리
3. 이것은 python만의 문제인데, `GIL(global interpreter lock)`이라는 개념 때문에 python의 쓰레드는 일반적인 쓰레드 처럼 동작하지 않는 문제가 있다.[^1]

쓰레드가 문제라면 프로세스를 쓰면 되긴 하지만, 프로세스는 쓰레드보다 오버헤드가 훨씬 크기 때문에 멀티코어를 이용한 CPU 연산 작업이 아닌, 일반적인 상황에서는 크게 얻는 이득은 없다.

### Callback

그럼 쓰레드를 사용하지 않는다면? 대안은 event-driven이다. Node.js등에서 많이 사용하는 콜백 패턴 등이 대표적이다. 그런데 콜백 패턴은,

1. 조금만 복잡해지면 가독성이 심하게 저하되어 개발자가 코드의 흐름을 읽기가 힘들어진다는 단점([콜백 지옥](https://www.google.co.kr/webhp?sourceid=chrome-instant&ion=1&espv=2&es_th=1&ie=UTF-8#q=%EC%BD%9C%EB%B0%B1%20%EC%A7%80%EC%98%A5)으로 검색하면 수많은 포스트를 볼 수 있다.)이 있다.[^2]
2. [아무튼 콜백에 존재하는 수많은 단점들…](http://yisangwook.tumblr.com/post/90919749574/farewell-node-js-tj-holowaychuk)도 있다.

그럼 코루틴은 어떨까? 코루틴도 event-driven으로 동시성 문제를 해결한다. 단순하게 말하자면, 일반적인 절차적인 모양새로 코드를 짜면서(가독성 상승) 비동기를 구현할 수 있다. '코루틴'이라는 단어 자체의 의미는 '상호작용하는 루틴'이라는 뜻인데, 일반적인 함수가 서브루틴`subroutine` 개념인 것과 대조적이다. 이런 코루틴을 이해하려면 먼저 제네레이터`generator` 개념에 대해서 알아야 한다. 다음을 참조한다.

- [Python Generator](https://github.com/qodot/wiki/wiki/Python-Generator)

제네레이터를 이용하면 두개의 함수가 서로 메세지를 주고 받으면서 코루틴`coroutine`으로서 동작할 수 있다는 것을 확인했다. 이것에 이어서, `asyncio`가 이 제네레이터와 코루틴 개념을 이용해서 이벤트 드리븐`event-driven`으로 비동기 작업을 처리할 수 있는지 알아보자.

<br>
## Asyncio

### Event Loop & Message Queue

코드가 이벤트 드리븐으로 동작하려면 이벤트를 받아줄 이벤트 루프`event loop`와 메세지 큐`message queue`가 필요하다. 파이썬의 `asyncio`에서 바로 이 부분을 제공해준다. 이벤트 루프를 만들고, 원하는 코루틴을 메세지 큐에 넣어 스케쥴링 하는 코드를 살펴보자.

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

### 비동기 처리

메세지 큐에 넣은 코루틴은 이벤트 루프에 의해 백그라운드에서 실행될 것이다. 이 실행 결과를 받을 수 있어야 비로소 비동기 처리를 한다고 말할 수 있을 것이다. 콜백 패턴에서는 비동기 작업의 실행 결과를 얻기 위해서 콜백 함수를 등록했다. `asyncio`에서는 다음과 같이 처리한다.

``` python
result = yield from asyncio.Task(another_coroutine())
if not result.name:
    ...
...
```

**오잉? 뭐야 이거 비동기 맞아??** 네 맞습니다. **그냥 평범한 synchronous 코드 같은데?** 네 그래서 좋은겁니다. `yield from`은 쉽게 말하면 '이 작업이 끝날 때 까지 기다린다'의 의미입니다. **그럼 비동기가 아니지 않나?** 그 기다리는 시간동안 다른 작업을 처리할 수 있습니다.

<br>
## 결론

`asyncio`를 이용하면 `callback/promise` 패턴 같은 스타일이 아닌, 평범하게 절차적/동기적 스타일로 코드를 작성하면서, (thread 같은 방법에 비해서) 리소스 대비 성능이 뛰어난 이벤트 드리븐 방식으로 비동기 작업을 처리할 수 있다.

자바스크립트에서도 제네레이터를 비롯하여 파이썬의 `asyncio`가 제공하는 기능을 거의 동일하게(진짜 똑같다 ㅋㅋ) 제공하고 있다. 이런 추세로 봐서, 제네레이터와 코루틴 개념을 이용한 비동기 처리는 지금도 그렇지만 앞으로는 더욱 일반적이고 중요한 개념이 될 것 같다.

<br>
## 참고한 사이트

- [Python 3, asyncio와 놀아보기](http://b.ssut.me/58)
- [asyncio - Python Tulip](http://www.flowdas.com/blog/asyncio-python-tulip/)
- [PyCon 2014 - Python 3.4:AsyncIO](http://www.pycon.kr/2014/program/4)
- http://stackoverflow.com/questions/27076577/yield-from-coroutine-vs-yield-from-task
- http://stackoverflow.com/questions/29819151/what-should-i-decorate-with-asyncio-coroutine-for-async-operations

[^1]: `GIL`까지 설명하기에는 너무 일이 커지는 느낌이 들어서 링크로 대체한다. 1) [Python에서 thread를 사용하지 마세요?](https://yinjae.wordpress.com/2012/04/02/python-thread/) 2) [파이썬 GIL 깊숙히! (上)](highthroughput.org/wp/cb-1136/) 3) [파이썬 GIL 깊숙히! (상) 에 대한 몇 가지 변명](http://highthroughput.org/wp/cb-1146/)

[^2]: `promise`패턴을 이용해 극복한 부분도 많다.