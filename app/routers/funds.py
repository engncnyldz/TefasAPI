from dataclasses import asdict
import traceback
from fastapi import status, HTTPException, APIRouter
from ..schemas import Fund
import requests
from bs4 import BeautifulSoup 
from babel.numbers import parse_decimal
from pydantic.json import pydantic_encoder
from ..utils.cache import push_to_cache, check_if_exists

router = APIRouter(
    prefix="/funds"
)

tefas_query_url = "https://www.tefas.gov.tr/FonAnaliz.aspx"

fund_profile = {}

def parse_fund_profile(fund_profile_table):
    for row in fund_profile_table:
        cols = row.find_all("td")
    
        fund_profile_header = cols[0].string
        fund_profile_header_value = cols[1].string

        if fund_profile_header and fund_profile_header_value:
            fund_profile.update({fund_profile_header: fund_profile_header_value})

def load_fund_page(url_params):
    r = requests.get(tefas_query_url, params=url_params)
    soup = BeautifulSoup(r.text, 'html.parser') 

    fund_main_content = soup.find("div", attrs={"id": "MainContent_PanelInfo"})
    fund_main_indicators = fund_main_content.find("div", attrs={"class": "main-indicators"})
    fund_profile_table = fund_main_content.find("div", attrs={"class": "fund-details"}).find("table", attrs={"id": "MainContent_DetailsViewFund"}).find_all("tr")
    fund_main_top_list = fund_main_indicators.find("ul").find_all("li")
    fund_main_price_list = fund_main_content.find("div", attrs={"class": "price-indicators"}).find("ul").find_all("li")

    return {
        "fund_main_content": fund_main_content,
        "fund_main_indicators": fund_main_indicators,
        "fund_profile_table": fund_profile_table,
        "fund_main_top_list": fund_main_top_list,
        "fund_main_price_list": fund_main_price_list
    }

def validate_fund_fields(fund_main_indicators, fund_main_top_list, fund_main_price_list):
    code = fund_profile.get("Kodu")
    if not code or len(code) < 1:
        code = ""
    
    title = fund_main_indicators.find("span")
    if title is None or title.string is None or len(title.string) < 1:
        title = ""
    else:
        title = fund_main_indicators.find("span").string

    last_price = fund_main_top_list[0].find("span")
    if last_price is None or last_price.string is None or len(last_price.string) < 1:
        last_price = None
    else:
        last_price = float(parse_decimal(fund_main_top_list[0].find("span").string, locale="tr"))
    
    daily_return = fund_main_top_list[1].find("span")
    if daily_return is None or daily_return.string is None or len(daily_return.string) < 2:
        daily_return = None
    else:
        daily_return = float(parse_decimal(fund_main_top_list[1].find("span").string.replace("%", ""), locale="TR"))

    total_value_try = fund_main_top_list[3].find("span")
    if total_value_try is None or total_value_try.string is None or len(total_value_try.string) < 1:
        total_value_try = None
    else:
        total_value_try = float(parse_decimal(fund_main_top_list[3].find("span").string, locale="tr"))

    last_1_month_return = fund_main_price_list[0].find("span")
    if last_1_month_return is None or last_1_month_return.string is None or len(last_1_month_return.string) < 2:
        last_1_month_return = None
    else:
        last_1_month_return = float(parse_decimal(fund_main_price_list[0].find("span").string.replace("%", ""), locale="tr"))

    last_3_months_return = fund_main_price_list[1].find("span")
    if last_3_months_return is None or last_3_months_return.string is None or len(last_3_months_return.string) < 2:
        last_3_months_return = None
    else: 
        last_3_months_return = float(parse_decimal(fund_main_price_list[1].find("span").string.replace("%", ""), locale="tr"))
    
    last_6_months_return = fund_main_price_list[2].find("span")
    if last_6_months_return is None or last_6_months_return.string is None or len(last_6_months_return.string) < 2:
        last_6_months_return = None
    else:
        last_6_months_return = float(parse_decimal(fund_main_price_list[2].find("span").string.replace("%", ""), locale="tr"))

    last_1_year_return = fund_main_price_list[3].find("span")
    if last_1_year_return is not None and last_1_year_return.string is not None and len(last_1_year_return.string) > 1:
        last_1_year_return = float(parse_decimal(fund_main_price_list[3].find("span").string.replace("%", ""), locale="tr"))
    else:
        last_1_year_return = None

    fund_fields = {
        "code": code,
        "title": title,
        "last_price": last_price,
        "daily_return": daily_return,
        "total_value_try": total_value_try,
        "last_1_month_return": last_1_month_return,
        "last_3_months_return": last_3_months_return,
        "last_6_months_return": last_6_months_return,
        "last_1_year_return": last_1_year_return
    }
    
    return fund_fields

def initialize_fund(fund_fields):
    fund = Fund(
    code= fund_fields.get("code"),
    title= fund_fields.get("title"),
    last_price= fund_fields.get("last_price"),
    daily_return= fund_fields.get("daily_return"),
    total_value_try= fund_fields.get("total_value_try"),
    last_1_month_return= fund_fields.get("last_1_month_return"),
    last_3_months_return= fund_fields.get("last_3_months_return"),
    last_6_months_return= fund_fields.get("last_6_months_return"),
    last_1_year_return= fund_fields.get("last_1_year_return")
    )

    return fund

@router.get("/{code}", response_model=Fund, status_code=status.HTTP_200_OK)
def get_fund(code: str):

    url_params = {"FonKod": code}

    try:
        cached_data = check_if_exists(code)

        if (cached_data):
            print("fetching from cache...")
            return cached_data
        else:
            print("getting fresh data...")
            fund_page = load_fund_page(url_params)
            parse_fund_profile(fund_page.get("fund_profile_table"))
            fund_fields = validate_fund_fields(fund_page.get("fund_main_indicators"), fund_page.get("fund_main_top_list"), fund_page.get("fund_main_price_list"))
            fund = initialize_fund(fund_fields)
            fund_dict = fund.__dict__
            fund_dict.pop("__pydantic_initialised__")
            print(fund_dict)
            push_to_cache(code, fund_dict)
            return fund_dict
        
    except Exception as error:
        print(error)
        traceback.print_exc()
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="An error occured!")

