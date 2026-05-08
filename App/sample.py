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

'''from nicegui import ui

def siblingW():
    with ui.card().classes('width-1/2') as siblingsWidget:
        def addSibling(i):
            with holderCard:
                row = ui.grid(columns=2).classes('gap-2 w-full')
                with row:ui.label(i);ui.button('',icon='delete',on_click=lambda row=row:holderCard.remove(row)).classes('ml-auto')
        holderCard = ui.card().style('width: 290px;height: 90px;overflow-y: auto;')
        with holderCard:pass
        with ui.grid(columns=2).classes('gap-2 w-full'):
            relationInput = ui.select(['Elder Brother','Elder Sister','Younger Brother','Younger Sister'],value='Elder Brother')
            status = ui.checkbox('Married')
        ui.button('Add',icon='add',on_click=lambda:addSibling(relationInput.value+(' - Married' if status.value else ' - Single'))).style('display:block; margin: 0 auto;')
        def addData(data):
            for i in data:addSibling(i)
        siblingsWidget.addData = addData
        return siblingsWidget

@ui.page('/')
def main():
    siblingsWidget = siblingW()
    ui.button('Apply',on_click=lambda:siblingsWidget.addData(['Elder Brother - Married','Elder Brother - Single','Younger Sister - Single']))
    
ui.run('0.0.0.0',port=80)'''

from cryptography.fernet import Fernet
key = b'nWjYyxV8EC5sbgkOMV_YekqyERDo1j2P4SAA_WNujVI='
cipher = Fernet(key)
print(cipher.encrypt('admin123'.encode()).decode('utf-8'))