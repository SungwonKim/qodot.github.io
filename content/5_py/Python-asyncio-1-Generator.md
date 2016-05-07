Title: Python asyncio 1: Generator
Slug: Python-asyncio-1-Generator
Date: 2016-03-06
Tags: python

## 개요

python 3.3에 추가된 `asyncio`는, 동시성 문제를 코루틴`coroutine` 기반으로 처리하는 비동기 IO 라이브러리다. 동시성 문제를 처리하는 방법은 대표적으로 쓰레드와 콜백 패턴이 있다.

### Thread

가장 대표적인 방법이다. 대중적인 방법이므로 이해도 쉽고 적용도 쉽다. 그런데 쓰레드에는 다음과 같은 문제가 있다.

1. 쓰레드를 생성하는데 드는 오버헤드
2. 쓰레드를 만들 때마다 추가되는 메모리
3. 이것은 python만의 문제인데, `GIL(global interpreter lock)`이라는 개념 때문에 python의 쓰레드는 일반적인 쓰레드 처럼 동작하지 않는 문제가 있다.[^1]

쓰레드가 문제라면 프로세스를 쓰면 되긴 하지만, 프로세스는 쓰레드보다 오버헤드가 훨씬 크기 때문에 멀티코어를 이용한 CPU 연산 작업이 아닌, 일반적인 상황에서는 크게 얻는 이득은 없다고 한다. (나도 만들어 본 적이 없어서 모르겠다)

### Callback

그럼 쓰레드를 사용하지 않는다면? 대안은 event-driven이다. `node.js`등에서 많이 사용하는 콜백 패턴 등이 대표적이다. 그런데 콜백 패턴은,

1. 조금만 복잡해지면 가독성이 심하게 저하되어 개발자가 코드의 흐름을 읽기가 힘들어진다는 단점([콜백 지옥](https://www.google.co.kr/webhp?sourceid=chrome-instant&ion=1&espv=2&es_th=1&ie=UTF-8#q=%EC%BD%9C%EB%B0%B1%20%EC%A7%80%EC%98%A5)으로 검색하면 수많은 포스트를 볼 수 있다.)이 있다.[^2]
2. [콜백 패턴 자체에 대한 지적](http://yisangwook.tumblr.com/post/90919749574/farewell-node-js-tj-holowaychuk)도 있다.

사실 되도않는 내공으로 콜백 패턴에 대해 논하는게 엄청 창피하지만 그냥 봐주세요 ㅠㅅㅠ 허허

그럼 코루틴은 어떨까? 코루틴도 event-driven으로 동시성 문제를 해결한다. 단순하게 말하자면, 일반적인 절차적인 모양새로 코드를 짜면서(가독성 상승) 비동기를 구현할 수 있다. '코루틴'이라는 단어 자체의 의미는 '상호작용하는 루틴'이라는 뜻인데, 일반적인 함수가 서브루틴`subroutine` 개념인 것과 대조적이다. 이런 코루틴을 이해하려면 먼저 제네레이터`generator` 개념에 대해서 알아야 한다.

<br>
## Generator

python에서 제네레이터는 이터레이터`iterator`의 확장 개념이라고 볼 수 있다. 이터레이터는 '순회 가능한`iterable`' 객체로서, 실제로는 `__next__` 함수가 구현되어 있는 객체라고 보면 된다. 예를 들면, `for`문을 수행할 때, 내부적으로 `__next__` 함수를 호출해서 동작한다. 제네레이터는 이터레이터의 확장 개념으로, `__next__` 함수의 리턴값은 `yield` 구문값으로 대신한다. 즉, `yield` 구문이 포함된 함수를 제네레이터라고 한다.

다음은 python의 `range(n)` 함수를 제네레이터를 이용해 구현해 본 것이다.

    def custom_range(n):
        c = 0
        while c < n:
            yield c
            c += 1
            
이 제네레이터를 실행해보면,
            
    >>> custom_range(5)
    <generator object custom_range at 0x1096d0870>
    >>> for i in custom_range(5):
            print(i)
    0
    1
    2
    3
    4
    
`__next__` 함수가 호출되면 다음 `yield`까지 진행되고 `yield`값이 반환된다. 이 때, 일반적인 서브루틴 함수처럼 `return`되면서 스택 메모리에서 사라지는 것이 아니라, 컨텍스트가 유지된 채로 제어권만 넘겨주는(양보`yield`하는) 것이다.

이 때, 위의 `yield c` 구문의 리턴 값은 `None`이다. 원래 `yield`문은 항상 `None`을 리턴하는데,` send` 함수를 이용해서 메인 루틴에서 제네레이터 루틴으로 값을 주입하면, `yield`문의 리턴값을 변경 할 수 있다.

    def gene():
        while True:
            input = yield 'output'
            print(input)

실행해보면,
    
    >>> g = gene()
    >>> next(g)
    'output'
    >>> next(g)
    None
    'output'
    >>> g.send('input')
    input
    'output'
    >>> g.send('hello')
    hello
    'output'

이렇게 `yield` 구문을 기준으로 메인 루틴과 제네레이터 루틴이 서로 메세지를 주고 받으며 상호작용할 수 있다. 코루틴처럼 동작하는 것이다.

다음 포스트에서 `asyncio`가 제네레이터를 이용해서 어떻게 비동기 작업을 처리하는지 알아보도록 하자.

<br>
## 참고한 사이트

- [Python 3, asyncio와 놀아보기](http://b.ssut.me/58)
- [asyncio - Python Tulip](http://www.flowdas.com/blog/asyncio-python-tulip/)
- [PyCon 2014 - Python 3.4:AsyncIO](http://www.pycon.kr/2014/program/4)

<br>
[^1]: `GIL`까지 설명하기에는 너무 일이 커지는 느낌이 들어서 링크로 대체한다. 1) [Python에서 thread를 사용하지 마세요?](https://yinjae.wordpress.com/2012/04/02/python-thread/) 2) [파이썬 GIL 깊숙히! (上)](highthroughput.org/wp/cb-1136/) 3) [파이썬 GIL 깊숙히! (상) 에 대한 몇 가지 변명](http://highthroughput.org/wp/cb-1146/)
[^2]: `promise`패턴을 이용해 극복한 부분도 많다.
