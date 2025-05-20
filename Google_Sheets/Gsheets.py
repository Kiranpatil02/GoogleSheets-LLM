import gspread
import os
import re
from dotenv import load_dotenv 
import asyncio
import google.auth
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from google.oauth2 import service_account
from typing import List,Tuple,Union
from pydantic import BaseModel,Field


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


async def get_CurrentSheet()-> str:
    """
    Tells the current Worksheet chosen. 
    """
    return gsheet.title

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
    """Logs all the data present in the Sheet, it helps to give all the information related to the spreadsheet. This can be used for further queries. 
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


async def update_values(range_name:str,values:List[List[str]],value_input_option:str="USER_ENTERED"):
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
                range=f"{gsheet.title}!{range_name}",
                valueInputOption=value_input_option,
                body=body,
            )
            .execute()
        )
        return result

    except HttpError as error:
        print(f"An error occurred: {error}")
        return error


COLUMN_LETTERS = {chr(ord('A') + i): i for i in range(26)}

async def a1_to_index(cell:str):
    match = re.match(r"^([A-Z]+)(\d+)$", cell.upper())
    if not match:
        raise ValueError(f"Invalid A1 cell reference: {cell}")
    col_letters, row_str = match.groups()
    # compute zero-based column index
    col = sum((COLUMN_LETTERS[ch] + 1) * (26 ** i) for i, ch in enumerate(reversed(col_letters))) - 1
    row = int(row_str) - 1
    return row, col

async def parse_a1_range(a1_range:str):
    """
    Accepts a string like "A1" or "B2:D4" and returns dict with startRowIndex, endRowIndex,
    startColumnIndex, endColumnIndex (exclusive).
    """
    parts = a1_range.split(':')
    if len(parts) == 1:
        start = end = parts[0]
        sr, sc =await a1_to_index(start)
        return {
            'startRowIndex': sr,
            'endRowIndex': sr + 1,
            'startColumnIndex': sc,
            'endColumnIndex': sc + 1
        }
    elif len(parts) == 2:
        sr, sc =await a1_to_index(parts[0])
        er, ec =await a1_to_index(parts[1])
        return {
            'startRowIndex': min(sr, er),
            'endRowIndex': max(sr, er) + 1,
            'startColumnIndex': min(sc, ec),
            'endColumnIndex': max(sc, ec) + 1
        }
    else:
        raise ValueError(f"Invalid A1 range: {a1_range}")


class SetBackgroundArgs(BaseModel):
    """
    Arguments for setting background color of cells.
    """        
    a1_range:str=Field(description="Single cell like 'C3' or range like 'A1:D4' (All in caps)")
    rgb:List[float]=Field(description="Three floats in [0,1] for (red, green, blue)")


async def Set_Background(args:SetBackgroundArgs):
    """
    Useful to change background color of cells either a single block of cell or range of cells.
    Example:
        >>> # change color from cell A1 to C3 with color Red
        >>> # Example: Set_Background(SetBackgroundArgs(a1_range="A1:C3",rgb=[1.0,0.0,0.0]))
    """
    if isinstance(args, dict):
        args = SetBackgroundArgs(**args)
      
    a1_range=args.a1_range
    rgb=args.rgb
    creds=service_account.Credentials.from_service_account_file(SERVICE_ACCOUNT_FILE,scopes=SCOPES)
    service=build("sheets","v4",credentials=creds)
    grid_range=await parse_a1_range(a1_range)
    grid_range['sheetId']=gsheet.id
    try:
        body={
            "requests": [
            {
                "repeatCell": {
                    "range":grid_range,
                    "cell": {
                        "userEnteredFormat": {
                            "backgroundColor":  {
                                "red": rgb[0],
                                "green":rgb[1],
                                "blue": rgb[2]
                            }
                        }
                    },
                    "fields": "userEnteredFormat.backgroundColor"
                }
            }
        ]
        }

        response=service.spreadsheets().batchUpdate(
            spreadsheetId=Sheet_ID,
            body=body,
        ).execute()
    except HttpError as error:
        print("ERROR",error)
    





