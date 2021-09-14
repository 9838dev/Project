# images
from tkinter import * 
from PIL import Image,ImageTk
import glob

total_images = []

# directory of the images
root_dir = r'E:\photos\importantpicture\downloaded images'
for filename in glob.iglob(root_dir + '**/*.jpg', recursive=True):
    total_images.append(filename)
for filename in glob.iglob(root_dir + '**/*.jpeg', recursive=True):
    total_images.append(filename)
for filename in glob.iglob(root_dir + '**/*.png', recursive=True):
    total_images.append(filename)


root = Tk()
root.title('Image Viewer')
#root.iconbitmap('favicon.ico')
root.geometry('700x500')
top = Frame(root)
bottom = Frame(root)
bottom.pack(side=BOTTOM,fill=BOTH,expand=True)

curr_ind = 0

def status():
    global curr_ind
    


def forward():
    global curr_ind,image_label,status_label
    curr_ind+=1
    if curr_ind<0:
        curr_ind = len(total_images)-1
    curr_ind%=len(total_images)
    
    image_label.pack_forget()
    
    new_image = Image.open(total_images[curr_ind])
    copy_of_image = new_image.copy()

    new_image = ImageTk.PhotoImage(new_image)
    image_label = Label(root,image=new_image)
    image_label.pack(fill=BOTH,expand=YES)

    new_width = 680
    new_height = 450
    image = copy_of_image.resize((new_width, new_height))
    photo = ImageTk.PhotoImage(image)
    image_label.configure(image=photo)
    image_label.image = photo
    status_label["text"] = 'Image '+str(curr_ind+1) + ' of '+str(len(total_images))
    
    
def backward():
    global curr_ind
    curr_ind-=2
    forward()
    
    
status_label = Label(root,text='Image '+str(curr_ind+1) + ' of '+str(len(total_images)),relief=SUNKEN) 

my_image = Image.open(total_images[curr_ind])
copy_of_image = my_image.copy()

my_image = ImageTk.PhotoImage(my_image)
image_label = Label(root,image=my_image)
image_label.pack(fill=BOTH,expand=YES)

new_width = 680
new_height = 450
image = copy_of_image.resize((new_width, new_height))
photo = ImageTk.PhotoImage(image)
image_label.configure(image=photo)
image_label.image = photo

btn_forward = Button(root,text = '>>',command=forward)
btn_backward = Button(root,text='<<',command=backward)
btn_forward.pack(in_ =bottom, side=RIGHT,padx=10)
btn_backward.pack(in_ =bottom,side=LEFT,padx=10)
status_label.pack(in_=bottom,side=BOTTOM,ipadx=30,pady=10)

root.mainloop()