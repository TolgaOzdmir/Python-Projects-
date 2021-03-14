from selenium import webdriver  # to install selenium package from terminal: python -m pip install selenium
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

# for serial communication, to install serial package from terminal: python -m pip install serial
import serial
# from serial import Serial


SERIAL_PORT = "COM3"
BAUD_RATE = 9600

driver = webdriver.Chrome('chromedriver.exe')
options = webdriver.ChromeOptions()
wait = WebDriverWait(driver, 600)

options.add_argument("chromedriver.exe")

driver.get("http://www.google.com/")
msg = "This is Lab03, CMPE 451."
contact_list = ["Zeynep Ekin", "Annem", "Ali Can Keskin"]
count = 0

# make an object of Serial port class
sp = serial.Serial(SERIAL_PORT, BAUD_RATE, timeout=5)
# flush the serial port
sp.flush()

send_msg = False
sp.flush()

while True:

    response = sp.read(1)  # get one byte
    if response == b"S":
        send_msg = not send_msg

    while send_msg:
        # if whatsapp is not open already, open it
        if not (len(driver.window_handles) == 2):
            print("Communication started")
            driver.execute_script("window.open('https://web.whatsapp.com/')")
            handles = driver.window_handles
            driver.switch_to.window(handles[1])
            WebDriverWait(driver, 600)
            sp.flush()

        # get next byte
        response = sp.read(1)
        if response == b"S":
            send_msg = not send_msg
        elif response == b"O":
            print("Got OK Byte.  Waiting for button press.")
        elif response == b"X":
            print("Got Send message Signal!")
            contact = contact_list[count]
            # Select the contact
            x_arg = "//span[@title='{}']".format(contact)
            try:
                user = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, x_arg)))
            except:
                # If contact not found, then search for it in chat search box
                chatSearchIcon = driver.find_element_by_class_name("_3FRCZ.copyable-text.selectable-text").send_keys(
                    contact + Keys.ENTER)
                try:
                    user = driver.find_element_by_xpath(x_arg)
                except:
                    print(f"Contact {contact} not found")
                    count = (count + 1) % len(contact_list)
                    continue
            user.click()

            # find the text box and put your message in it
            # text_box = driver.find_element_by_xpath('//*[@id="main"]/footer/div[1]/div[2]/div/div[2]')
            # text_box.send_keys(f"Salam {contact}: {msg}")
            # # find the send button and click it
            # button = driver.find_element_by_class_name("_1U1xa")
            # button.click()
            # print(f"message sent to {contact}.")
            count = (count + 1) % len(contact_list)
            x_arg = '//span[contains(@title,' + contact + ')]'
            group_title = wait.until(EC.presence_of_element_located((
                By.XPATH, x_arg)))
            group_title.click()

            message = driver.find_elements_by_xpath('//*[@id="main"]/footer/div[1]/div[2]/div/div[2]')[0]

            message.send_keys(msg)

            sendbutton = driver.find_elements_by_xpath('//*[@id="main"]/footer/div[1]/div[3]/button')[0]
            sendbutton.click()

        else:
            print("Got nothing.  Still waiting.")
    # close whatsapp
    if (len(driver.window_handles) == 2):
        handles = driver.window_handles;
        driver.switch_to.window(handles[1])
        driver.close()

        driver.switch_to.window(handles[0])

        print("Communication over.")