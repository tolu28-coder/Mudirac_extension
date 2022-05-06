import tkinter
from tkinter import ttk
from tkinter.filedialog import askopenfilename, askdirectory
import os
from ElementIntensities import Element
import threading


class ScrolledText(tkinter.Frame):
    def __init__(self, parent=None, text=''):
        tkinter.Frame.__init__(self, parent)
        self.make_widgets()
        self.set_text(text)

    def make_widgets(self):
        sbar = tkinter.Scrollbar(self)
        text = tkinter.Text(self, relief=tkinter.SUNKEN)

        sbar.config(command=text.yview)
        text.config(yscrollcommand=sbar.set)

        sbar.pack(side=tkinter.RIGHT, fill=tkinter.Y)
        text.pack(side=tkinter.LEFT, expand=tkinter.YES, fill=tkinter.BOTH)

        self.text = text

    def set_text(self, text=''):
        self.text.delete('1.0', tkinter.END)
        self.text.insert('1.0', text)
        self.text.mark_set(tkinter.INSERT, '1.0')
        self.text.focus()

    def get_text(self):
        return self.text.get('1.0', tkinter.END + '-1c')

    def add_text(self, text):
        self.text.insert(tkinter.END, text)


class MuonicXrayCalculatorGUI(tkinter.Frame):

    def __init__(self, parent=None):
        tkinter.Frame.__init__(self, parent)
        self.parameters_frame = tkinter.Frame(self)
        self.display = ScrolledText(parent=self)
        self.status_label = tkinter.Label(self, text="Ready")
        self.input_file = ""
        self.output_file_directory = ""
        self.is_busy = False
        self.setup_parameters_frame()
        self.display.pack(side=tkinter.TOP)
        self.status_label.pack(side=tkinter.TOP)

    def setup_parameters_frame(self):
        self.top_frame = tkinter.Frame(self.parameters_frame)

        #setup l-distribution option
        self.l_distribution_frame = tkinter.Frame(self.top_frame)
        self.l_distribution_label = tkinter.Label(self.l_distribution_frame, text="L-distribution")
        self.l_distribution_label.pack(side=tkinter.TOP)
        self.l_distribution_combobox = ttk.Combobox(self.l_distribution_frame)
        self.l_distribution_combobox['values'] = ["constant", "linear", "exponential", "quadratic"]
        self.l_distribution_combobox.pack(side=tkinter.TOP)

        #setup choosing file option
        self.choose_file_frame = tkinter.Frame(self.top_frame)
        self.choose_file_button = tkinter.Button(self.choose_file_frame, text="Select Mudirac Input File",
                                                 command=self.choose_file_clicked)
        self.choose_file_button.pack(side=tkinter.TOP)
        self.choose_file_label = tkinter.Label(self.choose_file_frame, text="")
        self.choose_file_label.pack(side=tkinter.TOP)

        #setup save to file option
        self.save_file_frame = tkinter.Frame(self.parameters_frame)
        self.save_file_button = tkinter.Button(self.choose_file_frame, text="Select directory to save output to a file",
                                                 command=self.save_file_clicked)
        self.save_file_button.pack(side=tkinter.TOP)
        self.save_file_label = tkinter.Label(self.choose_file_frame, text="")
        self.save_file_label.pack(side=tkinter.TOP)
        self.save_to_file_output_file_label = tkinter.Label(self.save_file_frame, text=" Output File name")
        self.save_to_file_output_file_label.pack(side=tkinter.TOP)
        self.save_to_file_entry = tkinter.Entry(self.save_file_frame)
        self.save_to_file_entry.pack(side=tkinter.TOP)

        #setup clear button
        self.clear_button = tkinter.Button(self.parameters_frame, text="Clear all parameters",
                                           command=self.clear_clicked)

        self.calculate_button = tkinter.Button(self.parameters_frame, text="Calculate",
                                               command=self.calculate_clicked)

        #adding widgets to GUI
        self.l_distribution_frame.pack(side=tkinter.LEFT)
        self.choose_file_frame.pack(side=tkinter.RIGHT)
        self.top_frame.pack(side=tkinter.TOP)
        self.save_file_frame.pack(side=tkinter.TOP)
        self.clear_button.pack(side=tkinter.TOP)
        self.calculate_button.pack(side=tkinter.TOP)
        self.parameters_frame.pack(side=tkinter.TOP)



    def choose_file_clicked(self):
        self.input_file = askopenfilename()
        self.choose_file_label.configure(text=self.input_file)

    def save_file_clicked(self):
        self.output_file_directory = askdirectory()
        self.save_file_label.configure(text=self.output_file_directory)

    def clear_clicked(self):
        self.output_file_directory = ""
        self.input_file = ""
        self.save_file_label.configure(text=self.input_file)
        self.choose_file_label.configure(text= self.input_file)

    def calculate_clicked(self):
        output_file = ""
        if self.save_to_file_entry.get():
            output_file = os.path.join(self.output_file_directory, self.save_to_file_entry.get() + ".txt")
        function_type = self.l_distribution_combobox.get()
        if self.is_busy:
            return
        else:
            threading.Thread(target=lambda: self.calculate_intensities(function_type, output_file)).start()


    def calculate_intensities(self, function_type, output_file):
        self.is_busy = True
        self.status_label.configure(text="Busy")
        calculator = Element(self.input_file, function_type, 20, 40, 20)
        text = calculator.calculate_intensity(output_file)
        self.display.set_text(text)
        self.status_label.configure(text="Ready")
        self.is_busy = False

