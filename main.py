import kivy
from kivy.app import App
from kivy.uix.widget import Widget
from kivy.properties import ObjectProperty
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.image import Image
from kivy.uix.behaviors import ButtonBehavior
from kivy.uix.button import Button
from kivy.uix.label import Label
import wikipedia
import requests
import bs4
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.core.window import Window

# The base of the url that the search function uses
baseRequestURL = "https://en.wikipedia.org/wiki/"

# region
# The main screen


class MainScreen(GridLayout):

    resultLabelsHolder = ObjectProperty(None)
    searchValue = "Search Anything"

    def textinput_update_text(self, _text):
        self.searchValue = _text

    def search(self):
        searchResults = wikipedia.search(self.searchValue)
        # print(searchResults)

        self.resultLabelsHolder.clear_widgets()

        for i in searchResults:
            _searchResultLabel = SearchResultLabel(i)
            self.resultLabelsHolder.add_widget(_searchResultLabel)


# The label that the window creates
# TODO: Mybe move the search function to the wikipedia screen


class SearchResultLabel(Label):
    def __init__(self, text):
        Label.__init__(self)
        self.text = text

    # Search wikipedia
    def on_touch_down(self, touch):
        Label.on_touch_down(self, touch)
        if self.collide_point(touch.pos[0], touch.pos[1]):
            _text = self.text.replace(" ", "_")
            response = requests.get(baseRequestURL + _text)

            if response is not None:
                html = bs4.BeautifulSoup(response.text, 'html.parser')

                page_title = html.select("#firstHeading")[0].text
                page_paragraphs = html.select("p")

                myApp.wikipedia_page.setTitle(page_title)
                myApp.wikipedia_page.setParagraphs(page_paragraphs)

                myApp.screen_manager.current = "Wikipedia Page"
# endregion


class WikipediaPage(Screen):
    pageTitle = ObjectProperty(None)
    paragraphsHolder = ObjectProperty(None)

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def setTitle(self, title):
        self.pageTitle.text = title

    def setParagraphs(self, paragraphs):
        for para in paragraphs:
            _paragraphLabel = ParagraphLabel(para.text)
            self.paragraphsHolder.add_widget(_paragraphLabel)

    @staticmethod
    def returnToMain():
        myApp.screen_manager.current = "Main Screen"

        pass


class ParagraphLabel(Label):
    def __init__(self, text):
        Label.__init__(self)
        self.text = text


class MyApp(App):
    def build(self):
        self.screen_manager = ScreenManager()

        # MAIN SCREEN
        self.main_screen = MainScreen()
        screen = Screen(name="Main Screen")
        screen.add_widget(self.main_screen)
        self.screen_manager.add_widget(screen)

        # WIKIPEDIA PAGE
        self.wikipedia_page = WikipediaPage()
        screen = Screen(name='Wikipedia Page')
        screen.add_widget(self.wikipedia_page)
        self.screen_manager.add_widget(screen)

        return self.screen_manager


if __name__ == "__main__":
    myApp = MyApp()
    myApp.run()
