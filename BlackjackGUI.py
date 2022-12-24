# Title: BlackjackGUI.pyw
# Author: Damian Archer
# Date: 2-8-2021
# Purpose: CIS 12O Programming Project 4

import tkinter as tk
import CardDeck
import time
"""
        Requirements:
            1) Implement a simple Blackjack game.
            2) Use Deck implementation from Programming Project 3.
"""
class Hand:
    def __init__(self):
        self.value = 0
        self.aces = 0
        self.cards = []

    def deal(self, card, BUSTED=False):
        """ pre: card is instance of Card
            post: returns BUSTED as True if hand busts, or False otherwise.
        """
        if (card.get_blackjack_value() == 11): self.aces += 1
        self.cards.append(card)
        self.value += card.get_blackjack_value()
        if self.value > 21:
            if self.aces > 0:
                self.value -= 10
                self.aces -= 1
            else: BUSTED = True
        return BUSTED

    def draw(self, gfx, y, x=20, hide=False):
        """
            pre: gfx is a Canvas object. x and y are ints representing the origin of drawing.
                 Hide is true to indicate the dealer has a hidden card.
            post: Draws the hand onto the gfx Canvas.
        """
        w, h = gfx.winfo_width()/9, gfx.winfo_height()/5
        if hide:
            gfx.create_rectangle(x, y, w+x, h+y, fill="white", stipple="gray12")
            x += 10 + gfx.winfo_width()/9   
            for card in self.cards[1:]:
                card.draw(gfx, x, y)
                x += 10 + gfx.winfo_width()/9
        else:
            for card in self.cards:
                card.draw(gfx, x, y)
                x += 10 + gfx.winfo_width()/9

    def get_value(self): return self.value

        
class Game:
    """
    Used with Tkinter App
    """
    def __init__(self):
        self.purse_amt = 1000
        self.bet_amt = 1
        self.deck = CardDeck.Deck()
        self.player = Hand()
        self.dealer = Hand()
        self.deal()

    def hit(self):
        """ post: returns True if hand busts, or False otherwise."""
        if (self.player.deal(self.deck.deal())): return True
        else: return False

    def deal(self):
        """
            post: creates new hands, deals two cards to both player and dealer.
        """
        self.player = Hand()
        self.dealer = Hand()
        for i in range(2):
            self.player.deal(self.deck.deal())
            self.dealer.deal(self.deck.deal())

    # Mutators     
    def raise_bet(self): self.bet_amt += 1
    def lower_bet(self): self.bet_amt -= 1
    def lose(self): self.purse_amt -= self.bet_amt
    def win(self): self.purse_amt += self.bet_amt   

    
class App(tk.Frame):
    """
        Tkinter driver
    """
    
    def __init__(self):
        super().__init__()
        self.master.title("Blackjack")
        self.game = Game()
        self.user_interface()        
        self.grid(row=0,
                  column=0,
                  sticky=tk.N+tk.S+tk.E+tk.W)


        # Configurations to make window resizable
        top= self.winfo_toplevel()
        top.columnconfigure(0, weight=1)
        top.rowconfigure(0, weight=1)
        self.columnconfigure(0, minsize=480, weight=1)
        self.rowconfigure(0, minsize=320, weight=1)

        # A hand is dealt initially, so the dealbutton is disabled initially
        self.dealbutton["state"]=tk.DISABLED
        
        # flag tells if it is players turn or not.
        self.playersturn = True

        # event to redraw window if it is resised
        self.bind_all('<Configure>', self.__redraw)

        

    def user_interface(self):
        # Canvas (cardtable)
        self.gfx = tk.Canvas(
            self,
            bg="#4f0",
            width=480,
            height=320,
            relief="ridge")
        self.gfx.grid(row=0,
                      column=0,
                      sticky=tk.N+tk.S+tk.E+tk.W)
   

        # Menu (sidebar)
        self.menu = tk.Frame(
            self,
            bg="#558",
            height=self.master.winfo_height(),
            width=160,
            borderwidth=4,
            relief="ridge")

        # Menu configurations for resizing
        self.menu.columnconfigure(
            0, weight=1)
        self.menu.rowconfigure(
            0, weight=1)
        self.menu.columnconfigure(
            1, weight=1)
        self.menu.rowconfigure(
            1, weight=2)
        self.menu.columnconfigure(
            2, weight=1)
        self.menu.rowconfigure(
            2, weight=2)
        self.menu.grid(row=0,
                       column=1,
                       sticky=tk.N+tk.S+tk.E+tk.W)

        # IntVar and StringVar for textvariables
        height = tk.IntVar()
        height.set(self.winfo_height())
        self.prompt = tk.StringVar()
        self.prompt.set("")        
        self.bet_amt = tk.StringVar()
        self.bet_amt.set(f"${self.game.bet_amt}.00")
        self.purse_amt = tk.StringVar()
        self.purse_amt.set(f"${self.game.purse_amt}.00")

        # Menu's betframe configurations for resizing
        self.betframe = tk.Frame(
            self.menu,
            bg="#fff")
        self.betframe.rowconfigure(
            0, weight=1)
        self.betframe.columnconfigure(
            0, weight=1)
        self.betframe.rowconfigure(
            1, weight=1)                
        self.betframe.columnconfigure(
            1, weight=1)
        self.betframe.rowconfigure(
            2, weight=0)
        self.betframe.columnconfigure(
            2, weight=1)
        self.betframe.grid(column=0,
                           row=1,
                           sticky=tk.E+tk.W+tk.N+tk.S)

        # Menu's Hit/Stay Frame
        self.hitorstayframe = tk.Frame(
            self.menu,
            bg="#fff")
        self.hitorstayframe.rowconfigure(
            0, weight=1)
        self.hitorstayframe.columnconfigure(
            0, weight=1)
        self.hitorstayframe.columnconfigure(
            1, weight=1)
        self.hitorstayframe.rowconfigure(
            1, weight=1)
        self.hitorstayframe.grid(column=0,
                                 row=2,
                                 sticky=tk.E+tk.W+tk.S+tk.N)

        #Button Group   
        self.betupbutton = tk.Button(
            self.betframe,
            text="Raise Bet",
            border=5,
            relief="raised",
            command=self.__raise_bet,
            font=["boldface", 16],
            activebackground="#f93",)
        self.betupbutton.grid(column=1,
                              row=2,
                              columnspan=2,
                              sticky=tk.E+tk.W+tk.N+tk.S)
        
        self.betdownbutton = tk.Button(
            self.betframe,
            text="Lower Bet",
            border=5,
            relief="raised",
            command=self.__lower_bet,
            font=["boldface", 16],
            activebackground="#8f4")
        self.betdownbutton.grid(column=0,
                                row=2,
                                sticky=tk.E+tk.W+tk.N+tk.S)

        self.hitbutton = tk.Button(
            self.hitorstayframe,
            text="Hit",
            width=6,
            command=self.__hit,
            font=["verdana", 16])
        self.hitbutton.grid(column=0,
                            row=2,
                            sticky=tk.E+tk.W+tk.N+tk.S)

        self.staybutton = tk.Button(
            self.hitorstayframe,
            text="Stay",
            width=6,
            command=self.__stay,
            font=["verdana", 16])
        self.staybutton.grid(column=1,
                             row=2,
                             sticky=tk.E+tk.W+tk.N+tk.S)
        
        self.dealbutton = tk.Button(
            self.hitorstayframe,
            width=6,
            text="Deal",
            command=self.__deal,
            font=["verdana", 16],
            activebackground="#33f")
        self.dealbutton.grid(column=2,
                             row=2,
                             sticky=tk.E+tk.W+tk.N+tk.S)

        # Label Group
        self.controlslabel = tk.Label(
            self.menu,
            borderwidth=3,
            relief="flat",
            text="Player Controls",
            bg="#111",
            fg="#55f",
            width=20,
            font=["jokerman", 24])
        self.controlslabel.grid(column=0,
                                row=0,
                                sticky=tk.E+tk.W+tk.N+tk.S)

        self.userprompt = tk.Label(
            self.hitorstayframe,
            textvariable=self.prompt,
            font=["jokerman", 36],
            bg="#558",
            fg="#eee")
        self.userprompt.grid(column=0,
                             row=0,
                             rowspan=2,
                             columnspan=3,
                             sticky=tk.N+tk.W+tk.E+tk.S)
  
        
        self.purselabel = tk.Label(
            self.betframe,
            borderwidth=3,
            relief="raised",
            text="Purse Amount: ",
            bg="#000",
            fg="#fff",
            anchor=tk.E,
            font=["verdana", 20])
        self.purselabel.grid(column=0,
                             row=0,
                             sticky=tk.E+tk.W+tk.N+tk.S)

        self.purseamtlabel = tk.Label(
            self.betframe,
            textvariable = self.purse_amt,
            borderwidth=1,
            relief="sunken",
            bg="#555",
            fg="#ff0",
            anchor=tk.E,
            font=["verdana", 20])
        self.purseamtlabel.grid(column=1,
                                row=0,
                                columnspan=2,
                                sticky=tk.E+tk.W+tk.N+tk.S)
        
        self.currentbetlabel = tk.Label(
            self.betframe,
            width=12,
            borderwidth=3,
            relief="raised",
            text="Stake Amount:",
            bg="#000",
            fg="#fff",
            anchor=tk.W,
            font=["verdana", 20])
        self.currentbetlabel.grid(column=0,
                                  row=1,
                                  columnspan=2,
                                  sticky=tk.E+tk.W+tk.N+tk.S)
        
        self.betamtlabel = tk.Label(
            self.betframe,
            width=12,
            borderwidth=1,
            relief="sunken",
            bg="#555",
            fg="#0f0",
            textvariable=self.bet_amt,
            anchor=tk.E,
            font=["verdana", 20])
        self.betamtlabel.grid(column=1,
                              row=1,
                              columnspan=2,
                              sticky=tk.E+tk.W+tk.N+tk.S)

    # command methods
    def __raise_bet(self):
        self.game.raise_bet()
        self.bet_amt.set(f"${self.game.bet_amt}.00")

    def __lower_bet(self):
        if self.game.bet_amt > 0: self.game.lower_bet()
        self.bet_amt.set(f"${self.game.bet_amt}.00")

    def __deal(self):
        self.prompt.set("")
        self.game.deck.shuffle()
        self.game.deal()
        self.playersturn = True
        self.draw()
        self.dealbutton["state"]=tk.DISABLED
        self.hitbutton["state"]=tk.ACTIVE
        self.staybutton["state"]=tk.ACTIVE
        self.hitbutton.update()
        self.staybutton.update()
        
    def __redraw(self, event):  
        if self.playersturn: self.hide = True
        else: self.hide= False
        self.gfx.create_rectangle(0, 0, self.gfx.winfo_width(), self.gfx.winfo_height(), fill="#6f0", outline="#6f0")
        self.gfx.create_text(96, 24, text="Dealers Hand:", anchor=tk.CENTER, font=["jokerman", 16])
        self.game.dealer.draw(self.gfx, 40, hide=self.hide)
        self.gfx.create_text(96, self.gfx.winfo_height()-(24+50+self.winfo_height()/4), text="Players Hand:", font=["jokerman", 16])
        self.game.player.draw(self.gfx, self.gfx.winfo_height()-(50+self.winfo_height()/4))

        
    def __hit(self):
        self.hitbutton["bg"] = "#f93"
        self.hitbutton.update()
        time.sleep(0.1)
        self.hitbutton["bg"] = "SystemButtonFace"
        self.hitbutton.update()   
        BUSTED = self.game.hit()
        self.draw()
        
        if BUSTED:
            self.game.purse_amt -= self.game.bet_amt
            self.purse_amt.set(f"${self.game.purse_amt}.00")            
            self.prompt.set("Player Busts!")
            self.deactivate_buttons()
            
    def __stay(self):
        self.playersturn=False
        self.hitbutton["state"]=tk.DISABLED
        self.draw()
        self.staybutton["bg"]="#8f4"
        self.staybutton.update()
        time.sleep(0.1)
        self.staybutton["bg"]="SystemButtonFace"
        self.staybutton.update()
        
        dealerbusted=False
        while self.game.dealer.get_value() < 16 or self.game.dealer.get_value() < self.game.player.get_value():
            dealerbusted = self.game.dealer.deal(self.game.deck.deal())

        if dealerbusted:
            self.game.win()
            self.purse_amt.set(f"${self.game.purse_amt}.00")
            self.prompt.set("Dealer Busts!")
        elif self.game.dealer.get_value() < self.game.player.get_value():
            self.game.win()
            self.purse_amt.set(f"${self.game.purse_amt}.00")
            self.prompt.set("Player Wins!")
        elif self.game.dealer.get_value() > self.game.player.get_value():
            self.game.lose()
            self.purse_amt.set(f"${self.game.purse_amt}.00")            
            self.prompt.set("Player Loses!")
        else: 
            self.prompt.set("Pushback!")
            
        self.draw()
        self.deactivate_buttons()

    # other UI methods
    def draw(self):
        if self.playersturn: self.hide=True
        else: self.hide=False
        self.gfx.create_rectangle(0, 0, self.gfx.winfo_width(), self.gfx.winfo_height(), fill="#6f0", outline="#6f0")
        self.gfx.create_text(96, 24, text="Dealers Hand:", anchor=tk.CENTER, font=["jokerman", 16])
        self.game.dealer.draw(self.gfx, 40, hide=self.hide)
        self.gfx.create_text(96, self.gfx.winfo_height()-(24+50+self.winfo_height()/4), text="Players Hand:", font=["jokerman", 16])
        self.game.player.draw(self.gfx, self.gfx.winfo_height()-(50+self.winfo_height()/4))
        
    def deactivate_buttons(self):
        self.dealbutton["state"]=tk.ACTIVE
        self.hitbutton["state"]=tk.DISABLED
        self.staybutton["state"]=tk.DISABLED

 
if __name__ == "__main__": App()
