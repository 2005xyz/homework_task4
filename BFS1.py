import pygame, sys, random, time
from pygame.locals import *

# ==================== 初始化部分 ====================

# 初始化Pygame库
pygame.init()

# 初始化游戏窗口，大小为300x300像素
DISPLAY = pygame.display.set_mode((300, 300))

# 设置游戏窗口标题
pygame.display.set_caption('贪吃蛇')

# 定义游戏帧率控制对象，用于控制蛇移动速度
FPSCLOCK = pygame.time.Clock()

# 初始化字体，用于显示文字信息（这里使用两种字体）
BASICFONT = pygame.font.SysFont("SIMYOU.TTF", 80)
font = pygame.font.SysFont('simsunnsimsun', 80)

# ==================== 定义颜色 ====================
BLACK = pygame.Color(0, 0, 0)           # 背景黑色
WHITE = pygame.Color(255, 255, 255)     # 白色（可用于显示文字或界面背景）
RED = pygame.Color(255, 0, 0)           # 食物红色
GREY = pygame.Color(150, 150, 150)      # 游戏结束提示文字灰色
GREEN = pygame.Color(0, 255, 255)       # 蛇尾亮绿色
YELLOW = pygame.Color(255, 255, 0)
FORESTGREEN = pygame.Color(34, 139, 34) # 蛇身体绿色
Purple3 = pygame.Color(125, 38, 205)    # 蛇头紫色

# ==================== 贪吃蛇初始状态 ====================

# 蛇头初始坐标
snake_Head = [100, 100]

# 蛇身初始坐标（蛇头在最前面，蛇身按顺序排列）
snake_Body = [[80, 100], [60, 100], [40, 100]]

# 初始移动方向向右
direction = "RIGHT"

# ==================== 食物生成 ====================

def randomfood(snake_Body):
    """
    随机生成食物位置，确保不会生成在蛇身上
    参数：
        snake_Body: 当前蛇身坐标列表
    返回：
        食物坐标列表 [x, y]
    """
    x = random.randrange(1, 15)
    y = random.randrange(1, 15)
    Position = [int(x * 20), int(y * 20)]  # 将格子转换为像素坐标
    # 如果生成的位置与蛇身重合，重新生成
    while Position in snake_Body:
        x = random.randrange(1, 15)
        y = random.randrange(1, 15)
        Position = [int(x * 20), int(y * 20)]
    return Position

# 随机生成第一个食物
food_Position = randomfood(snake_Body)
food_flag = 1

# ==================== 游戏结束 ====================

def GameOver():
    """
    游戏结束函数，根据蛇长度给出评价并退出游戏
    """
    # 根据蛇长度判断玩家水平
    if (len(snake_Body) - 3) <= 10:
        GameOver_Surf = font.render('太菜了', True, GREY)
    elif 10 <= (len(snake_Body) - 3) <= 20:
        GameOver_Surf = font.render('一般般', True, GREY)
    else:
        GameOver_Surf = font.render('很棒！', True, GREY)

    # 设置文字显示位置
    GameOver_Rect = GameOver_Surf.get_rect()
    GameOver_Rect.midtop = (320, 200)  # 文字居中显示
    DISPLAY.blit(GameOver_Surf, GameOver_Rect)
    pygame.display.flip()
    time.sleep(3)  # 显示3秒
    pygame.quit()
    sys.exit()

# ==================== 辅助路径函数 ====================

def walkable(location0, snake_body0):
    """
    返回蛇头可走的四个方向中的安全位置（不碰撞边界或蛇身）
    参数：
        location0: 蛇头当前坐标 [x, y]
        snake_body0: 当前蛇身列表
    返回：
        安全可走的坐标列表
    """
    l = []
    # 右移动
    if location0[0] + 20 < 300 and [location0[0] + 20, location0[1]] not in snake_body0:
        l.append([location0[0] + 20, location0[1]])
    # 左移动
    if location0[0] - 20 >= 0 and [location0[0] - 20, location0[1]] not in snake_body0:
        l.append([location0[0] - 20, location0[1]])
    # 下移动
    if location0[1] + 20 < 300 and [location0[0], location0[1] + 20] not in snake_body0:
        l.append([location0[0], location0[1] + 20])
    # 上移动
    if location0[1] - 20 >= 0 and [location0[0], location0[1] - 20] not in snake_body0:
        l.append([location0[0], location0[1] - 20])
    return l

def changexy(position0):
    """
    将二维坐标转换为一维，用于BFS访问记录
    """
    position = position0.copy()
    return position[1] * 15 + position[0]

# ==================== 广度优先搜索 ====================

def BFS(food_position0, snake_body0):
    """
    广度优先搜索路径，找到从蛇头到食物的最短路径
    参数：
        food_position0: 食物坐标
        snake_body0: 当前蛇身
    返回：
        path: 从蛇头到食物的路径列表
        flag: 是否找到路径，1为找到，0为未找到
    """
    food_position = food_position0.copy()
    snake_body = snake_body0.copy()
    flag = 0
    path = []
    search_stack = []
    visited_dict = {}

    # 将蛇头加入搜索队列并标记访问过
    search_stack.append([snake_body[0][0], snake_body[0][1]])
    visited_dict[changexy([snake_body[0][0], snake_body[0][1]])] = -1

    # BFS搜索
    while len(search_stack) > 0:
        currentlocation = search_stack.pop(0)
        if currentlocation != food_position:
            l1 = walkable(currentlocation, snake_body)
            for i in l1:
                if visited_dict.get(changexy(i)) == None:
                    search_stack.append(i)
                    visited_dict[changexy(i)] = currentlocation
        else:
            flag = 1  # 找到食物
            break

    # 回溯路径
    path.append(currentlocation)
    while visited_dict[changexy(currentlocation)] != -1:
        currentlocation = visited_dict[changexy(currentlocation)]
        path.append(currentlocation)
    path.reverse()  # 路径从蛇头到食物

    return path, flag

def tailBFS(tail_position0, snake_body0):
    """
    BFS搜索蛇尾路径，判断蛇吃完食物后是否能继续移动
    """
    tail_position = tail_position0.copy()
    snake_body = snake_body0.copy()
    flag = 0
    search_stack = []
    visited_dict = {}

    # 将蛇头加入搜索栈并标记访问
    search_stack.append([snake_body[0][0], snake_body[0][1]])
    visited_dict[changexy([snake_body[0][0], snake_body[0][1]])] = -1

    # BFS搜索到蛇尾
    while len(search_stack) > 0:
        currentlocation = search_stack.pop(0)
        if currentlocation != tail_position:
            tail = snake_body.pop()  # 暂时去掉尾巴，防止误判
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

# ==================== 蛇行走策略 ====================

def exploretheway(food_position0, snake_body0):
    """
    虚拟蛇模拟吃到食物后的路径，判断吃完后是否安全
    """
    snake_body = snake_body0.copy()
    food_position = food_position0.copy()
    while True:
        path, flag1 = BFS(food_position, snake_body)
        # 虚拟移动蛇头
        snake_body.insert(0, path[1])
        # 吃到食物则停止
        if snake_body[0][0] == food_position[0] and snake_body[0][1] == food_position[1]:
            flag2 = tailBFS(snake_body[-1], snake_body)  # 判断是否安全
            break
        else:
            snake_body.pop()
    return flag2

def longest_tail_path(snake_body0):
    """
    当直接吃食物不安全时，沿最长路径向蛇尾走一步
    """
    snake_body = snake_body0.copy()
    tail = snake_body.pop()  # 暂时移除尾巴
    l0 = walkable(snake_body[0], snake_body)  # 可走路径
    snake_body.append(tail)
    longest = -1

    # 遍历每个可走方向，寻找最长路径
    for i0 in l0:
        flag = 0
        path = []
        search_stack = []
        visited_dict = {}

        search_stack.append(i0)
        visited_dict[changexy(i0)] = -1

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

        # 回溯路径
        path.append(currentlocation)
        while visited_dict[changexy(currentlocation)] != -1:
            currentlocation = visited_dict[changexy(currentlocation)]
            path.append(currentlocation)
        path.reverse()

        if flag == 1 and len(path) > longest:
            longest = len(path)
            longest_path = path
    return longest_path

def wander(snake_body0):
    """
    随机走一步，当没有安全路径时使用
    """
    l = walkable(snake_body0[0], snake_body0)
    if len(l) > 1:
        x = random.randrange(0, len(l))
    elif len(l) == 1:
        x = 0
    else:
        return l
    return l[x]

# ==================== 绘图函数 ====================

def drawSnake(snake_body0):
    """
    绘制蛇
    蛇头紫色，身体绿色，尾巴亮绿色
    """
    pygame.draw.rect(DISPLAY, Purple3, Rect(snake_body0[0][0], snake_body0[0][1], 20, 20))
    for j in range(1, len(snake_body0)-1):
       pygame.draw.rect(DISPLAY, FORESTGREEN, Rect(snake_body0[j][0], snake_body0[j][1], 20, 20))
    pygame.draw.rect(DISPLAY, GREEN, Rect(snake_body0[-1][0], snake_body0[-1][1], 20, 20))

def drawFood(food_position0):
    """
    绘制食物
    """
    pygame.draw.rect(DISPLAY, RED, Rect(food_position0[0], food_position0[1], 20, 20))

# ==================== 游戏主循环 ====================

while True:
    # BFS搜索食物路径和尾巴路径
    food_path, food_flag = BFS(food_Position, snake_Body)
    tail_flag = tailBFS(snake_Body[-1], snake_Body)

    # 情况1：可以找到食物路径
    if food_flag == 1:
        virtual_tail_flag = exploretheway(food_Position, snake_Body)
        if virtual_tail_flag == 1:
            # 安全则沿最短路径向食物移动
            snake_Body.insert(0, food_path[1])
            if snake_Body[0][0] == food_Position[0] and snake_Body[0][1] == food_Position[1]:
                food_Position = randomfood(snake_Body)
            else:
                snake_Body.pop()
        else:
            # 吃食物不安全，则沿最长路径向蛇尾移动
            longest_path = longest_tail_path(snake_Body)
            snake_Body.insert(0, longest_path[0])
            if snake_Body[0][0] == food_Position[0] and snake_Body[0][1] == food_Position[1]:
                food_Position = randomfood(snake_Body)
            else:
                snake_Body.pop()

    # 情况2：找不到食物路径，但能找到尾巴路径
    elif tail_flag == 1:
        longest_path = longest_tail_path(snake_Body)
        snake_Body.insert(0, longest_path[0])
        snake_Body.pop()

    # 情况3：找不到食物路径也找不到尾巴路径
    elif food_flag != 1 and tail_flag != 1:
        if len(wander(snake_Body)) == 0:
            GameOver()
            break
        else:
            snake_Body.insert(0, wander(snake_Body))
            snake_Body.pop()

    # 绘制游戏界面
    DISPLAY.fill(BLACK)      # 背景填黑
    drawSnake(snake_Body)    # 绘制蛇
    drawFood(food_Position)  # 绘制食物
    pygame.display.flip()

    # 控制游戏速度
    FPSCLOCK.tick(20)

    # 游戏失败判定：撞墙或咬到自己
    if snake_Body[0][0] < 0 or snake_Body[0][0] >= 300:
        GameOver()
    if snake_Body[0][1] < 0 or snake_Body[0][1] >= 300:
        GameOver()
    for i in snake_Body[1:]:
        if snake_Body[0][0] == i[0] and snake_Body[0][1] == i[1]:
            GameOver()
