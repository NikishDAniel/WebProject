from nicegui import ui,app,run
import mysql.connector,base64,filetype,asyncio
from cryptography.fernet import Fernet

app.add_static_files('/icons','icons&Images')
fields = ['Name','Profession','Date of birth','Gender','Qualification','Height','Income','Background','Marital Status','Languages Known',"Father's Name","Mother's Name", "Parent's Number",'Whatsapp Number','Family Status','Hometown','Current Resident Address','Siblings','Local Faith Home','Centre Faith Home','Expectations']
key = b'nWjYyxV8EC5sbgkOMV_YekqyERDo1j2P4SAA_WNujVI='
cipher = Fernet(key)

def anyEmptyField(userForm,photo,languages):
    if not photo or not languages:return 1
    index = 0
    for widget in userForm:
        if index!=13 and widget.__class__.__name__ in ['Input','DateInput','Radio','Select','Textarea'] and widget.value in [None,'']:widget.run_method('focus');widget.style('border:2px solid red');return 1
        else:widget.style('border:2px white')
        index += 1

async def emailValidation(email='',check=0):
    container = ui.column()
    def fetchData():
        try:connection = mysql.connector.connect(host='127.0.0.1',user='root',password='Nikish@2003',database='pentecostmatrimony')
        except mysql.connector.Error as error:
            with container:ui.notification(f'Database error: {str(error)}',type='negative')
            return None
        try:
            cursor = connection.cursor()
            cursor.execute('''select email,passwords,role,requestStatus from userData where email = %s''',(email,))
            currentUser = cursor.fetchone()
            cursor.close();connection.close()
        except:currentUser = None
        return currentUser
    if email:
        currentUserData = await run.io_bound(fetchData)
        if check:return not currentUserData==None
        else:return currentUserData
    
def checkUser(data,passwordEntry):
    email,validPassword,role,requestStatus = data
    if cipher.decrypt(validPassword.encode('utf-8')).decode()==passwordEntry:
        if role=='admin':ui.navigate.to('/admin')
        else:
            if requestStatus=='Pending':ui.notification('Your request is pending approval.')
            else:ui.navigate.to(f'/Home/{email}')
    else:ui.notification('Please enter the email and password correctly')

ui.add_head_html('''
                <link rel="preload" href="/icons/ALGERIA.TTF" as="font" type="font/ttf" crossorigin>
                <style>
                @font-face {font-family: AlgerianCustom;src: url('/icons/ALGERIA.TTF');font-display: swap;}
                .algerian-text {font-family: AlgerianCustom;}
                </style>''',shared=1)

def searchWithFields():
    with ui.card().classes('w-fit p-2 h-18 mx-auto').style(f'background-color: #f0f0f0; border-radius: 8px; box-shadow: 0 4px 8px rgba(0, 0, 0, 0.5);'):
        with ui.row().classes('items-center gap-2'):
            searchInput = ui.input(label='Search by Email').style('width:350px')
            with searchInput.add_slot('prepend'):ui.icon('search').classes('text-2xl text-gray-500')
            ui.label('Category').classes('text-gray-500')
            searchField = ui.select(options=['Email']+fields,value='Email',on_change=lambda:searchInput.set_label('Search by '+searchField.value)).style('width:200px')
    return searchInput,searchField

async def scrollableDetailsWidgets(data,refresh=0):
    ui.add_css('''.hover-card {transition: all 0.3s ease;}
               .hover-card:hover {transform: scale(1.03);box-shadow: 0 10px 25px rgba(0,0,0,0.2);}''')
    def showDetails(i,image):
        index = 0
        detailsCard.data = i
        with detailsCard:
            ui.interactive_image(image).classes('w-1/3 h-2/3 object-cover')
            with ui.grid(columns=2).classes('gap-2 w-full'):
                for x in i[4:-2]:
                    ui.label(fields[index]).style('font-size: 24px; font-weight: bold; font-family: Times New Roman; color: #333')
                    ui.label(x).style('font-size: 24px; font-weight: bold; font-family: Times New Roman; color: #333')
                    index += 1
    def assignDetailsUnique(i):
        currentCard = ui.card().classes('w-full aspect-square p-0 overflow-hidden hover-card')
        with currentCard:avatarImage = f"data:image/{filetype.guess(i[1]).mime or 'jpeg'};base64,{base64.b64encode(i[1]).decode()}";ui.image(avatarImage).classes('w-full h-full object-cover')
        currentCard.on('click',lambda i=i:[overCoverCard.set_visibility(1),showDetails(i,avatarImage)])
    masterCard = ui.card().classes('w-full h-screen').style('overflow-y:auto;')
    overCoverCard = ui.card().classes('p-4 w-screen h-full bg-transparent shadow-none border border-gray-300').style('position: absolute; top:0px; left:0px; margin:0; border-radius:0;background-color: white; backdrop-filter: blur(10px); border-radius: 8px; box-shadow: 0 4px 8px rgba(0, 0, 0, 0.5); padding:20px;')
    with overCoverCard:
        with ui.row().classes('w-full justify-center'):currentCardDetails = ui.card().classes('w-1/2 h-screen')
        with currentCardDetails:
            with ui.row().classes('gap-4'):
                ui.button('back',on_click=lambda:[overCoverCard.set_visibility(0),detailsCard.clear()])
                downloadButton = ui.button('download')
        with currentCardDetails:detailsCard = ui.card().classes('w-full h-screen bg-gray-100 rounded-lg shadow-lg p-4').style('overflow-y:auto;');detailsCard.data = None
    overCoverCard.set_visibility(0)
    with masterCard:
        with ui.grid(columns=3).classes('gap-4 w-full') as gridStructure:
            for i in data:assignDetailsUnique(i)
    return masterCard,gridStructure,detailsCard,downloadButton

def form(textColor,bgColor,width='60'):
    ui.add_head_html(f'''<style>.avatar-container:hover .camera-icon {{background: {textColor} !important;color: {bgColor} !important;}}</style>''')
    ui.add_css(f'''
            .dynamic-form .q-field__label {{color: {textColor} !important;}}
            .dynamic-form .q-field__native {{color: {textColor} !important;}}
            .dynamic-form .q-field__control:before {{border-bottom: 1px solid {textColor} !important;}}
            .dynamic-form .q-field__control:after {{border-bottom: 2px solid {textColor} !important;}}
            .dynamic-form .q-field--standard .q-field__control:before {{border-bottom: 1px solid {textColor} !important;}}
            .dynamic-form .q-field__append i {{color: {textColor} !important;}}
            .dynamic-form .q-icon {{color: {textColor} !important;}}
            .dynamic-form .q-radio__label,
            .dynamic-form .q-option-group,
            .dynamic-form .q-select {{color: {textColor} !important;}}''')
    userForm = ui.card().classes(f'dynamic-form w-{width} h-screen text-center').style(f'background-color: {bgColor}; border-radius: 8px; box-shadow: 0 4px 8px rgba(0, 0, 0, 0.5); overflow-y: auto;')
    userForm.photo = None
    userForm.block = None
    with userForm:
        async def savePhoto(e):
            userForm.photo = await e.file.read()
            photoAvatar = base64.b64encode(userForm.photo).decode()
            avatarImage.set_source(f'data:{e.file.content_type};base64,{photoAvatar}')
            upload.reset()
        upload = ui.upload(auto_upload=True,on_upload=savePhoto).props('accept=image/*').style('display:none')
        with ui.element('div').classes('avatar-container relative w-[150px]'):
            with ui.avatar(size='150px').classes('p-0 overflow-hidden cursor-pointer hover:scale-105 transition-transform duration-300') as avatar:avatarImage = ui.image('https://cdn-icons-png.flaticon.com/512/1077/1077114.png').style('width:100%; height:100%; object-fit:cover')
            camera_icon = ui.icon('photo_camera').classes('camera-icon cursor-pointer hover:scale-110').style(f'''position:absolute;bottom:6px;right:6px;background:{bgColor};color:{textColor};border-radius:50%;padding:6px;font-size:20px;transition:0.3s;''')
        avatar.on('click', lambda: upload.run_method('pickFiles'))
        camera_icon.on('click', lambda: upload.run_method('pickFiles'))
        widgets = {'name':['input','Name',''],'profession':['input','Profession',''],'dateOfBirth':['date_input','Date of Birth',''],'gender':['radio','Gender','Male,Female'],'qualification':['input','Qualification',''],'height':['input','Height',''],'income':['input','Income',''],'background':['select','Family Origin','TPM Born,CSI/Other'],
                   'maritalStatus':['radio','Marital Status','Single,Widowed'],'languagesKnown':['language','Languages Known',''],'fatherName':['input','Father Name',''],'motherName':['input','Mother Name',''],'parentsNumber':['input','Parents Number',''],'WhatsAppNumber':['input','WhatsApp Number',''],
                   'familyStatus':['select','Family Status','High Class,Middle Class'],'hometown':['input','Hometown',''],'currentResidentAddress':['textarea','Current Resident Address',''],'siblings':['input','Siblings',''],'localFaithHome':['input','Local Faith Home',''],'centreFaithHome':['input','Centre Faith Home',''],'expectations':['textarea','Expectations','']}
        email = ui.input(label='Email',placeholder='Enter your Email').style(f'margin-top:10px')
        async def checkEmail():
            if await emailValidation(email.value,1):email.style('border:2px solid red');userForm.block = 1
            else:email.style('border:2px solid white');userForm.block = 0
        email.on('blur',checkEmail)
        password = ui.input(label='Password', placeholder='Enter your password', password=1,password_toggle_button=1).style(f'margin-top:10px')
        formWidgets = {}
        for key, (widgetType, label, value) in widgets.items():
            if widgetType in ['input', 'textarea']:widget = getattr(ui, widgetType)(label=label,placeholder=f'Enter your {label}').classes('w-full').style('margin-top:10px')
            elif widgetType == 'language':
                def add_chip():
                    currentLanguage = label_input.value.lower().strip()
                    if currentLanguage in chips.lists:return 1
                    with chips:
                        ui.chip(currentLanguage, icon='label', color='silver', removable=True).on('remove',lambda e:chips.lists.remove(currentLanguage))
                        chips.lists.append(currentLanguage)
                    label_input.value = ''
                label_input = ui.input('Add language').on('keydown.enter', add_chip)
                chips = ui.row().classes('gap-0')
                chips.lists = []
                with chips:pass
            elif widgetType == 'select':options = value.split(',');widget = ui.select(options=options,label=label,value=options[0]).classes('w-full').style('margin-top:10px')
            elif widgetType == 'radio':options = value.split(',');widget = ui.radio(options=options,value=options[0]).props('inline').classes('w-full').style('margin-top:10px')
            else:widget = getattr(ui, widgetType)(label=label).classes('w-full').style('margin-top:10px')
            formWidgets[key] = widget
        return formWidgets,userForm,avatarImage,email,password,chips
    
@ui.page('/test')
def test():
    ui.page_title('Test Page')
    with ui.card().style('width: 320px; height: 200px;'):
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

@ui.page('/admin')
def admin():
    ui.page_title('Admin')
    ui.add_css('''.hover-card {transition: all 0.3s ease;}
               .hover-card:hover {transform: scale(1.03);box-shadow: 0 10px 25px rgba(0,0,0,0.2);}''')
    async def update(email,value):
        try:
            connection = mysql.connector.connect(host='127.0.0.1',user='root',password='Nikish@2003',database='pentecostmatrimony')
            cursor = connection.cursor()
            cursor.execute('''update userData set requestStatus = %s where email = %s''',(value,email))
            connection.commit()
            cursor.close();connection.close()
        except:print('database error')
    async def fetchRequiredData():
        for i in masterLabel.data:
            if i[fields.index(searchField.value)+4].lower()==searchInput.value.lower():
                if type=='All Data':print(i[4:-2])
                else:await assignNewUser(i)
    async def assignNewUser(i):
        currentUserMaster = ui.row().classes('w-full items-center gap-2')
        with currentUserMaster:
            currentUserCard = ui.card().classes('flex-grow w-80 p-4 cursor-pointer')
            currentUserCard.status = 0
            def setStatus(currentUserCard):
                currentUserCard.status = not currentUserCard.status
                details.set_visibility(currentUserCard.status)
            currentUserCard.on('click',lambda:setStatus(currentUserCard))
            with currentUserCard:
                ui.image(f"data:image/{filetype.guess(i[1]).mime or 'jpeg'};base64,{base64.b64encode(i[1]).decode()}").classes('w-38 h-38 rounded-full object-cover')
                ui.label(i[2]).style('font-size: 24px; font-weight: bold; font-family: Times New Roman; color: blue')
                details = ui.grid(columns=2).classes('gap-2 w-full')
                details.set_visibility(False)
                with details:
                    index = 0
                    for data in i[4:-2]:ui.label(fields[index]).style('font-size: 20px; font-weight: bold; font-family: Times New Roman');ui.label(data).classes('break-words').style('font-size: 20px; font-family: Times New Roman');index += 1
            def removeUser():asyncio.create_task(update(i[2],'Rejected'));currentUserMaster.remove(currentUserCard);currentUserMaster.remove(approve);currentUserMaster.remove(reject)
            def updater():
                asyncio.create_task(update(i[2],'Approved'));ui.notification(f'{i[2]} approved successfully!');currentUserMaster.remove(currentUserCard);currentUserMaster.remove(approve)
                if masterLabel.text=='Pending Request Data':currentUserMaster.remove(reject)
            approve = ui.button('Approve',icon='check',on_click=updater).props('rounded outline color=green')
            if masterLabel.text=='Pending Request Data':reject = ui.button('Reject ',icon='clear',on_click=removeUser).props('rounded outline color=red')
    async def allDataRefresh(allDataMaster,i):
        with allDataMaster:
            with ui.card().classes('w-full aspect-square p-0 overflow-hidden hover-card'):
                ui.image(f"data:image/{filetype.guess(i[1]).mime or 'jpeg'};base64,{base64.b64encode(i[1]).decode()}").classes('w-full h-full object-cover')
    async def refreshDataMaster(type,databaseFilter=''):
        try:
            connection = mysql.connector.connect(host='127.0.0.1',user='root',password='Nikish@2003',database='pentecostmatrimony')
            cursor = connection.cursor()
            if type=='All Data':cursor.execute('select * from userData where role="user"')
            else:cursor.execute('select * from userData where requestStatus = %s',(databaseFilter,))
            masterLabel.data = cursor.fetchall()
            cursor.close()
            connection.close()
        except:masterLabel.data = []
        masterLabel.set_text(type)
        requestScrollable.clear()
        with requestScrollable:
            if type=='All Data':
                allDataMaster = ui.grid(columns=3).classes('gap-4 w-full')
                for i in masterLabel.data:await allDataRefresh(allDataMaster,i)
            else:
                for i in masterLabel.data:await assignNewUser(i)
    with ui.row().classes('w-full h-20 items-center'):
        with ui.button(icon='menu'):
            with ui.menu():
                ui.menu_item('All Data', on_click=lambda: asyncio.create_task(refreshDataMaster('All Data'))).props('icon=home')
                ui.menu_item('Pending Request Data', on_click=lambda: asyncio.create_task(refreshDataMaster('Pending Request Data','Pending'))).props('icon=back')
                ui.menu_item('Rejected Request Data', on_click=lambda: asyncio.create_task(refreshDataMaster('Rejected Request Data','Rejected'))).props('icon=menu')
                ui.menu_item('Admin Operation',)
                # ui.menu_item('Married Data',)
        searchInput,searchField = searchWithFields()
        searchInput.on('keydown.enter',fetchRequiredData);searchInput.on('blur',fetchRequiredData)
    with ui.card().classes('w-full h-screen p-4').style('background-color: grey; border-radius: 8px; box-shadow: 0 4px 8px rgba(0, 0, 0, 0.5)'):
        masterLabel = ui.label('All Data').classes('w-full text-center').style('font-size: 30px; font-weight: bold; font-family: Times New Roman; color: black')
        masterLabel.data = []
        requestScrollable = ui.card().classes('w-full h-full').style('max-height:100vh; overflow-y:auto;')
        asyncio.create_task(refreshDataMaster('All Data'))

@ui.page('/register')
def personnelForm():
    ui.page_title('Register Form')
    ui.label('Registration Form').classes('text-center w-full').style('font-size: 28px; font-weight: bold; font-family: Times New Roman; color: #333')
    with ui.column().classes('w-full h-screen items-center justify-center'):widgets,userForm,avatar,email,password,chips = form('#333','#f9f9f9',240)
    async def addData():
        def saveData():
            try:
                connection = mysql.connector.connect(host='127.0.0.1',user='root',password='Nikish@2003',database='pentecostmatrimony')
                cursor = connection.cursor()
                cursor.execute('''insert into userData(Photo,Email,Passwords,Name,Profession,Dob,Gender,Qualification,Height,Income,FamilyOrigin,MaritalStatus,Languages,FatherName,MotherName,ParentsNumber,WhatsAppTelegram,Status,Hometown,CurrentAddress,Siblings,LocalFaithHome,CenterFaithHome,Expectations,requestStatus) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)''',
                            (userForm.photo,email.value,cipher.encrypt(password.value.encode()).decode('utf-8'))+tuple(widgets[x].value if x!='languagesKnown' else ','.join(chips.lists) for x in widgets)+('Pending',))
                connection.commit()
                cursor.close();connection.close()
            except mysql.connector.Error as e:print(e)
        await run.io_bound(saveData)
        ui.notification('Request sent successfully!')
        await asyncio.sleep(0.4)
        ui.navigate.to('/')
    async def handleSubmit():
        if anyEmptyField(userForm,userForm.photo,chips.lists):ui.notification('Please fill all the fields')
        else:
            if userForm.block:ui.notification('This email is already registered. Please use a different email or login.',type='negative')
            else:await addData()
    ui.button('Submit', on_click=handleSubmit).style('display:block; margin: 0 auto;')
    
@ui.page('/Home/{email}')
async def home(email:str):
    ui.page_title('Pentacost Matrimony')
    import random
    verses = {'Genesis 2:18':"The LORD God said, 'It is not good for the man to be alone. I will make a helper suitable for him'",'Mark 10:6-8':"‘made them male and female.For this reason a man will leave his father and mother and be united to his wife,and the two will become one flesh.’",
              'Matthew 19:6':"Therefore what God has joined together, let no one separate.",'Proverbs 5:18':"“He who finds a wife finds what is good and receives favor from the Lord.”",'Proverbs 31:10':"“A wife of noble character who can find? She is worth far more than rubies.”",
              'Ephesians 4:32':"Be kind and compassionate to one another, forgiving each other, just as in Christ God forgave you.",'Colossians 3:14':"And over all these virtues put on love, which binds them all together in perfect unity.",'Colossians 3:19':"Husbands, love your wives and do not be harsh with them.",}
    ui.add_css("""body {background-image: url("/icons/userbg.png");background-size: cover;background-position:top center;background-repeat: no-repeat;height: 100vh;}
               .hover-card {transition: all 0.3s ease;}
               .hover-card:hover {transform: scale(1.03);box-shadow: 0 10px 25px rgba(0,0,0,0.2);}""")
    verseCard = ui.card().classes('w-full p-4').style('background-color: #f0f0f0; border-radius: 8px; box-shadow: 0 4px 8px rgba(0, 0, 0, 0.5); position:relative; overflow:hidden;')
    versesList = list(verses.keys())
    def showVerse():currentVerse = random.choice(versesList);verseLabel.set_text(verses[currentVerse]);verse.set_text(currentVerse)
    with verseCard:
        with ui.row().classes('w-full items-center'):
            verseLabel = ui.label().classes('text-center').style('font-size: 18px; font-style: italic; font-family: Times New Roman; color: black')
            verse = ui.label().classes('text-center').style('font-size: 16px; font-family: Times New Roman; color: blue')
    showVerse()
    ui.timer(5,showVerse)
    async def fetchData():
        connection = mysql.connector.connect(host='127.0.0.1',user='root',password='Nikish@2003',database='pentecostmatrimony')
        cursor = connection.cursor()
        cursor.execute('''select * from userData where email = %s''',(email,))
        data = cursor.fetchone()
        cursor.close();connection.close()
        return data
    data = await fetchData()
    if data is None:ui.navigate.to('/');return
    #ui.label(f'Welcome {data[4]}!').style('font-size: 24px; font-weight: bold; font-family: Times New Roman; color: #333')
    with ui.row().classes('w-full h-20 items-center'):ui.button('Logout', on_click=lambda: ui.navigate.to('/')).props('color=red');searchInput,searchField = searchWithFields()
    with ui.grid().classes('w-full h-screen grid-cols-[300px_1fr] gap-4 items-start') as mainSep:
        widgets,userForm,avatar,emailWidget,password,chips = form('#f9f9f9','#000000','75')
    userForm.photo = data[1]
    avatar.set_source(f"data:image/{filetype.guess(data[1]).mime or 'jpeg'};base64,{base64.b64encode(data[1]).decode()}")
    emailWidget.set_value(email)
    emailWidget.disable()
    password.set_value(cipher.decrypt(data[3].encode('utf-8')).decode())
    index = 4
    def addChips(currentLanguage):ui.chip(currentLanguage, icon='label', color='silver', removable=True).on('remove',lambda e:chips.lists.remove(currentLanguage))
    for i in widgets:
        if index==13:
            chips.lists = data[index].split(',')
            with chips:
                for i in chips.lists:addChips(i)
        else:widgets[i].set_value(data[index])
        index += 1
        if index in [7,8]:widgets[i].disable()
    async def updateData():
        def saveData():
            try:
                connection = mysql.connector.connect(host='127.0.0.1',user='root',password='Nikish@2003',database='pentecostmatrimony')
                cursor = connection.cursor()
                cursor.execute('''update userData set Photo=%s,Email=%s,Passwords=%s,Name=%s,Profession=%s,Dob=%s,Gender=%s,Qualification=%s,Height=%s,Income=%s,FamilyOrigin=%s,MaritalStatus=%s,Languages=%s,FatherName=%s,MotherName=%s,ParentsNumber=%s,WhatsAppTelegram=%s,Status=%s,Hometown=%s,CurrentAddress=%s,Siblings=%s,LocalFaithHome=%s,CenterFaithHome=%s,Expectations=%s,requestStatus=%s where Email=%s''',
                            (userForm.photo,email,cipher.encrypt(password.value.encode()).decode('utf-8'))+tuple(widgets[x].value if x!='languagesKnown' else ','.join(chips.lists) for x in widgets)+('Approved',email))
                connection.commit()
                cursor.close();connection.close()
            except mysql.connector.Error as e:print(e)
        await run.io_bound(saveData)
    async def handleSubmit():
        if anyEmptyField(userForm,userForm.photo,chips.lists):ui.notification('Please fill all the fields')
        else:await updateData();ui.notification('Details updated successfully!')
    ui.button('Update',icon='edit',on_click=handleSubmit)
    async def downloadPdf():
        from fpdf import FPDF,FontFace
        import io
        data = list(detailsCard.data)
        photo = data.pop(1)
        data = data[:1]+data[3:-2]
        pdf = FPDF()
        pdf.add_page()
        pdf.set_font('Times', 'B', 18)
        pdf.cell(0, 0, 'BIODATA', ln=True, align='C')
        pdf.set_font('Times', '', 10)
        pdf.multi_cell(0, 12,'The Lord God said, It is not good that the man should be alone; ''I will make him an help meet for him. - Genesis 2:18',align='C')
        pdf.image(r'icons&Images\logo.png', x=47, y=17, w=22,h=22)
        pdf.set_xy(70,25)
        pdf.set_text_color(10,10,255)
        pdf.add_font('Algerian','B',r'icons&Images\ALGERIA.ttf',uni=True)
        pdf.set_font('Algerian','B',25)
        pdf.cell(0,5,'TPM MATRIMONY',ln=True)
        pdf.line(10, 39, 200, 39)
        pdf.image(io.BytesIO(photo), x=3, y=43, w=80,h=100,type=filetype.guess(photo).mime or 'jpeg')
        pdf.set_text_color(0,0,0)
        pdf.set_xy(85,42)
        pdf.set_font('Arial','',11)
        updatedFields = ['Reg.No.']+fields
        with pdf.table(width=120,col_widths=(40,90),align="L") as holderTable:
            for i in range(len(data)):
                currentRow = holderTable.row()
                if i==0:headerStyle = FontFace(emphasis="ITALICS",color=(255,255,255),fill_color=(10, 10, 255))
                else:headerStyle = FontFace(color=(0,0,0))
                currentRow.cell(updatedFields[i],style=headerStyle);currentRow.cell(str(data[i]),style=headerStyle)
        y = pdf.get_y()+2
        pdf.line(10, y, 200, y)
        pdf.write_html('<p align="center">Clarification on your biodata to any of these nos. <b>Bro. D. Annadoss</b> (Telegram no. 9884153831), <b>Bro. Sekar</b> (Telegram no. 9940408879) for TPM Matrimony.</p>')
        pdfBytes = bytes(pdf.output(dest='S'))
        ui.download(pdfBytes,filename=f'{data[1]}_biodata.pdf')
    async def assignUsers():
        dob,gender = data[6],data[7]
        async def search():
            try:connection = mysql.connector.connect(host='127.0.0.1',user='root',password='Nikish@2003',database='pentecostmatrimony')
            except mysql.connector.Error as error:return None
            fieldValue = searchInput.value
            try:
                cursor = connection.cursor()
                query = f'''select * from userData where Dob BETWEEN {f'date_add("{dob}", INTERVAL 0 YEAR) AND date_add("{dob}", INTERVAL 5 YEAR)' if gender=='Male' else f'date_sub("{dob}", INTERVAL 5 YEAR) AND date_sub("{dob}", INTERVAL 0 YEAR)'} and requestStatus = %s and Gender = %s'''
                if fieldValue=='':cursor.execute(query,('Approved','Female' if gender=='Male' else 'Male',))
                else:cursor.execute(query+f' and {searchField.value} = %s',('Approved','Female' if gender=='Male' else 'Male',fieldValue,))
                result = cursor.fetchall()
                cursor.close();connection.close()
            except:result = []
            return result
        with mainSep:
            masterCard,gridStructure,detailsCard,downloadButton = await scrollableDetailsWidgets(await search())
            
    await assignUsers()
    searchInput.on('keydown.enter',lambda x:assignUsers())
    searchInput.on('blur',lambda x:assignUsers())

@ui.page('/')
def login():
    ui.page_title('Login Page')
    ui.add_css('''body {background-image: url("/icons/image1.png");background-size: cover;background-position:top center;background-repeat: no-repeat;height: 100vh;}
               .white-input .q-field__label {color: white !important;}
               .white-input .q-field__native {color: white !important;}
               .white-input .q-field__control:before {border-bottom: 1px solid white !important;}
               .white-input .q-field__control:after {border-bottom: 2px solid white !important;}
               .white-input .q-field__append .q-icon {color: white !important;}
               .white-input .q-field__append .q-icon:hover {color: grey !important;}''')
    with ui.column().classes('w-full h-screen items-center justify-center overflow-hidden'):
        with ui.card().classes('md:w-1/3 lg:w-1/4 p-6').style('background-color: rgba(0, 0, 0, 0.6); backdrop-filter: blur(8px); border-radius: 10px; box-shadow: 0 4px 8px rgba(0, 0, 0, 0.5);'):
            ui.label('Login to your Account').classes('text-center w-full').style('font-size: 28px; font-weight: bold; font-family: Times New Roman; color: white')
            currentUser = ui.input('Email', placeholder='Enter your email').classes('white-input w-full')
            password = ui.input('Password', placeholder='Enter your password', password=1,password_toggle_button=1).classes('white-input w-full')
            async def handleLogin():
                data = await emailValidation(currentUser.value)
                if data:checkUser(data, password.value)
                else:ui.notification('No account found with this email. Please register first.',close_button=True,type='negative')
            ui.button('Sign in',on_click=handleLogin,icon='login',color='red').classes('w-full')
            ui.link('Register',target='/register')
    ui.button('Try',on_click=lambda:ui.navigate.to('/test'))

ui.run(host='0.0.0.0', port=80)