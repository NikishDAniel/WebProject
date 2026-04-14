from nicegui import ui,app,run
import mysql.connector,base64,bcrypt,imghdr,smtplib,asyncio
# from datetime import datetime
from cryptography.fernet import Fernet
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

app.add_static_files('/icons','icons&Images')
fields = ['Name','Profession','Date of birth','Gender','Qualification','Height','Income','Background','Marital Status','Languages Known',"Father's Name","Mother's Name", "Parent's Number",'Whatsapp Number','Family Status','Hometown','Current Resident Address','Siblings','Local Faith Home','Centre Faith Home','Expectations']
key = b'nWjYyxV8EC5sbgkOMV_YekqyERDo1j2P4SAA_WNujVI='
cipher = Fernet(key)

def anyEmptyField(userForm,photo,languages):
    if not photo or not languages:return 1
    index = 0
    for widget in userForm:
        if index!=13 and widget.__class__.__name__ in ['Input','DateInput','Radio','Select','Textarea'] and widget.value in [None,'']:print(widget);widget.run_method('focus');widget.style('border:2px solid red');return 1
        else:widget.style('border:2px white')
        index += 1

async def emailValidation(email='',check=0):
    container = ui.column()
    def fetchData():
        try:connection = mysql.connector.connect(host='127.0.0.1',user='root',password='Nikish@2003',database='pentecostMatrimony',ssl_disabled=True)
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
            if requestStatus=='Pending':ui.notification('Your request is pending approval.') # ;ui.navigate.to('/notification')
            else:ui.navigate.to(f'/Home/{email}')
    else:ui.notification('Please enter the email and password correctly')

ui.add_head_html('''
                <link rel="preload" href="/icons/ALGERIA.TTF" as="font" type="font/ttf" crossorigin>
                <style>
                @font-face {font-family: AlgerianCustom;src: url('/icons/ALGERIA.TTF');font-display: swap;}
                .algerian-text {font-family: AlgerianCustom;}
                </style>''',shared=1)

def searchWithFields(positionX=0,positionY=0):
    with ui.card().classes('w-fit p-2').style(f'position:absolute; left:{positionX}px; top:{positionY}px; background-color: #f0f0f0; border-radius: 8px; box-shadow: 0 4px 8px rgba(0, 0, 0, 0.5);'):
        with ui.row().classes('items-center gap-2'):
            searchInput = ui.input(label='Search by Email').style('width:350px')
            with searchInput.add_slot('prepend'):ui.icon('search').classes('text-2xl text-gray-500')
            ui.label('Category').classes('text-gray-500')
            searchField = ui.select(options=['Email']+fields,value='Email',on_change=lambda:searchInput.set_label('Search by '+searchField.value)).style('width:200px')
    return searchInput,searchField

def form(textColor,bgColor,marginLeft,width='60%'):
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
    ui.spinner();ui.switch()

@ui.page('/admin')
def admin():
    ui.page_title('Admin')
    ui.add_css('''.scrollable::-webkit-scrollbar {width: 6px;}
                  .scrollable::-webkit-scrollbar-thumb {background: gray;border-radius: 10px;}''')
    async def update(email):
        try:
            connection = mysql.connector.connect(host='127.0.0.1',user='root',password='Nikish@2003',database='pentecostMatrimony',ssl_disabled=True)
            cursor = connection.cursor()
            cursor.execute('''update userData set requestStatus = %s where email = %s''',('Approved',email))
            connection.commit()
            cursor.close();connection.close()
        except:print('database error')
        
    def assignNewUser(i):
        currentUserMaster = ui.row().classes('w-full items-center gap-2')
        with currentUserMaster:
            currentUserCard = ui.card().classes('flex-grow w-80 p-4 cursor-pointer')
            currentUserCard.status = 0
            def setStatus(currentUserCard):
                currentUserCard.status = not currentUserCard.status
                details.set_visibility(currentUserCard.status)
            currentUserCard.on('click',lambda:setStatus(currentUserCard))
            with currentUserCard:
                ui.image(f"data:image/{imghdr.what(None,h=i[1]) or 'jpeg'};base64,{base64.b64encode(i[1]).decode()}").classes('w-38 h-38 rounded-full object-cover')
                ui.label(i[2]).style('font-size: 24px; font-weight: bold; font-family: Times New Roman; color: blue')
                details = ui.grid(columns=2).classes('gap-2 w-full')
                details.set_visibility(False)
                with details:
                    index = 0
                    for data in i[4:-3]:ui.label(fields[index]).style('font-size: 20px; font-weight: bold; font-family: Times New Roman');ui.label(data).classes('break-words').style('font-size: 20px; font-family: Times New Roman');index += 1
            def removeUser():currentUserMaster.remove(currentUserCard);currentUserMaster.remove(approve);currentUserMaster.remove(reject)
            def updater():asyncio.create_task(update(i[2]));ui.notification(f'{i[2]} approved successfully!');removeUser()
            approve = ui.button('Approve',icon='check',on_click=updater).props('rounded outline color=green')
            reject = ui.button('Reject ',icon='clear',on_click=removeUser).props('rounded outline color=red')

    with ui.card().classes('w-full h-screen p-4').style('background-color: grey; border-radius: 8px; box-shadow: 0 4px 8px rgba(0, 0, 0, 0.5)'):
        ui.label('User Registration Request').classes('w-full text-center').style('font-size: 30px; font-weight: bold; font-family: Times New Roman; color: black')
        async def fetchRequest():
            requestScrollable.clear()
            try:
                connection = mysql.connector.connect(host='127.0.0.1',user='root',password='Nikish@2003',database='pentecostMatrimony',ssl_disabled=True)
                cursor = connection.cursor()
                cursor.execute('select * from userData where requestStatus = %s',("Pending",))
                pendingData = cursor.fetchall()
                cursor.close()          
                connection.close()
            except:pendingData = []
            with requestScrollable:
                for i in pendingData:assignNewUser(i)
        requestScrollable = ui.card().classes('w-full h-full scrollable').style('max-height:100vh; overflow-y:auto;')
        asyncio.create_task(fetchRequest())

@ui.page('/register')
def personnelForm():
    ui.page_title('Register Form')
    ui.label('Registration Form').classes('text-center w-full').style('font-size: 28px; font-weight: bold; font-family: Times New Roman; color: #333')
    widgets,userForm,avatar,email,password,chips = form('#333','#f9f9f9',200)
    async def addData():
        def saveData():
            try:
                connection = mysql.connector.connect(host='127.0.0.1',user='root',password='Nikish@2003',database='pentecostMatrimony',ssl_disabled=True)
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
    ui.button('Submit', on_click=handleSubmit)
    
@ui.page('/Home/{email}')
def home(email:str):
    ui.page_title('Home Page')
    import random
    verses = {'Genesis 2:18':"The LORD God said, 'It is not good for the man to be alone. I will make a helper suitable for him'",'Mark 10:6-8':"‘made them male and female.For this reason a man will leave his father and mother and be united to his wife,and the two will become one flesh.’",
              'Matthew 19:6':"Therefore what God has joined together, let no one separate.",'Proverbs 5:18':"“He who finds a wife finds what is good and receives favor from the Lord.”",'Proverbs 31:10':"“A wife of noble character who can find? She is worth far more than rubies.”",
              'Ephesians 4:32':"Be kind and compassionate to one another, forgiving each other, just as in Christ God forgave you.",'Colossians 3:14':"And over all these virtues put on love, which binds them all together in perfect unity.",'Colossians 3:19':"Husbands, love your wives and do not be harsh with them.",}
    ui.page_title('Pentacost Matrimony')
    ui.add_css("""body {background-image: url("/icons/userbg.png");background-size: cover;background-position:top center;background-repeat: no-repeat;height: 100vh;}
               .hover-card {transition: all 0.3s ease;}
               .hover-card:hover {transform: scale(1.03);box-shadow: 0 10px 25px rgba(0,0,0,0.2);}""")
    verseCard = ui.card().classes('w-full p-4').style('background-color: #f0f0f0; border-radius: 8px; box-shadow: 0 4px 8px rgba(0, 0, 0, 0.5); position:relative; overflow:hidden;')
    versesList = list(verses.keys())
    def showVerse():currentVerse = random.choice(versesList);verseLabel.set_text(verses[currentVerse]);verse.set_text(currentVerse)
    with verseCard:
        verseLabel = ui.label().classes('text-center').style('font-size: 20px; font-style: italic; font-family: Times New Roman; color: #555')
        verse = ui.label().classes('text-center').style('font-size: 16px; font-family: Times New Roman; color: blue')
    ui.timer(5,showVerse)
    def fetchData():
        connection = mysql.connector.connect(host='127.0.0.1',user='root',password='Nikish@2003',database='pentecostMatrimony',ssl_disabled=True)
        cursor = connection.cursor()
        cursor.execute('''select * from userData where email = %s''',(email,))
        data = cursor.fetchone()
        cursor.close();connection.close()
        return data
    data = fetchData()
    if data is None:ui.navigate.to('/');return
    ui.label(f'Welcome {data[4]}!').style('font-size: 24px; font-weight: bold; font-family: Times New Roman; color: #333')
    ui.button('Logout', on_click=lambda: ui.navigate.to('/')).props('color=red')
    searchInput,searchField = searchWithFields('400','150')
    widgets,photo,avatar,emailWidget,password,chips = form('#f9f9f9','#000000',5,'25%')
    avatar.set_source(f"data:image/{imghdr.what(None, h=data[1]) or 'jpeg'};base64,{base64.b64encode(data[1]).decode()}")
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
    ui.button('Check',on_click=lambda:print(chips.lists))
    def downloadPdf():
        from fpdf import FPDF
        pdf = FPDF()
        pdf.
        for i in detailsCard:
            
            print(i)
    def showCurrentDetails(i):
        detailsCard.clear()
        with detailsCard:
            ui.interactive_image(f"data:image/{imghdr.what(None,h=i[1]) or 'jpeg'};base64,{base64.b64encode(i[1]).decode()}").style('background-color: #fff; border-radius: 8px; height:300px; width:300px; object-fit:cover;')
            for x in i[4:-2]:ui.label(x).style('font-size: 20px; font-weight: bold; font-family: Times New Roman; color: #333')
        userCardDetails.set_visibility(True)
    def refreshMaster(data):
        with matchDataMaster:
            for i in data:
                currentUser = ui.card().classes('hover-card p-4').style('background-color: #fff; border-radius: 8px; box-shadow: 0 2px 4px rgba(0, 0, 0, 0.5); height:300px; width:300px; display:flex; flex-direction:column; align-items:center; justify-content:center; cursor:pointer;')
                with currentUser:ui.image(f"data:image/{imghdr.what(None,h=i[1]) or 'jpeg'};base64,{base64.b64encode(i[1]).decode()}").style('background-color: #fff; border-radius: 8px; height:300px; width:300px; object-fit:cover;')
                currentUser.on('click',lambda i=i:showCurrentDetails(i))
    def assignUsers():
        matchDataMaster.clear()
        dob,gender = data[6],data[7]
        async def search():
            try:connection = mysql.connector.connect(host='127.0.0.1',user='root',password='Nikish@2003',database='pentecostMatrimony',ssl_disabled=True)
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
    with ui.card().classes('p-4 bg-transparent shadow-none border border-gray-300').style('position: absolute; top:250px; left:400px; width:1060px; height:1500px; background-color: grey; backdrop-filter: blur(10px); border-radius: 8px; box-shadow: 0 4px 8px rgba(0, 0, 0, 0.5)'):matchDataMaster = ui.grid(columns=3).classes('gap-4')
    assignUsers()
    searchInput.on('keydown.enter',lambda x:assignUsers())
    searchInput.on('blur',lambda x:assignUsers())
    userCardDetails = ui.card().style('position: absolute; top:250px; left:100px; width:1060px; height:1500px; background-color: grey; backdrop-filter: blur(10px); border-radius: 8px; box-shadow: 0 4px 8px rgba(0, 0, 0, 0.5); padding:20px; overflow-y:auto;')
    with userCardDetails:
        ui.label('User Details').classes('text-center').style('font-size: 24px; font-weight: bold; font-family: Times New Roman; color: #333')
        ui.button('back',on_click=lambda:userCardDetails.set_visibility(False))
        ui.button('Download',on_click=lambda:downloadPdf())
        detailsCard = ui.card().classes('w-[600px] h-[600px] bg-gray-100 rounded-lg shadow-lg p-4')
    userCardDetails.set_visibility(False)

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
            if data:checkUser(data, password.value)
            else:ui.notification('No account found with this email. Please register first.',close_button=True,type='negative')
        ui.button('Sign in',on_click=handleLogin,icon='login',color='red').classes('w-full')
        ui.link('Register',target='/register')
    ui.button('Try',on_click=lambda:ui.navigate.to('/test'))

ui.run(host='127.0.0.1', port=8080)       # page - http://127.0.0.1:8080/