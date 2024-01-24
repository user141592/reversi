import numpy as np


#---関数定義---------------------
#出力設定
def piece_color(a):
    if a == 0:
        return "-"
    elif a == 1:
        return "○"
    elif a == -1:
        return "●"
    else:
        return "+"

def display_boad(boad):
    r = 1
    print("    1   2   3   4   5   6   7   8")
    print("   _______________________________")
    for i in (boad[1:9]):
        print(f'{r} ',end="")
        c = 1
        for j in boad[r,1:9]:
            print(f'| {piece_color(boad[r][c])} ',end="")
            c+=1
        print('|')
        r+=1
    print("   _______________________________")

#選択位置は置けるか
#   返せる場合は返せる位置を[[r,c]]で
#   返せるコマが無い場合は[]を
#   コマが置いてある場合と範囲外はNoneを返す
def check1(boad,r,c,turn):
    #範囲内か(8*8以内)
    if r<1 or 8<r or c<1 or 8<c:
        print("行、列はそれぞれ1～8の数字でお願いします")
    else:
        #セルにコマがはいっているか
        if boad[r,c] == 0:
            #8方向に反対のコマがいるか(0,0は上で消してる)
            change_list = []
            for x in range(-1,2,1): #-1～1まで1つずつ
                for y in range(-1,2,1):
                    if turn == boad[r+x,c+y]*-1:
                        check_r = r
                        check_c = c
                        change_list_temporary = []
                        while True:
                            if boad[check_r+x,check_c+y] == 2:
#                                print("一番外")
                                break;
                            elif boad[check_r+x,check_c+y] == turn*-1:
                                change_list_temporary.extend([check_r+x,check_c+y])
                                check_r = check_r+x
                                check_c = check_c+y
                            elif boad[check_r+x,check_c+y] == turn:
                                change_list.append(change_list_temporary)
                                break;
                            elif boad[check_r+x,check_c+y] == 0:
#                                print("その先におまえの仲間はいない")
                                break;
                            else:
                                print(f'{boad[check_r+x,check_c+y]}わからん')
                                break;
            return change_list

#change_listの位置の色を反転する　listは([[r,c],[r,c]])で表記
def change(boad, change_list,r,c,turn):
    for i in range(len(change_list)):
        boad[int(change_list[i][0])][int(change_list[i][1])] = boad[change_list[i][0]][change_list[i][1]]*-1
        # 何回も処理するけどforに入らないと([]のときは)変わらない
        boad[r,c]=turn

#入力確認(int型のみ)
def int_input(prompt):

    while True:
        i = input(prompt)
        if i.isdecimal():
            i = int(i)
            if i<1 or 8<i:
                print(f"入力は1～8でお願いします")
            else:
                break
        else:
            print(f"{i}はint型である必要があります")
    return i

#置ける場所がまだあるか全検索(置ける場所のリストを返す)
def game_end_check(boad,turn):
    end_check=[]
    for r in range(1,9):
        for c in range(1,9):
            #コマが置かれていないとき
            if boad[r,c]==0:
                #返せるコマがあるとき
                if check1(boad,r,c,turn) !=[]:
#                    print(f'[{r},{c}]に置くと{check1(boad,r,c,turn)}が返せる')
                    end_check.append([r,c])
    print(end_check)
    return sum(map(sum,end_check))

#勝利判定(盤面の 1 v.s. -1)
def get_winnner(boad):
    boad_sum = sum(map(sum,boad))-(2*9*4) #10*10の外枠に2が入ってる
    print(boad_sum)
    if boad_sum>0:
        print("白の勝ち")
    elif boad_sum<0:
        print("黒の勝ち")
    elif boad_sum==0:
        print("引き分け")
    else:
        print("なにしたん？")
            

#---初期設定--------------------

boad_status =np.zeros((10,10))
boad_status[:,0]=2
boad_status[:,9]=2
boad_status[0,:]=2
boad_status[9,:]=2

#開始盤面
boad_status[4,4]=1
boad_status[5,5]=1
boad_status[4,5]=-1
boad_status[5,4]=-1

turn_player = -1
skip = 0 #2回連続スキップでゲームエンド
display_boad(boad_status)

while skip <=2:
    print(f'{piece_color(turn_player)}のターン')
    if game_end_check(boad_status,turn_player)==0:
        print(f'{piece_color(turn_player)}のターンはスキップ')
        turn_player =turn_player*-1
        skip = skip +1
    else:
        skip = 0
        row = int(int_input("行(1~8で入力)："))
        column = int(int_input("列(1~8で入力)："))
        if check1(boad_status,row,column,turn_player) == None:
            print("そこには置けません")
        elif check1(boad_status,row,column,turn_player) == []:
            print("そこだと返せるコマがありません")
        else:
            print(check1(boad_status,row,column,turn_player))
            change(boad_status, check1(boad_status,row,column,turn_player),row,column,turn_player)
            turn_player =turn_player*-1
    display_boad(boad_status)

get_winnner(boad_status)
