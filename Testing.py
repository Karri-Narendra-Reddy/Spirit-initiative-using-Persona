import ast
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from locators import *
from your_script import *
import string
import random


def answers_SCSS(array_object):
    data = array_object[0]
    element = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, f"//label[text()='{data}']")))
    element.click()
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    element = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "a.btn.next-btn")))
    element.click()
    WebDriverWait(driver, 60).until_not(EC.visibility_of_element_located((By.CSS_SELECTOR, ".spinner")))


def answers_MCMS(array_object):
    for i in range(len(array_object)):
        data = array_object[i]
        element = WebDriverWait(driver, 100).until(
            EC.element_to_be_clickable((By.XPATH, f"//label[text()='{data}']")))
        element.click()
    text_fields = driver.find_elements(By.CSS_SELECTOR, '.txtfield-max-width input[type="text"]')
    if(text_fields):
        text_fields = driver.find_elements(By.CSS_SELECTOR, '.txtfield-max-width input[type="text"]')
        for i, text_field in enumerate(text_fields):
            text_field.send_keys("random_string")
    else:
        print("continue")

    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    element = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "a.btn.next-btn")))
    element.click()
    WebDriverWait(driver, 60).until_not(EC.visibility_of_element_located((By.CSS_SELECTOR, ".spinner")))

def answers_numeric(array_object):
    text_fields = driver.find_elements(By.TAG_NAME, "tr")
    for i, text_field in enumerate(text_fields):
        locator = text_field.find_element(By.CSS_SELECTOR, 'td input[type="text"]')
        locator.send_keys(array_object[i])
        print("Success")

    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    element = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "a.btn.next-btn")))
    element.click()
    WebDriverWait(driver, 60).until_not(EC.visibility_of_element_located((By.CSS_SELECTOR, ".spinner")))


# Getting Question Type
def optiontype(questiontype):
    if "select one" in questiontype:
        return "single select"
    elif "Select all" in questiontype:
        return "Multi-select"
    elif "number" in questiontype:
        return "Answer for all options with number"
    elif "Instruction" in questiontype:
        return "Answer the question"
    elif "just hit Next" in questiontype:
        element = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "a.btn.next-btn")))
        element.click()
        WebDriverWait(driver, 60).until_not(EC.visibility_of_element_located((By.CSS_SELECTOR, ".spinner")))

        # Finding Question Type using UI
        questiontype = driver.find_element(By.CSS_SELECTOR, questionType).text
        type = optiontype(questiontype)
        return type

# Getting Options based on Question Type
def get_answers_from_pi(questiontype):
    # questiontype = driver.find_element(By.CSS_SELECTOR, questionType).text
    if "select one" in questiontype:
        locator = (By.CSS_SELECTOR, radioButtonAnswerList)
        elements = WebDriverWait(driver, 20).until(EC.visibility_of_all_elements_located(locator))
        texts = [element.text for element in elements]
        return texts
    elif "Select all" in questiontype:
        locator = (By.CSS_SELECTOR, checkBoxAnswerList)
        elements = WebDriverWait(driver, 20).until(EC.visibility_of_all_elements_located(locator))
        texts = [element.text for element in elements]
        return texts
    elif "Instruction" in questiontype:
        return ""
    else:
        # Finding number of table rows
        options = []
        text_fields = driver.find_elements(By.TAG_NAME, "tr")
        if (text_fields):
            text_fields = driver.find_elements(By.TAG_NAME, "tr")
            for i, text_field in enumerate(text_fields):
                locator = text_field.find_element(By.CSS_SELECTOR, '.col-md-12').text
                options.append(locator)
        return options



def generate_random_string(length):
    letters = string.ascii_letters
    return ''.join(random.choice(letters) for _ in range(length))



if __name__ == "__main__":
    ser_obj = Service("Driver/chromedriver.exe")
    driver = webdriver.Chrome(service=ser_obj)
    driver.maximize_window()
    link = "https://spirit-dev-webapp-mf.azurewebsites.net/spirit?invitation=665e9d5cdbf9ef1163553d4b&test=true"
    driver.get(link)
    question =""
    questions = []
    answers = []
    persona = createpersona("ROLE", "SOFTWARE ENGINEER", "ALCOHOL")

    while(driver.current_url != "https://www.google.com/?invitation=665e9d5cdbf9ef1163553d4b&test=true"):
        elem = WebDriverWait(driver, 90).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, questionsContainer))
        )

        # Finding Question Type using UI
        questiontype = driver.find_element(By.CSS_SELECTOR, questionType).text
        type = optiontype(questiontype)

        # Getting Question Text From UI
        question = driver.find_element(By.CSS_SELECTOR, questionText).text
        questions.append(question)


        # Getting All Options From UI
        answer1=get_answers_from_pi(questiontype)
        answers.append(answer1)

        # Sending Questions,Options,Question Type To LLM
        if(type == "Answer the question"):
            personaAnswers = answersfrompersona(question, persona, type)
        else:
            personaAnswers = answersfrompersonas(question,answer1,persona,type)
        # Converting the Response into Array
        array_object = ast.literal_eval(personaAnswers)
        print(array_object)

        # Answering the Options by LLM Based on Its response
        if(type == "single select"):
            answers_SCSS(array_object)
            print("Next")
        elif(type == "Multi-select"):
            answers_MCMS(array_object)
        elif(type == "Answer for all options with number"):
            answers_numeric(array_object)
        elif(type == "Answer the question"):
            text_fields = driver.find_elements(By.TAG_NAME, "tr")
            for i, text_field in enumerate(text_fields):
                locator = text_field.find_element(By.CSS_SELECTOR, 'td input[type="text"]')
                locator.send_keys(array_object[i])
                print("Success")

            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            element = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "a.btn.next-btn")))
            element.click()
            WebDriverWait(driver, 60).until_not(EC.visibility_of_element_located((By.CSS_SELECTOR, ".spinner")))
        else:
            print("Hello")

    # Printing All Questions and Options
    print(questions)
    print(answers)