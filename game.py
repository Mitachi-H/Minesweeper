import sys,random
import pygame


def setnumList(numList,bomb):
    for i,iList in enumerate(numList):
        for j in range(len(iList)):
            numList[i][j]=checkNumber(i,j,bomb)
    pass

def checkNumber(i,j,bomb):
    num=0
    for s in [-1,0,1]:
        for t in [-1,0,1]:
            if i+s<0 or i+s>19:
                continue
            if j+t<0 or j+t>27:
                continue
            if s==0 and t==0:
                continue
            num+=int(bomb[i+s][j+t])
    return num

def drawBackGround():
    black = (0,0,0)
    slategrey=(112,128,144)
    screen.fill(slategrey) # 背景を塗りつぶす
    #譜面生成
    for x in range(50,551,25):
        pygame.draw.line(screen,black, (x,50), (x,750), 1)#横20マス
    for y in range(50,751,25):
        pygame.draw.line(screen,black, (50,y), (550,y), 1)#縦28マス

def showAllClicked(clicked):
    for i,iList in enumerate(clicked):
        for j,click in enumerate(iList):
            if click:
                drawClicked(i,j)

def drawClicked(i,j):
    grey = (220,220,220)
    pygame.draw.rect(screen, grey, (50+i*25,50+j*25,25,25), width=0)
    pass

def showAllDoubtBomb(doubtBomb):
    for i,iList in enumerate(doubtBomb):
        for j,isDoubtbomb in enumerate(iList):
            if isDoubtbomb:
                drawDoubtBomb(i,j)

def drawDoubtBomb(i,j):
    lightsalmon	=(255,160,122)
    pygame.draw.circle(screen, lightsalmon,(63+i*25, 63+j*25), 10, width=0)
    pass

def drawBombLeft(bombLeft):
    black = (0,0,0)
    text2 = font.render(str(bombLeft), True,black)#描画する文字列の設定
    screen.blit(text2, (275,15))# 文字列の表示位置
    pass

def countbombLeft(bomb,bombLeft):
    ans=0
    for bombs,lefts in zip(bomb,bombLeft):
        ans+=sum(bombs)-sum(lefts)
    return ans

def showAllNumber(showNumList):
    colorList = [(0,0,0),(0,0,255),(0,138,0),(255,0,0),(0,0,139),(139,0,0)]#white,blue,green,red,darkblue,darkred
    for (i,j,num) in showNumList:
        drawNumber(i,j,num,colorList)

def drawNumber(i,j,num,colorList):
    text = font.render(str(num), True,colorList[num])#描画する文字列の設定
    screen.blit(text, [56+i*25, 52+j*25])# 文字列の表示位置

def showGameover(gameover):
    if gameover:
        black = (0,0,0)
        text = font.render("GameOver", True,black)#描画する文字列の設定
        screen.blit(text, (245,765))# 文字列の表示位置

def showAllBomb(gameover,bomb):
    if gameover:
        for i,iList in enumerate(bomb):
            for j,isbomb in enumerate(iList):
                if isbomb:
                    drawBomb(i,j)
    pass

def drawBomb(i,j):
    red = (255,0,0)
    pygame.draw.circle(screen, red,(63+i*25, 63+j*25), 10, width=0)
    pass

def showGameclear(gameclear):
    if gameclear:
        black = (0,0,0)
        text = font.render("GameClear", True,black)#描画する文字列の設定
        screen.blit(text, (245,765))# 文字列の表示位置

def getij(pos):
    x,y=pos
    return ((x-50)//25,(y-50)//25)

def checkij(i,j,clicked):
    if i<0 or i>19:
        return False
    if j<0 or j>27:
        return False
    return not clicked[i][j]

def showNearby0(i,j,numList,clicked,showNumList):
    for s in [-1,0,1]:
        for t in [-1,0,1]:
            if i+s<0 or i+s>19:
                continue
            if j+t<0 or j+t>27:
                continue
            if s==0 and t==0:
                continue
            if not clicked[i+s][j+t]:
                clicked[i+s][j+t]=True
                num=numList[i+s][j+t]
                if num==0:
                    showNearby0(i+s,j+t,numList,clicked,showNumList)
                else:
                    showNumList.append((i+s,j+t,num))

def main ():
    bomb=[[False if random.random()>0.2 else True for _ in range(28)] for _ in range(20)]#ボム管理、一定確率でボムセット
    doubtBomb=[[False]*28 for _ in range(20)]#旗管理
    showNumList=[]#見えている数字管理
    numList=[[0]*28 for _ in range(20)]#すべての数字管理
    setnumList(numList,bomb)#数値をボムに合わせる
    clicked=[[False]*28 for _ in range(20)]#クリック済み管理
    gameover=False
    gameclear=False
    while True:
        drawBackGround()#背景描写
        showAllClicked(clicked)#クリック済み色変更
        showAllDoubtBomb(doubtBomb)#旗表示
        drawBombLeft(countbombLeft(bomb,doubtBomb))#残り爆弾数管理
        showAllNumber(showNumList)#数字表示
        showGameover(gameover)#ゲームオーバー表示
        showAllBomb(gameover,bomb)#ゲームオーバー時ボム表示
        showGameclear(gameclear)#ゲームクリア表示
        pygame.display.update()#画面を更新

        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN:
                #ゲームオーバーかクリアなら操作無効
                if gameover or gameclear:
                    continue

                i,j = getij(event.pos)#クリックしたマス目取得
                if checkij(i,j,clicked):#i,jが適正値でclickされていないなら
                    if event.button==1:#左クリックなら
                        if bomb[i][j]:#ボムをクリックしたら
                            gameover=True
                        clicked[i][j]=True
                        if doubtBomb[i][j]:#旗をクリックしたら
                            doubtBomb[i][j]=False
                        num=numList[i][j]#数字取得
                        if num==0:
                            showNearby0(i,j,numList,clicked,showNumList)#隣接する0を表示
                        else:
                            showNumList.append((i,j,num))#数字表示
                    if event.button==3:#右クリックなら
                        doubtBomb[i][j]=not doubtBomb[i][j]
                        if bomb==doubtBomb:#旗を全て立てたら
                            gameclear=True
                        pass
            if event.type == pygame.QUIT: # 閉じるボタンが押されたら終了
                pygame.quit()     # Pygameの終了(画面閉じられる)
                sys.exit()
            # キーを押したとき
            if event.type == pygame.KEYDOWN:
                # ESCキーなら終了
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()

if __name__ == "__main__":
    pygame.init()#初期化
    screen = pygame.display.set_mode((600, 800))
    font = pygame.font.Font(None, 35)
    main()#ゲーム処理