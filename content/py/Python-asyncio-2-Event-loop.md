Title: Python asyncio 2: Event-loop
Slug: Python-asyncio-2-Event-loop
Date: 2016-03-06
Tags: python

## 이어서

[지난번 포스트](http://qodot.github.io/Python-asyncio.html)에서 python의 제네레이터`generator`에 대해서 알아봤다. 제네레이터를 이용하면 두개의 함수가 서로 메세지를 주고 받으면서 코루틴`coroutine`으로서 동작할 수 있다는 것을 확인했다. 이것에 이어서, `asyncio`가 이 제네레이터와 코루틴 개념을 이용해서 이벤트 드리븐`event-driven`으로 비동기 작업을 처리할 수 있는지 알아보자.

### Event Loop & Queue
코드가 이벤트 드리븐으로 동작하려면 이벤트를 받아줄 이벤트 루프`event loop`와 메세지 큐`message queue`가 필요하다. python의 `asyncio`에서 바로 이 부분을 제공해준다.

    import asyncio
    
    loop = asyncio.get_event_loop(


## 참고한 사이트

- [Python 3, asyncio와 놀아보기](http://b.ssut.me/58)
- [asyncio - Python Tulip](http://www.flowdas.com/blog/asyncio-python-tulip/)
- [PyCon 2014 - Python 3.4:AsyncIO](http://www.pycon.kr/2014/program/4)
