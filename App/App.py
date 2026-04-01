from nicegui import ui,app,run
import mysql.connector,base64,bcrypt,imghdr,smtplib
from datetime import datetime
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

connection = mysql.connector.connect(host='127.0.0.1',user='root',password='Nikish@2003',database='pentecostMatrimony')
app.add_static_files('/icons','icons&Images')
fields = ['Name','Profession','Date of birth','Gender','Qualification','Height','Income','Background','Marital Status','Languages Known',"Father's Name","Mother's Name", "Parent's Number",'Whatsappnumber','Familystatus','Hometown','Currentresidentaddress','Siblings','Localfaithhome','Centrefaithhome','Expectations']

def anyEmptyField(photo,block=0):
    if not photo:return 1
    for widget in userForm:
        if widget.__class__.__name__ in ['Input','DateInput','Radio','Select','Textarea'] and widget.value in [None,'']:widget.run_method('focus');widget.style('border:2px solid red');return 1
        else:widget.style('border:2px white')
        if widget.props.get('label')=='Email':return block

async def emailValidation(email='',check=0):
    def fetchData():
        try:
            cursor = connection.cursor()
            cursor.execute('''select email,passwords,role,requestStatus from userData where email = %s''',(email,))
            currentUser = cursor.fetchone()
            cursor.close()
        except:currentUser = None
        return currentUser
    if email:
        currentUserData = await run.io_bound(fetchData)
        if check:return not currentUserData==None
        else:return currentUserData
    
def checkUser(data,passwordEntry):
    email,validPassword,role,requestStatus = data
    if bcrypt.checkpw(passwordEntry.encode(),validPassword.encode()):
        if role=='admin':ui.navigate.to('/admin')
        else:
            if requestStatus=='Pending':ui.navigate.to('/notification')
            else:ui.navigate.to(f'/Home/{email}{passwordEntry}')
    else:ui.notification('Please enter the email and password correctly')

ui.add_head_html('''
                <link rel="preload" href="/icons/ALGERIA.TTF" as="font" type="font/ttf" crossorigin>
                <style>
                @font-face {font-family: AlgerianCustom;src: url('/icons/ALGERIA.TTF');font-display: swap;}
                .algerian-text {font-family: AlgerianCustom;}
                </style>''',shared=1)

def form(textColor,bgColor,marginLeft,width='60%'):
    global userForm
    ui.add_head_html(f'''<style>
        .avatar-container:hover .camera-icon {{background: {textColor} !important;color: {bgColor} !important;}}
        </style>''')
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
    
    userForm = ui.card().classes('dynamic-form').style(f'background-color: {bgColor}; border-radius: 8px; box-shadow: 0 4px 8px rgba(0, 0, 0, 0.5); margin-top: 20px;width:{width};margin-left:{marginLeft}px')
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
    
@ui.page('/notification')
def notify():
    with ui.card():
        ui.label('Dear user your request sent successfully.Kindly wait for the approval of your account.')
        ui.button('Back',on_click=lambda:ui.navigate.to('/'))
    
@ui.page('/test')
def test():
    ui.page_title('Test Page')
    def add_chip():
        currentLanguage = label_input.value.strip()
        if currentLanguage in chips.lists:return 1
        with chips:
            ui.chip(currentLanguage, icon='label', color='silver', removable=True).on('remove',lambda e:chips.lists.remove(currentLanguage))
            chips.lists.append(currentLanguage)
        label_input.value = ''
    label_input = ui.input('Add language').on('keydown.enter', add_chip)
    chips = ui.row().classes('gap-0')
    chips.lists = []
    with chips:pass
    ui.button('print',on_click=lambda:print(chips.lists))
        
@ui.page('/admin')
def admin():
    ui.page_title('Admin')
    ui.add_css('''.scrollable::-webkit-scrollbar {width: 6px;}
                  .scrollable::-webkit-scrollbar-thumb {background: gray;border-radius: 10px;}''')
    async def update(email):
        try:
            cursor = connection.cursor()
            cursor.execute('''update userData set requestStatus = %s where email = %s''',('Approved',email))
            connection.commit()
            cursor.close()
            ui.notification(f'{email} approved successfully!')
        except:print('database error')
        
    def assignNewUser(i):
        currentUserMaster = ui.row().classes('w-full items-center gap-2')
        with currentUserMaster:
            currentUserCard = ui.card().classes('flex-grow w-80 p-4 cursor-pointer')
            currentUserCard.status = 0
            def setStatus(currentUserCard):
                currentUserCard.status = not currentUserCard.status
                details.set_visibility(currentUserCard.status)
            currentUserCard.on('click',lambda : setStatus(currentUserCard))
            with currentUserCard:
                ui.image(f"data:image/{imghdr.what(None, h=i[1]) or 'jpeg'};base64,{base64.b64encode(i[1]).decode()}").classes('w-32 h-32 rounded-full object-cover')
                ui.label(i[2]).style('font-size: 26px; font-weight: bold; font-family: Times New Roman; color: blue')
                details = ui.grid(columns=2).classes('gap-2 w-full')
                details.set_visibility(False)
                with details:
                    index = 0
                    for data in i[4:-2]:ui.label(fields[index]).style('font-size: 20px; font-weight: bold; font-family: Times New Roman');ui.label(data).classes('break-words').style('font-size: 20px; font-family: Times New Roman');index += 1
            ui.button('Approve',icon='check',on_click=lambda:update(i[2])).props('color=green')
            ui.button('Reject ',icon='clear').props('color=red')
            
    with ui.card().classes('w-full h-screen p-4').style('background-color: grey; border-radius: 8px; box-shadow: 0 4px 8px rgba(0, 0, 0, 0.5)'):
        ui.label('User Registration Request').classes('w-full text-center').style('font-size: 30px; font-weight: bold; font-family: Times New Roman; color: black')
        def fetchRequest():
            requestScrollable.clear()
            try:
                cursor = connection.cursor()
                cursor.execute('select * from userData where requestStatus = %s',("Pending",))
                pendingData = cursor.fetchall()
                cursor.close()
            except:pendingData = []
            with requestScrollable:
                for i in pendingData:assignNewUser(i)
        ui.button('Refresh',on_click=fetchRequest,icon='refresh').props('color=green')
        requestScrollable = ui.card().classes('w-full h-full scrollable').style('max-height:100vh; overflow-y:auto;')
        fetchRequest()

@ui.page('/register')
def personnelForm():
    ui.page_title('Register Form')
    widgets,userForm,avatar,email,password,chips = form('#333','#f9f9f9',200)
    async def addData():
        def saveData():
            try:
                cursor = connection.cursor()
                cursor.execute('''insert into userData(Photo,Email,Passwords,Name,Profession,Dob,Gender,Qualification,Height,Income,FamilyOrigin,MaritalStatus,Languages,FatherName,MotherName,ParentsNumber,WhatsAppTelegram,Status,Hometown,CurrentAddress,Siblings,LocalFaithHome,CenterFaithHome,Expectations,requestStatus) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)''',
                            (userForm.photo,email.value,bcrypt.hashpw(password.value.encode(),bcrypt.gensalt()))+tuple(widgets[x].value if x!='languagesKnown' else ','.join(chips.lists) for x in widgets)+('Pending',))
                connection.commit()
                cursor.close()
            except:print('database error')
        await run.io_bound(saveData)
        ui.notification('Request sent successfully!')
        import asyncio
        await asyncio.sleep(0.4)
        ui.navigate.to('/')
    async def handleSubmit():
        if anyEmptyField(userForm.photo, userForm.block):ui.notification('Please fill all the fields')
        else:await addData()
    ui.button('Submit', on_click=handleSubmit)
    
@ui.page('/Home/{email}{password}')
def main(email:str,password:str):
    ui.page_title('Pentacost Matrimony')
    cursor = connection.cursor()
    cursor.execute('''select * from userData where email = %s''',(email,))
    data = cursor.fetchone()
    cursor.close()
    ui.label(f'Welcome {data[4]}!').style('font-size: 24px; font-weight: bold; font-family: Times New Roman; color: #333')
    ui.button('Logout', on_click=lambda: ui.navigate.to('/')).props('color=red')
    ui.icon('search')
    ui.input(label='Search').style('border-radius:9999px; width:300px; padding:8px 16px;')
    widgets,photo,avatar,emailWidget,password,chips = form('#f9f9f9','#000000',5,'25%')
    avatar.set_source(f"data:image/{imghdr.what(None, h=data[1]) or 'jpeg'};base64,{base64.b64encode(data[1]).decode()}")
    emailWidget.set_value(email)
    emailWidget.disable()
    password.set_value(password.decode())
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
    ui.button('Check',on_click=lambda:print(chips.lists))
    with ui.card().classes('p-4').style('position: absolute; top:150px; left:350px; width:600px; height:1500px; background-color: #f9f9f9; border-radius: 8px; box-shadow: 0 4px 8px rgba(0, 0, 0, 0.5)'):
        with ui.grid(columns=3).classes('gap-4'):
            for i in range(9):ui.card().classes('p-4').style('background-color: #fff; border-radius: 8px; box-shadow: 0 2px 4px rgba(0, 0, 0, 0.5);')
            
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
    with ui.card().classes('w-full md:w-1/3 lg:w-1/4 mx-auto mt-10 p-6').style('background-color: rgba(0, 0, 0, 0.6); backdrop-filter: blur(8px); border-radius: 10px; box-shadow: 0 4px 8px rgba(0, 0, 0, 0.5); margin-top: 270px; margin-left: 560px'):
        ui.label('Login to your Account').classes('text-center w-full').style('font-size: 28px; font-weight: bold; font-family: Times New Roman; color: white')
        currentUser = ui.input('Email', placeholder='Enter your email').classes('white-input w-full')
        password = ui.input('Password', placeholder='Enter your password', password=1,password_toggle_button=1).classes('white-input w-full')
        async def handleLogin():
            data = await emailValidation(currentUser.value)
            checkUser(data, password.value)
        ui.button('Sign in' , on_click=handleLogin,icon='login').classes('w-full').props('color=red')
        ui.link('Register',target='/register')
    ui.button('Try',on_click=lambda:ui.navigate.to('/test'))

ui.run(host='127.0.0.1', port=8080)       # page - http://127.0.0.1:8080/