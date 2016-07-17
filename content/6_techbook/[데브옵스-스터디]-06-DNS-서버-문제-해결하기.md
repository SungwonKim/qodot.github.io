Title: [데브옵스 스터디] 06 DNS 서버 문제 해결하기
Slug: [데브옵스-스터디]-06-DNS-서버-문제-해결하기
Date: 2016-05-29
Tags: linux, 데브옵스, 위키북스, 

이 포스트는 `위키북스`가 출판한 [데브옵스](http://www.aladin.co.kr/shop/wproduct.aspx?ItemId=26451777)의 챕터 06 `왜 호스트 이름이 해석되지 않을까? DNS 서버 문제 해결하기`을 요약한 내용입니다.

<br>
## DNS 클라이언트 문제 해결

가장 기초적인 테스트는 `nslookup`으로 부터 시작하는 것이 좋다. 설명을 위해 IP 주소가 10.1.1.7인 클라이언트와 IP 주소가 10.1.2.5이고 이름이 web1인 서버가 존재한다고 가정한다. web1을 성공적으로 해석한 `nslookup`의 예시는 다음과 같다.

``` bash
$ nslookup web1
Server: 10.1.1.3
Address: 10.1.1.3#53
Name: web1.example.com
Address: 10.1.2.5
```
    
처음 두 줄의 `Server`, `Address`는 DNS 서버에 관한 정보이다. 그 아래 결과에서, web1 호스트는 web1.example.com으로 확장되고 10.1.2.5 IP 주소로 해석되므로 올바르게 동작하고 있는 것을 알 수 있다.

### 네임서버 설정이 안 됐거나 네임 서버에 접근할 수 없는 경우

다음과 같은 오류가 출력된다면, 네임서버 설정이 안 됐거나 네임 서버에 접근할 수 없는 경우이다.

``` bash
$ nslookup web1
;; connection timed out; no servers could be reached
```

이 경우 먼저 `/etc/resolv.conf`를 살펴서 네임서버가 잘 등록되어 있는지 확인한다. 이 예시에선 다음과 같을 것이다.

```
nameserver 10.1.1.3
```

먼저 `ping` 명령을 네임서버로 보내서 네임서버와의 연결 상태를 확인해 볼 수 있다. 혹은 `nslookup` 대신 `dig` 명령을 사용해 볼 수 있다. 다음은 `naver.com`에 대한 `dig` 명령의 결과이다.

``` bash
$ dig naver.com

; <<>> DiG 9.8.3-P1 <<>> naver.com
;; global options: +cmd
;; Got answer:
;; ->>HEADER<<- opcode: QUERY, status: NOERROR, id: 20670
;; flags: qr rd ra; QUERY: 1, ANSWER: 4, AUTHORITY: 2, ADDITIONAL: 2

;; QUESTION SECTION:
;naver.com.			IN	A

;; ANSWER SECTION:
naver.com.		289	IN	A	125.209.222.142
naver.com.		289	IN	A	202.179.177.22
naver.com.		289	IN	A	125.209.222.141
naver.com.		289	IN	A	202.179.177.21

;; AUTHORITY SECTION:
naver.com.		94275	IN	NS	ns2.naver.com.
naver.com.		94275	IN	NS	ns1.naver.com.

;; ADDITIONAL SECTION:
ns1.naver.com.		7756	IN	A	125.209.248.6
ns2.naver.com.		7756	IN	A	125.209.249.6

;; Query time: 13 msec
;; SERVER: 168.126.63.1#53(168.126.63.1)
;; WHEN: Sun May 29 15:03:04 2016
;; MSG SIZE  rcvd: 159
```

`ADDITIONAL SECTION`을 보면 `naver.com`에 `ns1.naver.com`, `ns2.naver.com`라는 두 개의 네임서버가 있다는 것을 알 수 있다.

같은 서브넷 안의 네임서버에 `ping`을 보낼 수 없다면 네임서버가 동작하지 않는 문제이다. 만약 다른 서브넷의 네임서버에 `ping`을 보낼 수 없다면, DNS 서버가 동작하지 않거나 네트워크에 문제가 있다는 것이다.

### 검색 경로를 누락했거나 네임서버 문제인 경우

다음 `nslookup` 결과를 보자.

``` bash
$ nslookup web1
Server: 10.1.1.3
Address: 10.1.1.3#53
** server can't find web1: NXDOMAIN
```

서버가 응답했으나 도메인을 찾지 못하고 있다. 두 가지 경우가 있는데, 첫 째는 도메인 이름이 DNS 검색 경로에 없는 경우이다. 이는 `/etc/resolv.conf` 안에 `search`로 시작하는 줄에 설정되어 있다. 둘 째는 호스트 이름이 아니라 전체 도메인 이름(`web1.example.com`)으로도 검색이 되지 않는 경우인데, 이 경우 문제는 네임서버에 있는 것이다.

<br>
## DNS 서버 문제 해결

### `dig` 출력 결과 이해하기

`nslookup`에 비해 `dig`의 내용은 DNS의 실제 응답에 더 가깝다. 출력 결과를 보며 내용을 이해해보자.

``` bash
$ dig naver.com

; <<>> DiG 9.8.3-P1 <<>> naver.com
;; global options: +cmd
;; Got answer:
;; ->>HEADER<<- opcode: QUERY, status: NOERROR, id: 20670
;; flags: qr rd ra; QUERY: 1, ANSWER: 4, AUTHORITY: 2, ADDITIONAL: 2

# 어떤 DNS 질의가 보내졌는지
;; QUESTION SECTION:
;naver.com.			IN	A

# 요청한 질의에 대한 IP 주소 응답
;; ANSWER SECTION:
naver.com.		289	IN	A	125.209.222.142
naver.com.		289	IN	A	202.179.177.22
naver.com.		289	IN	A	125.209.222.141
naver.com.		289	IN	A	202.179.177.21

# 도메인이 등록된 네임서버들
;; AUTHORITY SECTION:
naver.com.		94275	IN	NS	ns2.naver.com.
naver.com.		94275	IN	NS	ns1.naver.com.

# 해당 네임서버들의 IP 주소
;; ADDITIONAL SECTION:
ns1.naver.com.		7756	IN	A	125.209.248.6
ns2.naver.com.		7756	IN	A	125.209.249.6

# 수행 시간, 어떤 DNS 서버가 검색을 수행하는지
;; Query time: 13 msec
;; SERVER: 168.126.63.1#53(168.126.63.1)
;; WHEN: Sun May 29 15:03:04 2016
;; MSG SIZE  rcvd: 159
```

### DNS 질의 추적하기

보통 다른 조직이나 ISP 업체로부터 제공받은 DNS 서버에 요청을 보낼 텐데, 이 서버가 응답을 갖지 못하는 경우  질문에 대한 답을 얻을 때 까지 재귀적 DNS 해석이라는 것을 수행해야 한다.

`web1.example.net`을 질의할 경우, DNS 해석 모듈은 인터넷에서 가장 중요한 네임서버인 13개의 루트 네임서버 중 하나에 요청을 보낸다. 루트 네임서버는 `web1.example.net`의 주소는 모르지만 대신 모든 `.net` 네임서버의 목록을 응답한다. `.net` 네임서버들은 `web1.example.net`에 대한 정보는 없지만 역시 `example.net`과 관련있는 네임서버들의 목록을 응답한다. 이런식으로 반복하면, DNS 해석 모듈은 결국 `web1.example.net`에 대응하는 IP를 응답한다.

`dig` 명령을 이용하면, 이 재귀적 DNS 해석 과정을 살펴 볼 수 있다. DNS에 대한 `traceroute`라고 생각해도 된다.

``` bash
$ dig naver.com +trace

; <<>> DiG 9.8.3-P1 <<>> naver.com +trace
;; global options: +cmd
.			351299	IN	NS	k.root-servers.net.
.			351299	IN	NS	f.root-servers.net.
.			351299	IN	NS	c.root-servers.net.
.			351299	IN	NS	l.root-servers.net.
.			351299	IN	NS	g.root-servers.net.
.			351299	IN	NS	h.root-servers.net.
.			351299	IN	NS	i.root-servers.net.
.			351299	IN	NS	a.root-servers.net.
.			351299	IN	NS	j.root-servers.net.
.			351299	IN	NS	b.root-servers.net.
.			351299	IN	NS	e.root-servers.net.
.			351299	IN	NS	d.root-servers.net.
.			351299	IN	NS	m.root-servers.net.
;; Received 496 bytes from 168.126.63.1#53(168.126.63.1) in 102 ms

com.			172800	IN	NS	e.gtld-servers.net.
com.			172800	IN	NS	b.gtld-servers.net.
com.			172800	IN	NS	j.gtld-servers.net.
com.			172800	IN	NS	m.gtld-servers.net.
com.			172800	IN	NS	i.gtld-servers.net.
com.			172800	IN	NS	f.gtld-servers.net.
com.			172800	IN	NS	a.gtld-servers.net.
com.			172800	IN	NS	g.gtld-servers.net.
com.			172800	IN	NS	h.gtld-servers.net.
com.			172800	IN	NS	l.gtld-servers.net.
com.			172800	IN	NS	k.gtld-servers.net.
com.			172800	IN	NS	c.gtld-servers.net.
com.			172800	IN	NS	d.gtld-servers.net.
;; Received 499 bytes from 198.41.0.4#53(198.41.0.4) in 320 ms

naver.com.		172800	IN	NS	ns2.naver.com.
naver.com.		172800	IN	NS	ns1.naver.com.
;; Received 95 bytes from 192.31.80.30#53(192.31.80.30) in 155 ms

naver.com.		300	IN	A	125.209.222.141
naver.com.		300	IN	A	125.209.222.142
naver.com.		300	IN	A	202.179.177.21
naver.com.		300	IN	A	202.179.177.22
;; Received 91 bytes from 125.209.249.6#53(125.209.249.6) in 6 ms
```

### 재귀적 네임서버 문제

**작성자: 개인적 생각인데, 만약 DNS 서버를 직접 관리해야 하는 상황이 아니라면 솔직히 여기서부터는 읽지 않아도 무방하다고 생각한다.**

만약 특정 도메인의 응답을 받는데 상당히 시간이 오래 걸린다면(30초 정도) 재귀 DNS 서버 중 하나에 문제가 있을 수 있다. 이 경우 `/etc/resolv.conf`에 나열된 네임서버 목록을 보고 `nslookup`, `dig` 등을 이용해 네임서버를 하나씩 지정해서 질의를 날릴 수 있다. 다른 변수를 통제하기 위해서 안정적인 `www.google.com` 같은 도메인을 해석하는 것이 좋다.

``` bash
$ nslookup www.google.com 10.1.1.4
Server: 10.1.1.4
Address: 10.1.1.4#53

Non-authoritative answer:
Name:	www.google.com
Address: 216.58.200.196
```

특정 네임서버에 문제가 있다는 것을 알았다면, 해당 네임서버가 재귀 DNS 설정이 잘 되어 있는지 확인해보자. 보통 `/etc/bind/named.conf`에 있으며, `recursion`, `allow-recursion` 같은 옵션을 살펴보면 된다. 다음은 모든 10.1.1.0 서브넷에 대해 재귀 해석 요청을 허용하는 옵션이다.

``` bash
options {
    allow-recursion { 10.1.1/24; };
    ...
};
```

다음은 해당 네임서버에서 재귀 해석 요청이 허용되지 않았을 경우를 보여준다.

``` bash
options {
    recursion no;
    ...
}
```

### 갱신 내역이 적용되지 않는 경우

파일을 수정 했더라도 실제로 적용되지 않는 경우도 발생할 수 있다. 크게 세 가지로 분류 할 수 있는데 다음과 같다.

#### DNS 캐싱과 TTL(Time To Live)

DNS 레코드는 기본적으로 자주 변하지 않기 때문에 주로 캐시를 오랫동안 해놓는다. 하지만 이 경우 캐시 기간을 설정해야 하는 문제가 있는데, DNS 레코드가 가지고 있는 초단우 값인 TTL이 그것이다. 실제로 TTL 때문에 변경된  설정이 모든 DNS 캐시를 업데이트 하기 까지 며칠이 걸릴 수도 있다. TTL을 작게 설정해도 특정 업체는 서버의 부하 이슈 때문에 작은 TTL 값은 무시하는 경우도 있으므로 안심할 수 없다.

특정 존의 TTL을 확인하는 방법은 `dig` 명령을 이용하는 것이다.

```
;; ANSWER SECTION:
naver.com.		289	IN	A	125.209.222.142
naver.com.		289	IN	A	202.179.177.22
naver.com.		289	IN	A	125.209.222.141
naver.com.		289	IN	A	202.179.177.21
```

이 경우 TTL은 289초이다. 따라서 특정 설정이 변경될 때 까지 최대 289초가 걸릴 것이라고 예측 할 수 있다. 만약 변경된 내용이 적용되지 않고 있는데, 이 문제가 정말 캐시 때문인지 알고 싶다면 `dig` 명령어에 네임서버의 주소를 지정해서 하나씩 확인해본다. 만약 충분한 시간이 지났는데도 여러 네임서버들에게 모두 변경사항이 적용되지 않았다면 캐시가 아니라 다른 문제가 있을지도 모른다.

즉시 캐시를 날릴 필요가 있을 경우 먼저 운영체제의 캐시를 초기화한다.

``` bash
$ sudo /etc/init.d/nsdc restart
```

재귀 DNS 네임서버의 캐시를 초기화하려면 다음 명령어를 입력한다.

``` bash
$ sudo /etc/init.d/named restart
```

레드햇 기준이고, 데비안에서는 `bind` 혹은 `bind9`라는 이름의 서비스일 수 있다. 만약 재귀 DNS 서버의 캐시를 초기화할 재량이 없다면, 시스템의 네임서버를 이전 캐시가 없는 네임서버로 변경하거나, `/etc/hosts` 파일에 변경하고 싶은 도메인의 IP를 직접 입력할 수도 있으나, 근시안적 방법이므로 권장하진 않는다.

#### 구문 오류

어떤 네임서버에도 변경사항이 적용되지 않았을 경우, 구문 오류일 확률이 높다. `/var/log/syslog`, `/var/log/messages`를 확인해서 서비스를 재시작하면서 구문 에러가 발생하지 않았는지 확인해본다.

#### 전송 문제

하... 흠... 후... 너무 복잡하면서 지엽적인 이야기 같다... 나중에 정리...
