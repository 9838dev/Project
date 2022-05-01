# Tools required to run the code
# Modules: tkinter,matplotlib,pandas,seaborn, requests

#%matplotlib qt
from tkinter import * 
from tkinter import filedialog,messagebox,ttk
import pandas as pd
from tkinter import Toplevel
import matplotlib.pyplot as plt
import seaborn as sns
import requests
import tkinter as tk

class Excel_Import:
    def __init__(self):
        self.root = Tk()
        self.root.geometry("500x500")
        self.root.title("Excel Data")
        
        # prevents resizing of frame from widget
        self.root.pack_propagate(False)
        # prevents resizing of window
        self.root.resizable(0,0)
        
        # Label Frame where Data Is shown
        frame1 = LabelFrame(self.root,text='Exel Data')
        frame1.place(height=300,width=500)
        
        # Label Frame where we can perform some operation
        file_frame = LabelFrame(self.root,text='Open File')
        file_frame.place(height=150,width=500,rely=0.65)
        
        # Buttons

        load = Button(file_frame,text='Browse A File',command=lambda: self.file_dialog())
        load.place(relx=0.2,rely=0.65)

        self.tool = Button(file_frame,text='Tools',state=DISABLED,command=lambda: self.open_statistical_tools())
        self.tool.place(relx=0.82,rely=0)
        
        self.api_button = Button(file_frame,text='Load From API',command=lambda: self.get_api())
        self.api_button.place(relx=0.5,rely=0.65)

        self.plot = Button(file_frame,text='Plot a Graph',state=DISABLED,command=lambda: self.open_graph_plotting())
        self.plot.place(relx=0.77,rely=0.35)

        self.label_file = ttk.Label(file_frame,text='No File Selected')
        self.label_file.place(relx=0,rely=0)
        
        # Tree View
        self.tv1 = ttk.Treeview(frame1)
        self.tv1.place(relheight=1,relwidth=1)
        
        # Scroll Bar
        treescrolly = Scrollbar(frame1,orient='vertical',command=self.tv1.yview)
        treescrollx = Scrollbar(frame1,orient='horizontal',command=self.tv1.xview)
        
        self.tv1.configure(xscrollcommand=treescrollx.set,yscrollcommand=treescrolly.set)
        treescrollx.pack(side='bottom',fill='x')
        treescrolly.pack(side='right',fill='y')
        
        self.root.mainloop()
        
    # Select file from storage
    def file_dialog(self):
        
        # In initialdir select your own default path
        # Only accessable file is .csv
        self.filename = filedialog.askopenfilename(initialdir='F:\pdf',
                                         title='Select a file',
                                         filetype=(('csv file',"*.csv"),("All file","*.*")))
        ShowFileName = self.filename.split('/')
        self.label_file['text'] = ShowFileName[-1]
        self.load_excel_data()
    
    # Showing chossen file
    def load_excel_data(self,file_name = None):
        if file_name == None:
            file_path = self.filename
            try:
                excel_filename = r"{}".format(file_path)
                self.df=pd.read_csv(excel_filename)
            except ValueError:
                messagebox.showerror("Infomation","Choosen File is invalid")
                return 
            except FileNotFoundError:
                messagebox.showerror("Information",f"No such file as {file_path}")
                return

        self.clear_data(self.tv1)
        self.tv1['column'] = list(self.df.columns)
        self.tv1["show"] = "headings"
        for column in self.tv1['columns']:
            self.tv1.heading(column,text=column,anchor=CENTER)
            self.tv1.column(column,anchor='n')

        df_rows = self.df.to_numpy().tolist()
        for row in df_rows:
            self.tv1.insert("","end",value=row)

        self.tool['state'] = NORMAL
        self.plot['state'] = NORMAL
    
    def get_api(self):
        self.api_win = Tk()
        self.api_win.geometry("300x100")
        self.api_win.title('Enter API')

        label = Label(self.api_win,text='Enter URL::')
        label.grid(row=0,column=0)

        self.url = tk.Entry(self.api_win,borderwidth=3)
        self.url.grid(row=0,column=1)

        Button(self.api_win,text='Save',command=self.api_data).grid(row=1,column=1)
        self.api_win.mainloop()
    
    def api_data(self):
        try:    
            response = requests.get(self.url.get())
            self.df = pd.json_normalize(response.json())
            self.label_file['text'] = "Api Data"
            self.load_excel_data("data from api")
        except Exception as e:
            messagebox.showerror("Error","Invalid API")
        finally:
            self.api_win.destroy()
    
    def clear_data(self,tree_view):
        tree_view.delete(*tree_view.get_children())
        
    def open_statistical_tools(self):
        Statistical_Operation(self.df)
        
    def open_graph_plotting(self):
        Graph_Operation(self.df)
        
        
class Statistical_Operation:
    def __init__(self,df):
        self.df = df
        
        # Create another window
        self.stats_tools = Toplevel()
        self.stats_tools.geometry("650x650")
        self.stats_tools.title("Basic Statistics")
        
        # prevents resizing of frame from widget and resizing of window 
        self.stats_tools.pack_propagate(False)
        self.stats_tools.resizable(0,0)

        select_frame = LabelFrame(self.stats_tools,text = "Select Tools")
        select_frame.place(width=200,height=150)
        
        self.about_data_frame = LabelFrame(self.stats_tools,text='About Data')
        self.about_data_frame.place(width=200,height=150,relx=0.4)
        
        output_frame = LabelFrame(self.stats_tools,text = "Output")
        output_frame.place(width=650,height=370,rely=0.4)

    
        # select frame
        
        # Create Option Menu for method
        options = ["Describe","Mean","Median","Mode"]
        self.tool = StringVar()
        self.tool.set(options[0])
        all_option = OptionMenu(select_frame,self.tool,*options)
        all_option.place(relx=0.2,rely=0.1)
        
        # Create Option Menu for selection of column
        columns =  ['All']
        for col in self.df.columns:
            if self.df[col].dtype == 'int64' or self.df[col].dtype == 'float64' or self.df[col].dtype == 'int32' or self.df[col].dtype == 'float32':
                columns.append(col)

        self.column = StringVar()
        self.column.set(columns[0])
        all_option = OptionMenu(select_frame,self.column,*columns)
        all_option.place(relx=0.3,rely=0.4)

        btn1 = Button(select_frame,text='Apply',command = lambda: self.get_selected_data())
        btn1.pack(side="bottom")

        # output frame
        
        self.output = ttk.Treeview(output_frame)
        self.output.place(relheight=1,relwidth=1)
        
        # ScrollBar for output Frame
        output_treescrollx = Scrollbar(output_frame,orient='horizontal',command = self.output.xview)
        output_treescrolly = Scrollbar(output_frame,orient='vertical',command=self.output.yview)

        self.output.configure(xscrollcommand=output_treescrollx.set,yscrollcommand=output_treescrolly.set)

        output_treescrollx.pack(side='bottom',fill='x')
        output_treescrolly.pack(side='right',fill='y')

        # about_data Frame
        methods = ['Shape','Description','DataTypes','ValuesCount']
        self.method = StringVar()
        self.method.set(methods[0])
        show_methods = OptionMenu(self.about_data_frame,self.method,*methods,command=self.show_optionsMenu)
        show_methods.pack(side='top')

        btn2 = Button(self.about_data_frame,text='Show',command=lambda: self.get_methods())
        btn2.pack(side='bottom')
    
    # From Select Frame
    # get  all the options selected
    def get_selected_data(self):
        get_tools = self.tool.get()
        get_column = self.column.get()

        if get_column == 'All':
            if get_tools == 'Describe':
                self.tools_show_data(list(self.df.columns),["","Mean","Median","Mode"])
            else:
                self.tools_show_data(list(self.df.columns),["",get_tools])
        else:
            if get_tools == 'Describe':
                self.tools_show_data([get_column],["","Mean","Median","Mode"])
            else:
                self.tools_show_data([get_column],["",get_tools])
    
    def tools_show_data(self,row,columns):
        self.clear_output()
        self.output['column'] = columns
        self.output['show'] = "headings"
        
        for col in self.output['columns']:
            self.output.heading(col,text=col,anchor=CENTER)
            self.output.column(col,anchor='n')
        
        # Creating row from selected options
        create_row = []
        if columns[1] == "Mode":
            for r in row:
                create_row.append([r,self.df[r].mode()[0]])
        elif len(columns) == 2:
            if columns[1] == "Mean":
                for r in row:
                    if self.df[r].dtype == 'int64' or self.df[r].dtype == 'float64' or self.df[r].dtype == 'int32' or self.df[r].dtype == 'float32':
                        create_row.append([r,self.df[r].mean()])
            else:
                for r in row:
                    if self.df[r].dtype == 'int64' or self.df[r].dtype == 'float64' or self.df[r].dtype == 'int32' or self.df[r].dtype == 'float32':
                        create_row.append([r,self.df[r].median()])
        else:
            for r in row:
                if r == 'All':
                    continue
                li = []
                li.append(r)
                if self.df[r].dtype == 'int64' or self.df[r].dtype == 'float64' or self.df[r].dtype == 'int32' or self.df[r].dtype == 'float32':
                        li.append(self.df[r].mean())
                        li.append(self.df[r].median())
                else:
                    li.append('-')
                    li.append('-')
                li.append(self.df[r].mode()[0])
                create_row.append(li)

        for r in create_row:
            self.output.insert("","end",value=r)
    
    # About Frame
    # if selected option is ValuesCount 
    # then show all the column
    def show_optionsMenu(self,event):
        if self.method.get() == 'ValuesCount':
            options = list(self.df.columns)
            self.option = StringVar()
            self.option.set(options[0])

            self.opt = OptionMenu(self.about_data_frame,self.option,*options)
            self.opt.pack(side='top')
        else:
            try:
                self.opt.pack_forget()
            except AttributeError:
                pass
            
    def get_methods(self):
        self.clear_output()
        curr_method = self.method.get()
    
        if curr_method == 'Shape':
            self.output['column'] = ["","row","column"]
            self.output['show'] = "headings"
            row,column = self.df.shape
            for col in self.output['columns']:
                self.output.heading(col,text=col,anchor=CENTER)
                self.output.column(col,anchor='n')

            self.output.insert("","end",value=['Total',row,column])
            
        elif curr_method == 'Description':
            curr_df = self.df.describe()

            self.output['column'] = [""] + list(curr_df.columns)
            self.output['show'] = 'headings'
            for col in self.output['columns']:
                self.output.heading(col,text=col,anchor=CENTER)
                self.output.column(col,anchor='n')

            rows = curr_df.to_numpy().tolist()
            index = curr_df.index
            j=0
            for r in rows:
                self.output.insert("",'end',value=[index[j]]+r)
                j+=1
        elif curr_method == 'DataTypes':
            self.output['column'] = ["Row","Datatype"]
            self.output['show'] = "headings"
            for col in self.output['columns']:
                self.output.heading(col,text=col,anchor=CENTER)
                self.output.column(col,anchor='n')

            for r in self.df.columns:
                self.output.insert("","end",value=[r,self.df[r].dtype])
        elif curr_method == 'ValuesCount':
            
            self.output['column'] = ["value","counts"]
            self.output['show'] = "headings"
            for col in self.output["columns"]:
                self.output.heading(col,text=col,anchor=CENTER)
                self.output.column(col,anchor='n')

            rows = self.df[self.option.get()].value_counts()
            ind = rows.index
            for i,row in enumerate(rows):
                self.output.insert("","end",value=[ind[i],row])
        
    def clear_output(self):
        self.output.delete(*self.output.get_children())
        
        
class Graph_Operation:
    def __init__(self,df):
        self.df = df
        self.graph_uncountable = ['boxplot','lineplot','scatterplot']
        self.graph_countable = ['bar','pie']
        self.types = ['countable','uncountable']
        
        # New window configuration
        self.graph_level = Toplevel()
        self.graph_level.geometry("300x300")
        self.graph_level.title("Plotting Graphs")
        self.graph_level.pack_propagate(False)
        self.graph_level.resizable(0,0)

        self.total_text = list(self.df.columns)
        
        # Create a option of type of data and command for switching the type
        self.set_type = StringVar()
        self.set_type.set(self.types[0])
        type_select = OptionMenu(self.graph_level,self.set_type,*self.types,command=self.set_graph_type)
        type_select.place(relx=0.1,rely=0)
        
        # create a option for countable
        self.graph_select = StringVar()
        self.graph_select.set(self.graph_countable[0])
        self.graph_select_options = OptionMenu(self.graph_level,self.graph_select,*self.graph_countable)
        self.graph_select_options.place(relx=0.5,rely=0)
        
        # create a 2 variable for 2 text 
        self.select_text1 = StringVar()
        self.select_text2 = StringVar()
        
        # create a Option for text1
        self.select_text1.set(self.total_text[0])
        self.text1_options = OptionMenu(self.graph_level,self.select_text1,*self.total_text)
        self.text1_options.place(relx=0.35,rely=0.2)

        plot = Button(self.graph_level,text='Plot a graph',command=self.plot_graph)
        plot.pack(side='bottom')

    def set_graph_type(self,event):
        
        # Remove graph options and text1_options
        self.graph_select_options.place_forget()
        self.text1_options.place_forget()
        
        # for uncountable data we take two column from user
        if self.set_type.get() == 'uncountable':
            
            # Create options for selection of uncountable 
            self.graph_select.set(self.graph_uncountable[0])
            
            self.graph_select_options = OptionMenu(self.graph_level,self.graph_select,*self.graph_uncountable)
            self.graph_select_options.place(relx=0.5,rely=0)
            
            # text option 1 
            self.select_text1.set(self.total_text[0])
            
            self.text1_options = OptionMenu(self.graph_level,self.select_text1,*self.total_text)
            self.text1_options.place(relx=0.25,rely=0.2)
            
            # text option 2
            self.select_text2.set(self.total_text[1])
            
            self.text2_options = OptionMenu(self.graph_level,self.select_text2,*self.total_text)
            self.text2_options.place(relx=0.30,rely=0.3)

        else:
            # remove text2_options if available
            try:
                self.text2_options.place_forget()
            except AttributeError:
                pass
            
            # Create options for selection of countable 
            self.graph_select.set(self.graph_countable[0])
            
            self.graph_select_options = OptionMenu(self.graph_level,self.graph_select,*self.graph_countable)
            self.graph_select_options.place(relx=0.5,rely=0)
            
            # text option 1
            
            self.select_text1.set(self.total_text[0])
            self.text1_options = OptionMenu(self.graph_level,self.select_text1,*self.total_text)
            self.text1_options.place(relx=0.35,rely=0.2)
            
            
    def plot_graph(self):
        # Plot of countable
        
        if self.set_type.get() == 'countable':
            
            # Plotting Bar graph
            if self.graph_select.get() == 'bar':
                sns.countplot(x=self.select_text1.get(),data=self.df)
                plt.show()
                
            # Plotting Pie Chart
            elif self.graph_select.get() == 'pie':
                data = self.df[self.select_text1.get()].value_counts()
                plt.pie(x=data,labels=data.index,autopct='%1.1f%%',shadow=True)
                plt.show()
        
        # Plot for Uncountable
        elif self.set_type.get() == 'uncountable':
            
            # Plotting BoxPlot
            if self.graph_select.get() == 'boxplot':
                sns.boxplot(x=self.select_text1.get(), y=self.select_text2.get(),data=self.df)
                plt.show()

            # Plotting Line Graph
            elif self.graph_select.get() == 'lineplot':
                sns.lineplot(x=self.select_text1.get(), y=self.select_text2.get(),data=self.df)
                plt.show()

            # Plotting ScatterPlot
            elif self.graph_select.get() == 'scatterplot':
                sns.scatterplot(x=self.select_text1.get(), y=self.select_text2.get(),data=self.df)
                plt.show()

# Main function
if __name__ == '__main__':
    obj = Excel_Import()