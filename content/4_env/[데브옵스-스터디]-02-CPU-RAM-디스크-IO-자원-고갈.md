Title: [데브옵스 스터디] 02 CPU, RAM, 디스크 I/O 자원 고갈
Slug: [데브옵스-스터디]-02-CPU-RAM-디스크-IO-자원-고갈
Date: 2016-04-30
Tags: linux, 데브옵스, 위키북스, 

이 포스트는 `위키북스`가 출판한 [데브옵스](http://www.aladin.co.kr/shop/wproduct.aspx?ItemId=26451777)의 챕터 02 `왜 서버가 이렇게 느리지? CPU, RAM 그리고 디스크 I/O의 자원 고갈`을 요약한 내용입니다.

<br>
## CPU

### Uptime

`uptime` 명령어로 간단하게 해당 장비의 최근 평균 CPU 부하를 알 수 있다.

    $ uptime
    15:23  up 45 mins, 2 users, load averages: 1.23 1.33 1.45

중요한 것은 `load averages` 부분인데, 세 값은 각각 1분 평균, 5분 평균, 15분 평균의 CPU 부하를 나태낸다. 만약 싱글코어인 장비의 평균 부하가 1이었다면, 그 시간 동안 쉬지 않고 100% 일을 했다고 보면 된다.[^1] 저 숫자의 의미를 더 정확히 말하자면,

> CPU를 사용중인 process 수 + CPU 사용을 위해 대기중인 process 수 + I/O를 기다리는 process 수

이다.

### Top

`top` 명령어를 이용하면 프로세스 별 CPU 부하를 알 수 있다. 다음은 우분투에서 `top` 명령어를 실행한 결과이다. (이미지 출처: [http://www.howtogeek.com/107217/how-to-manage-processes-from-the-linux-terminal-10-commands-you-need-to-know](http://www.howtogeek.com/107217/how-to-manage-processes-from-the-linux-terminal-10-commands-you-need-to-know))

![`top` 명령어]({filename}/images/top-command.png)

기본적으로 `uptime`에서 보던 `load averages` 수치를 볼 수 있다. 그 외에도 상당히 많은 정보가 있는데, 가장 유용한 것은 어떤 프로세스가 어느정도의 CPU를 점유하고 있는지, 어느정도의 메모리를 점유하고 있는지를 알 수 있다는 것이다. `o` 키를 누르면 정렬할 기준을 입력할 수 있는데, `cpu`, `mem` 등의 키워드를 입력해서 점유율 순서대로 정렬할 수 있다. 프로세스의 ID까지 보여주므로 문제가 되는 프로세스가 보인다면 kill signal을 날릴 수도 있다.

CPU의 사용처를 대략적으로 카테고라이징 해서 보여주는 부분이 있는데, `Cpu(s)` 항목이다. 각각의 카테고리는 다음과 같다.[^2]

- `us`: `nice`[^3]가 적용되지 않은 사용자 프로세스에 CPU가 소비한 시간의 비율
- `sy`: 커널과 커널 프로세스에 CPU가 소비한 시간의 비율
- `ni`: `nice`를 적용한 프로세스에 CPU가 소비한 시간의 비율
- `id`: CPU가 사용되지 않는 유휴 상태의 비율
- `wa`: CPU가 I/O를 기다리며 소비한 시간의 비율
- `hi`: 하드웨어 인터럽트를 제공하는데 CPU가 소비한 시간의 비율
- `si`: 소프트웨어 인터럽트를 제공하는데 CPU가 소비한 시간의 비율
- `st`: 가상머신을 실행 중일 경우, 가상머신에 CPU가 소비한 시간의 비율

이 중 `id`과 `wa`가 특히 중요하다. 시스템이 느려졌는데 `id`의 비율이 높다면 장애의 원인이 CPU는 아니라는 뜻이고, `wa`의 비율이 높다면 I/O이 부하의 원인일 확률이 높아진다.

<br>
## 메모리

### Top

`top` 명령어에서 메모리 문제도 진단할 수 있는데, 위 이미지에 표시된 `Mem:` 항목과 `Swap:` 항목이다. 대부분 척 봐도 무슨 뜻인지 알 수 있게 되어 있는데, 주의해야 할 점이 몇 가지 있다.

첫 째는, `free` 항목의 수치가 낮다는 것이 반드시 메모리가 부족하다는 의미는 아니라는 것이다. 그 이유는 `cached` 항목 때문인데, 리눅스에서 파일을 캐싱하기 위해 점유하고 있는 메모리의 양을 뜻한다. 따라서 `cached` 항목까지 고려해서 여유 메모리를 계산해야 한다.

둘 째는, `Swap:`의 `used` 항목에 값이 있다고 해서 반드시 메모리 부족 때문에 swapping이 일어나고 있는 것은 아니라는 것이다. 왜냐하면 리눅스는 특정 프로세스가 유휴 상태일 때, 다른 프로세스가 사용할 메모리를 미리 확보하기 위해서 스왑 영역으로 옮기기 때문이다.

### Out Of Memory Killer

커널에서 제공하는 기능으로, 시스템이 매우 낮은 메모리를 확보한 상태에서 실행되고 있을 때 강제로 프로세스를 종료하기 시작한다. 보통은 메모리를 많이 소모하는 프로세스를 종료시키려고 하지만, 가끔 엉뚱한 프로세스를 종료시켜 시스템 오작동의 원인이 되기도 한다. `/var/log/syslog` 파일에 `Out Of Memory Killer`가 종료시킨 프로세스의 로그가 남아있으니 확인해보면 좋다.

<br>
## I/O

### Swap

만약 CPU가 높은 입출력 대기 상태에 빠졌다면 가장 먼저 의심해야 할 것은 메모리 스왑이다. 메모리를 스왑시키는 경우 느린 디스크에 접근이 잦아지기 때문에 필연적으로 성능 문제가 생긴다. 위의 메모리 문제 해결법을 참조해서 이를 해결한다.

### Iostat

만약 시스템이 다중 파티션으로 구성되어 있을 경우, 어떤 파티션에서 입출력을 많이 사용하고 있는지 알고싶다면 대부분의 배포판에 설치되어 있는 `iostat` 명령어를 활용하면 좋다. 다음은 `iostat`을 실행한 결과이다. (이미지 출처: [http://coreygoldberg.blogspot.kr/2010/07/6-command-line-tools-for-linux.html](http://coreygoldberg.blogspot.kr/2010/07/6-command-line-tools-for-linux.html))

![`iostat` 명령어]({filename}/images/top-command.png)

항목의 의미는 다음과 같다

- `tps`: 초당 전송량
- `Blk_read/s`: 초당 읽는 블럭 수
- `Blk_wrtn/s`: 초당 쓰는 블럭 수
- `Blk_read`: 읽은 전체 블럭 수
- `Blk_wrtn`: 쓴 전체 블럭 수

예제는 sda 파티션 하나만 사용하고 있기 때문에 한 줄 만 보이지만, 여러 파티션이 있을 경우 여러줄로 보인다. 각각의 디스크를 사용하는 프로세스를 알고 있다면 원인을 유추하는데 도움이 될 것이다. 이 후, 입출력 부하가 읽기인지 쓰기인지 파악해서 원인을 찾도록 하자.

<br>
## 시스템 통계

### Sysstat

`top`이나 `iostat`의 한계는 문제가 발생한 순간에만 탐지가 가능하다는 점이다. 만약 위의 명령을 주기적인 로그로 남길 수 있다면, 이상 현상이 지나가버린 후에도 문제를 탐지할 수 있을 것이다. 데비안이나 레드햇 배포판에는 기본적으로 10분에 한 번 씩 통계를 기록하도록 설정되어 있는데, 데비안 기준으로 `/etc/default/sysstat` 파일에서 옵션을 설정하고, `/etc/cron.d/sysstat` 스크립트로 실행하며, `/var/log/sysstat` 파일에 로그를 남긴다. `sar` 명령어를 이용하면 그날의 통계를 바로 볼 수 있다.

![`sar` 명령어]({filename}/images/sar-command.png)

(이미지 출처: [http://mylinuxinf.blogspot.kr/2010/08/how-to-setup-sar-in-ubuntu-1004.html](http://mylinuxinf.blogspot.kr/2010/08/how-to-setup-sar-in-ubuntu-1004.html))

<br>
[^1]: 듀얼코어였다면 50%, 쿼드코어였다면 25%...
[^2]: OS X에서는 `us`, `sy`, `id`만 표기된다.
[^3]: 프로세스에 스케쥴링 우선순위를 확인/지정하는 명령어. http://openwiki.kr/tech/nice 를 참조.
