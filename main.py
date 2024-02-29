from tkinter import *
from PIL import Image, ImageTk
from tkinter import filedialog, messagebox
import re
import PyPDF2
import summa
import googletrans

url = 'C:/Users/yaman/PycharmProjects/marathi_pdf.py/garden.jpg'


class uploading_file:
    def __init__(self):
        self.eng_scroll = None
        self.tk = None
        self.upload_text = None
        self.summary_text = None
        self.translator = None
        self.num_pages = None
        self.pdf_text = ""
        self.words = ""
        self.summary = ""

    def upload_pdf(self, file_path):
        """Uploads a PDF document to a server.
      Args:
        file_path: The path to the PDF document."""

        # Create a PDF reader object.
        pdf_reader = PyPDF2.PdfReader(file_path)

        # Get the number of pages in the PDF document.
        self.num_pages = len(pdf_reader.pages)

        # Create a PDF writer object.
        pdf_writer = PyPDF2.PdfWriter()

        # Iterate over the pages in the PDF document and add them to the PDF writer object.
        for page_num in range(self.num_pages):
            page = pdf_reader.pages[page_num]
            pdf_writer.add_page(page)

            # extract text from pdf file
        # self.pdf_text = ""
        for page in pdf_reader.pages:
            self.pdf_text += page.extract_text()

        # Convert the text to lowercase.
        text = self.pdf_text.lower()

        # Remove punctuation.
        text = re.sub(r'[^\w\s]', '', text)

        # Split the text into words.
        self.words = text.split()
        self.words = set(self.words)

        # Join the text from all pages into a single string
        new_text = ''.join(self.pdf_text)

        # Summarize the text
        self.summary = summa.summarizer.summarize(new_text, ratio=0.2)

        # Insert data in Text Widget
        self.summary_text.insert(END, self.summary)
        self.upload_text.insert(END, self.words)

        # Write the PDF document to a file on the server.
        with open('uploaded_pdf.pdf', 'wb') as f:
            pdf_writer.write(f)
            return True

    # Browse PDF File and call upload_pdf()
    def upload_filepath(self):
        file_path = filedialog.askopenfilename(title="Select PDF File", filetypes=[("PDF Files", "*.pdf")])
        open(file_path, 'r')
        self.upload_pdf(file_path)

    @staticmethod
    def on_timeout(self):
        messagebox.showerror("time out")
        self.tk.destroy()

    def language_translate(self):

        english_label = Label(self.tk, text="English Summary", bg="#004526", fg="white", height=4, width=20,
                              font=("Helvetica", 14))
        english_label.place(x=300, y=590)

        # Create a Textarea to display english summary
        english_text = Text(self.tk, width=100, relief="solid")
        english_text.place(x=700, y=560)

        english_text.configure(yscrollcommand=self.eng_scroll.set, width=80, height=10)
        english_text.place(x=700, y=560)

        # Add Scrollbar to move english summary up and down
        self.eng_scroll.config(command=english_text.yview)
        self.eng_scroll.place(x=700, y=200)

        # Split the text into smaller chunks

        chunks = [self.summary[i:i + 500] for i in range(0, len(self.summary), 500)]

        # Translate each chunk
        translated_chunks = []
        for chunk in chunks:
            translation = self.translator.translate(chunk, dest='en')
            translated_chunks.append(translation.text)

        # Join the translated chunks back together
        translated_text = ''.join(translated_chunks)
        english_text.insert(END, translated_text)
        try:
            self.tk.after(2)
        except:
            self.on_timeout(self)

    def gui_func(self):
        # Initialize object
        self.translator = googletrans.Translator()

        # Initialize tkinter object
        self.tk = Tk()
        self.tk.title("Upload PDF Files")
        # Get screen resolution
        width = self.tk.winfo_screenwidth()
        height = self.tk.winfo_screenheight()
        self.tk.geometry("%dx%d" % (width, height))
        #  Initialize scrollbar objects
        scrollbar = Scrollbar(self.tk)
        scrollbar.config(orient=VERTICAL)

        scroll = Scrollbar(self.tk)
        scroll.config(orient=VERTICAL)

        self.eng_scroll = Scrollbar(self.tk)
        self.eng_scroll.config(orient=VERTICAL)

        # Resize the image to fit the screen
        image = Image.open(url)
        # "C:/Users/yaman/OneDrive/Documents/internshala/marathi_pdf/green.jpg"
        image = image.resize((width, height))

        # Convert the image to a PhotoImage object
        photo_image = ImageTk.PhotoImage(image)

        # Create a label to display the image
        img_label = Label(self.tk, image=photo_image)

        # Place the label in the window
        img_label.place(x=0, y=0)

        # Create a button to upload PDF File
        upload_button = Button(self.tk, text="Upload", bg="#004526", fg="White", command=lambda: self.upload_filepath(),
                               height=2, width=11,
                               font=("Helvetica", 14))
        upload_button.place(x=550, y=100)

        # Create a label for summary
        summary_label = Label(self.tk, text="Summary", bg="#004526", fg="white", height=4, width=20,
                              font=("Helvetica", 14))
        summary_label.place(x=300, y=250)

        # Create a Textarea to display summary
        self.summary_text = Text(self.tk, width=100, relief="solid")
        self.summary_text.place(x=700, y=200)

        self.summary_text.configure(yscrollcommand=scrollbar.set, width=80, height=10)
        self.summary_text.place(x=700, y=200)

        # Add Scrollbar to move summary up and down
        scrollbar.config(command=self.summary_text.yview)
        scrollbar.place(x=700, y=200)

        # Create a label for Keywords
        upload_label = Label(self.tk, text="Keywords", bg="#004526", fg="white", height=4, width=20,
                             font=("Helvetica", 14))
        upload_label.place(x=300, y=420)

        # Create a Textarea to display Keywords
        self.upload_text = Text(self.tk, width=10, relief="solid", height=8)
        self.upload_text.place(x=700, y=380)

        self.upload_text.configure(yscrollcommand=scroll.set, width=80, height=10)
        self.upload_text.place(x=700, y=380)

        # Add Scrollbar to move Keywords up and down
        scroll.config(command=self.upload_text.yview)
        scroll.place(x=700, y=380)

        translate_button = Button(self.tk, text="Translate", bg="#004526", fg="white",
                                  command=lambda: self.language_translate(), height=2, width=11,
                                  font=("Helvetica", 14))
        translate_button.place(x=800, y=100)

        mainloop()


if __name__ == "__main__":
    upload = uploading_file()
    upload.gui_func()
