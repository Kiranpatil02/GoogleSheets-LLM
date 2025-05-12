import gspread
import os
from dotenv import load_dotenv 

gc=gspread.service_account('C:/Users/Kiran Patil/Desktop/For fun/Google_sheets+LLM/Google_Sheets/credintials.json')

load_dotenv()

Sheet_ID=os.environ["GSHEET_ID"]

sh=gc.open_by_key(Sheet_ID)

gsheet=sh.sheet1

def getvalues(cellnumber):
    val=sh.sheet1.acell(cellnumber).value
    print(f"The value of cell ${cellnumber} is :",val)

def updateTitle(titlename):
    sh.update_title(titlename)
    print(f"Title of sheet to updated to :",titlename)
    
# getvalues("C5")
def getcolumn_value(row,col):
    val=gsheet.cell(row,col).value
    print("The values are:",val)

# getcolumn_value(1,2)

def get_entirecol(col):
    values_list=gsheet.col_values(2)
    print("Entire column values are:",values_list)
    

# get_entirecol(2)

def get_alldetails():
    lists=gsheet.get_all_values()
    print(lists)

# get_alldetails()

def get_alldetails_dict():
    records=gsheet.get_all_records()
    print(records)

# get_alldetails_dict()

def formatting():
    gsheet.format('A1',{'textFormat': {'bold': True}})



def create_newWorksheet(title):
    sh=gc.create(title)
    print(sh)
    print("New worksheet created with title",title)

def Share_Spreadsheet(email):
    sh.share(email,perm_type='user',role='writer')

def create_Sheet(title,rows=100,cols=20):
    worksheet=sh.add_worksheet(title,rows=rows,cols=cols)
    print("Worksheet",worksheet)

def delete_Sheet(title):
    worksheet=sh.worksheet(title)
    sh.del_worksheet(worksheet)
    print(f'"{title}" successfully delted ')

# create_Sheet("Kira's_Portfolio",200,20)

# delete_Sheet("Kira's1")

def Get_allSheets():
    list_of_worksheets=sh.worksheets()
    return list_of_worksheets

def UpdateValue(row,col,newvalue):
    gsheet.update_cell(row,col,newvalue)
    print(f'Value updated!!')

UpdateValue(38,2,"0.62%")
