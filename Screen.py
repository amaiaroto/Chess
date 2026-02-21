class Screen:
    def __init__(self, pygame_object, screen_width: int, screen_height: int, options: list = None):
        self.width = screen_width
        self.height = screen_height
        self.options = options
        self.pg = pygame_object

    @property
    def screen(self):
        return self.pg.display.set_mode(
            (self.width, self.height),
            *self.options if self.options else [self.pg.SCALED])
