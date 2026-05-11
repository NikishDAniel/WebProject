# from fpdf import FPDF,FontFace
# pdf = FPDF()
# pdf.add_page()
# pdf.set_font('Times', 'B', 18)
# pdf.cell(0, 0, 'BIODATA', ln=True, align='C')
# pdf.set_font('Times', '', 10)
# pdf.multi_cell(0, 12,'The Lord God said, It is not good that the man should be alone; ''I will make him an help meet for him. - Genesis 2:18',align='C')
# pdf.image(r'icons&Images\logo.png', x=47, y=17, w=22,h=22)
# pdf.set_xy(70, 25)
# pdf.set_text_color(10, 10, 255)
# pdf.add_font('Algerian', 'B', r'icons&Images\ALGERIA.ttf', uni=True)
# pdf.set_font('Algerian', 'B', 25)
# pdf.cell(0, 5, 'TPM MATRIMONY', ln=True)
# pdf.line(10, 39, 200, 39)
# fields = ['Reg.No.','Email','Password','Name','Profession','Date of birth','Gender','Qualification','Height','Income','Background','Marital Status','Languages Known',"Father's Name","Mother's Name", "Parent's Number",'Whatsapp Number','Family Status','Hometown','Current Resident Address','Siblings','Local Faith Home','Centre Faith Home','Expectations']
# data = ['16','nikishdaniel77@gmail.com','gAAAAABp2gGzRJgB5MEuztLXF7ZA2k960NEwkevstsBfAckNzsfGYEBGrRt9OIbiUMq7ru4U1WN4gkdZFL9t_ZjH_fLJCJAwEw==', 'Nikish', 'IT', '2003-12-03', 'Male', 'B.Tech', '174', '20000', 'CSI/Other', 'Single', 'tamil,english,japanese', 'Yosuva', 'Rani', '5678', '9789', 'Middle Class', 'Madurai', '12...', '1', 'TELC', 'TELC', 'None']
# pdf.set_text_color(0,0,0)
# pdf.set_xy(10,42)
# pdf.set_font('Arial','',10)
# with pdf.table(width=120,col_widths=(30,80),align="L") as holderTable:
#     for i in range(len(data)):
#         currentRow = holderTable.row()
#         if i==0:headerStyle = FontFace(emphasis="ITALICS",color=(255,255,255),fill_color=(10, 10, 255))
#         else:headerStyle = FontFace(color=(0,0,0))
#         currentRow.cell(fields[i],style=headerStyle);currentRow.cell(data[i],style=headerStyle)
# y = pdf.get_y()+2
# pdf.line(10, y, 200, y)
# pdf.write_html('<p align="center">Clarification on your biodata to any of these nos. <b>Bro. D. Annadoss</b> (Telegram no. 9884153831), <b>Bro. Sekar</b> (Telegram no. 9940408879) for TPM Matrimony.</p>')
# pdf.output('biodata.pdf')


from nicegui import ui

@ui.page('/')
def main_page():
    ui.dark_mode().enable()
    ui.label('Hello, World!')

ui.run()