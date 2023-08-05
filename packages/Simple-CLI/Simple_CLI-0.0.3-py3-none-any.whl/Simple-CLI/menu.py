import os

class menu:
    
    functions = {}

    def __init__(self, **kwargs):
        """Menu Constructor"""
        self.add_items(**kwargs)


    def add_items(self, **kwargs):
        """Add items to functions"""
        self.functions.update(kwargs.items())
        print(self.functions)

    def show(self, text = 'Select a menu option:'):
        """Executes menu routine"""
        self.clear()
        print(text)
        print()
        i=0
        menu = {}
        for key, value in self.functions.items():
            print(F'\t [{i}] {key}')
            menu.update({i:value})
            i+=1
        print()
        try:
            menu[int(input(">>>"))]()
        except:
            self.show(text='Invalid Option!\nSelect a menu option:')
        


    def clear(self):
        """Helper function for clearing screen"""
        if os.name == 'nt':
            _ = os.system('cls')
        else:
            _ = os.system('clear')

if __name__ == "__main__":
    print('[*]Unit testing menu generator')
    _menu = menu(**{'a':lambda: print(1),'b':lambda: print(2),'c':lambda: print(3)})
    _menu.show()



