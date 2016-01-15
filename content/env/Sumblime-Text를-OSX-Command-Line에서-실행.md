Title: Sumblime Text를 OSX Command Line에서 실행
Slug: Sumblime-Text를-OSX-Command-Line에서-실행
Date: 2015-04-15
Tags: env, sublimetext

## 1.
아래의 커맨드를 통해 서브라임 텍스트가 잘 설치되었나 확인해야 한다.

    /Applications/Sublime\ Text\ 2.app/Contents/SharedSupport/bin/subl .

해당 디렉토리를 기준으로 서브라임 텍스트가 열린다면 성공! (Sublime Text 3을 쓰는 사람은 위의 2와 2 바로 전의 공백(\포함)을 빼면 될거에요 아마 ㅎㅎ…)

## 2.
아래 커맨드를 통해 Symbolic link를 생성한다.

    ln -s /Applications/Sublime\ Text\ 2.app/Contents/SharedSupport/bin/subl /usr/local/bin/subl

실행하면 `/usr/local/bin/` 에 심볼릭 링크가 만들어진다. 본인은 그냥 유저 홈에 bin 디렉토리를 생성해서 거기에 심볼릭 링크를 만들었음.

## 3.
환경 변수를 설정한다. `echo $PATH` 를 실행해서 본인이 심볼릭 링크를 생성한 디렉토리가 등록되어 있는지 확인한다. 없으면 `.bash_profile`이나 `.zshrc`를 열어서 다음과 같이 추가해준다.

    export PATH=본인의 심볼릭 링크가 있는 디렉토리 경로:$PATH
    export EDITOR=‘subl -w’

본인은 `PATH` 에 `~/bin` 을 추가했음. (아마 `/usr/local/bin` 은 이미 등록되어 있을 것 같다.)

## 4.
터미널을 재실행하거나 `source .zshrc`(혹은 `.bash_profile`)을 실행한다.

## 5.
터미널에서 `subl` 을 입력해서 서브라임 텍스트가 열리면 성공!

<br>
##### 참고한 페이지
- [http://stackoverflow.com/questions/16199581/opening-sublime-text-on-command-line-as-subl-on-mac-os](http://stackoverflow.com/questions/16199581/opening-sublime-text-on-command-line-as-subl-on-mac-os)
- [https://www.sublimetext.com/docs/2/osx_command_line.html](https://www.sublimetext.com/docs/2/osx_command_line.html)
- [심볼릭 링크와 하드 링크](http://egloos.zum.com/sunnmoon/v/1858692)
