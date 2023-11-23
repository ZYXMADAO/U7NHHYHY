import numpy as np,cv2,random,time


class Main(object):
    def __init__(self):
        self.quit = True
       
       
    def generate(self,difficulty):
        self.chage_last_time = 0
        self.number_last_time= 0
        self.matrix = np.zeros((9,9))
        self.zeroindex = []#代填入空格的座標
        self.number_eng = ""


        while True:
            try:
                rows = [set(range(1,10)) for _ in range(9)]    #9個 包含1~9的集合(可選數字)
                cols = [set(range(1,10)) for _ in range(9)]    #9個 包含1~9的集合(可選數字)
                squares = [set(range(1,10)) for _ in range(9)] #9個 包含1~9的集合(可選數字)
                for r in range(9): #row
                    for c in range(9):#col
                        #遍歷每一格
                        choices = rows[r].intersection(cols[c]).intersection(squares[(r//3)*3 + c//3]) #! 未重複出現的可選數字(同一列、欄、九宮格)
                        choice = np.random.choice(list(choices)) #可選數字中 選一個
                        self.matrix[r,c] = choice
                       
                        #! 從可選數字中刪除已選數字
                        rows[r].discard(choice)
                        cols[c].discard(choice)
                        squares[(r//3)*3 + c//3].discard(choice)
               
                #=========14~30 、 31~47 、 48~64=============
                l = 14       + (difficulty - 1) * 17
                r = (14 - 1) + (difficulty)     * 17


                x = random.randint(l,r)#根據難度隨機挑選要抹除的數字量
                clear_indexs = random.sample(range(81), x) #隨機挑選x個位置(不重複)刪除數字
               
               
                for index in clear_indexs:
                    self.matrix[index // 9, index % 9] = 0 #清除
                    self.zeroindex.append([index // 9, index % 9])
               
                self.zeroindex = sorted(self.zeroindex, key=lambda x: (x[0], x[1]))#按照row排序 再按照col排序
                self.now_pos = self.zeroindex[0] #第一次的空格位置
               
                break
           
            except :
                continue

    def check(self):
        rows    = [set() for _ in range(9)]    #已出現數字
        cols    = [set() for _ in range(9)]    #已出現數字
        squares = [set() for _ in range(9)]    #已出現數字
       
        for r in range(9): #row
            for c in range(9):#col
                choice = self.matrix[r,c]#遍歷每一格
                if (choice in rows[r] or  
                    choice in cols[c] or
                    choice in squares[(r//3)*3 + c//3]) : #!數字重複出現(同一列、欄、九宮格)
                    return False
               
                else:#! 數字未重複出現(同一列、欄、九宮格) ==> 添加 已出現數字
                    rows[r].add(choice)
                    cols[c].add(choice)
                    squares[(r//3)*3 + c//3].add(choice)
        return True

    def text_btn(self,text,x,y,color = (0,255,0),scale=1,thick=2 ):
        font = cv2.FONT_HERSHEY_SIMPLEX
        text_size = cv2.getTextSize(text, font,scale,thick)[0] #文字的大小(x px 和 y px)
        rect =  [x, y, x+text_size[0], y-text_size[1]] #左下 右上
        cv2.putText(self.frame, text, (x,y),font,scale,color ,thick)
       
        return rect
       
    def pressed(self,mouse_pos,rect):
        if ((mouse_pos[0] > rect[0] ) and (mouse_pos[1] < rect[1] ) and #左下
            (mouse_pos[0] < rect[2] ) and (mouse_pos[1] > rect[3] )) : #右上
            return True
        else:
            return False

    def main(self,inter, start):
        self.frame = np.ones((480, 640, 3), np.uint8) * 240

        #辨識手勢 修改數字
        for i,n in enumerate(['one','two','three','four','five','six','seven','eight','nine']):
            if self.number_eng==n and time.time() - self.number_last_time > 2: #! 距離上次更改數字超過2秒
                self.matrix[self.now_pos[0]][self.now_pos[1]] = i+1
                self.number_last_time = time.time()

        # 顯示 線
        for i in range(10):
            x = start[0] + (i * inter)
            y = start[1] + (i * inter)
            cv2.line(self.frame, (x, start[1]), (x, start[1]+inter*9), (0, 0, 255), 1)#垂直
            cv2.line(self.frame, (start[0], y), (start[0]+inter*9, y), (0, 0, 255), 1)#水平

        # 顯示數字
        for i in range(9):
            for j in range(9):
                number = int(self.matrix[i,j])#先列在行
                if number != 0: #不為空(0)
                    font,scale,thick = cv2.FONT_HERSHEY_SIMPLEX, 1,1
                    text_size = cv2.getTextSize(str(number),font,scale,thick)[0]
                   
                    run = True
                    while run: #維持text為inter的一半大小(自動縮放)
                        if text_size[0] > inter/2:#text>格子一半px
                            scale -= 0.03
                        elif text_size[0] < inter/2:#text小<格子一半px
                            scale += 0.03
                        else: #text=格子一半px
                            run = False
                        text_size = cv2.getTextSize(str(number),font,scale,thick)[0]


                    center_x = start[0] + j * inter + inter//2 #每格的中心點
                    center_y = start[1] + i * inter + inter//2#每格的中心點
                    x = center_x  - text_size[0] // 2
                    y = center_y  + text_size[1] // 2
                    # cv2.circle(self.frame,(center_x,center_y), 3, (255,0 ,0 ), -1)
                    # cv2.rectangle(self.frame, (x,y), (x+text_size[0],y-text_size[0]), (0 ,255,0 ), 1, cv2.LINE_AA)
                    cv2.putText(self.frame, str(number), (x,y),font,scale, (255,0 ,0 ),thick)
                else:#未填充數字
                    x = start[0] + j * inter
                    y = start[1] + i * inter + inter
                    rect = [x, y, x+inter, y-inter]
 
                    if self.number_eng == 'thumbUp' and self.pressed(self.pos4,rect) and time.time()-self.chage_last_time > 2 : #! 距離上次更改位置超過2秒
                        self.chage_last_time = time.time()
                        self.now_pos = [i,j]
                        

        #綠框  
        x = start[0] + self.now_pos[1] * inter
        y = start[1] + self.now_pos[0] * inter
        cv2.rectangle(self.frame, (x,y), (x+inter ,y+inter ), (0 ,255,0 ), 1, cv2.LINE_AA)



        #按鈕
        quit_rect = self.text_btn('Quit',550, 200)
        if self.pressed(self.pos8,quit_rect ) and self.number_eng == 'zero':#! 手勢為0 + 食指位置
            self.quit = True
       
        done_rect = self.text_btn('Done',540, 300)
        if self.pressed(self.pos8,done_rect ) and self.number_eng == 'zero' :#! 手勢為0 + 食指位置
            if self.check():
                self.text_btn('WIN',200, 250,color=(0,0,255),scale=3,thick=3)
            else:
                self.text_btn('FAIL',200, 250,color=(0,0,255),scale=3,thick=3)
           
 


