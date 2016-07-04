
from graphics import *


def main():
    num_games=15

    win = GraphWin('Scoreboard', 2000, 1500) # give title and dimensions

    #Case: 15 Games
    if(num_games==15):
        row=0
        column=0
        square_width=300
        square_height=300
        while column < num_games/5:
            row=0
            while row < num_games/3:
                #square
                square = Rectangle(Point((row+1)*square_width,(column+1)*square_height),Point(row*square_width,column*square_height))
                
                if(column%2==0): 
                    if(row%2==0): 
                        square.setFill('#397D02')
                        print "1"
                    else:
                        square.setFill('#567E3A')
                        print "2"
                else:
                    if(row%2==1): 
                        square.setFill('#397D02')
                        print "1"
                    else:
                        square.setFill('#567E3A')
                        print "2"
                    
                    
                    
                square.draw(win)

                row = row + 1
            column = column + 1
            

    



    #Test Functions

    #square 1
    #square = Rectangle(Point(0,0),Point(250,250))
    #square.setFill('#000040')
    #square.draw(win)
    
    #square 2
    #square = Rectangle(Point(250,0),Point(500,250))
    #square.setFill('#000080')
    #square.draw(win)
    
    #logo
    #logo = Image(Point(200, 200), "1956-Cardinals.gif")
    #logo.draw(win)
    
    #diamond
    diamond = Image(Point(150, 125), "rsz_diamond.png")
    diamond.draw(win)
    
    #cardinals logo
    STL_logo = Image(Point(60, 60), "rsz_1956-cardinals.png")
    STL_logo.draw(win)
    STL_text = Text(Point(60, 260), "CARDINALS")
    STL_text.draw(win)
    
    #cubs logo
    CHI_logo = Image(Point(240, 60), "rsz_chicago_cubs_logo_1937_to_1940.png")
    CHI_logo.draw(win)
    CHI_text = Text(Point(60, 280), "CUBS")
    CHI_text.draw(win)

    #message = Text(Point(win.getWidth()/2, 20), 'Click anywhere to quit.')
    #message.draw(win)
    win.getMouse()
    win.close()


main()
