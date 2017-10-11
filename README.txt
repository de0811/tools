사용하기 전 필수 설정
config/__init__.py 파일을 자신의 파일에 맞게 수정합니다.

py 파일 설명
aapt.py             파일은 앱의 이름 등 알 수 있습니다. -h 참조
apptool.py          apktool.jar을 이용하여 좀 더 편하게 개선 하였습니다. 옵션 없이 사용해도 자동으로 진행시킵니다. -h 참조
binary_Diff.py      파일을 비교합니다. 어느 위치가 다른지 비교합니다.
copy_android.py     지워야하는데 지울줄 몰라서 냅둿습니다.
diff.py             폴더 내부의 다른 파일들을 모두 찾습니다.
doc.py              지울줄 몰라서 냅둿습니다.
memory_extract.py   scrdump와 함께 사용되며 자동으로 추출할 수 있는 곳에서 설정한 위치의 메모리를 추출합니다.
popLog.py           자동으로 앱을 실행시키고 시간재려고 만들었는데 만들다가 말아서 쓸모 없습니다.
screencap.py        android 화면의 스크린 캡쳐 기능입니다.
usbevent.py         /sys/class/power_supply/usb/uevent 내부의 내용을 찾는 것인데 이제 쓸모 없습니다.
xposed_detour.py    자동으로 xposed를 우회합니다. framework인 zip 파일이든 apk 파일이든 알아서 진행합니다.