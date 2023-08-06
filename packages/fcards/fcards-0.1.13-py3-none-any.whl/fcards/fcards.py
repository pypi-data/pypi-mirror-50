# Card files are semi colon seperated flash cards, with each flash card being 
# two elements (the front and back of the flash card) seperated by a comma
# Eg: Front1,Back1;Front2,Back2;Front3,Back3

import curses
import glob
import os

HOME_DIR = os.path.expanduser('~')

stdscr = curses.initscr()

menu = ['Practice', 'Edit']
current = 0

if not os.path.isdir(HOME_DIR+"/.cards"):
    os.mkdir(HOME_DIR+"/.cards")

def draw_menu(stdscr, menu, current, title=None, info=None):
    
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
    if info != None:
        x, y = w//2-len(info)//2, h - 3
        stdscr.addstr(y, x, info)

def interactive_menu(stdscr, menu, current, funcs=None, title=None, delete=False, info=None):
    
    while True:

        stdscr.clear()
        draw_menu(stdscr, menu, current, title, info)
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
        elif c == ord('d'):
            if delete and menu[current] not in ["New Card", "New Cardset"]:
                if interactive_menu(stdscr, ["Delete", "Cancel"], 0, title="Are you sure you want to delete that?") == 0:
                    return ["DELETE", current]
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

    cardsets = [cardset[len(HOME_DIR)+8:-7] for cardset in glob.glob(HOME_DIR+"/.cards/*.fcards")]
    current = 0
    
    while True:

        i = "Move: [arrow keys], select: [enter], back: [q]"
        selected = interactive_menu(stdscr, cardsets, current, title='Available Cardsets:', info=i)
        if selected == "BACK":
            return
        
        cardfile = HOME_DIR+"/.cards/"+cardsets[selected]+".fcards"
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

        cardsets = [cardset[len(HOME_DIR)+8:-7] for cardset in glob.glob(HOME_DIR+"/.cards/*.fcards")] + ["New Cardset"]
        i = "Move: [arrow keys], select: [enter], back: [q], delete: [d]"
        selected = interactive_menu(stdscr, cardsets, current, title='Available Cardsets:', delete=True, info=i)
        if type(selected) == list and selected[0] == "DELETE":
            os.remove(HOME_DIR+"/.cards/"+cardsets[selected[1]]+".fcards")
            continue
        if selected == "BACK":
            return
        if selected == len(cardsets)-1:
            cardfile = HOME_DIR+"/.cards/"+input_box(stdscr, "Select Name:")+".fcards"
            cards = [[]]
        else: 
            cardfile = HOME_DIR+"/.cards/"+cardsets[selected]+".fcards"
            cards = [elem.split(',') for elem in open(cardfile).read().split(';')]
        
        menu_cards = [', '.join(elem) for elem in cards] + ["New Card"]

        while True:

            current = 0
            if len(menu_cards) == 0 or len(menu_cards[0]) == 0:
                selected = interactive_menu(stdscr, menu_cards[1:], current, title="Cardset Empty:", info=i)
            else:
                selected = interactive_menu(stdscr, menu_cards, current, title="Loaded Cards:", delete=True, info=i)
            if type(selected) == list and selected[0] == "DELETE":
                cards.remove(cards[selected[1]])
                menu_cards.remove(menu_cards[selected[1]])
                f = open(cardfile, "w")
                f.write(';'.join([','.join(elem) for elem in cards]))
                f.close()
                continue
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



def fcards(stdscr, menu, current):

    curses.init_pair(1, curses.COLOR_BLACK, curses.COLOR_WHITE)
    curses.curs_set(0)

    funcs = [practice, edit]
    interactive_menu(stdscr, menu, current, funcs=funcs)

def main():
    curses.wrapper(fcards, menu, current)

if __name__=="__main__":
    main()

