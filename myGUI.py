from tkinter import *

from PIL import ImageTk, Image

LICHESSBGDARKMAIN = "#161512"

LICHESSBGDARK = "#302E2C"
LICHESSBGLIGHT = "#262421"

FGGRAY = "#BABABA"
FGWHITE = "#999999"

FONT15 = ("Arial", 15)


class RootWindowOfGrids(Tk):
    def __init__(self, title, geometry, bg):
        Tk.__init__(self)
        self.title = title
        self.geometry(geometry)
        self.config(bg=bg)
        self.resizable(False, False)
        self.grid_propagate(False)


class FrameOfGridsPackPlacement(Frame):
    def __init__(self, parent, widthXheight, side, bg):
        w, h = widthXheight
        Frame.__init__(self, parent, width=w, height=h, bg=bg)

        self.grid_propagate(False)

        self.pack(side=side)


class FrameOfPacksGridPlacement(Frame):
    def __init__(self, parent, widthXheight, rowXcol, bg, padX=None, padY=None):
        w, h = widthXheight
        Frame.__init__(self, parent, width=w, height=h, bg=bg)

        self.pack_propagate(False)

        row, col = rowXcol
        if padX != None and padY == None:
            self.grid(row=row, column=col, padx=padX)
        elif padX == None and padY != None:
            self.grid(row=row, column=col, pady=padY)
        elif padX != None and padY != None:
            self.grid(row=row, column=col, padx=padX, pady=padY)
        else:
            self.grid(row=row, column=col)

class FrameOfPacksPackPlacement(Frame):
    def __init__(self, parent, widthXheight, side, bg):
        w, h = widthXheight
        Frame.__init__(self, parent, width=w, height=h, bg=bg)

        self.pack_propagate(False)

        self.pack(side=side)


class FrameOfGridsGridPlacement(Frame):
    def __init__(self, parent, widthXheight, rowXcol, bg, padX=None, padY=None):
        w, h = widthXheight
        Frame.__init__(self, parent, width=w, height=h, bg=bg)

        self.grid_propagate(False)

        row, col = rowXcol
        if padX != None and padY == None:
            self.grid(row=row, column=col, padx=padX)
        elif padX == None and padY != None:
            self.grid(row=row, column=col, pady=padY)
        elif padX != None and padY != None:
            self.grid(row=row, column=col, padx=padX, pady=padY)
        else:
            self.grid(row=row, column=col)


class DummyFrameGridPlacement(Frame):
    def __init__(self, parent, widthXheight, rowXcol, bg):
        w, h = widthXheight
        Frame.__init__(self, parent, width=w, height=h, bg=bg)

        row, col = rowXcol
        self.grid(row=row, column=col)


class DummyFramePackPlacement(Frame):
    def __init__(self, parent, widthXheight, side, bg):
        w, h = widthXheight
        Frame.__init__(self, parent, width=w, height=h, bg=bg)

        self.pack(side=side)


class LabelPackPlacement(Label):
    def __init__(self, parent, text, bg, fg, font, side, padx=None, pady=None, width=None, height=None):
        Label.__init__(self, parent, text=text, bg=bg, fg=fg, font=font, width=width, height=height)

        if padx != None and pady == None:
            self.pack(side=side, padx=padx)
        elif padx == None and pady != None:
            self.pack(side=side, pady=pady)
        elif padx != None and pady != None:
            self.pack(side=side, padx=padx, pady=pady)
        else:
            self.pack(side=side)
class LabelGridPlacement(Label):
    def __init__(self, parent, text, bg, fg, font, rowXcolumn, padx=None, pady=None, width=None, height=None):
        Label.__init__(self, parent, text=text, bg=bg, fg=fg, font=font, width=width, height=height)
        parent.child = self
        row, col =  rowXcolumn

        if padx != None and pady == None:
            self.grid(row = row, column = col, padx=padx)
        elif padx == None and pady != None:
            self.grid(row = row, column = col, pady=pady)
        elif padx != None and pady != None:
            self.grid(row = row, column = col, padx=padx, pady=pady)
        else:
            self.grid(row = row, column = col)


class ImageOnFramePackPlacement():
    def __init__(self, frame, path, resize, bg, side=None):
        img = ImageTk.PhotoImage(Image.open(path).resize(resize))
        canvas = Canvas(frame, bg=bg, borderwidth=0, highlightthickness=0)
        frame.img = img
        if side != None:
            canvas.pack(side = side)
        else:
            canvas.pack()
        canvas.create_image(int(resize[0] / 2), 0, image=img, anchor=NW)

class ImageOnFrameGridPlacement():
    def __init__(self, frame, path, resize, bg, rowXcol):
        x = Image.open(path)
        y = x.resize(resize)
        img = ImageTk.PhotoImage(y)
        canvas = Canvas(frame, bg=bg, borderwidth=0, highlightthickness=0, width = resize[0], height = resize[1])
        frame.img = img

        canvas.create_image(0, 0, image=img, anchor=NW)
        row, col = rowXcol
        canvas.grid(row = row, column = col)


class PhotoImage(ImageTk.PhotoImage):
    def __init__(self, parent, **kwargs):
        image = kwargs['image']

        # PIL.Image => .PhotoImage
        super().__init__(image)

        # Update <widget>.children with [self.__photo.name] = self
        self._ref = parent.children
        self._ref[self.__photo.name] = self

    def destroy(self):
        # This gets called on `.destroy()` the parent
        # Delete the reference in parent.children
        del self._ref[self.__photo.name]


class PhotoImageLabel(Label):
    def __init__(self, parent, **kwargs):
        image = Image.open(kwargs['image'])

        # Get a PhotoImage object which is bound to 'self'
        kwargs['image'] = PhotoImage(self, image=image)

        super().__init__(parent, **kwargs)