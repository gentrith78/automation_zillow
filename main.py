from playwright.sync_api import sync_playwright
import time
import csv
import os
data = []

def read_csv():
    dirs = os.listdir(os.getcwd()+'/input')
    csv_path = f'{os.getcwd()}/input/{dirs[0]}'
    if '.csv'in csv_path:
        with open(f'{os.getcwd()}/input/{dirs[0]}','r') as f:
            csvFile = csv.reader(f)

            for lines in csvFile:
                data.append(lines)
            f.close()
    else:
        print('Please enter a csv file')

def select_beedroms_bathrooms_guests(frame,beedroms,bathrooms):
    beedroms = round(beedroms)
    print(bathrooms, 'bath number')
    if 'float' in str(type(bathrooms)):
        if float(bathrooms) - round(bathrooms) == 0:
            bathrooms= round(bathrooms)
    if 'float' in str(type(bathrooms)):
        if float(bathrooms) == 1.5:
            bathrooms = 1
        if float(bathrooms) == 2.5:
            bathrooms = 3
        if float(bathrooms) == 3.5:
            bathrooms = 5
        if float(bathrooms) == 4.5:
            bathrooms = 7
        if float(bathrooms) == 5.5:
            bathrooms = 9
        else:
            bathrooms = round(bathrooms)
    else:
        if 'int' in str(type(bathrooms)):
           if int(bathrooms) == 1:
               bathrooms = 0
           if int(bathrooms) == 2:
               bathrooms = 2
           if int(bathrooms) == 3:
               bathrooms = 4
           if int(bathrooms) == 4:
               bathrooms = 6
           if int(bathrooms) == 5:
               bathrooms = 8
           if int(bathrooms) >= 6:
               bathrooms = 10
           else:
               print('bathroom number not relevant')
    print(beedroms)
    print(bathrooms,'bath id')
    guests = beedroms * 2
    #select beedroms
    frame.click('//*[@id="root"]/div/div[2]/form/div/div[1]/button')
    if beedroms >= 6:
        beedroms = 6
    if beedroms >=1:
        frame.click(f'//*[@id="bedrooms-item-{beedroms}"]')
    #select bathrooms
    frame.click('//*[@id="root"]/div/div[2]/form/div/div[2]/button')
    try:
        if bathrooms >=1:
            frame.click(f'//*[@id="bathrooms-item-{bathrooms}"]')
    except:
        print('Calculating without bathroom number')
        pass
    #select guests
    frame.click('//*[@id="root"]/div/div[2]/form/div/div[3]/button')
    if guests >= 20:
        guests  = 20
    if guests > 1:
        frame.click(f'//*[@id="accommodates-item-{guests-1}"]')

def get_estimated_revenue(frame,address,bedrooms,bathrooms):
    print(address)
    print(address)
    frame.type(selector='css=[placeholder="Enter a Street Address"]',text=address,delay=10)
    time.sleep(1)
    #select addres in dropdown
    try:
        frame.click('//*[@id="geosuggest__list"]',timeout=5000)
    except:
        print("Couldn't Find Address")
        return "Couldn't Find Address"
    # print('Selected address by dropdown')
    time.sleep(1)
    #click search button
    frame.click('//*[@id="root"]/div/div[2]/form/div/button')
    # print('Search Button Clicked')
    time.sleep(1)
    #there comes the part to select bedrom number and bath number and guest number
    select_beedroms_bathrooms_guests(frame, bedrooms, bathrooms)
    #Calculate income
    time.sleep(2)
    frame.click('//*[@id="root"]/div/div[2]/form/button')
    # print('Calculate Income Clicked')
    time.sleep(2.5)
    #get estimated revenue
    estimated_revenue = frame.query_selector('//*[@id="root"]/div/div[2]/div[1]/div[3]/div')
    print(estimated_revenue.inner_text())
    time.sleep(1)
    #search again
    frame.click('//*[@id="root"]/div/div[2]/div[2]/button')
    return estimated_revenue.inner_text()
def run(playwright):
    chromium = playwright.chromium # or "firefox" or "webkit".
    browser = chromium.launch(headless=False)
    page = browser.new_page(user_agent='Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.0.0 Safari/537.36')
    page.goto("https://hostfinancial.com/airbnb-str-projected-revenue-calculator/",wait_until='networkidle',timeout=50000)
    # page.wait_for_load_state('domcontentloaded',timeout=50000)
    #fill the input
    frame = page.main_frame.child_frames[0]
    for index,line in enumerate(data):
        if index == 0:
            continue
        if index >20:
            break
        address = line[3],line[4],line[5]
        bedrooms = line[8]
        bathrooms = line[9]
        revenue = get_estimated_revenue(frame, str(address), float(bedrooms), float(bathrooms))
        if "Couldn't Find Address" in revenue:
            continue
        data[index].append(revenue)
    browser.close()




def write_csv():
    dirs = os.listdir(os.getcwd()+'/input')
    output_file =  os.getcwd()+'/output/'+f'RESULT {dirs[0]}'
    with open(output_file,'w') as f:
        csvwriter = csv.writer(f)
        csvwriter.writerows(data)

if __name__ == '__main__':
    read_csv()
    try:
        with sync_playwright() as playwright:
            run(playwright)
    except Exception as e:
        print(str(e))
    write_csv()