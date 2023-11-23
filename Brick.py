import pygame as pg, random, math  , os  ,threading,cv2,numpy as np,time

os.chdir(os.path.dirname(os.path.abspath(__file__))) #目前py檔路徑


    

class Ball(pg.sprite.Sprite):
    
    def __init__(self,screen,speed=8, x=250, y=300, r=10,  color=(255,123,255)):#初始值
        super().__init__()
        self.screen = screen
        self.x , self.y = x,y
        self.dx, self.dy = speed , -speed
        self.color = color

        self.image = pg.Surface([r*2, r*2])
        self.image.set_colorkey((0, 0, 0))
        pg.draw.circle(self.image, self.color, (r, r), r, 0)
        self.rect = self.image.get_rect()
        self.rect.center = (self.x , self.y)


    def update(self):#更新位置
        self.x += self.dx
        self.y += self.dy
        self.rect.center = (self.x , self.y)

        if self.rect.left <= 0 :#超過左邊界
            self.rect.left = 0
            self.bouncelr()
        
        if self.rect.right >= self.screen.get_width() :#超過右邊界
            self.rect.right = self.screen.get_width()
            self.bouncelr()
        
        if self.rect.top <= 0:#超過上邊界
            self.rect.top = 0
            self.bounceup()
        
        if self.rect.bottom >= self.screen.get_height():#超過下邊界
            return True # Game Over

        elif self.rect.bottom <= self.screen.get_height(): #未超過下邊界
            return False
        
        

    def bounceup(self):  #上邊界反彈
        self.dy *= -1

    def bouncelr(self):  #左右邊界反彈
        self.dx *= -1


    def size(self, r):
        self.image = pg.Surface([r*2, r*2])
        self.image.set_colorkey((0, 0, 0))
        pg.draw.circle(self.image, self.color, (r, r), r, 0)
        self.rect = self.image.get_rect()


class Pad(pg.sprite.Sprite):
    def __init__(self,screen, w=150, h=25, clr = (0,200,255)):
        super().__init__()
        self.clr = clr
        self.screen = screen
        self.image = pg.Surface((w,h))
        self.image.fill(self.clr)
        self.image.convert()#轉換實體
        self.rect = self.image.get_rect()#得到圖片rect
        self.rect.y = self.screen.get_height() - self.rect.height - 10#設定rect的y座標
        self.pos = (100 ,self.screen.get_height() - self.rect.height)
        
        

    def update(self):
        self.rect.centerx = self.pos[0]

        if self.rect.right > self.screen.get_width():#超過右邊界
            self.rect.right = self.screen.get_width()
        elif self.rect.left <= 0 :#超過左邊界
            self.rect.left = 0

    def size(self, w=100, h=25):
        self.image = pg.Surface((w,h))
        self.image.fill(self.clr)
        self.image.convert()#轉換實體
        self.rect = self.image.get_rect()
        self.rect.y = self.screen.get_height() - self.rect.height - 10
    
    def draw(self):
        self.screen.blit(self.image, (self.pos[0], self.screen.get_height() - self.rect.height))


class Brick(pg.sprite.Sprite):
    def __init__(self, w=38, h=13, tp = 1):#初始化
        super().__init__()
        self.image = pg.Surface((w, h)) #設定磚塊 長.寬
        self.tp = tp
        self.count = 0

        if self.tp == 1:
            self.image.fill((255,150,150)) #紅
        elif self.tp == 2 :
            self.image.fill((150,255,150))#綠

        self.rect = self.image.get_rect()

    def set_pos(self,x,y):
        self.rect.topleft = (x , y)

    def Type(self):
        # s = 0
        if self.tp == 1 :#紅
            self.kill()#從磚塊群組中刪除該磚塊
            # s = 1

        elif self.tp == 2:#綠
            self.count += 1
            if self.count == 3:
                self.kill()#從磚塊群組中刪除該磚塊
                # s = 3

        # return s


class Button(pg.sprite.Sprite):
    def __init__(self, screen, title, clr = [255,255,255], font = "Arial", fonsize =30 , x = None, y = None, x_start =0, x_end =1000 ):
        super().__init__()
        self.screen = screen
        bfont = pg.font.SysFont(font,fonsize)#按鈕字體
        self.surface = bfont.render(title, 1, clr)

        self.WIDTH = self.surface.get_width()
        self.HEIGHT = self.surface.get_height()

        if x == 'center':
            self.x = ((x_end-x_start) // 2) - (self.WIDTH // 2)   +  x_start
        else:
            self.x = x

        self.y = y

        self.screen.blit(self.surface , (self.x,self.y))
        pg.display.update() 

    def pressed(self,pos): 
        if (pos[0] > self.x ) and (pos[1] > self.y ) and (pos[0] < self.x+self.WIDTH  ) and (pos[1] < self.y+self.HEIGHT) : #滑鼠座標在按鈕內
            return True
        
        else:#滑鼠座標不在按鈕內
            return False


class Skill(pg.sprite.Sprite):
    skill_dic = {   'fast':(20,40), 
                    'slow':(30,30), 
                    'big':(25,25),
                    'small':(25,25),
                    'arrow w in' : (36,14), 
                    'arrow w out': (36,14), 
                    'arrow h in' : (14,36), 
                    'arrow h out': (14,36)
                    }

    def __init__(self,screen,bottomleft):
        super().__init__()
        self.screen = screen
        self.sknm = random.choice(list(self.skill_dic.keys()))#skill name
        self.speed = 5
        self.image = pg.image.load('Brick_data/img/' + self.sknm + '.png')  
        self.image = pg.transform.scale(self.image, self.skill_dic[self.sknm])#變更圖片大小
        self.image.convert_alpha()
        self.rect = self.image.get_rect()
        self.rect.topleft = bottomleft#技能左上角座標=被擊破的磚塊的左下角



    def update(self):#更新位置
        if self.rect.right >= self.screen.get_width():
            self.rect.right = self.screen.get_width() 
        elif self.rect.bottom >= self.screen.get_height():
            self.kill()#從skill群組中刪除skill
        self.rect.y += self.speed

    def skill(self, ball, pad):
        #球
        if self.sknm == 'fast':
            ball.speed = random.randint(12,16) #原speed的1.2~1.6倍
        elif self.sknm == 'slow':
            ball.speed = random.randint(4,8) #原speed的0.4~0.8倍
        elif self.sknm == 'big':
            ball.size(random.randint(25,45))
        elif self.sknm == 'small':
            ball.size(random.randint(5,10))

        #板子    
        elif self.sknm == 'arrow w in':#寬短
            pad.size(w=random.randint(20,60) , h = pad.rect.height)
        elif self.sknm == 'arrow w out':#寬長
            pad.size(w=random.randint(200,600), h = pad.rect.height)
        elif self.sknm == 'arrow h in':#高短
            pad.size(h= random.randint(5,15), w = pad.rect.width)
        elif self.sknm == 'arrow h out':#高長
            pad.size(h=random.randint(50,150), w = pad.rect.width)
        

class Main():
    def __init__(self):
        pg.init()  #初始化
        self.w, self.h = 640,480  #初始化視窗大小
        self.screen = pg.display.set_mode((self.w, self.h))  #設置視窗大小
        self.mouse_pos = (0,0)
        self.quit = True #離開(true) 表示未啟用
        self.screen_convert()
        


    def show_text(self,text, clr = [255,255,255], font = "Arial", fonsize = 60 , x = None, y = None ):
        f = pg.font.SysFont(font, fonsize) 
        ren = f.render(text, 1, clr)
        rect = ren.get_rect()
        rect.center = (x,y)

        self.screen.blit(ren, rect.center)

    def screen_convert(self): #pygame畫面轉opencv格式  
        pg_cv = cv2.cvtColor(pg.surfarray.array3d(pg.display.get_surface().convert()), cv2.COLOR_RGB2BGR)#pygame畫面轉opencv格式
        pg_cv = cv2.flip(pg_cv, 1) #水平翻轉
        pg_cv = np.rot90(pg_cv) #向左轉
        self.pg_cv = pg_cv
    
    def th(self):        
        self.thread_ = threading.Thread(target = self.start_end_screen, args=('start',)) #target = self.play
        self.thread_.start()


    def start_end_screen(self,se):
        self.bg = pg.transform.scale(pg.image.load('Brick_data/img/bg.png'), (self.w, self.h))

        while 1:
            # self.mouse_pos = pg.mouse.get_pos() #!=====滑鼠操作時=====
            self.screen.blit(self.bg, (0, 0)) 
            self.screen.blit(pg.transform.scale(pg.image.load('Fruit_data/刀.png'),(30,30)), self.mouse_pos)#更新刀的位置
            dic = {'start':["Start Screen" ,'Play' ] , 'end':["Game Over",'Again']}
            self.show_text(dic[se][0],fonsize = 90, x=120,y = 25 )#標題
            se_btn   = Button(self.screen,  dic[se][1], x = 170, y = 200) #開始or再一次 按鈕
            quit_btn = Button(self.screen,  "Quit"    , x = 420, y = 200)#離開 按鈕
            self.screen_convert()


            if se_btn.pressed(self.mouse_pos):
                self.play()

            if quit_btn.pressed(self.mouse_pos):
                self.quit = True
                # break
                exit()
                


    def collide(self,ball, board):
        if (board.rect.left < ball.rect.center[0] and 
            ball.rect.center[0] < board.rect.right and 
            board.rect.top < ball.rect.center[1] and  
            ball.rect.center[1]< board.rect.bottom):
            return True
   



    def play(self):

        
        all_sprite = pg.sprite.Group()  # 建立所有角色群組
        brick_Group = pg.sprite.Group() # 建立磚塊群組
        skill_Group = pg.sprite.Group() # 建立技能群組

        w , h =27.5, 13
        for r in range(10):
            for c in range(15):
                brick = Brick(w , h , random.randint(1,1))#設定磚塊顏色.長.寬
                brick.set_pos(x = 8 + c * (w + 15), y = 4 + r * (h + 15))#設定位置 
                brick_Group.add(brick) # 加入磚塊群組
                all_sprite.add(brick) # 加入所有角色群組
        pad = Pad(self.screen)
        ball = Ball(self.screen)
        all_sprite.add(ball)


        #背景
        playbg = pg.Surface((self.w, self.h))
        playbg = playbg.convert()
        playbg.fill((255,255,255))
        

        #音效
        bricksou = pg.mixer.Sound("Brick_data/sound/brick.mp3")  
        skillsou = pg.mixer.Sound('Brick_data/sound/skill.wav')
        padsou   = pg.mixer.Sound("Brick_data/sound/pad.mp3")
        failsou  = pg.mixer.Sound("Brick_data/sound/fail.mp3")
        winsou   = pg.mixer.Sound("Brick_data/sound/win.mp3")
        bricksou.set_volume(0.4)
        skillsou.set_volume(0.2)
        padsou.set_volume(0.2)
        failsou.set_volume(0.2)
        winsou.set_volume(0.2)

        skll_prob = 30 #以多少機率產生技能

    
        while 1:  
            # self.mouse_pos = pg.mouse.get_pos()#!=====滑鼠操作時=====
            

            
            #! 檢查球是否掉出下邊界
            if  ball.update():#掉出下邊界
                failsou.play()
                self.start_end_screen('end')
                
            #! 檢查球和磚塊碰撞
            bhb = pg.sprite.spritecollide(ball, brick_Group , False)  #ball hit brick
            if len(bhb) > 0:
                bricksou.play()    #撞磚塊聲
                for brick in bhb:#取得碰撞到的每一個磚塊
                    brick.Type()
                    #產生技能
                    if  random.choice([1] * skll_prob + [0]*(100-skll_prob)):#
                        skill = Skill(self.screen,brick.rect.bottomleft)#產生技能(技能的左上角pos為磚塊的左下角pos)
                        skill_Group.add(skill)
                        all_sprite.add(skill)
                    ball.bounceup()
        
                #! 檢查磚塊是否都消失了
                if (False not in [ i not in [b.tp for b in brick_Group] for i in [1,2]]):
                    winsou.play()
                    self.start_end_screen('end')

            #! 檢查技能和滑板碰撞
            shp = pg.sprite.spritecollide(pad, skill_Group, True) #skill hit pad
            if len(shp) > 0:#技能和滑板發生碰撞 
                for s in shp:#遍歷每個技能
                    skillsou.play()
                    s.skill(ball, pad)#做出技能對應的動作
            
            #! 檢查球和滑板碰撞
            if pg.sprite.collide_rect(ball, pad) :  #球和滑板發生碰撞  #pg.sprite.collide_rect
                padsou.play()
                ball.rect.bottom = pad.rect.top
                ball.bounceup()


            self.screen.blit(playbg, (0,0))  #清除繪圖視窗
            all_sprite.update()#使用所有腳色(磚塊,球,技能)UPDATE方法
            all_sprite.draw(self.screen)#繪製所有角色(磚塊,球,技能)
            pad.pos = self.mouse_pos
            pad.update()
            pad.draw()      
            pg.display.update()#更新畫面
            pg.time.Clock().tick(15) #fps
            self.screen_convert()
        
        




