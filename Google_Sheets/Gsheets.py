import gspread
gc=gspread.service_account('C:/Users/Kiran Patil/Desktop/For fun/Google_sheets+LLM/Google_Sheets/credintials.json')

sh=gc.open_by_key("1GOqloR-cN1Jq6NFhEDh84BP8OqAMcNv7LJB8jG0SXtg")
print(sh.sheet1.get("A1"))

gsheet=sh.sheet1

def getvalues(cellnumber):
    val=sh.sheet1.acell(cellnumber).value
    print(f"The value of cell ${cellnumber} is :",val)

def updateTitle(titlename):
    gsheet.update_title("QuizMarks1")
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

formatting()