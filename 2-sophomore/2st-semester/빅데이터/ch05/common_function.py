import platform
from matplotlib import rc
from matplotlib import pyplot as plt

#현재 파이썬이 실행되는 OS확인
def is_windows_platform():
    return platform.system() == 'Windows'

def is_mac_platform():
    return platform.system() == 'Darwin'

def is_linux_platform():
    return platform.system() == 'Linux'

def get_font_name():
    if is_mac_platform():
        return 'AppleGothic'
    elif is_linux_platform():
        return 'linuxfont!!'
    else:
        return 'Malgun Gothic'

#한글폰트 초기화
def init_plt():
    # 한글폰트설정
    rc('font', family=get_font_name())
    plt.rcParams['axes.unicode_minus'] = False



