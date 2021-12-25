import numpy as np
import cv2
from jamo import h2j,j2hcj
from PIL import Image
from tkinter import *



####초기 설정
win = Tk()
win.title("Image Processing")
win.geometry("1000x800")
win.option_add("*Font","고딕 20")

#### 입력 안내창
lab1 = Label(win)
lab1.config(text = "손글씨 전환 프로그램")
lab1.pack()


#### 변환할 글씨 입력창
ent1 = Text(win)
ent1.config(width = 50, height = 20)
ent1.insert(1.0, "손글씨로 전환할 문장을 입력해주세요.")
def clear(event):       #입력창 안내메시지 클릭하면 지워지도록 하는 함수
    if ent1.get(1.0,1.21) == "손글씨로 전환할 문장을 입력해주세요.":
        ent1.delete(1.0,20.50)

ent1.bind("<Button-1>", clear)           # 위 함수 실행(마우스 오른쪽 클릭하면 안내메시지 삭제)     
ent1.pack()

#### 입력 버튼
btn = Button(win)
btn.config(text = "입력", command=lambda :[new_win(), msg()])

def msg():    #입력 값 변수 저장 함수
    global contents
    contents = ent1.get(1.0,50.20)
    
btn.pack()

def new_win():
    global nw
    nw=Toplevel(win)
    nw.title("손글씨 출력")
    nw.geometry("900X700")
    lab3 = Label(nw)
    img = PhotoImage(file = 'paper', master = nw)    
    lab3.config(image = img)
    lab3.pack()
    
win.mainloop()

#초성 중성 종성 배열선언
first=['ㄱ','ㄲ','ㄴ','ㄷ','ㄸ','ㄹ','ㅁ','ㅂ','ㅃ','ㅅ','ㅆ','ㅇ','ㅈ','ㅉ','ㅊ','ㅋ','ㅌ','ㅍ','ㅎ']
mid=['ㅏ','ㅐ','ㅑ','ㅒ','ㅓ','ㅔ','ㅕ','ㅖ','ㅣ','ㅗ','ㅛ','ㅜ','ㅠ','ㅡ','ㅘ','ㅙ','ㅚ','ㅝ','ㅞ','ㅟ','ㅢ']
last=['ㄱ', 'ㄲ', 'ㄳ ','ㄴ', 'ㄵ', 'ㄶ', 'ㄷ', 'ㄹ', 'ㄺ','ㄻ', 'ㄼ', 'ㄽ', 'ㄾ', 'ㄿ', 'ㅀ','ㅁ', 'ㅂ', 'ㅄ', 'ㅅ', 'ㅆ','ㅇ', 'ㅈ', 'ㅊ', 'ㅋ', 'ㅌ','ㅍ', 'ㅎ']

#배열first mid last 이미지 순서에 따라 데이터를 반복문을 통한 잘라내기로 초성 중성 종성에 대한 '이미지 배열'을 만듦
firstim = {}
midim = {}
lastim={}

#이미지 불러오기
field=cv2.imread('korean/unit250.jpg')  #글자의 기본 틀이됨/ 높이 250 , 너비 200
paper=cv2.imread('white500700.jpg')     #종이의 역할을 함 / 가로 500,세로700 

#반복문을 이용한 이미지 데이터화하기 cutting
#초성 이미지 배열 데이터화  //(세로 100,가로1900)으로 100*100씩 잘라서 오른쪽으로 이동하며 데이터화
for i in range(19):
    cutting=cv2.imread('/Users/suacho/Desktop/STUDY/웰씨코기/결과물/korean/firstsum.jpg')
    x=i*100
    y=0
    firstim[i]=cutting[y:y+100,x:x+100]
#중성 이미지 배열 데이터화
#중성은 세로모음 ㅣㅓㅏ가로모음 ㅡㅗㅜ, 이중모음 ㅝ ㅙ 같이 차지하는 공간이 다르기 때문에 mid{}의 경우에도 가로모음,세로모음,이중모음순서로 선언을 했고
#커팅 방식을 3가지로 나누어서 진행했음. (가로*세로) 세로모음(100*200) 가로모음(200*100) 이중모음(200*200)
for j in range(21):
    if j<9:
        cutting=cv2.imread('결과물/korean/heightmid.jpg')  #세로모음
        x=j*100
        y=0
        midim[j]=cutting[y:y+200,x:x+100]    
    elif j<14 :
        cutting=cv2.imread('결과물/korean/widthmid.jpg')   #가로모음
        x=(j-9)*200
        y=0
        midim[j]=cutting[y:y+100,x:x+200]
    else:
        cutting=cv2.imread('korean/doublemid.jpg')  #이중모음
        x=(j-14)*200
        y=0
        midim[j]=cutting[y:y+200,x:x+200]
#종성 이미지 데이터화
#(2700*100)으로 100*100씩 잘라서 오른쪽으로 이동하며 데이터화   
for h in range(27):
    cutting=cv2.imread('결과물/korean/lastsum.jpg')
    x=h*100
    y=0
    lastim[h]=cutting[y:y+100,x:x+100]
    
#이미지 마스킹 기법인 비트연산을 활용했음 (흰색이면 1 , 검은색이면 0)
#초성이 img1, 중성이 img2 , 종성이 있는 경우 조건문을 활용해 다음의 과정을 한번 더 반복함.
#img1은 글자유닛인 unit250과 bitwise_and연산을 함 ->img1(초성)의 마스킹 부분에 흰 유닛인 field 이미지 2개를 and연산을 하면 모두 흰색(1)인 부분만 흰색으로
#나타남 , 그 다음 중성인 img2와 bitwise_and 연산을 진행. 마찬가지로 흰색인 부분만 흰색이므로 글자인 부분은 검정색으로 표시. 이것으로 글자 이미지를 겹침.
def sumimg(img1,img2):
    img1=masking(img1)
    img2=masking(img2)
    A=cv2.bitwise_and(field,field,mask=img1)   
    result=cv2.bitwise_and(A,field,mask=img2)      #masking field에 덮어 씌우기
    return result
    
    
#masking 함수 구현

def masking(img):
    gray=cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)   #이미지를 흑,백으로 바꿈
    ret,mask=cv2.threshold(gray,160,255,cv2.THRESH_BINARY)    #ret, out = cv2.threshold(img, 임계값, value, 스레시홀딩 적용방법) 
    return mask                                               #cv2.THRESH_BINARY: 픽셀 값이 임계값을 넘으면 value로 지정하고, 넘지 못하면 0으로 지정



string = contents #string 변수에 input 값 저장
size=len(string)        #문자열의 길이
#jamo는 한글의 초성,중성,종성을 분리해주는 라이브러리함수
#문자열에서 글자수 만큼 반복하며
#한글자를 초성,중성,종성으로 나누어 배열에 넣고 반복문을 수행
for letter in range(size):                 #letter 글자단위 유닛
    jamo_str=j2hcj(h2j(string[letter]))    #string[0] = 박 //string[1]=주 //string[2]=영
    print(jamo_str)                        #jamo_str[0]=ㅂ //jamo_str[1]=ㅏ//jamo_str[2]=ㅇ
    size_jamo=len(jamo_str)                #size_jamo=3
    
    #글자를 종이(글자가 나열되는 공간 paper변수)에 나열할 때 줄바꿈 및 좌표를 반복문 횟수에 따라 설정
    #글자 유닛을 200*250에서 size를 축소하여 20*25로 만들고 이에 따라 좌표값을 설정
    #line-줄 left=x왼쪽좌표 right=x오른쪽 좌표 up = y 위쪽 좌표 down = y 아래쪽 좌표
    line = letter//25      
    left = letter*20 - 500*line  
    up = line*25
    right = (letter+1)*20 - 480*line
    down = (line+1)*25
    
    
    #글자에 대한 이미지를 불러오기 위해서는 index값이 필요한데  이는 jamo_str에 저장된 초성 중성 종성을 기존의 first mid last 배열에서
    #index 값을 검색하는 것으로 알 수 있다. 초성만 쓰이는 경우 종성이  없는 경우 있는 경우에 따라 가정법을 사용하여 index값을 num1,num2,num3에 저장했다.
    num1=first.index(jamo_str[0],0,19)
    if size_jamo>1:
        num2=mid.index(jamo_str[1],0,21)
    if size_jamo>2:
        num3=last.index(jamo_str[2],0,27) 
    
    #unit250은 가로200세로250의 흰색의 빈 유닛이다. index값에 따라 이미지 파일을 불러오고 이것의 위치를 중성의 스타일에 따라 좌표를 지정해준다.
    #예를 들면 중성이 가로모음이냐, 세로모음이냐, 이중모음이냐에 따라 초성의 위치가 달라지게 된다.
    fstunit=cv2.imread('korean/unit250.jpg')
    midunit=cv2.imread('korean/unit250.jpg')
    lastunit=cv2.imread('korean/unit250.jpg')
    # 초성자음만 쓰는 경우 ex) ㅎㅎㅎ, ㅋㅋㅋ 
    if size_jamo==1 :
        if jamo_str[0] in first:
            fx=40
            fy=50
            fstunit[fy:fy+100,fx:fx+100]=firstim[num1]
            a=masking(fstunit)
            result=sumimg(fstunit,midunit)
            result=cv2.bitwise_and(field,field,mask=a)
    #종성이 없는 경우
    elif size_jamo==2 :
        if jamo_str[1] in {'ㅏ', 'ㅐ', 'ㅑ', 'ㅒ','ㅓ', 'ㅔ', 'ㅕ', 'ㅖ','ㅣ'}: #세로모음
            fx=20
            fy=70
            fstunit[fy:fy+100,fx:fx+100]=firstim[num1]                   #중성의 타입에 따라서 초성의 위치 설정 후 합성,index값으로 이미지파일 불러옴
            mx=80
            my=20
            midunit[my:my+200,mx:mx+100]=midim[num2]                     #중성의 위치 설정 후 합성
            result=sumimg(fstunit,midunit)                               #suming 함수를 통해 두 이미지를 비트연산 기법으로 합성함
        if jamo_str[1] in {'ㅗ','ㅛ','ㅜ','ㅠ','ㅡ'}:                           #가로모음
            fx=53
            fy=55
            fstunit[fy:fy+100,fx:fx+100]=firstim[num1]
            mx=0
            my=130
            midunit[my:my+100,mx:mx+200]=midim[num2]
            result=sumimg(fstunit,midunit)
        if jamo_str[1] in {'ㅘ','ㅙ','ㅚ','ㅝ','ㅞ','ㅟ','ㅢ'}:                 #이중모음
            fx=30
            fy=45
            fstunit[fy:fy+100,fx:fx+100]=firstim[num1]
            mx=0
            my=20
            midunit[my:my+200,mx:mx+200]=midim[num2]
            result=sumimg(fstunit,midunit)
    #종성이 있는 경우
    #(종성이 없으면 초성 중성만 있기 때문에 이 경우를 나누지 않으면 글자의 종성부분이 빈 공간으로 남아있어 어색함.)
    elif size_jamo==3 :
        if jamo_str[1] in {'ㅏ', 'ㅐ', 'ㅑ', 'ㅒ','ㅓ', 'ㅔ', 'ㅕ', 'ㅖ','ㅣ'}:
            print("세로모음")
            fx=20
            fy=50
            fstunit[fy:fy+100,fx:fx+100]=firstim[num1]
            mx=80
            my=0
            midunit[my:my+200,mx:mx+100]=midim[num2]
            result=sumimg(fstunit,midunit)
        if jamo_str[1] in {'ㅗ','ㅛ','ㅜ','ㅠ','ㅡ'}:
            print("가로모음")
            fx=55
            fy=25
            fstunit[fy:fy+100,fx:fx+100]=firstim[num1]
            mx=0
            my=75
            midunit[my:my+100,mx:mx+200]=midim[num2]
            result=sumimg(fstunit,midunit)
        if jamo_str[1] in {'ㅘ','ㅙ','ㅚ','ㅝ','ㅞ','ㅟ','ㅢ'}:
            print("이중모음")
            fx=15
            fy=10
            fstunit[fy:fy+100,fx:fx+100]=firstim[num1]
            mx=0
            my=0
            midunit[my:my+200,mx:mx+200]=midim[num2]
            result=sumimg(fstunit,midunit)
        #종성자음 suming함수를 사용하여 초성+중성 이미지와 종성이미지 합성
        fx=50
        fy=140
        lastunit[fy:fy+100,fx:fx+100]=lastim[num3]
        result=sumimg(result,lastunit)              
    

    #글자 사이즈를 축소함
    resize = cv2.resize(result, dsize=(0, 0), fx=0.1, fy=0.1)
    #result 변수에 반복문 한번에 한글자의 이미지가 할당됨. 이를 paper에 위치 지정을 하여 합성
    paper[up:up+25,left:left+20]=resize
        
    
    
#반복문이 끝나고 paper를 띄우는 새로운 창 함수


