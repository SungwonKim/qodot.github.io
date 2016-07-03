Title: [Http & Network Basic 스터디] 06 HTTP 헤더
Slug: [Http-&-Network-Basic-스터디]-06-HTTP-헤더
Date: 2016-06-12
Tags: http, httpnetworkbasic, 영진닷컴,

이 포스트는 `영진닷컴`이 출판한 [Http & Network Basic](http://www.aladin.co.kr/shop/wproduct.aspx?ItemId=51908132)의 챕터 06 `HTTP 헤더`를 요약한 내용입니다.

## HTTP 메세지 헤더

HTTP 프로토콜의 요청과 응답에는 반드시 헤더가 포함되어 있다.

### 요청의 HTTP 메세지

- 메세지 헤더
	- 리퀘스트 라인 (메소드, URI, HTTP 버전)
	- 요청 헤더 필드
	- 일반 헤더 필드
	- 엔티티 헤더 필드
	- 기타
- 개행 문자 (CR + LF)
- 메세지 바디

### 응답의 HTTP 메세지

- 메세지 헤더
	- 상태 라인 (HTTP 버전, 상태 코드)
	- 응답 헤더 필드
	- 일반 헤더 필드
	- 엔티티 헤더 필드
	- 기타
- 개행 문자 (CR + LF)
- 메세지 바디

이 구조 중에서, (요청(응답) 헤더 필드 + 일반 헤더 필드 + 엔티티 헤더 필드)를 합쳐 HTTP 헤더 필드라 한다.

<br>
## HTTP 헤더 필드

보통 부가적이지만, 중요한 정보를 다루고 있다.

### HTTP 헤더 필드의 구조

HTTP 헤더 필드는 `헤더 필드 명: 필드 값`의 구조로 되어있다. `Keep-Alive: timeout=15, max=100`과 같이 하나의 키가 여러개의 값을 가질 수도 있다. 만약 키가 중복되어 있다면 어떤 브라우저는 최초의 헤더 필드를 우선적으로 처리하고 어떤 브라우저는 마지막 헤더 필드를 우선적으로 처리한다.

### 4종류의 HTTP 헤더 필드

HTTP 헤더 필드는 일반 헤더 필드, 요청/응답 헤더 필드, 엔티티 헤더 필드의 4종류로 구분된다.

### HTTP/1.1 헤더 필드 일람

[모질라 개발자 문서](https://developer.mozilla.org/en-US/docs/Web/HTTP/Headers)를 참조 한다.

### HTTP/1.1 이외의 헤더 필드

RFC2616에서 정의된 47종류 외에 `Set-Cookie`, `Content-Disposition`과 같은 비표준 헤더 필드 중에도 폭 넓게 사용되는 것도 있다.

### End-To-End 헤더와 Hop-By-Hop 헤더

HTTP 헤더 필드는 캐시와 비캐시 프록시 동작을 정의하기 위해서 두 가지의 카테고리로 분류되어 있다.

#### End-To-End 헤더

이 헤더 필드는 요청/응답의 초종 수신자에게 전송된다. 캐시에서 구축된 응답 중 보존되어야 하고, 항상 다시 전송되도록 되어 있다. (무슨 말인지...)

#### Hop-By-Hop 헤더

이 헤더 필드는 한 번 전송에 대해서만 유효하고 캐시와 프록시에 의해서 전송되지 않는 것도 있다. HTTP/1.1과 그 이후 버전에서의 Hop-By-Hop 헤더는 `Connection` 헤더 필드에 열거해 주어야 한다.

다음과 같은 헤더 필드가 Hop-By-Hop 헤더로 분류된다.

- Connection
- Keep-Alive
- Proxy-Authenticate
- Proxy-Authorization
- Trailer
- TE
- Transfer-Encoding
- Upgrade

<br>
## HTTP 일반 헤더 필드

요청과 응답 양쪽에서 모두 사용되는 헤더이다.

### Cache-Control

여러개의 디렉티브를 이용해 캐싱 동작을 정의한다.

#### 캐시가 가능한지 여부를 결정하는 디렉티브

- public: 다른 유저에게도 캐시를 돌려줄 수 있다.
- private: 특정 유저만 대상으로 하는 캐시이다.
- no-cache:
	- 클라이언트: 캐시된 것을 받아오지 말고 서버에서 직접 받아오도록 요청한다.
	- 서버: 재요청이 올 때마다 서버에 유효성 검증을 받아야지만 응답이 나가도록 설정한다.

#### 캐시로 보존 가능한 것을 제어하는 디렉티브

- no-store: 요청 혹은 응답에 기밀 정보가 포함되어 있음을 알린다. 따라서 로컬 스토리지에 저장이 되지 않는다.

#### 캐시 기한이나 검증을 지정하는 디렉티브

- max-age: 지정된 시간(초)보다 이전에 들어온 요청에 대해서는 캐시를 사용할 수 있다. 만약 값이 0이면 항상 오리진 서버로 요청된다. 동시에 `Expire` 헤더가 적용되었을 경우 `max-age`를 우선시 한다.
- s-maxage: `max-age`와 유사하나 여러 유저가 사용 가능한 공유 캐시 서버에만 적용된다. 즉, 같은 유저에게 반복해서 응답을 전달하는 경우에는 무효이다.
- min-fresh: 지정된 시간(초)안의 요청에는 항상 최신 리소스를 반환하도록 설정한다.
- max-stale: 지정된 시간(초)안의 요청에는 리소스의 유효기간이 끝났더라도 응답이 나가도록 설정한다.
- only-if-cached: 캐시 서버에 응답의 리로드 혹은 유효성을 재확인하지 않고 로컬 캐시에 있는 경우에만 응답을 반환한다. 로컬 캐시에 값이 없으면 504 Gateway Timeout을 반환한다.
- must-revalidate: 캐시의 유효성을 오리진 서버에서 조회한다. `max-stale` 디렉티브보다 우선한다.
- proxy-revalidate: 모든 캐시 서버에 대해서 이후의 요청에 대해 반드시 유효성 재확인을 하도록 요구
- no-transform: 캐시가 엔티티 바디의 미디어 타입을 변경하지 않도록 지정한다. (이미지 압축 등을 방지)

#### cache-extension 토큰을 이용한 Cache-Control 확장

```
Cache-Controle: private, community="UCI"
```

위와 같이 캐시 서버에서 이해할 수 있는 디렉티브가 있다면, extension-token을 추가할 수 있다. 캐시 서버가 이해하지 못하는 디렉티브는 무시된다.

### Connection

`Connection` 헤더는 프록시에 더 이상 전송하지 않는 헤더 필드를 지정하거나, 지속적인 접속을 관리하는 역할을 한다.

#### 프록시에 더 이상 전송하지 않는 헤더 필드(Hop-By-Hop 헤더)를 지정

```
Connection: 프록시를 통과하고 나면 전송하지 않는 헤더 필드 명 (Hop-By-Hop 헤더)
```

#### 지속적 접속 관리

HTTP/1.1에서는 지속적 접속(Keep-Alive)이 기본값이다. 따라서 서버측에서 명시적으로 접속을 끊고 싶을 때는 다음과 같이 헤더를 지정한다.

```
Connection: Close
```

### Date

HTTP 메세지를 생성한 날짜를 나타낸다. HTTP/1.1에서는 다음의 날짜 포맷을 지정하고 있다.

```
Date: Tue, 03 Jul 2012 04:40:58 GMT
```

### Pragma

HTTP/1.0과의 호환성만을 위해 정의된 헤더이다. (생략)

### Trailer

메세지 바디의 가장 뒤에 헤더를 전송할 수 있는데, 이 때, 해당 헤더를 `Trailer` 헤더 필드에 명시해주어야 한다.

```
HTTP/1.1 200 OK
...
Trailer: Expires

message body
...
0
Expires: Tue, 28 Sep 2004 23:59:59 GMT
```

### Transfer-Encoding

메세지 바디의 전송 코딩 형식을 지정한다. HTTP/1.1에서는 메세지 바디를 분할해서 전송하는 `chunked` 형식만 적용이 가능하다.

```
HTTP/1.1 200 OK
...
Transfer-Encoding: chunked

message body
Cf0 (16진수, 10진수로는 3312)
... (3312 바이트 정도의 chunk 데이터)
392 (16진수, 10진수로는 914)
... (914 바이트 정도의 chunk 데이터)
0
```

### Upgrade

프로토콜을 바꿀 수 있다. Connection 필드에도 같이 지정해줘야 하며, 서버는 응답을 101 Switching Protocols로 할 수 있다.

```
GET /index.html HTTP/1.1
Upgrade: TLS/1.0
Connection: Upgrade
```
```
HTTP/1.1 101 Switching Protocols
Upgrade: TLS/1.0, HTTP/1.1
Connection: Upgrade
```

### Via

오리진 서버까지 가는 동안 거치는 모든 프록시 서버가 자신의 정보를 헤더에 추가한다. `TRACE` 헤더와 자주 연계되어 사용된다. `Max-Forwards: 0`의 TRACE 리퀘스트가 도달하면 더이상 메세지를 전송할 수 없다.

시작

```
GET / HTTP/1.1
```

프록시 1

```
GET / HTTP/1.1
Via: 1.0 gw.hackr.jp (Squid/3.1)
```

프록시 2

```
GET / HTTP/1.1
Via: 1.0 gw.hackr.jp (Squid/3.1)
1.1 a1.example.com (Squid/2.7)
```

### Warning

리스폰스에 관한 추가 경고를 전달하는데, 기본적으로 캐시에 관한 문제의 경고를 유저에게 전달한다.

```
Warning: [경고 코드][경고한 호스트:포트]"[경고문]" ([날짜])
```

경고 코드와 설명 링크: [http://www.iana.org/assignments/http-warn-codes/http-warn-codes.xhtml](http://www.iana.org/assignments/http-warn-codes/http-warn-codes.xhtml)

<br>
## 요청 헤더 필드

클라이언트에서 서버로 송신된 요청 메세지에 사용되는 헤더를 뜻한다.

### Accept

클라이언트가 받고싶은 리소스의 형태를 지정할 수 있다. 타입/서브타입 형태로 한번에 여러개를 설정할 수도 있다.

```
Accept: text/plain; q=0.3, text/html
```

위의 헤더는 html을 우선으로 하고 plain text를 차선으로 하겠다는 뜻이다. q값은 우선순위를 뜻하고 1부터 0 사이의 값이 올 수 있으며 기본값은 1이다.

가능한 대표적인 리소스 형태는 다음과 같다.

- 텍스트: text/html, text/plain, text/css, application/xml...
- 이미지: image/jpeg, image/gif...
- 동영상: video/mpeg, video/quicktime...
- 애플리케이션: application/zip...

### Accept-Charset

클라이언트가 원하는 문자셋을 지정할 수 있고, `Accept` 필드와 동일하게 서브 타입과 우선순위를 지정할 수 있다.

### Accept-Encoding

클라이언트가 원하는 콘텐츠 코딩 상태와 우선순위를 지정한다.

- gzip: 압축 프로그램인 `gzip`에서 생성된 인코딩 포맷
- compress: 압축 프러그램 `compress`에서 생성된 포맷
- defalte: `Zlib` 포맷과 `deflate` 압축 알고리즘에 의해 만들어진 포맷
- identity: 압축과 변형을 하지 않은 포맷

### Accept-Language

클라이언트가 원하는 자연어 세트와 우선순위를 지정할 수 있다.

### Authorization

유저의 인증 정보를 전달하기 위해 사용된다.

최초 요청

```
GET /index.html
```

응답(401)

```
401 Unauthorized
WWW-Authenticate: Basic...
```

인증 정보 추가하여 재요청

```
GET /index.html
Authorization: Basic dWdfdf...
```

### Expect

클라이언트가 특정 요구를 서버에게 전달. HTTP/1.1에서는 100 Continue 밖에 되지 않음. (무슨 의미인지 전혀 모르겠음)

### From

클라이언트 유저의 메일 주소를 전달한다.

### Host

요청한 리소스의 호스트와 포트를 전달한다. HTTP/1.1의 유일한 필수 헤더 필드이다. 왜냐하면 1대의 서버에서 복수의 가상 호스팅을 할 수 있기 때문이다.

### If-xxx

`If-xxx`라는 포맷의 헤더 필드는 조건부 요청이라고 한다. 서버는 조건에 맞는 경우에만 요청을 처리한다.

- If-Match: 요청한 리소스의 ETag 값이 일치할 경우 (틀리면 412 Precondition Failed)
- If-Modified-Since: 요청한 리소스의 수정 날짜가 보낸 날짜보다 이전일 경우 (이후면 304 Not Modified)
- If-None-Match: `If-Match`와 반대
- If-Range: `If-Match`와 같은 동작인데, 실패시 412가 아니라 리소스 전체(최신)을 반환한다.
- If-Unmodified-Since: `If-Modified-Since`와 반대

### Max-Forwards

프록시를 하나 지날 때마다 값이 1씩 빠지고, 값이 0인 요청을 받았다면 더 이상 재전송하지 말고 응답해야 한다.

### Proxy-Authorization

프록시 서버가 인증을 요구할 때 클라이언트가 인증 정보를 담아 보내는 필드

### Range

리소스의 일부분만 취득하는 Range 요청을 할 때 지정 범위를 전달한다. 5001-10000 등으로 바이트 범위로 전달한다. 성공하면 206 Partial Content 응답을 받는다. 200 OK가 왔다면 Range가 동작하지 않은 것이다.

### Referer

요청이 발생한 본래 리소스의 URI를 전달한다. 주소창에 직접 입력한 경우는 보내지지 않는다.

### TE

`Accept-Encoding`과 매우 유사한데, TE는 전송 코딩에 해당된다.

### User-Agent

요청을 생성한 브라우저와 유저 에이전트의 이름을 전달한다.

<br>
## 응답 헤더 필드

서버에서 송신하는 응답 메세지에 적용된 헤더 필드이다.

### Accept-Ranges

서버가 요청 헤더의 `Range` 필드를 받아들일 수 있는지 지정하는 것

### Age

특정 캐시가 오리진 서버에서 생성된지 얼마나 지났는지를 초 단위로 나타내는 필드

### ETag

엔티티 태그라고 하며, 리소스가 갱신 될 때마다 붙는 값이다. 버전이라고 생각하면 될 듯 하다. 엔티티 태그 필드에 태그를 지정하면 특정 버전의 리소스를 가져올 수 있다.

### Location

3XX 상태코드의 리다이렉션이 일어나는 경우 Location 필드에 있는 주소로 엑세스를 시도한다.

### Proxy-Authenticate

프록시 서버에서의 인증 요구를 클라이언트에게 전달한다. 클라이언트-서버의 경우라면 `WWW-Authorization` 헤더 필드와 같은 역할을 한다.

### Retry-After

날짜/초 등의 값으로 언제 다시 요청을 다시 해야 하는지를 알려준다. 주로 503 Service Unavailable 등에서 사용된다.

### Server

서버의 소프트웨어를 전달한다. (아파치, S3 등등)

### Vary

오리진 서버에서 프록시 서버로 캐시가 전달 될 때, 요청 헤더에 특정 필드가 같은 값일 때만 캐시를 내어주도록 지정한다.

아래의 경우 `Accept-Language` 필드가 같아야지만 캐시를 내어준다.

```
Vary: Accept-Language
```

### WWW-Authenticate

인증이 필요한 리소스인 경우 클라이언트에게 전달된다. 401 Unauthorized 응답인 경우 반드시 포함된다.

<br>
## 엔티티 헤더 필드

요청/응답에 포함된 엔티티에 사용되는 헤더이다.

### Allow

특정 URI에서 사용가능한 메소드의 목록을 전달한다.

다음의 경우 GET과 HEAD 메소드만 사용 가능하다는 뜻이다.

```
Allow: GET, HEAD
```

### Content-Encoding

서버가 엔티티 바디에 대해 적용한 콘텐츠 인코딩 형식을 전달한다. 값은 `Accept-Encoding` 헤더의 값과 같다.

### Content-Language

서버가 엔티티 바디에 대해 적용한 자연어를 전달한다.

### Content-Length

엔티티 바디의 크기를 바이트 단위로 전달한다. 만약 인코딩이 따로 적용된 엔티티 바디의 경우라면 해당 필드를 사용해서는 안된다.

### Content-Location

바디에 대응하는 URI를 전달한다. 실제 요구한 리소스와 다른 리소스가 반환될 수도 있기 때문에 (`Accept-Language` 필드를 이용했을 경우 등) 실제 URI를 포함해야 할 필요가 있다.

### Content-MD5

메세지 바디가 변경되지 않고 도착했는지 확인하기 위해 MD5 값을 전달한다. MD5로 얻은 128비트의 바이너리를 base64로 인코딩해서 기록한다. (바이너리를 HTTP 헤더에 직접 담을 수 없기 때문) 클라이언트에서 같은 MD5 알고리즘을 실행하면 메세지 바디가 올바른지 알 수 있다.

우발적으로 변경된 컨텐츠는 감지가 되지만 공격에 의해 고의로 변경했을 경우, `Content-MD5` 값도 변경이 가능하기 때문에 이 경우는 알 수 없다.

### Content-Range

`Range` 필드가 포함된 요청에 답할 때 사용된다.

### Content-Type

바디의 미디어 타입을 전달한다. `타입/서브 타입` 형태로 값을 구성하고 `charset` 파라메터로 문자셋을 지정할 수 있다.

### Expires

리소스의 유효기간 날짜를 지정한다. 오리진 서버가 캐시 서버에게 알려주는 용도이다. 지정한 날짜까지만 복사본을 유지하고 캐시로 응답한다. 날짜가 지난 경우에 오리진 서버로 리소스를 얻으러 간다. `Cache-Control` 필드에 `max-age` 디렉티브가 지정되어 있다면 `max-age` 값이 우선된다.

### Last-Modified

리소스의 마지막 갱신 날짜를 전달한다.

<br>
## 쿠키를 위한 헤더 필드

쿠키는 HTTP/1.1의 사양은 아니지만 이미 웹 사이트에서 널리 사용되고 있다.

### Set-Cookie

서버가 클라이언트에 대해서 쿠키를 설정했을 때 응답에 포함된다.

#### NAME=VALUE

쿠키에 부여된 이름과 값 (필수)

#### Expires=DATE

쿠키의 유효기간 (지정되지 않으면 브라우저를 닫을 때 까지)

#### Path=PATH

쿠키의 적용 대상이 되는 서버상의 디렉토리 (지정하지 않으면 도큐먼트와 같은 디렉토리)

#### Domain=DOMAIN

쿠키의 적용 대상이 되는 도메인 명 (지정하지 않은 경우는 쿠키를 생성한 서버의 도메인)

#### Secure

HTTPS로 통신하고 있는 경우에만 쿠키를 송신하게 함

#### HttpOnly

쿠키를 Javascript에서 엑세스하지 못하도록 제한함

### Cookie

클라이언트가 서버에서 수신한 쿠키를 다시 요청에 포함시켜 전달할 때 쓰는 헤더 필드
