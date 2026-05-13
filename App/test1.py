from nicegui import ui,app,run
import mysql.connector,base64,filetype,asyncio
from cryptography.fernet import Fernet

app.add_static_files('/icons','icons&Images')   # adds floder into the ui
fields = ['Name','Profession','Date of birth','Gender','Qualification','Height','Income','Background','Marital Status','Languages Known',"Father's Name","Mother's Name", "Parent's Number",'Whatsapp Number','Family Status','Hometown','Current Resident Address','Siblings','Local Faith Home','Centre Faith Home','Expectations']
key = b'nWjYyxV8EC5sbgkOMV_YekqyERDo1j2P4SAA_WNujVI='
cipher = Fernet(key)

# checks whether all the feilds in the form are filled or not
def anyEmptyField(userForm,photo,languages):
    if not photo or not languages:return 1
    index = 0
    for widget in userForm:
        if index!=13 and widget.__class__.__name__ in ['Input','DateInput','Radio','Select','Textarea'] and widget.value in [None,'']:widget.run_method('focus');widget.style('border:2px solid red');return 1
        else:widget.style('border:2px white')
        index += 1

# fn to fetch admin data
async def fetchAdmin():
    try:
        connection = mysql.connector.connect(host='127.0.0.1',user='root',password='Nikish@2003',database='pentecostmatrimony')
        cursor = connection.cursor()
        cursor.execute('''select id,email,passwords,name,profession,WhatsAppTelegram from userData where role = "admin"''')
        result = cursor.fetchall()
        return result
    except mysql.connector.Error as error:return None

# fn to verify the email at the time of login
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
    
# checks the match of the password
def checkUser(notifier,data,passwordEntry):
    email,validPassword,role,requestStatus = data
    if cipher.decrypt(validPassword.encode('utf-8')).decode()==passwordEntry:
        if role=='admin':ui.navigate.to('/admin')
        else:
            if requestStatus=='Pending':notifier.message='Your request is still pending';notifier.type='warning';notifier.spinner=False;notifier.timeout=2
            elif requestStatus=='Rejected':notifier.message='Your request is rejected';notifier.type='negative';notifier.spinner=False;notifier.timeout=2
            else:notifier.message='Login successful!';notifier.type='positive';notifier.spinner=False;notifier.timeout=2;ui.navigate.to(f'/Home/{email}')
    else:notifier.message='Please enter the email and password correctly';notifier.type='negative';notifier.spinner=False;notifier.timeout=2

ui.add_head_html('''
                <link rel="preload" href="/icons/ALGERIA.TTF" as="font" type="font/ttf" crossorigin>
                <style>
                @font-face {font-family: AlgerianCustom;src: url('/icons/ALGERIA.TTF');font-display: swap;}
                .algerian-text {font-family: AlgerianCustom;}
                </style>''',shared=1)

# custom search widget
def searchWithFields():
    with ui.card().classes('w-fit p-2 h-18 mx-auto').style(f'background-color: #f0f0f0; border-radius: 8px; box-shadow: 0 4px 8px rgba(0, 0, 0, 0.5);'):
        with ui.row().classes('items-center gap-2'):
            searchInput = ui.input(label='Search by Id').style('width:350px')
            with searchInput.add_slot('prepend'):ui.icon('search').classes('text-2xl text-gray-500')
            ui.label('Category').classes('text-gray-500')
            searchField = ui.select(options=['Id','Email']+fields,value='Id',on_change=lambda:searchInput.set_label('Search by '+searchField.value)).style('width:200px')
    return searchInput,searchField

# testrun in sample.py
def siblingsWidget():
    ui.add_css(f'''.sibling-widget .q-field__label,.sibling-widget .q-field__native,.sibling-widget .q-icon,.sibling-widget .q-checkbox__label,.sibling-widget .q-select {{color: black  !important;}}''')
    with ui.card().classes('w-full h-[40%] sibling-widget') as siblingsWidgets:
        def addSibling(i):
            with holderCard:
                row = ui.grid(columns=2).classes('gap-2 w-full')
                with row:ui.label(i);ui.button('',icon='delete',on_click=lambda row=row:holderCard.remove(row)).classes('ml-auto')
        holderCard = ui.card().classes('w-full h-[40%] overflow-auto')
        with holderCard:pass
        with ui.grid(columns=2).classes('gap-2 w-full'):
            relationInput = ui.select(['Elder Brother','Elder Sister','Younger Brother','Younger Sister'],value='Elder Brother').props('outlined')
            status = ui.checkbox('Married')
        ui.button('Add',icon='add',on_click=lambda:addSibling(relationInput.value+(' - Married' if status.value else ' - Single'))).style('display:block; margin: 0 auto;')
        def addData(data):
            for i in data:addSibling(i)
        siblingsWidgets.addData = addData
        return siblingsWidgets,holderCard

# registration and user form
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
            .dynamic-form .q-select {{color: black  !important;}}''')
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
                   'familyStatus':['select','Family Status','High Class,Middle Class'],'hometown':['input','Hometown',''],'currentResidentAddress':['textarea','Current Resident Address',''],'siblings':['siblings','Siblings',''],'localFaithHome':['input','Local Faith Home',''],'centreFaithHome':['input','Centre Faith Home',''],'expectations':['textarea','Expectations','']}
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
            elif widgetType == 'siblings':
                with userForm:sibling,holderCard = siblingsWidget()
            elif widgetType == 'select':options = value.split(',');widget = ui.select(options=options,label=label,value=options[0]).classes('w-full').style('margin-top:10px')
            elif widgetType == 'radio':options = value.split(',');widget = ui.radio(options=options,value=options[0]).props('inline').classes('w-full').style('margin-top:10px')
            else:widget = getattr(ui, widgetType)(label=label).classes('w-full').style('margin-top:10px')
            formWidgets[key] = widget
        return formWidgets,userForm,avatarImage,email,password,chips,sibling,holderCard
    
@ui.page('/adminOperation')
async def adminOperation():
    ui.page_title('Admin Operation')
    dataFields = ['Email','Password','Name','Contact Details']
    # fn to update the data
    async def updateAdmin(id='',state=''):
        notifier = ui.notification(message='Saving data...',type='ongoing',timeout=None,spinner=True)
        try:
            connection = mysql.connector.connect(host='127.0.0.1',user='root',password='Nikish@2003',database='pentecostmatrimony')
            cursor = connection.cursor()
            if adminLabel.text=='Add New Admin':
                for i in adminGrid:email,password,name,contact = [x.value for x in i if x.__class__.__name__ == 'Input']
                cursor.execute('''insert into userData (Email,Passwords,Name,Profession,WhatsAppTelegram,requestStatus,role) VALUES (%s,%s,%s,%s,%s,%s,%s)''',
                (email,cipher.encrypt(password.encode()).decode('utf-8'),name,'0',contact,'Approved','admin'))
            elif adminLabel.text=='All Admins':
                email,password,name,contact = [i.value for i in adminGrid if hasattr(i, 'value')]
                cursor.execute('''update userData set Email=%s,Passwords=%s,Name=%s,Profession=%s,WhatsAppTelegram=%s where id=%s''',(email,cipher.encrypt(password.encode()).decode('utf-8'),name,state,contact,id))
            else:
                for i in adminGrid:name,contact = i._text.split('-');cursor.execute('''update userData set Profession=%s where WhatsAppTelegram=%s''',('1' if i.value else '0',contact))
            connection.commit()
            cursor.close();connection.close()
        except mysql.connector.Error as error:notifier.message=f'Database error: {str(error)}';notifier.type='negative';notifier.spinner=False;notifier.timeout=2;return
        notifier.message='Data saved successfully!';notifier.type='positive';notifier.spinner=False;notifier.timeout=2
    # fn to show the update form
    def changeAdminData(i):
        adminGrid.clear()
        index = 1
        with adminGrid:
            with ui.grid(columns='50% 50%').classes('gap-2 w-full'):
                ui.button('Back',icon='arrow_back',on_click=lambda:changeAdminMenu('All Admins')).props('color=red rounded outline').classes('w-full')
                ui.button('Save',icon='save',on_click=lambda:updateAdmin(i[0],i[4])).props('color=green rounded outline').classes('w-full')
            for x in dataFields:
                dataValue = i[index+(1 if x=='Contact Details' else 0)]
                if index==2:dataValue = cipher.decrypt(dataValue.encode('utf-8')).decode()
                ui.input(label=x,value=dataValue).classes('w-full').style('font-size: 24px; font-weight: bold; font-family: Times New Roman; color: blue');index += 1
    def showAdminData(i):ui.label(i[3]).style('font-size: 24px; font-weight: bold; font-family: Times New Roman; color: blue');ui.label(i[5]).style('font-size: 20px; font-family: Times New Roman; color: black');ui.button('Edit',icon='edit',on_click=lambda:changeAdminData(i)).props('color=blue rounded outline');ui.button('Delete',icon='delete').props('color=red rounded outline')
    # fn to change the admin operation scrollable widget based on the selection
    async def changeAdminMenu(type):
        adminLabel.set_text(type)
        adminGrid.clear()
        if type=='Add New Admin':
            saveButton.set_visibility(1)
            with adminGrid:
                with ui.grid(columns='40% 60%').classes('gap-2 w-full'):
                    for i in dataFields:ui.label(f'Enter the {i}').classes('w-full mt-auto').style('font-weight: bold; font-family: Times New Roman; color: black; font-size: 20px;');ui.input(label=i).classes('w-full')
        else:
            with adminGrid:
                for i in await fetchAdmin():
                    if type=='All Admins':
                        saveButton.set_visibility(0)
                        with ui.grid(columns='30% 30% 18% 20%').classes('w-full items-center gap-2'):showAdminData(i)
                    else:
                        saveButton.set_visibility(1)
                        ui.checkbox(text=f'{i[3]} - {i[5]}',value=True if i[4]=='1' else False).style('font-weight: bold; font-family: Times New Roman; color: black; font-size: 24px;')
    with ui.card().classes('w-full h-screen'):
        with ui.grid(columns='30% 70%').classes('w-full h-full gap-1'):
            with ui.card().classes('w-full h-full'):
                ui.button('All Admins',on_click=lambda:changeAdminMenu('All Admins'),icon='group').classes('w-full text-center')
                ui.button('Add New Admin',on_click=lambda:changeAdminMenu('Add New Admin'),icon='add').classes('w-full text-center')
                ui.button('Update Contact Info.',on_click=lambda:changeAdminMenu('Update Contact Info.'),icon='edit').classes('w-full text-center')
            with ui.card().classes('w-full h-full'):
                adminLabel = ui.label('Add Admin').classes('w-full text-center').style('font-size: 30px; font-weight: bold; font-family: Times New Roman; color: black')
                adminGrid = ui.card().classes('w-[90%] h-full p-4 mx-auto overflow-auto')
                saveButton = ui.button('Save',icon='save',on_click=updateAdmin).props('color=green rounded outline').classes('w-full mt-4')
                saveButton.set_visibility(0)
                await changeAdminMenu('All Admins')

@ui.page('/admin')
async def admin():
    ui.page_title('Admin')
    ui.add_css('''.custom-table thead th {font-family: "Times New Roman";font-size: 24px;font-weight: bold;text-align: center;color: blue;}
               .custom-table tbody td {font-family: "Times New Roman";font-size: 18px;;text-align: center}''')
    # fn to update the request status of the user in the database when the admin approves or rejects a request
    async def update(id,value):
        notifier = ui.notification(message='Saving..',spinner=True,timeout=None,type='ongoing')
        try:
            connection = mysql.connector.connect(host='127.0.0.1',user='root',password='Nikish@2003',database='pentecostmatrimony')
            cursor = connection.cursor()
            cursor.execute('''update userData set requestStatus = %s where id = %s''',(value,id))
            connection.commit()
            cursor.close();connection.close()
            notifier.message='Saved';notifier.spinner=False;notifier.type='positive';notifier.timeout=2
        except mysql.connector.Error as e:
            notifier.message=f'Database error: {str(e)}';notifier.type='negative';notifier.spinner=False;notifier.timeout=2;return
    # fn to show the details of the user in a dialog when the admin clicks on a row in the table
    async def showDetails(ids):
        try:
            connection = mysql.connector.connect(host='127.0.0.1',user='root',password='Nikish@2003',database='pentecostmatrimony')
            cursor = connection.cursor()
            cursor.execute('select * from userData where id = %s',(ids,))
            data = cursor.fetchone()
            cursor.close();connection.close()
        except mysql.connector.Error as error:ui.notification(f'Database error: {str(error)}',type='negative');return
        masterType = masterLabel.text
        index = 0
        with ui.dialog() as detailsMaster,ui.card().classes('w-full h-screen'):
            with ui.row().classes('w-full items-center no-wrap gap-2'):
                ui.button('Back',icon='arrow_back',on_click=detailsMaster.close).props('color=red rounded outline').classes('w-1/2 text-left')
                ui.label('User Details').classes('w-full text-center').style('font-size: 30px; font-weight: bold; font-family: Times New Roman; color: black')
                ui.button('Delete',icon='delete',).props('color=red rounded outline').classes('w-1/2 text-left').set_visibility(1 if masterType=='All Data' else 0)
                if masterType!='All Data':ui.space().classes('w-1/2')
            ui.separator()
            if masterType!='All Data':
                with ui.row().classes('w-full items-center gap-2'):
                    ui.button('Approve',icon='check',on_click=lambda:update(ids,'Approved')).props('color=green rounded outline').classes('w-[40%] mx-auto')
                    rejectButton = ui.button('Reject',icon='close',on_click=lambda:update(ids,'Rejected')).props('color=red rounded outline').classes('w-[40%] mx-auto')
                    if masterType=='Rejected Request Data':rejectButton.set_visibility(0)
            ui.label(f'Registration Number: {data[0]}').classes('w-full text-center').style('font-size: 20px; font-family: Times New Roman; color: black')
            ui.interactive_image(f"data:image/{filetype.guess(data[1]).mime or 'jpeg'};base64,{base64.b64encode(data[1]).decode()}").classes('w-[90%] h-[90%] mx-auto rounded-full').style('object-fit:cover')
            with ui.grid(columns=2).classes('gap-2 w-full'):
                for i in data[4:-2]:
                    ui.label(fields[index]).classes('w-full text-left text-bold').style('font-size: 20px; font-family: Times New Roman; color: black')
                    ui.label(i).classes('w-full text-left').style('font-size: 20px; font-family: Times New Roman; color: black')
                    index += 1
        detailsMaster.open()
    async def refreshDataMaster(type='',databaseFilter='',searchField=''):
        try:
            connection = mysql.connector.connect(host='127.0.0.1',user='root',password='Nikish@2003',database='pentecostmatrimony')
            cursor = connection.cursor(dictionary=True)
            if searchField:
                if masterLabel.text=='All Data':
                    if databaseFilter=='':cursor.execute(f'select id,email,name from userData where role="user" limit 1000')
                    else:cursor.execute(f'select id,email,name from userData where role="user" and {searchField}=%s limit 1000',(databaseFilter,))
                elif databaseFilter=='':cursor.execute(f'select id,email,name from userData where requestStatus=%s limit 1000',('Pending' if masterLabel.text=='Pending Request Data' else 'Rejected',))
                else:cursor.execute(f'select id,email,name from userData where requestStatus=%s and {searchField}=%s limit 1000',('Pending' if masterLabel.text=='Pending Request Data' else 'Rejected',databaseFilter,))
            else:
                if type=='All Data':cursor.execute('select id,email,name from userData where role="user" limit 1000')
                else:cursor.execute('select id,email,name from userData where requestStatus=%s limit 1000',('Pending' if type=='Pending Request Data' else 'Rejected',))
            data = cursor.fetchall()
            cursor.close();connection.close()
        except mysql.connector.Error as e:ui.notification(f'Database error: {str(e)}',type='negative');data = []
        masterTable.rows = data
        masterTable.update()
    with ui.row().classes('w-full h-20 items-center'):  # aligns the search and menu in a row
        with ui.button(icon='menu'):
            with ui.menu():
                ui.menu_item('All Data', on_click=lambda:[masterLabel.set_text('All Data'),asyncio.create_task(refreshDataMaster(type='All Data'))])
                ui.menu_item('Pending Request Data', on_click=lambda:[masterLabel.set_text('Pending Request Data'),asyncio.create_task(refreshDataMaster(type='Pending Request Data',databaseFilter='Pending'))])
                ui.menu_item('Rejected Request Data', on_click=lambda:[masterLabel.set_text('Rejected Request Data'),asyncio.create_task(refreshDataMaster(type='Rejected Request Data',databaseFilter='Rejected'))])
                ui.menu_item('Admin Operation',on_click=lambda:ui.navigate.to('/adminOperation'))
                ui.menu_item('Married Data',)
        searchInput,searchField = searchWithFields()
        searchInput.on('keydown.enter',lambda:refreshDataMaster(databaseFilter=searchInput.value,searchField=searchField.value))
        # searchInput.on('blur',lambda:refreshDataMaster(databaseFilter=searchInput.value,searchField=searchField.value))
    with ui.card().classes('w-full h-screen'):
        masterLabel = ui.label('All Data').classes('w-full text-center').style('font-size: 30px; font-weight: bold; font-family: Times New Roman; color: black')
        tableColumns = [{'name':'id','label':'ID','field':'id'},{'name':'email','label':'Email','field':'email'},{'name':'name','label':'Name','field':'name'}]
        masterTable = ui.table(columns=tableColumns,rows=[],pagination=25).classes('custom-table w-full h-[90%]')
        masterTable.on('rowClick',lambda e:showDetails(e.args[1]['id']))
        await refreshDataMaster(type='All Data')

@ui.page('/register')
def personnelForm():
    ui.page_title('Register Form')
    ui.label('Registration Form').classes('text-center w-full').style('font-size: 28px; font-weight: bold; font-family: Times New Roman; color: #333')
    with ui.column().classes('w-full h-screen items-center justify-center'):widgets,userForm,avatar,email,password,chips,sibling,holderCard = form('#333','#f9f9f9',240)
    async def addData():
        async def saveData(data):
            try:
                connection = mysql.connector.connect(host='127.0.0.1',user='root',password='Nikish@2003',database='pentecostmatrimony')
                cursor = connection.cursor()
                cursor.execute('insert into userData(Photo,Email,Passwords,Name,Profession,Dob,Gender,Qualification,Height,Income,FamilyOrigin,MaritalStatus,Languages,FatherName,MotherName,ParentsNumber,WhatsAppTelegram,Status,Hometown,CurrentAddress,Siblings,LocalFaithHome,CenterFaithHome,Expectations,requestStatus) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)',data)
                connection.commit()
                cursor.close();connection.close()
            except mysql.connector.Error as e:print(e)
        data = (userForm.photo,email.value,cipher.encrypt(password.value.encode()).decode('utf-8'),)
        for x in widgets:
            if x=='languagesKnown':data += (','.join(chips.lists),)
            elif x=='siblings':
                siblingValue = ''
                for i in holderCard.default_slot.children:label_widget = i.default_slot.children[0];siblingValue += label_widget._text+','
                data += (siblingValue,)
            else:data += (widgets[x].value,)
        notifier = ui.notification('Submitting...',type='ongoing',timeout=None,spinner=True)
        await saveData(data+('Pending',))
        notifier.message = 'Request sent successfully!';notifier.type = 'positive';notifier.spinner = False;notifier.timeout = 2
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
    async def showVerse():currentVerse = random.choice(versesList);verseLabel.set_text(verses[currentVerse]);verse.set_text(currentVerse)
    with verseCard:
        with ui.row().classes('w-full items-center'):
            verseLabel = ui.label().classes('text-center').style('font-size: 18px; font-style: italic; font-family: Times New Roman; color: black')
            verse = ui.label().classes('text-center').style('font-size: 16px; font-family: Times New Roman; color: blue')
    await showVerse()
    ui.timer(5,showVerse)
    # fetch user data
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
    with ui.grid().classes('w-full h-screen grid-cols-[300px_1fr] gap-2 items-start'):
        widgets,userForm,avatar,emailWidget,password,chips,sibling,holderCard = form('#f9f9f9','#000000','75')
        # here is the master card
        with ui.card().classes('p-4 bg-transparent shadow-none border border-gray-300 w-full h-screen overflow-auto').style('background-color: grey; backdrop-filter: blur(10px); border-radius: 8px; box-shadow: 0 4px 8px rgba(0, 0, 0, 0.5)'):matchDataMaster = ui.grid(columns=3).classes('w-full gap-2 items-start')
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
        elif index==21:sibling.addData(data[index].split(',')[:-1])
        else:widgets[i].set_value(data[index])
        index += 1
        if index in [7,8]:widgets[i].disable()
    # fn to update the data in the database
    async def updateData(data):
        def saveData():
            try:
                connection = mysql.connector.connect(host='127.0.0.1',user='root',password='Nikish@2003',database='pentecostmatrimony')
                cursor = connection.cursor()
                cursor.execute('update userData set Photo=%s,Email=%s,Passwords=%s,Name=%s,Profession=%s,Dob=%s,Gender=%s,Qualification=%s,Height=%s,Income=%s,FamilyOrigin=%s,MaritalStatus=%s,Languages=%s,FatherName=%s,MotherName=%s,ParentsNumber=%s,WhatsAppTelegram=%s,Status=%s,Hometown=%s,CurrentAddress=%s,Siblings=%s,LocalFaithHome=%s,CenterFaithHome=%s,Expectations=%s,requestStatus=%s where Email=%s',data)
                connection.commit()
                cursor.close();connection.close()
            except mysql.connector.Error as e:print(e)
        await run.io_bound(saveData)
    # fn to handle the submit button click and update the data in the database
    async def handleSubmit():
        if anyEmptyField(userForm,userForm.photo,chips.lists):ui.notification('Please fill all the fields')
        else:
            data = (userForm.photo,email,cipher.encrypt(password.value.encode()).decode('utf-8'),)
            for x in widgets:
                if x=='languagesKnown':data += (','.join(chips.lists),)
                elif x=='siblings':
                    siblingValue = ''
                    for i in holderCard.default_slot.children:label_widget = i.default_slot.children[0];siblingValue += label_widget._text+','
                    data += (siblingValue,)
                else:data += (widgets[x].value,)
            data += ('Approved',email)
            await updateData(data);ui.notification('Details updated successfully!')
    with ui.grid(columns='24% 76%').classes('w-full items-center justify-center'):ui.button('Update',icon='edit',on_click=handleSubmit);ui.label(supportLabel[:-1]).classes('flex-grow text-center').style('font-size: 17px; font-family: Times New Roman; color: black')
    # it creates a pdf
    async def downloadPdf():
        notifier = ui.notification(message='Generating PDF...',type='ongoing',timeout=None,spinner=True)
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
        notifier.message = 'PDF Generated! Downloading...';notifier.type = 'success';notifier.spinner = False;notifier.timeout = 2
        ui.download(pdfBytes,filename=f'{data[1]}_biodata.pdf')
    # fn that creates a details card to show the details of the user
    def showCurrentDetails(i):
        index = 0
        detailsCard.clear()
        detailsCard.data = i
        with detailsCard:
            with ui.column().classes('w-full h-full items-center justify-center'):ui.interactive_image(f"data:image/{filetype.guess(i[1]).mime or 'jpeg'};base64,{base64.b64encode(i[1]).decode()}").classes('w-90 h-90').style('background-color: #fff; border-radius: 8px; object-fit:cover;')
            with ui.grid(columns=2).classes('gap-2 w-full'):
                for x in i[4:-2]:
                    ui.label(fields[index]).style('font-size: 24px; font-weight: bold; font-family: Times New Roman; color: #333')
                    ui.label(x).style('font-size: 24px; font-weight: bold; font-family: Times New Roman; color: #333')
                    index += 1
        overCoverCard.set_visibility(True)
    # fn to refresh the master card with the updated data after search or any operation
    def refreshMaster(data):
        with matchDataMaster:
            for i in data:
                currentUser = ui.card().classes('hover-card w-full h-90').style('background-color: #fff; border-radius: 8px; box-shadow: 0 2px 4px rgba(0, 0, 0, 0.5)')
                with currentUser:ui.image(f"data:image/{filetype.guess(i[1]).mime or 'jpeg'};base64,{base64.b64encode(i[1]).decode()}").classes('w-full h-full').style('background-color: #fff; border-radius: 8px')
                currentUser.on('click',lambda i=i:showCurrentDetails(i))
    # fn to assign the users in the master card based on the search or any operation
    async def assignUsers():
        matchDataMaster.clear()
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
        task = asyncio.create_task(search())
        task.add_done_callback(lambda x:refreshMaster(x.result()))
    await assignUsers()
    searchInput.on('keydown.enter',lambda x:assignUsers())
    # searchInput.on('blur',lambda x:assignUsers())
    # from this details card set-up
    overCoverCard = ui.card().classes('p-4 w-screen h-full bg-transparent shadow-none border border-gray-300 items-center justify-center').style('position: absolute; top:0px; left:0px; margin:0; border-radius:0;background-color: white; backdrop-filter: blur(10px); border-radius: 8px; box-shadow: 0 4px 8px rgba(0, 0, 0, 0.5); padding:20px;')
    with overCoverCard:userCardDetails = ui.card().classes('w-[60%] h-full items-center justify-center').style('background-color: grey; backdrop-filter: blur(10px); border-radius: 8px; box-shadow: 0 4px 8px rgba(0, 0, 0, 0.5); padding:20px;')
    with userCardDetails:
        ui.label('User Details').classes('w-full text-center').style('font-size: 28px; font-weight: bold; font-family: Times New Roman; color: white')
        with ui.row().classes('w-full items-center justify-between'):
            ui.button('back',icon='arrow_back',on_click=lambda:overCoverCard.set_visibility(False))
            ui.button('Download',icon='download',on_click=lambda:downloadPdf())
        detailsCard = ui.card().classes('w-full h-full bg-gray-100 rounded-lg shadow-lg p-4 overflow-auto')
        detailsCard.data = None
    overCoverCard.set_visibility(False)

@ui.page('/')
async def login():
    # fetches admin contact details
    ui.page_title('Login Page')
    global supportLabel
    ui.add_css('''body {background-image: url("/icons/image1.png");background-size: cover;background-position:top center;background-repeat: no-repeat;height: 100vh;}
               .white-input .q-field__label {color: white !important;}
               .white-input .q-field__native {color: white !important;}
               .white-input .q-field__control:before {border-bottom: 1px solid white !important;}
               .white-input .q-field__control:after {border-bottom: 2px solid white !important;}
               .white-input .q-field__append .q-icon {color: white !important;}
               .white-input .q-field__append .q-icon:hover {color: grey !important;}''')
    with ui.column().classes('w-full h-screen items-center justify-center overflow-hidden'):
        with ui.card().classes('md:w-1/3 lg:w-1/4 p-6').style('background-color: rgba(0, 0, 0, 0.6); backdrop-filter: blur(8px); border-radius: 10px; box-shadow: 0 4px 8px rgba(0, 0, 0, 0.5);'):  # master frame
            ui.label('Login to your Account').classes('text-center w-full').style('font-size: 28px; font-weight: bold; font-family: Times New Roman; color: white')
            currentUser = ui.input('Email', placeholder='Enter your email').classes('white-input w-full')
            password = ui.input('Password', placeholder='Enter your password', password=1,password_toggle_button=1).classes('white-input w-full')
            # fetches the user data
            async def handleLogin():
                notifier = ui.notification(message='Checking credentials...',type='ongoing',timeout=5,spinner=True)
                data = await emailValidation(currentUser.value)
                if data:checkUser(notifier,data,password.value)
                else:notifier.message='No account found with this email. Please register first.';notifier.type='negative';notifier.spinner=False;notifier.timeout=2
            ui.button('Sign in',on_click=handleLogin,icon='login',color='red').classes('w-full')
            ui.link('Register',target='/register')
    supportLabel = 'Contact us:'
    for i in await fetchAdmin():
        if i[4]=='1':supportLabel += f' Bro.{i[3]} (Ph no.{i[5]}),'
    ui.label(supportLabel[:-1]).classes('absolute bottom-4 left-2').style('font-size: 16px; font-family: Times New Roman; color: white')

ui.run(host='0.0.0.0', port=80)