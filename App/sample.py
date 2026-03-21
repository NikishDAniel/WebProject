# n = 99999
# if n>999:
#     length = len(str(n))-3
#     if length==1:print(n-1000+1)
#     else:
#         power = 10**(length+2)
#         print(9*power+n-power)
# else:print(0)

widgets = {'name':['input','Name',''],'profession':['input','Profession',''],'dateOfBirth':['date_input','Date of Birth',''],'qualification':['input','Qualification',''],'currentResidentAddress':['textarea','Current Resident Address',''],'background':['select','Family Origin','TPM Born,CSI/Other'],'gender':['radio','Gender','Male,Female']
                ,'maritalStatus':['radio','Marital Status','Single,widowed'],'income':['input','Income',''],'languagesKnown':['input','Languages Known',''],'fatherName':['input','Father Name',''],'motherName':['input','Mother Name',''],'parentsNumber':['input','Parents Number',''],'WhatsAppNumber':['input','WhatsApp Number',''],
                'familyStatus':['select','Family Status','High Class,Middle Class'],'hometown':['input','Hometown',''],'siblings':['input','Siblings',''],'localFaithHome':['input','Local Faith Home',''],'centreFaithHome':['input','Centre Faith Home',''],'expectations':['textarea','Expectations','']}
data = list(widgets.keys())
index = 0
for i in 'Name,Profession,Dob,Qualification,Height,Income,FamilyOrigin,Languages,FatherName,MotherName,ParentsNumber,WhatsAppTelegram,Status,Hometown,CurrentAddress,Siblings,LocalFaithHome,CenterFaithHome,Expectations'.split(','):
    if i!=data[index]:print(i,data[index])
    index += 1