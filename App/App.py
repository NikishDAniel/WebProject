from nicegui import ui,app
import mysql.connector
import base64,bcrypt
from datetime import datetime

connection = mysql.connector.connect(host = '127.0.0.1',user="root",password="Nikish@2003",database="pentecostMatrimony")
cursor = connection.cursor()
app.add_static_files('/icons', 'icons&Images')
photo = b''
currentUserData = None

def anyEmptyField():
    for widget in userForm:
        print(widget);return 1
        # if widget.value in [None,'']:widget.style('border:2px solid red');return 1
        # else:widget.style('')
    return 0

def emailValidation(email='',check=0):
    global currentUserData
    if email:
        cursor.execute('''select * from userData where email = %s''',(email,))
        currentUserData = cursor.fetchone()
        cursor.close()
        if check:
            result = False if currentUserData else True
            return result
    else:return True
    
def checkUser(password):
    if currentUserData[2] == password:
        if currentUserData[-1]=='admin':ui.navigate.to('/admin')
        else:ui.navigate.to('/Home')
    else:ui.notification('Please enter the email and password correctly')

ui.add_head_html('''
                <link rel="preload" href="/icons/ALGERIA.TTF" as="font" type="font/ttf" crossorigin>
                <style>
                @font-face {font-family: AlgerianCustom;src: url('/icons/ALGERIA.TTF');font-display: swap;}
                .algerian-text {font-family: AlgerianCustom;}
                </style>''',shared=1)

def form(textColor,bgColor,update,marginLeft,width='60%'):
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
    with userForm:
        async def savePhoto(e):
            global photo
            photo = await e.file.read()
            photoAvatar = base64.b64encode(photo).decode()
            avatarImage.set_source(f'data:image/jpeg;base64,{photoAvatar}')
            upload.reset()
        upload = ui.upload(auto_upload=True,on_upload=savePhoto).props('accept=image/*').style('display:none')
        with ui.element('div').classes('avatar-container relative w-[150px]'):
            with ui.avatar(size='150px').classes('p-0 overflow-hidden cursor-pointer hover:scale-105 transition-transform duration-300') as avatar:avatarImage = ui.image('https://cdn-icons-png.flaticon.com/512/1077/1077114.png').style('width:100%; height:100%; object-fit:cover')
            camera_icon = ui.icon('photo_camera').classes('camera-icon cursor-pointer hover:scale-110').style(f'''position:absolute;bottom:6px;right:6px;background:{bgColor};color:{textColor};border-radius:50%;padding:6px;font-size:20px;transition:0.3s;''')
        avatar.on('click', lambda: upload.run_method('pickFiles'))
        camera_icon.on('click', lambda: upload.run_method('pickFiles'))
        widgets = {'name':['input','Name',''],'profession':['input','Profession',''],'dateOfBirth':['date_input','Date of Birth',''],'gender':['radio','Gender','Male,Female'],'qualification':['input','Qualification',''],'height':['input','Height',''],'income':['input','Income',''],'background':['select','Family Origin','TPM Born,CSI/Other'],
                   'maritalStatus':['radio','Marital Status','Single,Widowed'],'languagesKnown':['input','Languages Known',''],'fatherName':['input','Father Name',''],'motherName':['input','Mother Name',''],'parentsNumber':['input','Parents Number',''],'WhatsAppNumber':['input','WhatsApp Number',''],
                   'familyStatus':['select','Family Status','High Class,Middle Class'],'hometown':['input','Hometown',''],'currentResidentAddress':['textarea','Current Resident Address',''],'siblings':['input','Siblings',''],'localFaithHome':['input','Local Faith Home',''],'centreFaithHome':['input','Centre Faith Home',''],'expectations':['textarea','Expectations','']}
        email = ui.input(label='Email',placeholder='Enter your Email').style(f'margin-top:10px')
        if update==0:email.validation={'Email Already Exists':lambda x:emailValidation(email=x,check=1)}
        password = ui.input(label='Password', placeholder='Enter your password', password=1,password_toggle_button=1).style(f'margin-top:10px')
        formWidgets = {}
        for key, (widgetType, label, value) in widgets.items():
            if widgetType in ['input', 'textarea']:widget = getattr(ui, widgetType)(label=label,placeholder=f'Enter your {label}').classes('w-full').style('margin-top:10px')
            elif widgetType == 'select':options = value.split(',');widget = ui.select(options=options,label=label,value=options[0]).classes('w-full').style('margin-top:10px')
            elif widgetType == 'radio':options = value.split(',');widget = ui.radio(options=options,value=options[0]).props('inline').classes('w-full').style('margin-top:10px')
            else:widget = getattr(ui, widgetType)(label=label).classes('w-full').style('margin-top:10px')
            formWidgets[key] = widget
        return formWidgets,email,password
    
@ui.page('/test')
def test():
    ui.page_title('Test Page')
    
@ui.page('/admin')
def admin():
    global userRequestFrame
    ui.page_title('Admin Panel')
    ui.label('Admin Panel').style('font-size: 24px; font-weight: bold; font-family: Times New Roman; color: #333')
    userRequestFrame = ui.card().classes('p-4').style('background-color: #f9f9f9; border-radius: 8px; box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1); margin-top: 20px;width:100%')
            
@ui.page('/register')
def personnelForm():
    ui.page_title('Register Form')
    widgets,email,password = form('#333','#f9f9f9',0,200)
    # photoAvatar = base64.b64encode(user.photo).decode();avatarImage.set_source(f'data:image/jpeg;base64,{photoAvatar}')
    # if update:
    #     user = sessions.query(User).filter(User.email == currentUser.value).first()
    #     if user:
    #         email.value = user.email
    #         name.value = user.name
    #         password.value = user.password
    #         dateOfBirth.value = user.dateOfBirth
    #         address.value = user.address
    #         background.value = user.background
    #         gender.value = user.gender
    #         if user.photo:photoAvatar = base64.b64encode(user.photo).decode();avatarImage.set_source(f'data:image/jpeg;base64,{photoAvatar}')
    #     name.disable();email.disable();dateOfBirth.disable();gender.disable()
    # def updateData():
    #     user = sessions.query(User).filter(User.email == currentUser.value).first()
    #     if user:
    #         user.name = name.value
    #         user.password = password.value
    #         user.address = address.value
    #         user.background = background.value
    #         if photo:user.photo = photo
    #         sessions.commit()
    #         sessions.close()
    #         ui.notification('Data updated successfully!')
    #         ui.navigate.to('/Home')
    def addData():
        cursor.execute('''insert into userData(Photo,Email,Passwords,Name,Profession,Dob,Qualification,Height,Income,FamilyOrigin,Languages,FatherName,MotherName,ParentsNumber,WhatsAppTelegram,Status,Hometown,CurrentAddress,Siblings,LocalFaithHome,CenterFaithHome,Expectations,Role) values(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)''',
                       (photo,email.value,password.value)+tuple(widgets[x].value for x in widgets))
        cursor.commit()
        cursor.close()
        ui.notification('Request sent successfully!')
        ui.navigate.to('/')
    ui.button('Submit', on_click=lambda:ui.notification('Please fill all the fields') if anyEmptyField() else []) # addData(),
    
@ui.page('/Home')
def main():
    ui.page_title('Pentacost Matrimony')
    data = cursor.execute('''select * from userData where email = %s''',(currentUser.value,)).fetchone()
    print(data)
    ui.label(f'Welcome {data[1]}!').style('font-size: 24px; font-weight: bold; font-family: Times New Roman; color: #333')
    ui.button('Logout', on_click=lambda: ui.navigate.to('/')).props('color=red')
    ui.icon('search')
    ui.input(label='Search').style('border-radius:9999px; width:300px; padding:8px 16px;')
    form('#f9f9f9','#000000',1,10,'25%')
    with ui.card().classes('p-4').style('background-color: #f9f9f9; border-radius: 8px; box-shadow: 0 4px 8px rgba(0, 0, 0, 0.5); margin-top: 20px;width:80%;margin-left:300px'):
        with ui.grid(columns=3).classes('gap-4'):
            for i in range(9):
                ui.card().classes('p-4').style('background-color: #fff; border-radius: 8px; box-shadow: 0 2px 4px rgba(0, 0, 0, 0.5);')
            
@ui.page('/')
def login():
    global currentUser
    ui.page_title('Login Page')
    with ui.header().props('elevated'):
        ui.image('/icons/download (7).png').style('width: 150px; height: 150px; margin-top: 4px; margin-left: 4px')
        ui.label('The Pentacoast Missions').classes('algerian-text uppercase absolute-center text-6xl font-bold')
    ui.add_css('body {background-image: url("/icons/images.jpg");background-size: cover;background-position: center;}')
    with ui.card().classes('w-full md:w-1/3 lg:w-1/4 mx-auto mt-10 p-6').style('background-color: #f9f9f9; border-radius: 8px; box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1); margin-top: 100px; margin-left: 340px'):
        ui.page_title('Login')
        currentUser = ui.input('Email', placeholder='Enter your email')
        password = ui.input('Password', placeholder='Enter your password', password=1,password_toggle_button=1)
        ui.button('Login' , on_click=lambda: [emailValidation(currentUser.value),checkUser(password.value)]).props('color=red')
        ui.button('Register', on_click=lambda: ui.navigate.to('/register')).props('color=blue')
    ui.button('Try',on_click=lambda:ui.navigate.to('/test'))
         
ui.run(host='127.0.0.1', port=8080)       # page - http://127.0.0.1:8080/