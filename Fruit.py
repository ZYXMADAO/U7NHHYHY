import pygame as pg,  os, random, threading, cv2, numpy as np
os.chdir(os.path.dirname(os.path.abspath(__file__)))#目前py檔路徑



class Button(pg.sprite.Sprite):
    def __init__(self, screen,title, clr = [255,255,255], font = "Arial", fonsize =60 , x = None, y = None ):
        super().__init__()
        self.screen = screen
        self.surface = pg.font.SysFont(font,fonsize).render(title, 1, clr)

        self.WIDTH = self.surface.get_width()
        self.HEIGHT = self.surface.get_height()
        
        self.x = x
        self.y = y

        self.screen.blit(self.surface  , (self.x,self.y))
        pg.display.update()

    def pressed(self,pos):
        if (pos[0] > self.x ) and (pos[1] > self.y ) and (pos[0] < self.x+self.WIDTH  ) and (pos[1] < self.y+self.HEIGHT) : #滑鼠座標在按鈕內
            return True
        else:#滑鼠座標不在按鈕內
            return False
        

class ThrowFruit(pg.sprite.Sprite): 
    def __init__(self,screen,path,flag):
        super().__init__()
        self.screen = screen

        self.image = pg.transform.scale(pg.image.load(path), (75, 75))

        self.rect = self.image.get_rect()
        self.rect.x = random.randint(0, self.screen.get_width())
        
        self.rect.y = self.screen.get_height()

        self.speed_x = random.randint(-15, 15)
        self.speed_y = random.randint(-30, -20)
        self.t = 0
        self.flag = flag
        


    def update(self):
        self.rect.x += self.speed_x
        self.rect.y += self.speed_y
        self.speed_y += (0.15 * self.t) #隨時間經過y位移加快(往上)
        self.t += 1 

        if self.rect.y >= self.screen.get_height() + self.rect.height: #掉落到下邊界
            self.kill()


class Main(object):
    def __init__(self):
        pg.init()#初始化
        self.WIDTH = 640
        self.HEIGHT = 480
        self.SCREEN = pg.display.set_mode((self.WIDTH, self.HEIGHT)) # 固定視窗大小
        self.mouse_pos = (0,0)
        self.score =  0
        self.quit = True #離開(true) 表示未啟用
        self.screen_convert()

    
    def create_fruit(self,bomb_prob, fruit_prob):
        if round(random.random(), 3) <= bomb_prob:#炸彈生成機率
            boom = ThrowFruit(self.SCREEN,"Fruit_data/炸彈.png",-1)
            self.fruit_list.add(boom)

        if round(random.random(), 3) <= fruit_prob:#水果生成機率
            fruit_names = ['西瓜','蘋果','香蕉']
            fruit_number = random.randint(1, len(fruit_names)) #一次丟出幾個
            for i in range(fruit_number):
                fruit_index = random.randint(0,len(fruit_names)-1)
                fruit = ThrowFruit(self.SCREEN,'Fruit_data/'+fruit_names[fruit_index] + ".png",fruit_index)
                self.fruit_list.add(fruit)
                

    def show_text(self, text, fontsize = 60, x = None, y = None):
        f = pg.font.SysFont("Arial", fontsize) 
        ren = f.render(text, 1, [255,255,255])    
        self.SCREEN.blit(ren, (x,y))

    def screen_convert(self): #pygame畫面轉opencv格式  
        pg_cv = cv2.cvtColor(pg.surfarray.array3d(pg.display.get_surface().convert()), cv2.COLOR_RGB2BGR)#pygame畫面轉opencv格式
        pg_cv = cv2.flip(pg_cv, 1) #水平翻轉
        pg_cv = np.rot90(pg_cv) #向左轉
        self.pg_cv = pg_cv
            
    def th(self):        
        self.thread_ = threading.Thread(target = self.start_end_screen, args=('start',))
        self.thread_.start()


       
        

    def start_end_screen(self,S_E): #! 開始結束畫面
        self.background = pg.transform.scale(pg.image.load('Fruit_data/背景.jpg'), (self.WIDTH, self.HEIGHT)) #變更圖片大小成視窗大小

        while 1:
            self.SCREEN.blit(self.background, (0,0))
            self.SCREEN.blit(pg.transform.scale(pg.image.load('Fruit_data/刀.png'),(30,30)), self.mouse_pos)#更新刀的位置
            dic = {'start':["Start Screen" ,'Play' ] , 'end':["Game Over",'Again']}
            self.show_text(dic[S_E][0], fontsize = 80, x=130,y = 25 )#標題
            se_btn   = Button(self.SCREEN, dic[S_E][1], x = 150, y = 300) #開始or再一次 按鈕
            quit_btn = Button(self.SCREEN, "Quit"     , x = 400, y = 300)#離開 按鈕
            if S_E =='end':#結束遊戲
                self.show_text("Score : " + str(self.score ), fontsize =50, x = 225, y=200)#成績
            self.screen_convert()



            if se_btn.pressed(self.mouse_pos):
                self.play()

            if quit_btn.pressed(self.mouse_pos):
                self.quit = True
                # break
                exit()




                    


    def collision_detection(self): #! 碰撞檢測
        self.create_fruit(0.01,0.03) #建立水果
        self.fruit_list.update()#路徑變數更新
        self.fruit_list.draw(self.SCREEN)#路徑顯示
        self.SCREEN.blit(pg.transform.scale(pg.image.load('Fruit_data/刀.png'),(30,30)), self.mouse_pos)#更新刀的位置

        for item in self.fruit_list:
            if (self.mouse_pos[0] > item.rect.left and self.mouse_pos[0] < item.rect.right and 
                self.mouse_pos[1] > item.rect.top  and self.mouse_pos[1] < item.rect.bottom   ): 
                self.fruit_list.remove_internal(item) #將切到的水果從精靈組中刪除

                if item.flag == -1 : #切到炸彈
                    killsound = pg.mixer.Sound('Fruit_data/bomb.mp3')
                    killsound.set_volume(0.2)
                    killsound.play()
                    self.fruit_list = pg.sprite.Group()#清空
                    self.start_end_screen('end')


                else:
                    killsound = pg.mixer.Sound('Fruit_data/cut.mp3')
                    killsound.set_volume(0.3)
                    killsound.play()
                    self.score += 1
    
    
    def play(self): #! 遊戲執行時
        self.score = 0
        self.fruit_list = pg.sprite.Group()
        pg.mouse.set_visible(False) #隱藏滑鼠
        
        while 1:
            # self.mouse_pos = pg.mouse.get_pos()
            self.SCREEN.blit(self.background, (0, 0)) #更新背景
            self.show_text('Score: ' + str(self.score),fontsize = 42 , x=0, y=0)
            self.collision_detection() 
            pg.display.update()
            pg.time.Clock().tick(30)
            self.screen_convert()



