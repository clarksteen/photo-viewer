''' Photo Viewer

A program to display and interact with pictures.


'''

import os, glob, shutil
from time import sleep
import keyboard
import tkinter
from tkinter import ttk
from PIL import Image, ImageTk, ImageOps
from random import shuffle
import json


def get_files(path: list, ignore=[''], recursive=True) -> list:
    '''Get all files in directory. '''

    files = []
    for p in path:
        if recursive:
            dirs = glob.glob(p + '/**/*', recursive=True)
        else:
            dirs = glob.glob(p + '/*')

        f = []

        for d in dirs:
            if os.path.isfile(d):
                f.append(d)

        files.extend(f)

    files = [f for f in files if f[-3:] not in ignore]

    return files


class Photo():
    '''Photograph objects'''

    def __init__(self, file: str):
        self.data = None
        self.file = file
        self.rotation = 0
        self.open()
        

    def open(self):
        ''' Open the file.
        '''

        try:
            self.data = Image.open(self.file)

            # Auto-rotate using EXIF tag.
            self.data = ImageOps.exif_transpose(self.data)

        except:
            self.data = None
            print(f'Warning: file is not an image: {self.file}')


class Viewer():
    '''Manage the display of Photo objects.
    '''

    def __init__(self, photo):
        
        self.trigger = None
        self.timer = 60
        self.index = -1
        self.files = files
        self.root = self.get_root()
        self.canv = self.get_canvas()
        self.photo = photo
        self.hidden_dir = "Hide"
        self.favorites_dir = None


    def get_root(self):
        '''
        Get screen root object and set its properties and key bindings.
        Return the root object.
        '''

        root = tkinter.Tk()
        ttk.Style().theme_use('alt')
        self.scr_width = root.winfo_screenwidth()
        self.scr_height = root.winfo_screenheight()

        # Create borderless window.
        root.overrideredirect(True)
        root.geometry(f"{int(self.scr_width)}x{int(self.scr_height)}+0+0")
        root.config(cursor="none")
        
        # Make sure it is active.
        root.lift()
        root.attributes('-topmost',True)
        root.after_idle(root.attributes,'-topmost',False)

        # Bind key presses.
        root.bind("<Escape>", lambda e: self.root.destroy())
        root.bind("<Up>", lambda e: self.rotate90())
        root.bind("<Right>", lambda e: self.next(1))
        root.bind("<Left>", lambda e: self.next(-1))
        root.bind("<Delete>", lambda e: self.hide_photo())
        root.bind("<f>", lambda e: self.star_photo())
        root.bind("<o>", lambda e: self.open_photo())
    
        return root
    

    def get_canvas(self):
        '''
        Create and return a fullscreen TKINTER canvas which will display 
        the Photo. 
        '''

        canvas = tkinter.Canvas(self.root, width=self.scr_width, 
                                height=self.scr_height)
        canvas.pack()
        canvas.configure(background='black')

        return canvas
    

    def display(self):
        ''' Display a Photo object. '''

        # Must save persistent ImageTk object. Otherwise MAINLOOP() destroys 
        # local instance and it displays for only a fraction of a second.
        self.image = ImageTk.PhotoImage(self.fit())

        # Add image to canvas. Position the center of the image in the center of
        # the canvas.
        #self.canv.delete("all")
        self.canv.create_image(self.scr_width/2, self.scr_height/2, 
                               image=self.image)
        
        
    def fit(self):
        ''' Resize image data to fit screen. '''
        
        w, h = self.photo.data.size
        ratio = [w/self.scr_width, h/self.scr_height]

        # Check for non-unity ratios and resize if necessary.
        if set(ratio) != set([1]):
            w_fit = int(w / max(ratio))
            h_fit = int(h / max(ratio))

            p = self.photo.data.resize((w_fit, h_fit), Image.Resampling.LANCZOS)

        else:
            p = self.photo.data

        return p
            
         
    def scale(self, scale: float):
        '''Unused function. '''
        pass

        w, h = self.data.size
        newWidth = int(w * scale)
        newHeight = int(h * scale)
        self.data = self.data.resize((newWidth, newHeight),
                                    Image.Resampling.LANCZOS)
        
        self.display()
    
    
    def rotate90(self):
        '''Rotate Photo and re-display. '''
        
        self.photo.data = self.photo.data.rotate(-90, expand=True)
        self.display()
        self.photo.rotation += -90


    def next(self, increment=1):
        '''Get next valid photo file and display it. '''

        self.index += increment         

        # Ensure that file is a photo. If not, keep looking.
        while Photo(self.files[self.index]).data is None:
            self.index += increment 

        self.photo = Photo(self.files[self.index])

        self.display()

        # Cancel previous AFTER call so that they don't accumulate. Otherwise
        # each call to NEXT (left or right arrows) creates a cascade of 
        # automatic triggers.
        if self.trigger is not None:
            self.canv.after_cancel(self.trigger)
        self.trigger = self.canv.after(self.timer*1000, self.next)
        
    
    def hide_photo(self):
        '''Move current file to folder in same directory. '''

        current_file = self.files[self.index]
        current_name = os.path.basename(current_file)
        current_dir = os.path.dirname(current_file)

        # Create new directory if necessary.
        new_dir = os.path.join(current_dir, self.hidden_dir)
        if not os.path.exists(new_dir):
            os.mkdir(new_dir)

        
        new_file = os.path.join(new_dir, current_name)

        # Go to next photo to free up this file.
        self.next()
        
        os.rename(current_file, new_file)
        

    def star_photo(self):
        '''Copy current file to favorites folder. '''

        current_file = self.files[self.index]

        # Create new directory if necessary.
        if not os.path.exists(self.favorites_dir):
            os.mkdir(self.favotites_dir)

        shutil.copy(current_file, self.favorites_dir)


    def open_photo(self):
        '''Open directory of current photo and exit program. '''

        current_file = self.files[self.index]
        current_dir = os.path.dirname(current_file)

        os.startfile(current_dir)

        self.root.destroy()



if __name__ == '__main__':

    # Read settings file.
    with open("photo-viewer-settings.json") as f:
        config = json.load(f)

    # Get image files.
    all_files = get_files(config["path"], ignore=config["ignore_extension"])
    
    # Remove files in hidden folder.
    files = [f for f in all_files if os.path.basename(os.path.dirname(f))
                  != config["hidden_directory"]]

    # Create Viewer object and run.
    view = Viewer(shuffle(files))
    view.timer = config["delay_time"]
    view.hidden_dir = config["hidden_directory"]
    view.favorites_dir = config["favorites"]
    
    view.next()
    view.root.focus_set()
    view.root.mainloop()
