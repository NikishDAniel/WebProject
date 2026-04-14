# from nicegui import ui
# import mysql.connector, base64, imghdr

# connection = mysql.connector.connect(
#     host='127.0.0.1',
#     user="root",
#     password="Nikish@2003",
#     database="pentecostMatrimony"
# )

# photo = b''

# @ui.page('/')
# def sample():
#     global photo

#     # ---------- IMAGE ----------
#     with ui.avatar(size='150px') as avatar:
#         avatarImage = ui.image().style('width:100%; height:100%; object-fit:cover')

#     # ---------- BUTTONS ----------
#     save_btn = ui.button('Save', on_click=lambda: save())
#     ui.button('Load', on_click=lambda: load())
#     save_btn.disable()

#     # ---------- UPLOAD ----------
#     async def savePhoto(e):
#         global photo
#         photo = await e.file.read()   # ✅ RAW BYTES

#         encoded = base64.b64encode(photo).decode()
#         avatarImage.set_source(f'data:image/jpeg;base64,{encoded}')

#         upload.reset()
#         save_btn.enable()

#     upload = ui.upload(auto_upload=True, on_upload=savePhoto)\
#         .props('accept=image/*')\
#         .classes('hidden')

#     avatar.on('click', lambda: upload.run_method('pickFiles'))

#     # ---------- LOAD ----------
#     def load():
#         global photo

#         cursor = connection.cursor()
#         cursor.execute("SELECT photo FROM sample ORDER BY id DESC LIMIT 1")
#         data = cursor.fetchone()[0]
#         cursor.close()

#         img_type = imghdr.what(None, h=data) or 'jpeg'

#         encoded = base64.b64encode(data).decode()
#         avatarImage.set_source(f"data:image/{img_type};base64,{encoded}")
#         avatarImage.update()

#         print("Loaded:", img_type, len(data))

#     # ---------- SAVE ----------
#     def save():
#         global photo

#         if not photo:
#             ui.notify('No image uploaded', color='red')
#             return
#         connection.ping(reconnect=True)

#         cursor = connection.cursor()
#         cursor.execute(
#             "INSERT INTO sample(photo) VALUES (%s)",
#             (photo,)
#         )
#         connection.commit()

#         print("Inserted ID:", cursor.lastrowid)

#         cursor.close()
#         ui.notify('Saved successfully', color='green')


# ui.run(host='127.0.0.1', port=8080)

# import bcrypt,mysql.connector

# connection = mysql.connector.connect(host = '127.0.0.1',user="root",password="Nikish@2003",database="pentecostMatrimony")
# cursor = connection.cursor()
# cursor.execute("update userData set passwords = %s where email='nikishdaniel1@gmail.com'",(bcrypt.hashpw(b'nikish', bcrypt.gensalt()),))
# connection.commit()
# cursor.close()
# print("Password updated successfully")


