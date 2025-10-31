import math
from random import randint
import pygame
from enum import Enum

# ===========================
# 全局变量设置
# ===========================
CELL_WIDTH = 16   # 地图中每个单元格的宽度（像素）
CELL_HEIGHT = 16  # 地图中每个单元格的高度（像素）
BORDER_WIDTH = 1  # 单元格边框宽度（像素）
BLOCK_NUM = 50    # 随机生成的障碍物数量

# ===========================
# 定义颜色枚举类
# ===========================
class Color(Enum):
    RED = (255, 0, 0)       # 红色，用于终点或路径显示
    GREEN = (0, 255, 0)     # 绿色，用于普通可通行单元格
    BLUE = (0, 0, 255)      # 蓝色，用于起点显示
    WHITE = (255, 255, 255) # 白色，用作背景颜色
    BLACK = (0, 0, 0)       # 黑色，用于障碍物显示

    @staticmethod
    def random_color():
        """ 返回随机颜色，用于其他可扩展功能 """
        r = randint(0, 255)
        g = randint(0, 255)
        b = randint(0, 255)
        return (r, g, b)

# ===========================
# 地图类
# ===========================
class Map(object):
    """ 地图类，用于生成地图的单元格坐标 """
    def __init__(self, mapsize):
        """
        :param mapsize: 地图大小 (宽, 高)，单位为单元格
        """
        self.mapsize = mapsize

    def generate_cell(self, cell_width, cell_height):
        """
        生成器函数，逐个生成地图中每个单元格的左上角坐标
        :param cell_width: 单元格宽度（像素）
        :param cell_height: 单元格高度（像素）
        :return: 单元格左上角坐标 (x, y)
        """
        x_cell = -cell_width
        for num_x in range(self.mapsize[0] // cell_width):
            y_cell = -cell_height
            x_cell += cell_width
            for num_y in range(self.mapsize[1] // cell_height):
                y_cell += cell_height
                yield (x_cell, y_cell)  # 生成单元格左上角坐标

# ===========================
# 节点类
# ===========================
class Node(object):
    """ 节点类，用于存储每个地图节点的信息 """
    def __init__(self, pos):
        self.pos = pos        # 节点坐标 (x, y)
        self.father = None    # 父节点，用于回溯最短路径
        self.gvalue = 0       # 起点到当前节点的实际代价（累积代价）
        self.fvalue = 0       # f值 = g值 + h值

    def compute_fx(self, enode, father):
        """
        计算节点的 g 值和 f 值
        :param enode: 终点节点
        :param father: 父节点
        :return: g值, f值
        """
        if father is None:
            print('未设置当前节点的父节点！')

        # 父节点到起点的代价
        gx_father = father.gvalue
        # 父节点到当前节点的距离（欧式距离）
        gx_f2n = math.sqrt((father.pos[0] - self.pos[0])**2 + (father.pos[1] - self.pos[1])**2)
        gvalue = gx_f2n + gx_father

        # 当前节点到终点的启发式距离（欧式距离）
        hx_n2enode = math.sqrt((self.pos[0] - enode.pos[0])**2 + (self.pos[1] - enode.pos[1])**2)
        fvalue = gvalue + hx_n2enode

        return gvalue, fvalue

    def set_fx(self, enode, father):
        """ 设置节点的 g 值、f 值，并记录父节点 """
        self.gvalue, self.fvalue = self.compute_fx(enode, father)
        self.father = father

    def update_fx(self, enode, father):
        """ 如果找到更优路径，则更新 g 值、f 值和父节点 """
        gvalue, fvalue = self.compute_fx(enode, father)
        if fvalue < self.fvalue:  # 如果新路径更优
            self.gvalue, self.fvalue = gvalue, fvalue
            self.father = father

# ===========================
# A*算法类
# ===========================
class AStar(object):
    """ A* 搜索算法实现类 """
    def __init__(self, mapsize, pos_sn, pos_en):
        self.mapsize = mapsize      # 地图大小 (宽, 高)
        self.openlist = []          # open列表，存放待扩展节点
        self.closelist = []         # close列表，存放已扩展节点
        self.blocklist = []         # 障碍物列表
        self.snode = Node(pos_sn)   # 起点节点
        self.enode = Node(pos_en)   # 终点节点
        self.cnode = self.snode     # 当前搜索节点

    def run(self):
        """ 执行 A* 搜索 """
        self.openlist.append(self.snode)

        while len(self.openlist) > 0:
            # 查找 openlist 中 f 值最小的节点
            fxlist = [node.fvalue for node in self.openlist]
            index_min = fxlist.index(min(fxlist))
            self.cnode = self.openlist[index_min]

            # 从 openlist 中移除当前节点，并加入 closelist
            del self.openlist[index_min]
            self.closelist.append(self.cnode)

            # 扩展当前节点的邻居
            self.extend(self.cnode)

            # 如果找到终点，结束搜索
            if self.cnode.pos == self.enode.pos:
                break

        # 返回搜索结果，1表示成功，-1表示失败
        if self.cnode.pos == self.enode.pos:
            self.enode.father = self.cnode.father
            return 1
        else:
            return -1

    def get_minroute(self):
        """ 获取最优路径 """
        minroute = []
        current_node = self.enode

        while True:
            minroute.append(current_node.pos)
            current_node = current_node.father
            if current_node.pos == self.snode.pos:
                break

        minroute.append(self.snode.pos)
        minroute.reverse()  # 从起点到终点
        return minroute

    def extend(self, cnode):
        """ 扩展当前节点的邻居节点 """
        nodes_neighbor = self.get_neighbor(cnode)

        for node in nodes_neighbor:
            # 如果邻居在 closelist 或障碍物列表中，跳过
            if node.pos in [n.pos for n in self.closelist] or node.pos in self.blocklist:
                continue
            # 如果邻居在 openlist 中，尝试更新更优路径
            if node.pos in [n.pos for n in self.openlist]:
                node.update_fx(self.enode, cnode)
            else:
                # 新邻居，设置 f 值并加入 openlist
                node.set_fx(self.enode, cnode)
                self.openlist.append(node)

    def setBlock(self, blocklist):
        """ 设置障碍物 """
        self.blocklist.extend(blocklist)

    def get_neighbor(self, cnode):
        """ 获取当前节点的8个方向邻居节点 """
        offsets = [(-1,1),(0,1),(1,1),(-1,0),(1,0),(-1,-1),(0,-1),(1,-1)]
        nodes_neighbor = []
        x, y = cnode.pos

        for os in offsets:
            x_new, y_new = x + os[0], y + os[1]
            # 判断新坐标是否在地图范围内
            if 0 <= x_new < self.mapsize[0] and 0 <= y_new < self.mapsize[1]:
                nodes_neighbor.append(Node((x_new, y_new)))

        return nodes_neighbor

# ===========================
# 主程序入口
# ===========================
def main():
    # 输入地图大小、起点、终点
    mapsize = tuple(map(int, input('请输入地图大小，以逗号隔开：').split(',')))
    pos_snode = tuple(map(int, input('请输入起点坐标，以逗号隔开：').split(',')))
    pos_enode = tuple(map(int, input('请输入终点坐标，以逗号隔开：').split(',')))

    myAstar = AStar(mapsize, pos_snode, pos_enode)

    # 随机生成障碍物
    blocklist = gen_blocks(mapsize[0], mapsize[1])
    myAstar.setBlock(blocklist)

    # 执行A*算法，获取路径
    routelist = []
    if myAstar.run() == 1:
        routelist = myAstar.get_minroute()
        print("最优路径：", routelist)
        showresult(mapsize, pos_snode, pos_enode, blocklist, routelist)
    else:
        print('路径规划失败！')

# ===========================
# 随机生成障碍物
# ===========================
def gen_blocks(width, height):
    """ 随机生成障碍物坐标 """
    i, blocklist = 0, []
    while i < BLOCK_NUM:
        block = (randint(0, width-1), randint(0, height-1))
        if block not in blocklist:  # 避免重复障碍物
            blocklist.append(block)
            i += 1
    return blocklist

# ===========================
# 可视化显示结果
# ===========================
def showresult(mapsize, pos_sn, pos_en, blocklist, routelist):
    """ 使用pygame可视化显示地图、障碍物、路径 """
    pygame.init()
    mymap = Map((mapsize[0]*CELL_WIDTH, mapsize[1]*CELL_HEIGHT))
    pix_sn = (pos_sn[0]*CELL_WIDTH, pos_sn[1]*CELL_HEIGHT)
    pix_en = (pos_en[0]*CELL_WIDTH, pos_en[1]*CELL_HEIGHT)

    # 将障碍物和路径转换为像素坐标
    bl_pix = list(map(transform, blocklist))
    rl_pix = list(map(transform, routelist))

    # 初始化窗口
    screen = pygame.display.set_mode(mymap.mapsize)
    pygame.display.set_caption('A*算法路径搜索演示：')
    screen.fill(Color.WHITE.value)  # 填充背景为白色

    # 绘制地图单元格
    for (x, y) in mymap.generate_cell(CELL_WIDTH, CELL_HEIGHT):
        if (x, y) in bl_pix:  # 障碍物单元格
            pygame.draw.rect(screen, Color.BLACK.value, ((x+BORDER_WIDTH, y+BORDER_WIDTH), (CELL_WIDTH-2*BORDER_WIDTH, CELL_HEIGHT-2*BORDER_WIDTH)))
        else:  # 普通可通行单元格
            pygame.draw.rect(screen, Color.GREEN.value, ((x+BORDER_WIDTH, y+BORDER_WIDTH), (CELL_WIDTH-2*BORDER_WIDTH, CELL_HEIGHT-2*BORDER_WIDTH)))

    # 绘制起点和终点
    pygame.draw.circle(screen, Color.BLUE.value, (pix_sn[0]+CELL_WIDTH//2, pix_sn[1]+CELL_HEIGHT//2), CELL_WIDTH//2 - 1)
    pygame.draw.circle(screen, Color.RED.value, (pix_en[0]+CELL_WIDTH//2, pix_en[1]+CELL_HEIGHT//2), CELL_WIDTH//2 - 1)

    # 绘制最优路径
    pygame.draw.aalines(screen, Color.RED.value, False, rl_pix)

    # Pygame主循环，等待退出
    keepGoing = True
    while keepGoing:
        pygame.time.delay(100)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:  # 点击关闭按钮退出
                keepGoing = False
        pygame.display.flip()

# ===========================
# 坐标转换函数
# ===========================
def transform(pos):
    """ 将地图坐标转换为像素坐标 """
    xnew, ynew = pos[0]*CELL_WIDTH, pos[1]*CELL_HEIGHT
    return (xnew, ynew)

# ===========================
# 程序入口
# ===========================
if __name__ == '__main__':
    main()
