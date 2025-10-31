'''
  贪吃蛇：蛇头紫色，蛇尾蓝色，蛇身绿色。
  注意：当程序运行到最后时，蛇头会一直追着蛇尾跑而无法退出，所以需要手动退出。
'''

# BFS 自动寻路算法位于文件第111行

# ===== 模块导入 =====
import pygame, sys, random, time
from pygame.locals import *

# ===== 游戏初始化 =====
# 初始化Pygame库
pygame.init()

# 初始化一个游戏界面窗口
DISPLAY = pygame.display.set_mode((300, 300))

# 设置游戏窗口的标题
pygame.display.set_caption('贪吃蛇')

# 定义一个变量来控制游戏速度
FPSCLOCK = pygame.time.Clock()

# 初始化游戏界面内使用的字体
BASICFONT = pygame.font.SysFont("SIMYOU.TTF", 80)
font = pygame.font.SysFont('simsunnsimsun', 80)

# ===== 颜色常量定义 =====
BLACK = pygame.Color(0, 0, 0)
WHITE = pygame.Color(255, 255, 255)
RED = pygame.Color(255, 0, 0)
GREY = pygame.Color(150, 150, 150)
GREEN = pygame.Color(0, 255, 255)
YELLOW = pygame.Color(255, 255, 0)
FORESTGREEN = pygame.Color(34, 139, 34)
Purple3 = pygame.Color(125, 38, 205)

# ===== 游戏状态初始化 =====
# 贪吃蛇的的初始位置
snake_Head = [100, 100]

# 初始化贪吃蛇的长度 (注：这里以20*20为一个标准小格子)
snake_Body = [[80, 100], [60, 100], [40, 100]]

# 指定蛇初始前进的方向，向右
direction = "RIGHT"

# ===== 功能函数定义 =====

# 随机生成食物
def randomfood(snake_Body):
    # 随机生成x, y
    x = random.randrange(1, 15)
    y = random.randrange(1, 15)
    Position = [int(x * 20), int(y * 20)]
    # 确保食物不出现在蛇身上
    while Position in snake_Body:
        x = random.randrange(1, 15)
        y = random.randrange(1, 15)
        Position = [int(x * 20), int(y * 20)]
    return Position

# 随机出现第一个食物
food_Position = randomfood(snake_Body)
food_flag = 1

# 游戏结束函数
def GameOver():
    # 根据得分显示不同评价
    if (len(snake_Body) - 3) <= 10:
        GameOver_Surf = font.render('太菜了', True, GREY)
    elif 10 <= (len(snake_Body) - 3) <= 20:
        GameOver_Surf = font.render('一般般', True, GREY)
    else:
        GameOver_Surf = font.render('很棒！', True, GREY)

    # 设置GameOver的位置
    GameOver_Rect = GameOver_Surf.get_rect()
    GameOver_Rect.midtop = (320, 200)

    # 绑定以上设置到句柄
    DISPLAY.blit(GameOver_Surf, GameOver_Rect)
    pygame.display.flip()

    # 等待3秒
    time.sleep(3)

    # 退出游戏
    pygame.quit()
    # 退出程序
    sys.exit()

# 获取可以行走的位置
def walkable(location0, snake_body0):
    l = []
    # 检查四个方向的可行性
    if location0[0] + 20 < 300 and [location0[0] + 20, location0[1]] not in snake_body0:
        l.append([location0[0] + 20, location0[1]])

    if location0[0] - 20 >= 0 and [location0[0] - 20, location0[1]] not in snake_body0:
        l.append([location0[0] - 20, location0[1]])

    if location0[1] + 20 < 300 and [location0[0], location0[1] + 20] not in snake_body0:
        l.append([location0[0], location0[1] + 20])

    if location0[1] - 20 >= 0 and [location0[0], location0[1] - 20] not in snake_body0:
        l.append([location0[0], location0[1] - 20])

    return l

# 坐标转换函数
def changexy(position0):
    position = position0.copy()
    return position[1] * 15 + position[0]

# ===== 路径搜索算法 =====

# 广度优先搜索 - 寻找食物路径
def BFS(food_position0, snake_body0):
    food_position = food_position0.copy()
    snake_body = snake_body0.copy()
    flag = 0
    path = []
    search_stack = []
    visited_dict = {}

    # 初始化搜索栈和访问字典
    search_stack.append([snake_body[0][0], snake_body[0][1]])
    visited_dict[changexy([snake_body[0][0], snake_body[0][1]])] = -1

    # BFS搜索循环
    while len(search_stack) > 0:
        currentlocation = search_stack.pop(0)  # 初始时currentlocation为食物坐标

        if currentlocation != food_position:
            l1 = walkable(currentlocation, snake_body)
            # 遍历所有可行走方向
            for i in l1:
                if visited_dict.get(changexy(i)) == None:
                    search_stack.append(i)
                    visited_dict[changexy(i)] = currentlocation
        else:
            flag = 1
            break

    # 构建路径
    path.append(currentlocation)
    while visited_dict[changexy(currentlocation)] != -1:
        currentlocation = visited_dict[changexy(currentlocation)]
        path.append(currentlocation)
    path.reverse()

    return path, flag

# 广度优先搜索 - 寻找蛇尾路径
def tailBFS(tail_position0, snake_body0):
    tail_position = tail_position0.copy()
    snake_body = snake_body0.copy()
    flag = 0
    path = []
    search_stack = []
    visited_dict = {}

    search_stack.append([snake_body[0][0], snake_body[0][1]])
    visited_dict[changexy([snake_body[0][0], snake_body[0][1]])] = -1

    # BFS搜索循环
    while len(search_stack) > 0:
        currentlocation = search_stack.pop(0)
        if currentlocation != tail_position:
            # 临时移除蛇尾以计算可行走路径
            tail = snake_body.pop()
            l1 = walkable(currentlocation, snake_body)
            snake_body.append(tail)

            for i1 in l1:
                if visited_dict.get(changexy(i1)) == None:
                    search_stack.append(i1)
                    visited_dict[changexy(i1)] = currentlocation
        else:
            flag = 1
            break

    return flag

# 寻找安全路径吃食物
def exploretheway(food_position0, snake_body0):
    snake_body = snake_body0.copy()
    food_position = food_position0.copy()

    # 虚拟蛇模拟吃食物过程
    while True:
        path, flag1 = BFS(food_position, snake_body)
        snake_body.insert(0, path[1])

        if snake_body[0][0] == food_position[0] and snake_body[0][1] == food_position[1]:
            flag2 = tailBFS(snake_body[-1], snake_body)
            break
        else:
            snake_body.pop()
    return flag2

# 真实的蛇沿最长路径向蛇尾走一步
def longest_tail_path(snake_body0):
    snake_body = snake_body0.copy()
    tail = snake_body.pop()
    l0 = walkable(snake_body[0], snake_body)
    snake_body.append(tail)
    longest = -1

    # 遍历所有可行走方向，寻找最长路径
    for i0 in l0:
        flag = 0
        path = []
        search_stack = []
        visited_dict = {}

        search_stack.append(i0)
        visited_dict[changexy(i0)] = -1

        # BFS搜索最长路径
        while len(search_stack) > 0:
            currentlocation = search_stack.pop(0)
            if currentlocation != snake_body[-1]:
                tail = snake_body.pop()
                l1 = walkable(currentlocation, snake_body)
                snake_body.append(tail)
                for j in l1:
                    if visited_dict.get(changexy(j)) == None:
                        search_stack.append(j)
                        visited_dict[changexy(j)] = currentlocation
            else:
                flag = 1
                break

        # 构建路径
        path.append(currentlocation)
        while visited_dict[changexy(currentlocation)] != -1:
            currentlocation = visited_dict[changexy(currentlocation)]
            path.append(currentlocation)
        path.reverse()

        # 更新最长路径
        if flag == 1:
            if len(path) > longest:
                longest = len(path)
                longest_path = path
    return longest_path

# 漫步函数，随机选择蛇头周围四个方向中可走的方向走一步
def wander(snake_body0):
    l = walkable(snake_body0[0], snake_body0)
    if len(l) > 1:
        x = random.randrange(0, len(l))
    elif len(l) == 1:
        x = 0
    else:
        return l
    return l[x]

# ===== 图形绘制函数 =====

# 画出蛇的位置
def drawSnake(snake_body0):
    # 蛇头紫色
    pygame.draw.rect(DISPLAY, Purple3, Rect(snake_body0[0][0], snake_body0[0][1], 20, 20))
    # 蛇身绿色
    for j in range(1, len(snake_body0)-1):
       pygame.draw.rect(DISPLAY, FORESTGREEN, Rect(snake_body0[j][0], snake_body0[j][1], 20, 20))
    # 蛇尾蓝色
    pygame.draw.rect(DISPLAY, GREEN, Rect(snake_body0[-1][0], snake_body0[-1][1], 20, 20))

# 画出食物的位置
def drawFood(food_position0):
    pygame.draw.rect(DISPLAY, RED, Rect(food_position0[0], food_position0[1], 20, 20))

# 设置得分机制
def drawScore(score):
    # 设置分数的显示颜色
    score_Surf = BASICFONT.render('%s' % (score), True, GREY)
    # 设置分数的位置
    score_Rect = score_Surf.get_rect()
    score_Rect.midtop = (50, 20)
    # 绑定以上设置到句柄
    DISPLAY.blit(score_Surf, score_Rect)

# ===== 主游戏循环 =====
########################################################################################
while True:
    # ===== 路径搜索逻辑 =====
    food_path, food_flag = BFS(food_Position, snake_Body)
    tail_flag = tailBFS(snake_Body[-1], snake_Body)

    # 情况1：当前布局能找到食物路径
    if food_flag == 1:
        virtual_tail_flag = exploretheway(food_Position, snake_Body)

        # 情况1.1：虚拟蛇吃完食物后找得到蛇尾路径
        if virtual_tail_flag == 1:
            # 真实的蛇沿最短路径向食物走一步
            snake_Body.insert(0, food_path[1])
            if snake_Body[0][0] == food_Position[0] and snake_Body[0][1] == food_Position[1]:
                food_Position = randomfood(snake_Body)
            else:
                snake_Body.pop()

        # 情况1.2：虚拟蛇吃完食物后找不到蛇尾路径
        else:
            # 真实的蛇沿最长路径向蛇尾走一步
            longest_path = longest_tail_path(snake_Body)
            snake_Body.insert(0, longest_path[0])
            if snake_Body[0][0] == food_Position[0] and snake_Body[0][1] == food_Position[1]:
                food_Position = randomfood(snake_Body)
            else:
                snake_Body.pop()

    # 情况2：当前布局能找到蛇尾路径（找不到食物路径）
    elif tail_flag == 1:
        # 真实的蛇沿最长路径向蛇尾走一步
        longest_path = longest_tail_path(snake_Body)
        snake_Body.insert(0, longest_path[0])
        snake_Body.pop()

    # 情况3：找不到食物路径也找不到蛇尾路径时，随机走一步
    elif food_flag != 1 and tail_flag != 1:
        if len(wander(snake_Body)) == 0:
            GameOver()
            break
        else:
            snake_Body.insert(0, wander(snake_Body))
            snake_Body.pop()

    # ===== 图形渲染 =====
    DISPLAY.fill(BLACK)
    # 画出贪吃蛇
    drawSnake(snake_Body)
    # 画出食物的位置
    drawFood(food_Position)
    # 打印出玩家的分数
    drawScore(len(snake_Body) - 3)
    # 刷新Pygame的显示层
    pygame.display.flip()
    # 控制游戏速度
    FPSCLOCK.tick(20)

    # ===== 碰撞检测 =====
    # 检测是否撞墙
    if snake_Body[0][0] < 0 or snake_Body[0][0] > 300:
        GameOver()
    if snake_Body[0][1] < 0 or snake_Body[0][1] > 300:
        GameOver()

    # 检测贪吃蛇是否触碰到自己
    for i in snake_Body[1:]:
        if snake_Body[0][0] == i[0] and snake_Body[0][1] == i[1]:
            GameOver()