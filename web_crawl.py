def web_crawl_fnc(arg_email, arg_password, arg_company, arg_customer, arg_due_date, arg_invoice_num, arg_item01_name, arg_item01_description, arg_item01_quantity, arg_item01_price, arg_item02_name, arg_item02_description, arg_item02_quantity, arg_item02_price, arg_item03_name, arg_item03_description, arg_item03_quantity, arg_item03_price):
    try:
        #import undetected_chromedriver, open url_link-------------------------------------------------------------------------------------
        from seleniumbase import Driver

        driver = Driver(uc=True, headless=False)
        driver.uc_open_with_reconnect("https://akaunting.com/login", 4)




        #get html_tag-----------------------------------------------------------------------------------------------------------------------
        from selenium.webdriver.support.wait import WebDriverWait
        from selenium.webdriver.support.expected_conditions import presence_of_element_located
        from selenium.webdriver.common.by import By

        wait = WebDriverWait(driver, 10)

        username = driver.find_element(By.NAME, "email")
        password = driver.find_element(By.NAME, "password")
        login = wait.until(presence_of_element_located((By.XPATH, '//*[@id="login-form"]/div/div[5]/button')))




        #key_in html_tag, click html_tag(outer_div can bubble into inner_div)----------------------------------------------------------------
        from selenium.webdriver.common.keys import Keys

        selected_account_email = arg_email 
        selected_account_password = arg_password 
        username.clear()
        username.send_keys(selected_account_email)
        password.clear()
        password.send_keys(selected_account_password)

        driver.uc_gui_click_captcha()
        login.click()




        #repeat(get html_tag, key_in html_tag, click html_tag)-------------------------------------------------------------------------------
        #get all html_tag that contain finding_xpath 
        wait.until(presence_of_element_located((By.XPATH, "/html/body/div[1]/div[2]/div[2]/div[2]/div[3]/div[1]/section/ul/li/div/dl/div[1]/dd"))) 
        companies = driver.find_elements(By.XPATH, "/html/body/div[1]/div[2]/div[2]/div[2]/div[3]/div[1]/section/ul/li/div/dl/div[1]/dd")
        '''html_tag_01 = /html/body/div[1]/div[2]/div[2]/div[2]/div[3]/div[1]/section/ul/li[1]/div/dl/div[1]/dd
        html_tag_02 = /html/body/div[1]/div[2]/div[2]/div[2]/div[3]/div[1]/section/ul/li[2]/div/dl/div[1]/dd'''

        #find selected_company_index
        selected_company = arg_company 
        for company in companies:
            if company.text == selected_company:
                selected_company_index = companies.index(company)

        #click selected_company_index html_tag 
        wait.until(presence_of_element_located((By.XPATH, "/html/body/div[1]/div[2]/div[2]/div[2]/div[3]/div[1]/section/ul/li/div/dl/div[3]/a")))
        login = driver.find_elements(By.XPATH, "/html/body/div[1]/div[2]/div[2]/div[2]/div[3]/div[1]/section/ul/li/div/dl/div[3]/a") 
        login[selected_company_index].click()




        #repeat(get html_tag, key_in html_tag, click html_tag)-------------------------------------------------------------------------------
        #driver switch to new_tab
        driver.switch_to.window(driver.window_handles[-1])

        #force desktop layout
        driver.set_window_size(1366, 768)
        driver.refresh()

        #get html_tag by tag_type, class, href
        sales = wait.until(presence_of_element_located((By.CSS_SELECTOR, "summary.block[href='#navbar-sales']")))
        sales.click()

        #get html_tag by tag_type, id, class
        invoices = wait.until(presence_of_element_located((By.CSS_SELECTOR, "a#menu-sales-invoices.text-purple")))
        invoices.click()

        #get html_tag by tag_type, id
        new_invoice = wait.until(presence_of_element_located((By.CSS_SELECTOR, "a#index-more-actions-new-invoice")))
        new_invoice.click()




        #iframe(same url_link but diffrent_html)------------------------------------------------------------------------------------------------
        try:
            wait.until(presence_of_element_located((By.CSS_SELECTOR, "iframe#ug-tooltip-frame")))
            driver.switch_to.frame("ug-tooltip-frame")
            close_btn = wait.until(presence_of_element_located((By.CSS_SELECTOR, ".ug-preview-quit-button"))) 
            driver.execute_script("arguments[0].click();", close_btn)
            driver.switch_to.default_content()
        except:
            pass




        #repeat(get html_tag, key_in html_tag, click html_tag)-------------------------------------------------------------------------------
        selected_customer = arg_customer

        add_customer = wait.until(presence_of_element_located((By.CSS_SELECTOR, "button.w-full.h-full.flex.flex-col.items-center.justify-center")))
        add_customer.click()

        type_customer = wait.until(presence_of_element_located((By.CSS_SELECTOR, "input[placeholder='Type a Customer name']")))
        type_customer.clear()
        type_customer.send_keys(selected_customer) 

        wait.until(presence_of_element_located((By.XPATH, '//*[@id="select-contact-card-5"]/div/div[1]/div/div[2]/ul/div')))
        customer_list = driver.find_elements(By.XPATH, '//*[@id="select-contact-card-5"]/div/div[1]/div/div[2]/ul/div') 
        if customer_list[0].text != "No matching data":
            old_customer = wait.until(presence_of_element_located((By.XPATH, '//*[@id="select-contact-card-5"]/div/div[1]/div/div[2]/ul/div[1]')))
            old_customer.click()
        else:
            new_customer = wait.until(presence_of_element_located((By.XPATH, '//*[@id="select-contact-card-5"]/div/div[1]/div/div[2]/div[2]'))) 
            new_customer.click()

            #modal(same_html but overlapped & need_interact_first)
            modal = wait.until(presence_of_element_located((By.CSS_SELECTOR, "div.modal-add-new.show")))
                
            new_customer_name = wait.until(presence_of_element_located((By.CSS_SELECTOR, "input[placeholder='Enter Name']"))) 
            new_customer_name.clear()
            new_customer_name.send_keys(selected_customer)
            new_customer_currency = wait.until(presence_of_element_located((By.CSS_SELECTOR, "input[placeholder='- Select Currency -']"))) 
            new_customer_currency.click()

            from selenium.webdriver.support.ui import Select
            dropdown = wait.until(presence_of_element_located((By.CSS_SELECTOR, 'select[name="currency_code"]')))
            dropdown = Select(dropdown)
            dropdown.select_by_index(0)

            save = wait.until(presence_of_element_located((By.CSS_SELECTOR, "button.bg-green.text-white.rounded-lg")))
            save.click()




        #repeat(get html_tag, key_in html_tag, click html_tag)-------------------------------------------------------------------------------
        selected_due_date = arg_due_date
        selected_invoice_num = arg_invoice_num

        due_date = wait.until(presence_of_element_located((By.CSS_SELECTOR, 'input[type="hidden"][placeholder="Enter Due Date"]'))) 
        driver.execute_script("flatpickr(arguments[0]).setDate(arguments[1], true, 'd-m-Y')", due_date, selected_due_date)

        invoice_number = wait.until(presence_of_element_located((By.CSS_SELECTOR, 'input[placeholder="Enter Invoice Number"]'))) 
        invoice_number.clear()
        invoice_number.send_keys(selected_invoice_num)




        #repeat(get html_tag, key_in html_tag, click html_tag)-------------------------------------------------------------------------------
        #loop through dict_i, dict_i[key] pass to function
        list_01 = [
        {"name" : arg_item01_name,
        "description" : arg_item01_description,
        "quantity" : arg_item01_quantity,
        "price" : arg_item01_price},

        {"name" : arg_item02_name,
        "description" : arg_item02_description,
        "quantity" : arg_item02_quantity,
        "price" : arg_item02_price},

        {"name" : arg_item03_name,
        "description" : arg_item03_description,
        "quantity" : arg_item03_quantity,
        "price" : arg_item03_price}
        ]

        def add_item(index, dict_i):
            add_item = wait.until(presence_of_element_located((By.CSS_SELECTOR, "button.w-full.h-10.flex.items-center.justify-center.text-purple")))
            add_item.click()

            type_item = wait.until(presence_of_element_located((By.CSS_SELECTOR, "input[placeholder='Type an item name']")))
            type_item.clear()
            type_item.send_keys(dict_i["name"]) 

            wait.until(presence_of_element_located((By.XPATH, '//*[@id="select-item-button-14"]/div/div/div[2]/ul/div')))
            item_list = driver.find_elements(By.XPATH, '//*[@id="select-item-button-14"]/div/div/div[2]/ul/div')
            if item_list[0].text != "No matching data":
                old_item = wait.until(presence_of_element_located((By.XPATH, '//*[@id="select-item-button-14"]/div/div/div[2]/ul/div[1]')))
                old_item.click()
            else:
                new_item = wait.until(presence_of_element_located((By.XPATH, '//*[@id="select-item-button-14"]/div/div/div[3]'))) 
                new_item.click()

                new_item_i_table = wait.until(presence_of_element_located((By.CSS_SELECTOR, f"tr[index='{index}']")))
                new_item_i_description = new_item_i_table.find_element(By.CSS_SELECTOR, f"textarea[name='items.{index}.description']") 
                new_item_i_description.clear()
                new_item_i_description.send_keys(dict_i["description"])
        
                new_item_i_price = new_item_i_table.find_element(By.CSS_SELECTOR, "input[name='price']") 
                new_item_i_price.clear()
                new_item_i_price.send_keys(dict_i["price"])

            new_item_i_table = wait.until(presence_of_element_located((By.CSS_SELECTOR, f"tr[index='{index}']")))
            new_item_i_quantity = new_item_i_table.find_element(By.CSS_SELECTOR, f"input[name='items.{index}.quantity']") 
            new_item_i_quantity.clear()
            new_item_i_quantity.send_keys(dict_i["quantity"])

        for index, dict_i in enumerate(list_01):
            if dict_i["name"]:
                add_item(index, dict_i)




        #repeat(get html_tag, key_in html_tag, click html_tag)-------------------------------------------------------------------------------
        save = wait.until(presence_of_element_located((By.CSS_SELECTOR, 'button[type="submit"].bg-green')))
        save.click()

        mark_sent = wait.until(presence_of_element_located((By.CSS_SELECTOR, 'a#show-slider-actions-mark-sent-invoice'))) 
        mark_sent.click()

        return{"status":"Success"}
    except:
        return {"status":"Fail"}
    finally:
        driver.quit()




#run at web_crawl.py, __name__ == main
#run at others.py(as import), __name__ == web_crawl
if __name__ == "__main__":
    result = web_crawl_fnc("ngjohn0996@gmail.com", "akaunting268", "HH Chef", "Gon", "31-08-2026", "8088", "Oreo", "Classic Flavour", "3", "4.00", "Coca-Cola", "Ice", "1", "2.00", "", "", "", "")
    print(result)