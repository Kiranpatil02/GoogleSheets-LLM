import gspread
gc=gspread.service_account('C:/Users/Kiran Patil/Desktop/For fun/Google_sheets+LLM/Google_Sheets/credintials.json')

sh=gc.open("sheets1")
print(sh.sheet1.get("A1"))

sh.update_title("Check-OUT!!")