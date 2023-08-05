# Card files are semi colon seperated flash cards, with each falsh card being 
# two elements (the front and back of the flash card) seperated by a comma
# Eg: Front1,Back1;Front2,Back2;Front3,Back3

import curses
import glob
import os

stdscr = curses.initscr()

menu = ['Practice', 'Edit']
current = 0

if not os.path.isdir("cards"):
    os.mkdir("cards")

def draw_menu(stdscr, menu, current, title=None):
    
    h, w = stdscr.getmaxyx()
    for i, elem in enumerate(menu):
        x, y = w//2-len(elem)//2, h//2-len(menu)//2+i
        if i==current:
            stdscr.addstr(y, x, elem, curses.color_pair(1))
        else:
            stdscr.addstr(y, x, elem)
    if title != None:
        x, y = w//2-len(title)//2, h//2-len(menu)//2-2
        stdscr.addstr(y, x, title)

def interactive_menu(stdscr, menu, current, funcs=None, title=None):
    
    while True:

        stdscr.clear()
        draw_menu(stdscr, menu, current, title)
        stdscr.refresh()

        c = stdscr.getch()
        if c == curses.KEY_UP:
            current = max(0, current-1)
        elif c == curses.KEY_DOWN:
            current = min(len(menu)-1, current+1)
        elif c == curses.KEY_ENTER or c in [10, 13]:
            if funcs != None:
                funcs[current](stdscr)
            else:
                return current
        elif c == ord('q'):
            return "BACK"

def input_box(stdscr, title=None):
    curses.curs_set(1)
    text = ''
    h, w = stdscr.getmaxyx()
    while True:
        x, y = w//2-len(text)//2, h//2
        stdscr.clear()
        if title!=None:
            x_, y_ = w//2-len(title)//2, h//2-2
            stdscr.addstr(y_, x_, title)
        stdscr.addstr(y, x, text)
        stdscr.refresh()
        c = stdscr.getch()
        if c == curses.KEY_ENTER or c in [10, 13]:
            curses.curs_set(0)
            return text
        elif c == curses.KEY_BACKSPACE or c == 127:
            text = text[:-1]
        else:
            text += chr(c)

def practice(stdscr):
    
    h, w = stdscr.getmaxyx()

    cardsets = [cardset[6:-7] for cardset in glob.glob("cards/*.fcards")]
    current = 0
    
    while True:

        selected = interactive_menu(stdscr, cardsets, current, title='Available Cardsets:')
        if selected == "BACK":
            return
        
        cardfile = "cards/"+cardsets[selected]+".fcards"
        cards = [elem.split(',') for elem in open(cardfile).read().split(';')]
        if cards == [[""]]:
            stdscr.clear()
            t = "No Cards In This Set"
            x, y = w//2-len(t)//2, h//2
            stdscr.addstr(y, x, t)
            stdscr.getch()
        else:
            i=0
            while True:
                stdscr.clear()
                if i%2==0:
                    t = cards[i//2%len(cards)][0]
                else:
                    t = cards[i//2%len(cards)][1]
                x, y = w//2-len(t)//2, h//2
                stdscr.addstr(y, x, t)
                stdscr.refresh()
                if stdscr.getch() == ord('q'):
                    break
                i+=1   

def edit(stdscr):

    h, w = stdscr.getmaxyx()

    current = 0
    
    while True:

        cardsets = [cardset[6:-7] for cardset in glob.glob("cards/*.fcards")] + ["New Cardset"]
        selected = interactive_menu(stdscr, cardsets, current, title='Available Cardsets:')
        if selected == "BACK":
            return
        if selected == len(cardsets)-1:
            cardfile = "cards/"+input_box(stdscr, "Select Name:")+".fcards"
            cards = [[]]
        else: 
            cardfile = "cards/"+cardsets[selected]+".fcards"
            cards = [elem.split(',') for elem in open(cardfile).read().split(';')]
        
        menu_cards = [', '.join(elem) for elem in cards] + ["New Card"]

        while True:

            current = 0
            if len(menu_cards) == 0 or len(menu_cards[0]) == 0:
                selected = interactive_menu(stdscr, menu_cards[1:], current, title="Cardset Empty:")
            else:
                selected = interactive_menu(stdscr, menu_cards, current, title="Loaded Cards:")
            if selected == "BACK":
                break
            else:
                f = input_box(stdscr, "Front Of Flashcard:")
                b = input_box(stdscr, "Back Of Flashcard:")
                if selected == len(menu_cards)-1:
                    cards.append([f, b])
                else:
                    cards[selected] = [f, b]
                menu_cards = [', '.join(elem) for elem in cards] + ["New Card"]
                f = open(cardfile, "w")
                f.write(';'.join([','.join(elem) for elem in cards]))
                f.close()



def main(stdscr, menu, current):

    curses.init_pair(1, curses.COLOR_BLACK, curses.COLOR_WHITE)
    curses.curs_set(0)

    funcs = [practice, edit]
    interactive_menu(stdscr, menu, current, funcs=funcs)

if __name__=='__main__':
    curses.wrapper(main, menu, current)

