class Function:
    def __init__(self, *args):
        self.__args = args

    def render(self) -> str:
        name = self.__class__.__name__

        args = ', '.join(map(str, self.__args))

        return f'{name}({args})'
