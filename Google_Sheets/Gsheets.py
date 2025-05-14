import gspread
import os
from dotenv import load_dotenv 
import asyncio

gc=gspread.service_account('C:/Users/Kiran Patil/Desktop/For fun/Google_sheets+LLM/Google_Sheets/credintials.json')

load_dotenv()

Sheet_ID=os.environ["GSHEET_ID"]

sh=gc.open_by_key(Sheet_ID)

global gsheet
gsheet=sh.sheet1

async def getvalues(cellnumber):
    val=sh.sheet1.acell(cellnumber).value
    print(f"The value of cell ${cellnumber} is :",val)

async def updateTitle(titlename:str)->any:
    """
    This function Renames the spreadsheet.
    by taking title as parameter.
    """
    return sh.update_title(titlename)
    

def getcolumn_value(row,col):
    val=gsheet.cell(row,col).value
    print("The values are:",val)


async def SelectSheet(sheetname:str):
    """
    Selects a worksheet by taking name of the sheet and updates to the global variable.
    """
    global gsheet
    gsheet=sh.worksheet(sheetname)
    return gsheet


async def get_entirecol(col:int)->list:
    """
    Returns a list of all values  in column.
    EXAMPLE:
        get_enirecol(3): Returns list of all values in column 3 of spread sheet. 
    """
    values_list=gsheet.col_values(col)
    return values_list
    

async def get_alldetails() -> str:
    """Logs all the details in the Spreadsheet in details as lists, it helps to give all the information related to the spreadsheet"""
    lists=gsheet.get_all_values()
    print("ok ok")
    return str(lists)




def get_alldetails_dict():
    records=gsheet.get_all_records()
    print(records)


def formatting():
    gsheet.format('A1',{'textFormat': {'bold': True}})

def create_newWorksheet(title):
    sh=gc.create(title)
    print(sh)
    print("New worksheet created with title",title)

async def Share_Spreadsheet(email:str,permission:str,role:str):
    """
    Share the spreadsheet with other accounts.
    """
    sh.share(email,perm_type='user',role='writer')

async def create_Sheet(title:str,rows:int=100,cols:int=20) -> str:
    """
    Adds a new worksheet to a spreadsheet, given a title, rows, and columns.
    Returns the title of the newly created worksheet.
    """
    worksheet=sh.add_worksheet(title,rows=rows,cols=cols)
    return worksheet

async def delete_Sheet(title:str) -> any:
    """
    Deletes a worksheet from a spreadsheet, 
    takes title(str) as parameter.
    """
    worksheet=sh.worksheet(title)
    return sh.del_worksheet(worksheet)
    

async def Get_allSheets()-> list:
    """
    Returns a list of all sheets`
    in a spreadsheet. 
    Example:
    returns: a list of :class:`worksheets <gspread.worksheet.Worksheet>
    """
    list_of_worksheets=sh.worksheets()
    return list_of_worksheets

async def UpdateValue(row:int,col:int,newvalue:str)-> any:
    """
    This function helps to Update the value of a cell by taking row,column and then new value to be updated.
    Example::

        worksheet.update_cell(1, 1, '42')

    """
    return gsheet.update_cell(row,col,newvalue)
    

