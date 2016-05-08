Title: [Http & Network Basic 스터디] 02 간단한 프로토콜 HTTP
Slug: [Http-&-Network-Basic-스터디]-02-간단한-프로토콜-HTTP
Date: 2016-05-08
Tags: http, httpnetworkbasic, 영진닷컴,

이 포스트는 `영진닷컴`가 출판한 [`Http & Network Basic`](http://www.aladin.co.kr/shop/wproduct.aspx?ItemId=51908132)의 챕터 02 `간단한 프로토콜 HTTP`를 요약한 내용입니다.

## 기본 작동 방식

- HTTP는 기본적으로 클라이언트-서버 방식으로 작동한다. 상황에 따라 역할이 뒤집힐 수도 있지만 클라이언트-서버의 형식은 유지된다.
- 클라이언트-서버간에 요청과 응답을 교환하며 동작한다. 반드시 클라이언트에서 요청을 보내면서 통신이 시작된다. 서버에서 요청이 없이 응답을 주는 경우는 없다.
    - push에서 소켓을 써야 하는 이유

    ### Request

    다음은 HTTP 요청의 예시이다.

        POST /form/entry HTTP/1.1
        Host: hackr.jp
        Connection: keep-alive
        Content-Type: application/x-www-form-urlencoded
        Content-Length: 16
        
        name=ueno&age=37
    
    - `POST`: 메소드
    - `/form/entry`: URI
    - `HTTP/1.1`: 프로토콜 버전
    - 그 아래에 있는 것들은 HTTP 요청 헤더들
    - 그 한 줄 아래에 있는 것은 엔티티[^1]
    
    ### Response
    
    다음은 HTTP 응답의 예시이다.
    
        HTTP/1.1 200 OK
        Date: Tue, 10 Jul 2012 06:50:15 GMT
        Content-Length: 362
        Content-Type: text/html
        
        <html>
            ...
        </html>
    
    - HTTP/1.1: 프로토콜 버전
    - 200 OK: HTTP 상태 코드와 설명
    - 그 아래에 있는 것들은 HTTP 응답 헤더들
    - 그 한 줄 아래에 있는 것은 HTTP 응답의 body (이 경우에는 HTML 문서)
- 상태를 저장하지 않는(Stateless) 프로토콜이다. 프로토콜의 레벨에서는 이전의 요청과 응답에 대한 정보를 가지고 있지 않는다.
    - 그런데 상태는 애플리케이션에서 반드시 필요한 개념이기 때문에 이를 해결하기 위해 후에 쿠키(Cookie)가 도입되었다.
- URI로 리소스를 탐색하고 메소드로 임무를 구분한다.
    - `GET`: 리소스 획득
    - `POST`: 엔티티 전송
    - `PUT`: 파일 전송 (인증 기능 없음)
    - `DELETE`: 파일 삭제 (인증 기능 없음)
    - `OPTIONS`: URI가 제공하는 메소드 목록
    - `HEAD`: 메세지 헤더 취득 (GET에서 body 제거)
    - `TRACE`, `CONNECT`: 프록시, TCP 터널링 관련 (보안 문제 있을 수 있으므로 쓰지 않음)
    - HTTP 메소드에 관한 더 상세한 설명은 [`w3.org 문서`](https://www.w3.org/Protocols/rfc2616/rfc2616-sec9.html)를 참조한다.
- 지속 연결:
    
    ### 지속 연결
    
    지속 연결이 없다면 이런식으로 HTTP 요청을 처리해야 한다.
    
    > TCP 연결  -> HTTP 요청 -> HTTP 응답 -> TCP 종료 -> TCP 연결 -> HTTP 요청 -> HTTP 응답 -> TCP 종료
    
    요청마다 TCP 커넥션을 맺으면 오버헤드가 많이 소비되므로 한번 연결한 TCP 연결을 끊지 않음 (`keep-alive`)
    
    > TCP 연결  -> HTTP 요청 -> HTTP 응답 -> HTTP 요청 -> HTTP 응답 -> TCP 종료
    
    ### 파이프라인화
    
    용량이 큰 파일 전송 등 리퀘스트를 여러번에 나누어 보내야 할 경우 속도가 증가한다.
    
    > TCP 연결  -> HTTP 요청 1 -> HTTP 요청 2 -> HTTP 응답 1 -> HTTP 응답 2 -> TCP 종료

## Cookie

애플리케이션에서 어쩔 수 없이 발생하는 상태(state) 개념의 요구 때문에, stateless 프로토콜인 HTTP에서도 쿠키를 통해서 상태 개념을 도입 할 수 있다.

클라이언트의 모든 상태를 서버에서 처리할 경우 서버 리소스에 큰 부하가 될 수 있기 때문에(세션의 경우 서버에서 처리한다), 쿠키는 클라이언트에게 상태 정보를 떠 넘길 수 있도록 설계되었다.

쿠키가 설정된 경우 설정된 HTTP 응답에 `Set-Cookie` 헤더에 어떤 쿠키가 어떤 값으로 설정되었는지 알 수 있다. 다음 응답 예시를 보자.

    HTTP/1.1 200 OK
    Date: Thu, 12 Jul 2012 07:12:20 GMT
    Server: Apache
    <Set-Cookie: sid=134.....; path=/; expires=Wed, => 10-Oct-12 07:12:20 GMT>
    Content-Type: text/plain; charset=UTF-8

<br>
[^1]: `POST` 메소드이기 때문에 HTTP body에 내용이 들어가 있고, `GET` 메소드일 경우 URI의 뒤에 따라 붙게 된다. (Query String)
