class Menu(): 
    """
    Dict-based Menu class
    
    Attributes
    ----------
    title: str
        Menu title
    _menu: dict
        A dictionary structured as following:
        {
            idx1: {
                'label': label1,
                'action': action1
            },
            idx2: {
                'label': label2,
                'action': action2
            },
            ...
        }
        It can be initialized by a list of (idx, label, action) tuples
    """    

    def __init__(self, title:str = '', entries: list[tuple[str|int, str, callable]] = None):
        self.title = title
        self._menu = {}
        if entries:
            for idx, label, action in entries:
                self.add_action(idx, label, action)

    def add_action(self, idx: str|int, label: str, action: callable) -> None:
        """
        Parameters
        ----------
        idx: str|int
            The short name of the menu entry (i.g. '1', 1, 'A', 'X', ...)
        label: str
            The menu entry description (i.g. 'Back to the Main Menu')
        action: callable
            the function-like object that must be called by its idx        
        """

        self._menu[idx] = {'label' : label, 
                           'action': action}
        
    def execute(self, idx: str|int, *args) -> bool:
        """
        Parameters
        ----------
        idx: str|int
            short name of the menu entry
        *args
            parameters which must be passed to the executed function
        Returns 
        -------
        bool
            True if it actually executes the action
            associated with the menu entry labelled idx, 
            else False
        """

        if self._menu.get(idx):
            self._menu.get(idx)['action'](*args)
            return True
        return False
    
    def __str__(self) -> str:
        string = f"\n{self.title}\nActions:\n"
        for key, value in self._menu.items():
           string += f"   {key} - {value['label']}\n"
        return string

    def print(self) -> None:
        print(self)

    def __getitem__(self, idx):
        return self._menu.get(idx) # no index error will be raised

    def __iter__(self):
        for dictitem in self._menu:
            yield dictitem


# test library
if __name__ == '__main__':
    def fun1():
        print('fun1 works!')
    def fun2():
        print('fun2 works!')
    def fun3():
        print('fun3 works!')
    def quit():
        pass

    actions = [('1', 'function 1', fun1),
               ('2', 'function 2', fun2),
               ('3', 'function 3', fun3),
               ('X', 'quit', quit)]
    menu = Menu('MAIN MENU', actions)
    menu.print()
    choice = ''
    while(choice != 'X'):
        choice = input('Choose option: ').upper()
        if choice == 'X':
            break
        menu.execute()
        menu.print()