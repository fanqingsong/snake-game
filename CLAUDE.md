# 贪吃蛇游戏项目

## 项目概述

这是一个使用纯前端技术实现的经典贪吃蛇游戏，包含完整的游戏逻辑、美观的UI界面和用户友好的交互体验。

## 技术栈

- **HTML5** - 页面结构
- **Canvas API** - 游戏渲染
- **Vanilla JavaScript** - 游戏逻辑
- **CSS3** - 样式和动画

## 项目结构

```
.
├── snake.html       # 主游戏文件（包含所有HTML、CSS、JS）
├── GAME_GUIDE.md    # 用户使用指南
├── CLAUDE.md        # 本文件（项目上下文）
└── .gitignore       # Git忽略规则
```

## 核心功能

### 游戏机制
- 网格化游戏区域（20x20格子）
- 蛇身数组管理（头部为第一个元素）
- 随机食物生成（避免生成在蛇身上）
- 碰撞检测（墙壁和自身）
- 难度递增（每5分加速一次）

### 控制系统
- 方向键控制移动方向
- 空格键暂停/继续
- 防止180度转向
- 按键启动游戏机制

### 数据持久化
- 使用 localStorage 保存最高分
- 键名：`snakeHighScore`

## 关键代码组件

### 全局变量
```javascript
const gridSize = 20;        // 每格像素大小
const tileCount = 20;       // 横纵向格子数
let snake = [];             // 蛇身坐标数组
let food = {};              // 食物坐标
let dx, dy;                 // 移动方向
let score = 0;              // 当前分数
let gameSpeed = 100;        // 游戏循环间隔
let isPaused = false;       // 暂停状态
let gameStarted = false;    // 游戏开始状态
```

### 主要函数
- `changeDirection(event)` - 处理键盘输入
- `draw()` - 游戏主循环
- `moveSnake()` - 移动蛇的位置
- `checkCollision()` - 碰撞检测
- `checkFood()` - 食物检测
- `generateFood()` - 生成新食物
- `drawSnake()` - 绘制蛇
- `drawFood()` - 绘制食物
- `gameOver()` - 游戏结束处理
- `restartGame()` - 重置游戏

## 设计特点

### 视觉效果
- 渐变背景（紫色主题）
- 发光效果（蛇头和食物）
- 圆润UI组件
- 半透明卡片设计
- 阴影效果

### 游戏平衡
- 初始速度：100ms/帧
- 最小速度：50ms/帧
- 每5分加速5ms
- 防止快速按键导致的自殺

## 开发指南

### 添加新功能
1. **修改游戏参数**：编辑 `snake.html` 顶部的全局变量
2. **调整视觉样式**：修改 `<style>` 标签内的CSS
3. **添加游戏机制**：在 `<script>` 标签内添加新函数

### 常见修改点
- 调整游戏大小：修改 `canvas.width/height` 和 `tileCount`
- 修改颜色方案：调整CSS中的渐变色和`drawSnake/drawFood`中的颜色
- 添加难度选择：创建速度预设选项
- 添加音效：使用 Web Audio API
- 添加排行榜：使用后端存储或增加更多本地存储槽位

### 调试技巧
- 打开浏览器开发者工具（F12）
- 在Console中查看变量值
- 使用 `console.log()` 调试游戏逻辑
- 检查 localStorage 中的最高分数据

## 已知限制

- 单文件架构，代码都在 `snake.html` 中
- 本地存储仅限单个浏览器
- 没有移动端触控支持
- 游戏区域固定为400x400像素

## 未来改进方向

- [ ] 添加移动端触控支持
- [ ] 实现关卡系统
- [ ] 添加障碍物
- [ ] 多种游戏模式（穿墙模式、加速模式等）
- [ ] 在线排行榜
- [ ] 音效和背景音乐
- [ ] 主题切换功能
- [ ] 分享到社交媒体功能

## 部署

### GitHub Pages
1. 仓库已推送到 GitHub
2. 在 Settings > Pages 中启用
3. 选择 main/master 分支
4. 访问 `https://fanqingsong.github.io/snake-game/snake.html`

### 本地运行
```bash
# 方法1：直接在浏览器中打开
# 双击 snake.html 文件

# 方法2：使用本地服务器
python3 -m http.server 8080
# 访问 http://localhost:8080/snake.html
```

## 相关资源

- Canvas API 文档：https://developer.mozilla.org/en-US/docs/Web/API/Canvas_API
- LocalStorage API：https://developer.mozilla.org/en-US/docs/Web/API/Window/localStorage
- 游戏开发最佳实践：https://developer.mozilla.org/en-US/docs/Games

---

**项目状态：** 已完成基础功能，可正常运行和游玩

**最后更新：** 2025-04-05
