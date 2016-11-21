Title: Python Generator
Slug: Python-Generator
Date: 2016-03-06
Tags: python

파이썬에서 제네레이터는 이터레이터`iterator`의 확장 개념이라고 볼 수 있다. 이터레이터는 '순회 가능한`iterable`' 객체로서, 실제로는 `__next__` 함수가 구현되어 있는 객체라고 보면 된다. 예를 들면, `for`문을 수행할 때, 내부적으로 `__next__` 함수를 호출해서 동작한다. 제네레이터는 이터레이터의 확장 개념으로, `__next__` 함수의 리턴값은 `yield` 구문값으로 대신한다. 즉, `yield` 구문이 포함된 함수를 제네레이터라고 한다.

다음은 파이썬의 `range(n)` 함수를 제네레이터를 이용해 구현해 본 것이다.

``` python
def custom_range(n):
    c = 0
    while c < n:
        yield c
        c += 1
```

이 제네레이터를 실행해보면,

``` python
>>> custom_range(5)
<generator object custom_range at 0x1096d0870>
>>> for i in custom_range(5):
        print(i)
0
1
2
3
4
```
    
`__next__` 함수가 호출되면 다음 `yield`까지 진행되고 `yield`값이 반환된다. 이 때, 일반적인 서브루틴 함수처럼 `return`되면서 스택 메모리에서 사라지는 것이 아니라, 컨텍스트가 유지된 채로 제어권만 넘겨주는(양보`yield`하는) 것이다.

이 때, 위의 `yield c` 구문의 리턴 값은 `None`이다. 원래 `yield`문은 항상 `None`을 리턴하는데,` send` 함수를 이용해서 메인 루틴에서 제네레이터 루틴으로 값을 주입하면, `yield`문의 리턴값을 변경 할 수 있다.

``` python
def gene():
    while True:
        input = yield 'output'
        print(input)
```

실행해보면,
    
``` python
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
```

이렇게 `yield` 구문을 기준으로 메인 루틴과 제네레이터 루틴이 서로 메세지를 주고 받으며 상호작용할 수 있다. 이렇게 프로그래머가 직접 제어권을 수동으로 설정할 수 있기 때문에, 직접 루틴을 제어할 수 없는 쓰레드 프로그래밍을 대체할 수 있는 비동기 프로그래밍에 매우 중요하게 사용되기도 한다.