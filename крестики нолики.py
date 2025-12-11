import pygame #библиотека для создания визуализации.
import sys 

def check_win(mas, sign): #чеклист для проверки есть ли победитель или ничья.sing - символы которые вводят игроки х или о.
    zeroes = 0 #считает пустые клеточки.
    for row in mas: #mas - игровая доска.
        zeroes += row.count(0)  
        if row.count(sign) == 3: # подсчитывает символы в клетках. если есть исход с 3 одинаковыми символами, то высвечивается Победа.
            return sign 
    
    for col in range(3): #по вертикали/горизонтали.
        if mas[0][col] == sign and mas[1][col] == sign and mas[2][col] == sign:
            return sign 
    
    if mas[0][0] == sign and mas[1][1] == sign and mas[2][2] == sign:
        return sign #по диагонали (главная диагональ. от верхнего левого, к нижнему правому.)
    
    if mas[0][2] == sign and mas[1][1] == sign and mas[2][0] == sign:
        return sign #по диагонали (побочная диагональ. от верхнего правого, к левому нижнему.)
    
    if zeroes == 0:
        return 'Piece' #ничья, нет победителя и пустых клеток.
    
    return False #возаращет при ничьей.

pygame.init() #инициализация модуля пайгейм.
size_block = 100 #размер одной клетки.
margin = 20 #отступы между клетками.
width = height = size_block * 3 + margin * 4 #общие размеры, 3 клетки, 4 отсупа.

size_window = (width, height)
screen = pygame.display.set_mode(size_window)
pygame.display.set_caption("Крестики-нолики") #задается игровая зона по заданным размерам.

black = (0, 0, 0)
red = (255, 0, 0)
green = (0, 255, 0)
white = (255, 255, 255) #все цвета в форме RGB.


mas = [[0, 0, 0] for i in range(3)]  #размер игрового поля 3х3.
query = 0  #счетчик попыток. четные и не четные ходы в зависимости от порядка игроков.
game_over = False #окончание игры.

while True:
    for event in pygame.event.get(): #обработка ивентов(событий).
        if event.type == pygame.QUIT:  
            pygame.quit()
            sys.exit(0)
        
        elif event.type == pygame.MOUSEBUTTONDOWN and not game_over: #обработка координат мыши пока игра не законченна.
            x_mouse, y_mouse = pygame.mouse.get_pos() #получение координат.
            col = x_mouse // (size_block + margin) #опеделение по координатам где находится мышь.
            row = y_mouse // (size_block + margin)
            
            if 0 <= row < 3 and 0 <= col < 3 and mas[row][col] == 0: #проверяет пустая ли клетка.
                if query % 2 == 0:  #расчитывает цвет в зависимости от порядка игроков.
                    mas[row][col] = 'x'
                else:
                    mas[row][col] = 'o' #если ячейка путая, ставит х или о.
                query += 1  #увеличивается счётчик ходов.
        elif event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE: #после окончания игры при нажатии на пробел игра обнуляется.
            game_over = False
            mas = [[0, 0, 0] for i in range(3)]
            query = 0 #счётчик сбрасывается.
            screen.fill(black) #поле очищается.
    
    screen.fill(black) #подготовка нового чистого поля.
    
    for row in range(3): #ход по ячейкам.
        for col in range(3):
            if mas[row][col] == 'x': #в зависимости от хода ставит значение и цвет в клетке.
                color = red  
            elif mas[row][col] == 'o':
                color = green  
            else:
                color = white
            
            x = col * size_block + (col + 1) * margin #вычисляет каординаты для каждого квадрата.
            y = row * size_block + (row + 1) * margin #левый и нижний углы.
            
            pygame.draw.rect(screen, color, (x, y, size_block, size_block)) #рисунок в квадрате через модуль.
            
            if color == red: #если красный, значит ходит крестик.
                pygame.draw.line(screen, white, (x + 5, y + 5), #высчитывается центр клетки.
                                 (x + size_block - 5, y + size_block - 5), 3) #с нужными отступами рисуется крестик из двух белых линий.
                pygame.draw.line(screen, white, (x + size_block - 5, y + 5), 
                                 (x + 5, y + size_block - 5), 3)
            elif color == green: #зеленый, значит ходит кружок.
                pygame.draw.circle(screen, white, 
                                  (x + size_block // 2, y + size_block // 2), 
                                  size_block // 2 - 3, 3)
    
    if not game_over and query > 0: #после каждого хода проверяется есть ли победитель.
        if (query - 1) % 2 == 0: #счётчик подсчитывает какой ход был сделан и анализирует следующий(чётный или не четный).
            game_over = check_win(mas, 'x') #игра заканчивается при победе крестика.
        else:  
            game_over = check_win(mas, 'o') #игра заканчивается при победе кружка.
    
    if game_over: #если игра закончилась.
        screen.fill(black) #очищается экран.
        font = pygame.font.SysFont('arial', 80) #отображается сообщение победа или ничья.
        
        if game_over == 'Piece': #проверяет на наличиеничьей.
            text1 = font.render("НИЧЬЯ!", True, white) #если итог игры - ничья, выводится сообщение НИЧЬЯ.
        else:
            text1 = font.render(f"ВЫИГРАЛ {game_over.upper()}!", True, white) #если есть победитель, выводит это на экран.
        
        text_rect = text1.get_rect() #задают размеры прямоугольника.
        text_x = screen.get_width() / 2 - text_rect.width / 2 #на прямоугольнике высчитывается ширина и высота.
        text_y = screen.get_height() / 2 - text_rect.height / 2 #ищется центр для ровного размещения текста.
        screen.blit(text1, [text_x, text_y])  #показывает текст по нужным каординатам.
        

        font_small = pygame.font.SysFont('arial', 30) #параметры для высвечивания подсказки.
        restart_text = font_small.render("Нажмите ПРОБЕЛ для новой игры", True, white) #подсказка чтобы начать новую игру.
        restart_rect = restart_text.get_rect() #получает каординаты для ровного размещения подстказки.
        restart_x = screen.get_width() / 2 - restart_rect.width / 2 #ищет центр.
        screen.blit(restart_text, [restart_x, text_y + 100]) #для удобства чтения выводит подсказку ниже на 100 пиксиле .
    
    pygame.display.update() #экран обнвляется для точных результатов.