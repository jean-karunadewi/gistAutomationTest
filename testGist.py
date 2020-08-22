import unittest
from selenium import webdriver
from time import sleep

class GistTest(unittest.TestCase):
    USERNAME = "USERNAME"
    PASSWORD = "PASSWORD"

    def setUp(self):
        self.browser = webdriver.Chrome('/usr/local/bin/chromedriver')

        self.browser.get("https://github.com/login")
        login = self.browser.find_element_by_name("login")
        login.send_keys(self.USERNAME)
        passw = self.browser.find_element_by_name("password")
        passw.send_keys(self.PASSWORD)
        self.browser.find_element_by_name("commit").click()

        self.browser.get("https://gist.github.com")
        
        #assert if it landed on the right page
        assert "Create a new Gist" in self.browser.title, "Title must be Create a new Gist"

    def testCreateGist(self):
        descriptionText = "Deskripsi dari Gist yang saya buat"
        filenameText = "Nama file dari Gist yang saya mau buat"
        contentText = "Isi dari Gist saya"

        self.createGist(descriptionText, filenameText, contentText)

        #assert if it goes to another page after submitting that shows the newly added gist
        assert descriptionText in self.browser.title, "Title should be the same with description text entered"

        #assert if it has the right description text
        assert descriptionText in self.browser.find_element_by_xpath("//div[@itemprop='about']").text, "Description should be the same with description text entered"

        #assert if it has the right filename text
        assert filenameText in self.browser.find_element_by_class_name("gist-blob-name").text, "Filename should be the same with filename text entered"
        
        #assert if it has the right content text
        assert contentText in self.browser.find_element_by_class_name("blob-code-inner").text, "Content should be the same with content text entered"

    def testCreateGist_noContent(self):
        #assert if the button is disabled or not
        assert not self.browser.find_element_by_name("gist[public]").is_enabled(), "Button 'Create Public Gist' should be disabled"

    def testEditGist(self):        
        descriptionText = "Deskripsi dari Gist yang saya buat"
        filenameText = "Nama file dari Gist yang saya mau buat"
        contentText = "Isi dari Gist saya"
        self.createGist(descriptionText, filenameText, contentText)
        self.browser.get("https://gist.github.com")

        #click on the first gist (assume we want to edit that)
        self.browser.find_element_by_class_name("meta").click()
        
        #assert if it landed on the page where the gist we want to edit
        assert descriptionText in self.browser.title, "Title should be the same with description of gist"
        
        #click on the "Edit" button
        self.browser.find_element_by_xpath("//a[@aria-label='Edit this Gist']").click()

        #assert if it landed on the edit page of the right gist
        assert "Editing "+filenameText in self.browser.title, "Title should be 'Editing [filename of gist]'"

        content = self.browser.find_element_by_class_name("CodeMirror-code")
        contentText = contentText+ " addition after editing" #adding the content of the gist
        content.clear()
        content.send_keys(contentText) #setting the new content field using contentText

        #click on "Update public gist" button
        self.browser.find_element_by_class_name("btn-primary").click()
        
        #assert if the content of gist is updated
        assert contentText in self.browser.find_element_by_class_name("blob-code-inner").text, "Content should be the same with new content text entered"

    def testDeleteGist(self):
        descriptionText = "Deskripsi dari Gist yang saya buat"
        filenameText = "Nama file dari Gist yang saya mau buat"
        contentText = "Isi dari Gist saya"
        self.createGist(descriptionText, filenameText, contentText)
        self.browser.get("https://gist.github.com")
        
        #click on the first gist (assume we want to delete that)
        self.browser.find_element_by_class_name("meta").click()
        
        #assert if it landed on the page where the gist we want to delete
        assert descriptionText in self.browser.title, "Title should be the same with description of gist"
        
        #click on the "Delete" button
        self.browser.find_element_by_xpath("//button[@aria-label='Delete this Gist']").click()

        #switch to alert object to confirm deletion
        alert = self.browser.switch_to.alert
        alert.accept()

        #assert if it goes to the right page and showing message successfully deleting gist
        assert "Gist deleted successfully." in self.browser.find_element_by_class_name("flash-notice").text, "There should be a success message"

    def testListGist(self):
        descriptionText = "Deskripsi dari Gist yang saya buat"
        filenameText = "Nama file dari Gist yang saya mau buat"
        contentText = "Isi dari Gist saya"
        self.createGist(descriptionText, filenameText, contentText)
        self.browser.get("https://gist.github.com/"+self.USERNAME) #go to list of my gist page

        counterGist = int(self.browser.find_element_by_class_name("Counter").text) #get gist counter next to "All Gist" text on the tab for verifying purpose later
        
        gistSnippets = self.browser.find_elements_by_class_name("gist-snippet") #get a list of gists that we have to be counted and for verifying purpose later

        #assert if the number shown on counter and the actual count of the gists are the same
        assert counterGist == len(gistSnippets), "Counter from gist and number of gists shown should be equal"

    def tearDown(self):
        self.browser.quit()

    def createGist(self, descriptionText, filenameText, contentText):
        description = self.browser.find_element_by_name("gist[description]")
        description.send_keys(descriptionText) #set description field using descriptionText

        filename = self.browser.find_element_by_name("gist[contents][][name]")
        filename.send_keys(filenameText)  #set filename field using filenameText

        content = self.browser.find_element_by_class_name("CodeMirror-code")
        content.send_keys(contentText)  #set content field using contentText

        #click on "Create Public Gist" button
        self.browser.find_element_by_name("gist[public]").click()
    
if __name__ == "__main__":
    username = raw_input("Please input username / email for github: ")
    password = raw_input("Please input password for github: ")

    GistTest.USERNAME = username
    GistTest.PASSWORD = password
    unittest.main()
