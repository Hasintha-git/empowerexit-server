from datetime import date
from dateutil.relativedelta import relativedelta
import random

def get_current_month_name():
        return date.today().strftime("%B")

def get_current_year():
        return date.today().year

def get_current_month_start_date():
        current_month = date.today().month
        current_year = date.today().year
        return str(current_year)+"-"+str(current_month)+"-01"
     
def get_current_month_end_date():
        current_month = date.today().month
        current_year = date.today().year
        return str(current_year)+"-"+str(current_month)+"-31"

def get_tuned_count(pred_amount):

        rand_int = random.randint(0,3)

        if pred_amount<20:
                return [12,15,18,21][rand_int]
        elif pred_amount < 40:
                 return [11,10,9,8][rand_int]
        elif pred_amount< 60:
                return [7,6,5,4][rand_int]
        elif pred_amount< 80:
                return [3,2,3,2][rand_int]
        else:
                return [1,2,1,2][rand_int]

# returns custom past date from the today date by substracting number of months
def get_custom_past_date(months_number):
        return date.today() - relativedelta(months=months_number)

def get_month_from_the_date(date_input):
        return str(date_input.month).zfill(2)

def get_year_from_the_date(date_input):
        return date_input.year

def get_month_name(date):
        return date.strftime("%B")

