class _MP():
    def __init__(self):
        self.MP_hands = mp.solutions.hands.Hands(static_image_mode=False, max_num_hands=1,min_detection_confidence=0.8, min_tracking_confidence=0.8)# 設定mediapipe 
        self.frame = None

        self.hand_pos = [[0,0]*21]
        self.hand_tag = ''
        self.static = ''
        self.dynamic = ''  # 動態手勢
        self.deq = deque(maxlen = 10) 

    #靜態手勢識別
    def Static(self):
        def vector_2d_angle(x1,y1,  x2,y2):  # 求二维向量的角度
            try:
                '''      A向量 * B向量 = A向量的長度 * B向量的長度 * COS(A)     
                    ==>  COS(A) = (A向量 * B向量) / (A向量的長度 * B向量的長度)
                '''  
                angle  = math.degrees( math.acos((x1 * x2 + y1 * y2) / (((x1 ** 2 + y1 ** 2) ** 0.5) * ((x2 ** 2 + y2 ** 2) ** 0.5))) )
                    
                if angle > 180.:
                    angle = None
            except:
                angle = None

            return angle

        # ==================================================================================
        # 求每根手指的角度 

        大拇指 = vector_2d_angle( #0,2  3,4
            (self.hand_pos[0][0] - self.hand_pos[2][0]), (self.hand_pos[0][1] - self.hand_pos[2][1]),
            (self.hand_pos[3][0] - self.hand_pos[4][0]), (self.hand_pos[3][1] - self.hand_pos[4][1]))

        食指 = vector_2d_angle(  #0,6  7,8
            (self.hand_pos[0][0] - self.hand_pos[6][0]), (self.hand_pos[0][1] - self.hand_pos[6][1]),
            (self.hand_pos[7][0] - self.hand_pos[8][0]), (self.hand_pos[7][1] - self.hand_pos[8][1]))
    
        中指 = vector_2d_angle(  #0,10  11,12
            (self.hand_pos[0][0]  - self.hand_pos[10][0]),  (self.hand_pos[0][1]  - self.hand_pos[10][1]),
            (self.hand_pos[11][0] - self.hand_pos[12][0]),  (self.hand_pos[11][1] - self.hand_pos[12][1]))
        
        無名指 = vector_2d_angle(  #0,14  15,16
            (self.hand_pos[0][0]  - self.hand_pos[14][0]),  (self.hand_pos[0][1]  - self.hand_pos[14][1]),
            (self.hand_pos[15][0] - self.hand_pos[16][0]),  (self.hand_pos[15][1] - self.hand_pos[16][1]))

        小拇指 = vector_2d_angle(  #0,18  19,20
            (self.hand_pos[0][0]  - self.hand_pos[18][0]),  (self.hand_pos[0][1]  - self.hand_pos[18][1]),
            (self.hand_pos[19][0] - self.hand_pos[20][0]),  (self.hand_pos[19][1] - self.hand_pos[20][1]))

        # ==================================================================================
        # 根據手指角度識別靜態手勢

        thr_angle = 65.
        thr_angle_thumb = 53.   # 大拇指角度閾值
        thr_angle_s = 49.

        if (大拇指 and 食指 and 中指 and 無名指 and 小拇指) :   # 五隻手指角度都不等於None
            if (大拇指 > thr_angle_thumb)     and (食指 > thr_angle)    and (中指 > thr_angle)    and (無名指 > thr_angle)         and (小拇指 > thr_angle):
                self.static = "zero"

            elif (大拇指 > thr_angle_s)       and (食指 < thr_angle_s)  and (中指 > thr_angle)    and (無名指 > thr_angle)      and (小拇指 > thr_angle):
                self.static = "one"

            elif (大拇指 > thr_angle_thumb)   and (食指 < thr_angle_s)  and (中指 < thr_angle_s)  and (無名指 > thr_angle)      and (小拇指 > thr_angle):
                self.static = "two"

            elif (大拇指 > thr_angle_thumb)   and (食指 < thr_angle_s)  and (中指 < thr_angle_s)  and (無名指 < thr_angle_s)    and (小拇指 > thr_angle):
                self.static = "three"

            elif (大拇指 > thr_angle_thumb)   and (食指 < thr_angle_s)  and (中指 < thr_angle_s)  and (無名指 < thr_angle_s)    and (小拇指 < thr_angle_s):
                self.static = "four"

            elif (大拇指 < thr_angle_s)       and (食指 < thr_angle_s)  and (中指 < thr_angle_s)  and (無名指 < thr_angle_s)    and (小拇指 < thr_angle_s):
                self.static = "five"
            
            elif (大拇指 < thr_angle_s)       and (食指 > thr_angle)    and (中指 > thr_angle)    and (無名指 > thr_angle)      and (小拇指 < thr_angle_s):
                self.static = "six"        
            
            elif (大拇指 < thr_angle_s)       and (食指 < thr_angle_s)  and (中指 > thr_angle)    and (無名指 > thr_angle)      and (小拇指 > thr_angle):
                self.static = "seven"
            
            elif (大拇指 < thr_angle_s)       and (食指 < thr_angle_s)  and (中指 < thr_angle_s)  and (無名指 > thr_angle)      and (小拇指 > thr_angle):
                self.static = "eight"   

            elif (大拇指 < thr_angle_s)       and (食指 < thr_angle_s)  and (中指 < thr_angle_s)  and (無名指 < thr_angle_s)    and (小拇指 > thr_angle):
                self.static = "nine"

            elif (大拇指 < thr_angle_s)       and (食指 < thr_angle_s)  and (中指 > thr_angle)    and (無名指 > thr_angle)      and (小拇指 < thr_angle_s):
                self.static = "love"        
            
            elif (大拇指 < thr_angle_s)       and (食指 < thr_angle_s)  and (中指 > thr_angle)    and (無名指 < thr_angle_s)    and (小拇指 < thr_angle_s):
                self.static = "rock" 

            elif (大拇指 < thr_angle_s)       and (食指 > thr_angle)    and (中指 > thr_angle)    and (無名指 > thr_angle)      and (小拇指 > thr_angle):
                self.static = "thumbUp"

            elif (大拇指 > thr_angle_thumb)   and (食指 > thr_angle)    and (中指 < thr_angle_s)  and (無名指 < thr_angle_s)    and (小拇指 < thr_angle_s):
                self.static = "ok"

            else:   
                self.static = 'Undefined'
                

        elif (大拇指 or 食指 or 中指 or 無名指 or 小拇指):   # 任一指為None
            map = { '大拇指': "Thumb angle is None",
                    '食指': "index angle is None",
                    '中指': "middle angle is None",
                    '無名指': "ring angle is None",
                    '小拇指': "little angle is None"}

            for t, s in zip([大拇指, 食指, 中指, 無名指, 小拇指],
                            ['大拇指', '食指', '中指', '無名指', '小拇指']):
                if t == None:
                    self.static = map.get(s)

    #動態手勢識別
    def Dynamic(self):
        kp_total = np.sum([self.hand_pos[i] for i in [0, 1, 5, 9, 13, 17]], axis=0)   # 0.1.5.9.13.17關鍵點的x,y座標的總和
        hand_center = (kp_total[0] // 6, kp_total[1] // 6)
        cv2.circle(self.frame, hand_center, 2, 0, 2)   # 顯示手的中心

        self.deq.append(hand_center)   # 往隊列後方增加
        
        if len(self.deq) == self.deq.maxlen:   # 如果隊列滿了 
            dx = self.deq[self.deq.maxlen-1][0] - self.deq[0][0]
            dy = self.deq[self.deq.maxlen-1][1] - self.deq[0][1]
            angle = np.arctan2(dy, dx) * 180 / np.pi
            th = 40 #閾值
            
            if abs(dx) > th or abs(dy)>th:
                if 135 < angle < 45 :
                    self.dynamic = 'up'
                elif -45 < angle < -135:
                    self.dynamic = 'down'
                elif -135 < angle < 135:
                    self.dynamic = 'left'
                elif 45 < angle < -45:
                    self.dynamic = 'right'
            else:
                self.dynamic = 'N'


    #
    def Hand_info(self,hand_landmarks, handedness ):
        #關鍵點座標、左右手、靜態手勢
        self.hand_pos = ([(int(hand_landmarks.landmark[i].x * self.frame.shape[1]), 
                        int(hand_landmarks.landmark[i].y * self.frame.shape[0]))
                        for i in range(21)]   ) # 獲得21關鍵點的座標      
        self.hand_tag = handedness.classification[0].label   #左手 or 右手 

        if self.hand_tag == 'Right': # 顯示右手手勢(靜態+動態)  淺藍色
            self.Static() 
            # cv2.putText(self.frame, self.static, tuple(self.hand_pos[5]), 0, 0.9, (255, 255, 0), 2) # 顯示靜態手勢(隨關鍵點移動)  
            # self.Dynamic()
            # cv2.putText(self.frame, self.dynamic, (500, 400), 0, 1.3,  (255, 255, 0), 3) # 顯示動態手勢(固定)             

        elif self.hand_tag == 'Left': # 顯示左手手勢(靜態+動態)  深藍色
            self.Static()
            # cv2.putText(self.frame, self.static, tuple(self.hand_pos[13]), 0, 0.9, (255, 100, 0), 2 )  # 顯示靜態手勢(隨關鍵點移動)
            # self.Dynamic()
            # cv2.putText(self.frame, self.dynamic, (0, 400), 0, 1.3, (255, 100, 0), 3) # 顯示動態手勢(固定)  
                

    #畫面處理函數
    def main(self) :
        option_color = [[253, 191, 61], [67, 206, 246], [255, 54, 176], [243, 109, 38], [130, 50, 180], 
                       [231, 101, 208], [220, 12, 75], [251, 179, 152], [44, 130, 38], [119, 152, 196]]
        #圓重疊面積比例
        def is_circles_overlap(c1, c2):
            dis = math.sqrt((c1[0] - c2[0]) ** 2 + (c1[1] - c2[1]) ** 2) #圓心距離
            overlap_area = np.pi * 10 ** 2 * (1 - (dis / (2 * 10)) ** 2)#重疊面積
            if overlap_area / (np.pi * 10 ** 2) >= 0.9 : #重疊比例>90%
                return True
            else:
                return False
        
        results = self.MP_hands.process(cv2.cvtColor(self.frame, cv2.COLOR_BGR2RGB)) # 對每幀進行處理得到multi_hand_landmarks與multi_handedness
        
        if results.multi_hand_landmarks and results.multi_handedness:  # 檢測到手
            for hand_landmarks, handedness in zip(results.multi_hand_landmarks,  results.multi_handedness): #遍歷每隻手的關鍵點、左or右手
                # mp.solutions.drawing_utils.draw_landmarks(self.frame, hand_landmarks ) # 顯示關鍵點及手骨  # , mp.solutions.hands.HAND_CONNECTIONS 
                self.Hand_info(hand_landmarks, handedness)
                
                #傳參數
                _fruit.mouse_pos = self.hand_pos[8]
                _brick.mouse_pos = self.hand_pos[8]
                _sudoku.pos8 = self.hand_pos[8]
                _sudoku.pos4 = self.hand_pos[4]
                _sudoku.number_eng = _mp.static
                

                if ((self.static == "five" or self.static == "four") and 
                    _fruit.quit == True and _brick.quit == True and _sudoku.quit == True):

                    CircularBox = (self.hand_pos[12][0], self.hand_pos[12][1]-20)#圓框座標
                    cv2.circle(self.frame,   CircularBox, 12, (255,255,0),  2)  #圓框

                    xy_list = np.linspace(0, 2*np.pi, 6, endpoint=False) #圍繞圓的周圍產生距離相等的圓  (角度)
                    
                    r = math.sqrt((CircularBox[0] - self.hand_pos[9][0])**2 + (CircularBox[1] - self.hand_pos[9][1])**2) #圓框與9點的距離
                    center = self.hand_pos[9] #cv2.circle(frame, center, 12, (255,255,255), -1)
                    
                    for i,(x,y) in enumerate(zip(np.cos(xy_list+time.time()*1.5),  np.sin(xy_list+time.time()*1.5))): #建立圍繞手的小圓
                        x,y = int(center[0] + r * x), int(center[1] + r * y)
                        cv2.circle(self.frame, (x,y), 12, option_color[i], -1)
                        cv2.putText(self.frame, str(i+1), (x-6,y+6), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 1)
                    
                        if is_circles_overlap(CircularBox, (x,y)): #圓框與實心圓重疊
                            if self.static == 'four':
                                cv2.circle(self.frame, (x,y),  16, option_color[i], -1) #實心圓變大 
                                if i+1 == 1:
                                    _fruit.th()
                                    _fruit.quit =  False #遊戲啟動
                                
                                if i+1 == 3:
                                    _brick.th()
                                    _brick.quit =  False#遊戲啟動

                                if i+1 == 5:
                                    _sudoku.generate(1)
                                    _sudoku.quit =  False#遊戲啟動






#=========================
import cv2, math, time, sys, pygame as pg, numpy as np, mediapipe as mp,os
from collections import deque
sys.path.append(os.path.dirname(os.path.abspath(__file__))) #新增模組載入路徑(目前py檔路徑)
import Fruit,Brick, Sudoku



_fruit = Fruit.Main()
_brick = Brick.Main()
_sudoku = Sudoku.Main()
pg.display.set_mode((640, 480), flags=pg.HIDDEN)#隱藏pygame視窗


_mp = _MP()
cap = cv2.VideoCapture(0, cv2.CAP_DSHOW) # 使用攝影機
last_time = 0
while cap.isOpened():
    Success, _mp.frame = cap.read() # 讀取攝影機的每一幀
    if Success :
        _mp.frame = cv2.flip(_mp.frame,1)
        _mp.main()
        
        if _fruit.quit == False: #遊戲啟動
            f = _fruit.pg_cv
            
        elif _brick.quit == False: #遊戲啟動
             f = _brick.pg_cv

        elif _sudoku.quit == False: #遊戲啟動
            _sudoku.main(50,(60,15))
            f = _sudoku.frame
           
        else:
            f = _mp.frame

        
        cv2.imshow('', cv2.addWeighted(_mp.frame, 0.15, f, 0.85, 0) )#透明 合併
        
        
    if (cv2.waitKey(1) and cv2.getWindowProperty('', cv2.WND_PROP_VISIBLE) <= 0 ):#右上角叉叉被按下
        cap.release() # 釋放攝影機
    
    





