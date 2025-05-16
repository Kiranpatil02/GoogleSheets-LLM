import gspread
import os
from dotenv import load_dotenv 
import asyncio
import google.auth
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from google.oauth2 import service_account
from typing import List

gc=gspread.service_account('C:/Users/Kiran Patil/Desktop/For fun/Google_sheets+LLM/Google_Sheets/credintials.json')

load_dotenv()

global Sheet_ID
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
    """Logs all the details in the Spreadsheet in details as lists, it helps to give all the information related to the spreadsheet. It contains all the data present in the entire Spreadsheet."""
    lists=gsheet.get_all_values()
    print("ok ok")
    return str(lists)

async def Find_byValue(value:str):
    """
    Finds the first cell matching the query, and returns the row and cell value of that value.
    Example:
        Find_byValue("Housing price")
        returns (1,2) -> Explains that Housing price is found on 1st row and 2nd column.
    """
    cell=gsheet.find(value)
    return {
      "row": cell.row,
        "column": cell.col
    }


async def get_alldetails_dict()-> dict:
    """Logs all the details in the Spreadsheet in details as lists, it helps to give all the information related to the spreadsheet. It contains all the data present in the entire Spreadsheet. and returns in dictionary.
    """
    records=gsheet.get_all_records()
    print("DATA:",records)
    return records


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

async def Update_TabColor(color:str):
    """
    Changes the color of a spreadsheet tab. Accepts color in hex format. You may convert common color to appropriate HEX codes.
    """
    print("Inside udpate_tab_COlor")
    return gsheet.update_tab_color(color)


def formatting():
    gsheet.format('A1',{'textFormat': {'bold': True}})

def create_newWorksheet(title):
    sh=gc.create(title)
    print(sh)
    print("New worksheet created with title",title)

SCOPES = ['https://www.googleapis.com/auth/spreadsheets']
SERVICE_ACCOUNT_FILE = 'C:/Users/Kiran Patil/Desktop/For fun/Google_sheets+LLM/Google_Sheets/credintials.json'


async def update_values(range_name:str,values:List[List[str]]):
    """
    Useful for writing values into the spreadsheet, the range_name should be in A1 notation. and values should in list.
    Example usecase:
        update_values("A1:D2",[["A", "B"], ["C", "D"]])
    """
    creds=service_account.Credentials.from_service_account_file(SERVICE_ACCOUNT_FILE,scopes=SCOPES)

    try:
        service=build("sheets","v4",credentials=creds)

        body = {"values": values}
        print("INisde..",values)
        result=(
            service.spreadsheets()
            .values()
            .update(
                spreadsheetId=Sheet_ID,
                range=range_name,
                valueInputOption="USER_ENTERED",
                body=body,
            )
            .execute()
        )
        print(f"{result.get('updatedCells')} cells updated.")
        print("OOO",result)
        return result

    except HttpError as error:
        print(f"An error occurred: {error}")
        return error






