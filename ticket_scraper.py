# %%
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
import time
import json

# %%


def start_browser():
    options = webdriver.ChromeOptions()
    options.add_argument("--disable-blink-features=AutomationControlled")
    options.add_experimental_option('useAutomationExtension', False)
    options.add_argument("--start-maximized")
    options.add_argument("--log-level=3")
    # options.add_argument('headless')
    driver = webdriver.Chrome(options=options, service_log_path='NUL')
    return driver


def read_json():
    with open('autofill.json') as json_file:
        data = json.load(json_file)
        return data


data = read_json()


def login(driver):

    try:
        driver.get('https://tickets.museivaticani.va/agency/login')
        username_xpath = "/html/body/app-root/app-empty-layout/div/div/main/app-login/div/form/div[2]/div/div[1]/input"
        pass_xpath = "/html/body/app-root/app-empty-layout/div/div/main/app-login/div/form/div[2]/div/div[2]/input"
        username = WebDriverWait(driver, 100).until(
            EC.visibility_of_element_located((By.XPATH, username_xpath)))
        password = WebDriverWait(driver, 100).until(
            EC.visibility_of_element_located((By.XPATH, pass_xpath)))
        username.send_keys(data['username'])
        password.send_keys(data['password'])
        # click ok
        driver.find_element_by_xpath(
            "/html/body/app-root/app-empty-layout/div/div/main/app-login/div/form/div[2]/div/div[3]/div/button").click()
        print("login successful")
    except:
        print('login Failed!!!, sleeping for 100 sec')
        # time.sleep(100)


def search_dates_helper(input_date, driver):
    # this function only clicks the date specified, not month or year.

    row1 = driver.find_element(
        By.XPATH, "/html/body/div[2]/div[2]/div/mat-datepicker-content/div[3]/mat-calendar/div/mat-month-view/table/tbody/tr[1]")
    row2 = driver.find_element(
        By.XPATH, "/html/body/div[2]/div[2]/div/mat-datepicker-content/div[3]/mat-calendar/div/mat-month-view/table/tbody/tr[2]")
    row3 = driver.find_element(
        By.XPATH, "/html/body/div[2]/div[2]/div/mat-datepicker-content/div[3]/mat-calendar/div/mat-month-view/table/tbody/tr[3]")
    row4 = driver.find_element(
        By.XPATH, "/html/body/div[2]/div[2]/div/mat-datepicker-content/div[3]/mat-calendar/div/mat-month-view/table/tbody/tr[4]")
    row5 = driver.find_element(
        By.XPATH, "/html/body/div[2]/div[2]/div/mat-datepicker-content/div[3]/mat-calendar/div/mat-month-view/table/tbody/tr[5]")
    row6 = 0
    try:
        row6 = driver.find_element(
            By.XPATH, "/html/body/div[2]/div[2]/div/mat-datepicker-content/div[3]/mat-calendar/div/mat-month-view/table/tbody/tr[6]")
    except:
        pass
    array = []
    array.append(row1.find_elements_by_xpath(".//*"))
    array.append(row2.find_elements_by_xpath(".//*"))
    array.append(row3.find_elements_by_xpath(".//*"))
    array.append(row4.find_elements_by_xpath(".//*"))
    array.append(row5.find_elements_by_xpath(".//*"))
    parent_array = array
    if row6 != 0:
        array.append(row6.find_elements_by_xpath(".//*"))
    for a in range(len(parent_array)):
        array = parent_array[a]
        complete = False
        for i in range(len(array)):
            if array[i].text == str(input_date):
                time.sleep(1)
                array[i].click()
                complete = True
                print('clicked')
                print(array[i].text)

                break
        if complete == True:
            break


def search_dates(driver):

    lang_button_xpath = "/html/body/app-root/app-main-layout/mat-sidenav-container/mat-sidenav-content/div/app-header/mat-toolbar/mat-toolbar-row/div[2]/div[4]/app-dropdown/article/div/input[1]"
    WebDriverWait(driver, 10).until(
        EC.visibility_of_element_located((By.XPATH, lang_button_xpath)))
    english_lang_xpath = "/html/body/app-root/app-main-layout/mat-sidenav-container/mat-sidenav-content/div/app-header/mat-toolbar/mat-toolbar-row/div[2]/div[4]/app-dropdown/article/section/div[3]"
    driver.find_element_by_xpath(lang_button_xpath).click()
    driver.find_element_by_xpath(english_lang_xpath).click()
    for i in range(100):
        WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located((By.XPATH, "/html/body/app-root/app-main-layout/mat-sidenav-container/mat-sidenav-content/app-home/div[1]/app-main-search/div/div/div/h1")))
        some_text = driver.find_element(
            By.XPATH, "/html/body/app-root/app-main-layout/mat-sidenav-container/mat-sidenav-content/app-home/div[1]/app-main-search/div/div/div/h1")
        if "Book your visit" not in some_text.text:
            time.sleep(1)
            print('Language is not fully changed')
            some_text = driver.find_element(
                By.XPATH, "/html/body/app-root/app-main-layout/mat-sidenav-container/mat-sidenav-content/app-home/div[1]/app-main-search/div/div/div/h1")
        else:
            break
    visitors_xpath = "/html/body/app-root/app-main-layout/mat-sidenav-container/mat-sidenav-content/app-home/div[1]/app-main-search/div/div/div/div/app-filters/form/div[1]/div[1]/input"
    visitors = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, visitors_xpath)))
    time.sleep(1)
    visitors.send_keys(data["Visitors"])
    time.sleep(1)
    # Date Mechanism,
    '''click on date element, check the current month, lowercase the text found,
    check if input month is same, while its not same keep pressing next
    once it is iterate through div and find the same date 
    '''
    date_xpath = "/html/body/app-root/app-main-layout/mat-sidenav-container/mat-sidenav-content/app-home/div[1]/app-main-search/div/div/div/div/app-filters/form/div[1]/div[2]/app-datepicker/mat-form-field/div/div[1]/div[1]/input"
    driver.find_element_by_xpath(date_xpath).click()
    month_array = ["January", "February", "March", "April", "May", "June",
                   "July", "August", "September", "October", "November", "December"]
    text_xpath = "/html/body/div[2]/div[2]/div/mat-datepicker-content/div[3]/mat-calendar/app-calendar-header/div/span"
    text = WebDriverWait(driver, 10).until(
        EC.visibility_of_element_located((By.XPATH, text_xpath))).text
    #text = driver.find_element_by_xpath(text_xpath).text
    for i in range(20):
        if (len(text) < 5) or 'Luglio' in text:
            for i in month_array:
                if i in text:
                    break
            time.sleep(1)
            text = driver.find_element_by_xpath(text_xpath).text
    right_arrow = driver.find_element_by_xpath(
        "/html/body/div[2]/div[2]/div/mat-datepicker-content/div[3]/mat-calendar/app-calendar-header/div/button[2]")

    print('Trying to choose')
    print(data['Date Month'])
    for i in range(40):
        if data['Date Month'] in text:
            break
        right_arrow.click()
        text = driver.find_element_by_xpath(
            '/html/body/div[2]/div[2]/div/mat-datepicker-content/div[3]/mat-calendar/app-calendar-header/div/span').text
        print(text)
        if i == 39:
            print('Coding mistake found when retrievting month text')

    search_dates_helper(data["Date Digit"], driver)
    print('choosing date successful')
    # Date Machenism over
    # Area
    area = driver.find_element_by_xpath(
        "/html/body/app-root/app-main-layout/mat-sidenav-container/mat-sidenav-content/app-home/div[1]/app-main-search/div/div/div/div/app-filters/form/div[1]/div[3]/app-dropdown/article/div/input[1]")
    area.click()
    vatician_museums = driver.find_element_by_xpath(
        "/html/body/app-root/app-main-layout/mat-sidenav-container/mat-sidenav-content/app-home/div[1]/app-main-search/div/div/div/div/app-filters/form/div[1]/div[3]/app-dropdown/article/section/div[1]")
    vatician_museums.click()
    print('choosing area successful')
    # area complete
    # choose who
    who = driver.find_element_by_xpath(
        "/html/body/app-root/app-main-layout/mat-sidenav-container/mat-sidenav-content/app-home/div[1]/app-main-search/div/div/div/div/app-filters/form/div[1]/div[4]/app-dropdown/article/div/input[1]")
    who.click()
    groups_xpath = "/html/body/app-root/app-main-layout/mat-sidenav-container/mat-sidenav-content/app-home/div[1]/app-main-search/div/div/div/div/app-filters/form/div[1]/div[4]/app-dropdown/article/section/div[3]"
    groups = WebDriverWait(driver, 10).until(
        EC.visibility_of_element_located((By.XPATH, groups_xpath)))
    groups.click()
    search = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, "/html/body/app-root/app-main-layout/mat-sidenav-container/mat-sidenav-content/app-home/div[1]/app-main-search/div/div/div/div/app-filters/form/div[2]/div/button")))
    search.click()

###


def choose_time_and_procced_to_payment(driver):
    book_xpath = "/html/body/app-root/app-main-layout/mat-sidenav-container/mat-sidenav-content/app-visit/div/div[3]/div/div/app-ticket/div[1]/div/div[4]/div[3]/button"
    book = WebDriverWait(driver, 100).until(
        EC.presence_of_element_located((By.XPATH, book_xpath)))
    book.click()
    ticket_quantity_xpath = "/html/body/app-root/app-main-layout/mat-sidenav-container/mat-sidenav-content/app-visit/div/div[3]/div/div/app-ticket/div[1]/app-ticket-details/div/form/div[2]/app-ticket-price-list/div[1]/div/div[1]/div[1]/app-dropdown/article/div/input[1]"
    ticket_quantity = WebDriverWait(driver, 10).until(
        EC.visibility_of_element_located((By.XPATH, ticket_quantity_xpath)))
    ticket_quantity.click()
    # select 25
    driver.find_element_by_xpath(
        "/html/body/app-root/app-main-layout/mat-sidenav-container/mat-sidenav-content/app-visit/div/div[3]/div/div/app-ticket/div[1]/app-ticket-details/div/form/div[2]/app-ticket-price-list/div[1]/div/div[1]/div[1]/app-dropdown/article/section/div["+str(int(data["Visitors"])+1)+"]").click()
    # select afternoon
    morning_xpath = "/html/body/app-root/app-main-layout/mat-sidenav-container/mat-sidenav-content/app-visit/div/div[3]/div/div/app-ticket/div[1]/app-ticket-details/div/form/div[4]/div[2]/div/app-ticket-time/div/div/div[1]/div/div[1]"
    lunch_xpath = "/html/body/app-root/app-main-layout/mat-sidenav-container/mat-sidenav-content/app-visit/div/div[3]/div/div/app-ticket/div[1]/app-ticket-details/div/form/div[4]/div[2]/div/app-ticket-time/div/div/div[1]/div/div[2]"
    afternoon_xpath = "/html/body/app-root/app-main-layout/mat-sidenav-container/mat-sidenav-content/app-visit/div/div[3]/div/div/app-ticket/div[1]/app-ticket-details/div/form/div[4]/div[2]/div/app-ticket-time/div/div/div[1]/div/div[3]"
    evening_xpath = "/html/body/app-root/app-main-layout/mat-sidenav-container/mat-sidenav-content/app-visit/div/div[3]/div/div/app-ticket/div[1]/app-ticket-details/div/form/div[4]/div[2]/div/app-ticket-time/div/div/div[1]/div/div[4]"
    WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, lunch_xpath)))
    final_xpath = ""
    if data['Portion Of Day'] == "Morning":
        final_xpath = morning_xpath
    if data['Portion Of Day'] == "Lunch":
        final_xpath = lunch_xpath
    if data['Portion Of Day'] == "Evening":
        final_xpath = evening_xpath
    if data['Portion Of Day'] == "Afternoon":
        final_xpath = afternoon_xpath
    driver.find_element_by_xpath(final_xpath).click()
    # select Time
    row_element = driver.find_element(
        By.XPATH, "/html/body/app-root/app-main-layout/mat-sidenav-container/mat-sidenav-content/app-visit/div/div[3]/div/div/app-ticket/div[1]/app-ticket-details/div/form/div[4]/div[2]/div/app-ticket-time/div/div/div[1]/app-ticket-time-table/div")
    row_array = row_element.find_elements_by_xpath(".//*")
    for i in row_array:
        if data['Time Of day'] in i.text:
            print(i.text)
            if "SOLD OUT" in i.text:
                print(
                    'Tickets for THIS TIME ARE SOLD OUT!!! Please SELECT DIFfferent time in JSON file. RERUN THE PROGRAM')
            i.click()
            break
    # press proceed
    driver.find_element_by_xpath(
        "/html/body/app-root/app-main-layout/mat-sidenav-container/mat-sidenav-content/app-visit/div/div[3]/div/div/app-ticket/div[1]/app-ticket-details/div/form/app-ticket-footer/div/div[4]/button").click()
    print("proceeding to payment, this function was a success")


def select_birthdate_from_picker(driver):
    date = list(data["Birthdate"])
    date_num = ""
    month_str = ""
    year_num = ""
    for a in range(len(date)):
        i = date[a]
        if(i.isnumeric()):
            if a < 3:
                date_num = date_num+i
            else:
                year_num = year_num+i
        else:
            month_str = month_str+i
    month_str = month_str.replace(" ", "")
    birthdate = driver.find_element_by_xpath(
        "/html/body/app-root/app-main-layout/mat-sidenav-container/mat-sidenav-content/app-checkout/form[1]/div/div[9]/app-manager-form/div/div/div[7]/div/app-datepicker/mat-form-field/div/div[1]/div[1]/input")
    birthdate.click()

    # first check if left should be pressed by checking if year is less than 1981
    if int(year_num) < 1981:
        back_button = driver.find_element_by_xpath(
            "/html/body/div[2]/div[2]/div/mat-datepicker-content/div[2]/mat-calendar/mat-calendar-header/div/div/button[2]")
        back_button.click()

    if int(year_num) < 1957:
        back_button = driver.find_element_by_xpath(
            "/html/body/div[2]/div[2]/div/mat-datepicker-content/div[2]/mat-calendar/mat-calendar-header/div/div/button[2]")
        back_button.click()

    matrix_element_xpath = "/html/body/div[2]/div[2]/div/mat-datepicker-content/div[2]/mat-calendar/div/mat-multi-year-view/table/tbody"
    matrix_element = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, matrix_element_xpath)))
    matrix = matrix_element.find_elements_by_xpath(".//*")
    found = False

    # first find year then repeat code to find month and repeat to find day
    for a in matrix:
        curr_elements = a.find_elements_by_xpath(".//*")
        for i in curr_elements:
            if i.text == year_num:
                i.click()
                found = True
                break
        if found == True:
            break

    # repeating code for month
    matrix_element = driver.find_element_by_xpath(
        "/html/body/div[2]/div[2]/div/mat-datepicker-content/div[2]/mat-calendar/div/mat-year-view/table/tbody")
    matrix = matrix_element.find_elements_by_xpath(".//*")
    found = False
    for a in matrix:
        curr_elements = a.find_elements_by_xpath(".//*")
        for i in curr_elements:
            if (month_str[0:3]).upper() in i.text:
                i.click()
                found = True
                print('found')
                break
        if found == True:
            break

    # repeating code for date
    matrix_element = driver.find_element_by_xpath(
        "/html/body/div[2]/div[2]/div/mat-datepicker-content/div[2]/mat-calendar/div/mat-month-view/table/tbody")
    matrix = matrix_element.find_elements_by_xpath(".//*")
    found = False
    for a in matrix:
        curr_elements = a.find_elements_by_xpath(".//*")
        for i in curr_elements:
            if (date_num).upper() in i.text:
                i.click()
                found = True
                print('found')
                break
        if found == True:
            break


def last_page_autofill(driver):
    group_name_xpath = "/html/body/app-root/app-main-layout/mat-sidenav-container/mat-sidenav-content/app-checkout/form[1]/div/div[9]/app-manager-form/div/div/div[1]/div/input"
    WebDriverWait(driver, 10).until(
        EC.visibility_of_element_located((By.XPATH, group_name_xpath)))
    group_name = driver.find_element(By.XPATH, group_name_xpath)
    group_name.send_keys(data['Group Name'])
    surname = driver.find_element_by_xpath(
        "/html/body/app-root/app-main-layout/mat-sidenav-container/mat-sidenav-content/app-checkout/form[1]/div/div[9]/app-manager-form/div/div/div[2]/div/input")
    surname.send_keys(data['Surname'])
    name = driver.find_element_by_xpath(
        "/html/body/app-root/app-main-layout/mat-sidenav-container/mat-sidenav-content/app-checkout/form[1]/div/div[9]/app-manager-form/div/div/div[3]/div/input")
    name.send_keys(data["Name"])
    press_sex = driver.find_element_by_xpath(
        "/html/body/app-root/app-main-layout/mat-sidenav-container/mat-sidenav-content/app-checkout/form[1]/div/div[9]/app-manager-form/div/div/div[4]/div/app-dropdown/article/div/input[1]")
    press_sex.click()
    sex_option1_xpath = "/html/body/app-root/app-main-layout/mat-sidenav-container/mat-sidenav-content/app-checkout/form[1]/div/div[9]/app-manager-form/div/div/div[4]/div/app-dropdown/article/section/div[1]"
    WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, sex_option1_xpath)))
    two_options_for_sex = [driver.find_element(By.XPATH, sex_option1_xpath),
                           driver.find_element_by_xpath("/html/body/app-root/app-main-layout/mat-sidenav-container/mat-sidenav-content/app-checkout/form[1]/div/div[9]/app-manager-form/div/div/div[4]/div/app-dropdown/article/section/div[1]")]
    for i in two_options_for_sex:
        if i.text == data['Sex']:
            i.click()

    country_xpath = "/html/body/app-root/app-main-layout/mat-sidenav-container/mat-sidenav-content/app-checkout/form[1]/div/div[9]/app-manager-form/div/div/div[5]/div/app-dropdown/article/div"
    country = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, country_xpath)))

    driver.find_element(
        By.XPATH, "/html/body/app-root/app-main-layout/mat-sidenav-container/mat-sidenav-content/app-checkout/form[1]/div/div[9]/app-manager-form/div/div/div[5]/div/app-dropdown/article/div").click()
    try:
        country.send_keys(data['Country'])
    except:
        time.sleep(1)
        country.send_keys(data['Country'])

    first_selection_tag = "/html/body/app-root/app-main-layout/mat-sidenav-container/mat-sidenav-content/app-checkout/form[1]/div/div[9]/app-manager-form/div/div/div[5]/div/app-dropdown/article/section/div"
    first_selection = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, first_selection_tag)))
    first_selection.click()

    city_xpath = "/html/body/app-root/app-main-layout/mat-sidenav-container/mat-sidenav-content/app-checkout/form[1]/div/div[9]/app-manager-form/div/div/div[6]/div/input"
    city = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, city_xpath)))
    city.send_keys(data["City"])

    birth_date_filler_updated(driver)

    email = driver.find_element_by_xpath(
        "/html/body/app-root/app-main-layout/mat-sidenav-container/mat-sidenav-content/app-checkout/form[1]/div/div[9]/app-manager-form/div/div/div[8]/div/input")
    email.send_keys(data['Email'])
    confirm_email = driver.find_element_by_xpath(
        "/html/body/app-root/app-main-layout/mat-sidenav-container/mat-sidenav-content/app-checkout/form[1]/div/div[9]/app-manager-form/div/div/div[9]/div/input")
    confirm_email.send_keys(data["Email"])
    mobile_num = driver.find_element_by_xpath(
        "/html/body/app-root/app-main-layout/mat-sidenav-container/mat-sidenav-content/app-checkout/form[1]/div/div[9]/app-manager-form/div/div/div[10]/div/input")
    mobile_num.send_keys(data["Mobile Number"])
    language = driver.find_element_by_xpath(
        "/html/body/app-root/app-main-layout/mat-sidenav-container/mat-sidenav-content/app-checkout/form[1]/div/div[9]/app-manager-form/div/div/div[11]/div/app-dropdown/article/div/input[1]")
    language.click()

    language_array_element_xpath = "/html/body/app-root/app-main-layout/mat-sidenav-container/mat-sidenav-content/app-checkout/form[1]/div/div[9]/app-manager-form/div/div/div[11]/div/app-dropdown/article/section/div[1]"
    language_array_element = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, language_array_element_xpath)))
    language_array = language_array_element.find_elements_by_xpath(".//*")
    for i in language_array:
        if i.text == data['Language']:
            i.click()

    check_box_1_xpath = "/html/body/app-root/app-main-layout/mat-sidenav-container/mat-sidenav-content/app-checkout/form[1]/div/div[14]/div[1]/div/div/mat-checkbox/label/span[1]"
    check_box_1 = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, check_box_1_xpath)))
    check_box_1.click()
    close_xpath = "/html/body/div[2]/div[2]/div/mat-dialog-container/app-purchase-rules/div/div[1]/button"
    close_popup = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, close_xpath)))
    close_popup.click()
    check_box_2 = driver.find_element_by_xpath(
        "/html/body/app-root/app-main-layout/mat-sidenav-container/mat-sidenav-content/app-checkout/form[1]/div/div[14]/div[2]/div/div/mat-checkbox/label/span[1]")
    check_box_2.click()
    iframe = driver.find_element_by_xpath(
        "/html/body/app-root/app-main-layout/mat-sidenav-container/mat-sidenav-content/app-checkout/form[1]/div/div[13]/div/ngx-recaptcha2/div/div/div/div/iframe")
    driver.switch_to.frame(iframe)
    driver.find_element_by_xpath(
        "/html/body/div[2]/div[3]/div[1]/div/div/span/div[1]").click()
    driver.switch_to.default_content()

    buy_button_xpath = "/html/body/app-root/app-main-layout/mat-sidenav-container/mat-sidenav-content/app-checkout/form[1]/div/div[15]/app-checkout-footer/div/div/div[2]/button"

    try:
        buy_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, buy_button_xpath)))
        buy_button.click()
    except:
        print("Buy button not accessible")

##


def birth_date_filler_updated(driver):
    # portion 1 of logic
    date = list(data["Birthdate"])
    date_num = ""
    month_str = ""
    year_num = ""
    for a in range(len(date)):
        i = date[a]
        if(i.isnumeric()):
            if a < 3:
                date_num = date_num+i
            else:
                year_num = year_num+i
        else:
            month_str = month_str+i
    month_str = month_str.replace(" ", "")
    birth_date_xpath = "/html/body/app-root/app-main-layout/mat-sidenav-container/mat-sidenav-content/app-checkout/form[1]/div/div[9]/app-manager-form/div/div/div[7]/div/app-datepicker/mat-form-field/div/div[1]/div[1]/input"
    birthdate = WebDriverWait(driver, 100).until(
        EC.presence_of_element_located((By.XPATH, birth_date_xpath)))
    birthdate.click()
    if int(year_num) < 1981:
        back_button = driver.find_element_by_xpath(
            "/html/body/div[2]/div[2]/div/mat-datepicker-content/div[2]/mat-calendar/mat-calendar-header/div/div/button[2]")
        back_button.click()

    if int(year_num) < 1957:
        back_button = driver.find_element_by_xpath(
            "/html/body/div[2]/div[2]/div/mat-datepicker-content/div[2]/mat-calendar/mat-calendar-header/div/div/button[2]")
        back_button.click()
    matrix_element_xpath = "/html/body/div[2]/div[2]/div/mat-datepicker-content/div[2]/mat-calendar/div/mat-multi-year-view/table/tbody"
    matrix_element = WebDriverWait(driver, 100).until(
        EC.presence_of_element_located((By.XPATH, matrix_element_xpath)))
    matrix = matrix_element.find_elements_by_xpath(".//*")
    found = False
# get the remainder, get the closest number by mulplication
    year_num = int(year_num)
    first_element = matrix[0].find_elements_by_xpath(".//*")[0].text

    print(first_element)
    difference = int(year_num)-int(first_element)
    print(difference)
    remainder = difference % 4
    print(remainder)
    times = int((difference-remainder)/4)
    print(int(times))
    row = times
    column = remainder
    print(row)
    print(column)
    year_element_xpath = "/html/body/div[2]/div[2]/div/mat-datepicker-content/div[2]/mat-calendar/div/mat-multi-year-view/table/tbody/tr["+str(
        row+1)+"]"+"/td["+str(column+1)+"]"
    year_element = WebDriverWait(driver, 100).until(
        EC.element_to_be_clickable((By.XPATH, year_element_xpath)))
    print(year_element.text)
    year_element.click()
    month_array = ["January", "February", "March", "April", "May", "June",
                   "July", "August", "September", "October", "November", "December"]
    month_index = 0
    for i in range(len(month_array)):
        if month_array[i].upper() in month_str.upper():
            month_index = i
            break
    column = month_index % 4
    row = int((month_index-column)/4)
    month_element_xpath = "/html/body/div[2]/div[2]/div/mat-datepicker-content/div[2]/mat-calendar/div/mat-year-view/table/tbody/tr["+str(
        row+2)+"]/td["+str(column+1)+"]"
    month_element = WebDriverWait(driver, 100).until(
        EC.element_to_be_clickable((By.XPATH, month_element_xpath)))
    month_element.click()

    matrix_element_xpath = "/html/body/div[2]/div[2]/div/mat-datepicker-content/div[2]/mat-calendar/div/mat-month-view/table/tbody"
    matrix_element = WebDriverWait(driver, 100).until(
        EC.visibility_of_element_located((By.XPATH, matrix_element_xpath)))
    matrix = matrix_element.find_elements_by_xpath(".//*")
    found = False
    for a in matrix:
        curr_elements = a.find_elements_by_xpath(".//*")
        for i in curr_elements:
            if (date_num).upper() in i.text:
                i.click()
                found = True
                print('found')
                break
        if found == True:
            break


def main_run_all():

    driver = start_browser()
    login(driver)
    search_dates(driver)
    choose_time_and_procced_to_payment(driver)

    last_page_autofill(driver)
    print('task successful')
    time.sleep(100000)


# %%
main_run_all()
