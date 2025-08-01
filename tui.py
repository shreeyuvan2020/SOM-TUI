from textual.app import App, ComposeResult, Screen
from textual.widgets import Static, Input, Label, Button, Link, Header
from textual.containers import Container, Horizontal, VerticalScroll, Vertical
from rich.segment import Segment
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from main import main
from textual.style import Style
class Screen1(Screen):
    CSS_PATH = "landing.tcss"
    print("hi")
    def compose(self) -> ComposeResult:
        yield Label("Paste the cookie value of _journey_session from your network tap in devtools to start voting via the terminal!", classes="welcome-label")
        yield Input(placeholder="Cookies", id="cookie-input")
    def on_input_submitted(self, event: Input.Submitted) -> None:
        if event.value:
            with open("som-cookie.txt", "w") as f:
                f.write(event.value)
            self.app.push_screen(Screen2())
class Screen2(Screen):
    CSS_PATH = "layout.tcss"
    def compose(self) -> ComposeResult:
        scraper_stuff = main(driver=self.app.driver)
        self.left_project = scraper_stuff[0]
        self.right_project = scraper_stuff[1]
        self.devlog_1 = scraper_stuff[2]
        self.time_1 = scraper_stuff[3]
        self.devlog_2 = scraper_stuff[4]
        self.time_2 = scraper_stuff[5]
        important_buttons = scraper_stuff[6]
        usernames = scraper_stuff[7]
        left_devlogs = scraper_stuff[8]
        left_stuff = scraper_stuff[9]
        right_stuff = scraper_stuff[10]
        right_devlogs = scraper_stuff[11]
        left_description = scraper_stuff[12]
        right_description = scraper_stuff[13]
        self.driver = scraper_stuff[14]
        self.left_button = scraper_stuff[15]
        self.right_button = scraper_stuff[16]
        self.tie_button = scraper_stuff[17]
        self.feedback_form = scraper_stuff[18]
        self.submit_button = scraper_stuff[19]
        for e, button in enumerate(important_buttons):
            if e == 0:
                demo_1 = button.get("href")
            elif e == 1:
                repo_1 = button.get("href")
            elif e == 2:
                demo_2 = button.get("href")
            elif e == 3:
                repo_2 = button.get("href")
        left_devlog_widgets = [
        Static(
            f"[b]{left_stuff[i]}[/b]\n{left_devlogs[i].text.strip()}",
            classes="left-quarter-devlogs"
        )
        for i in range(len(left_devlogs))
    ]

        right_devlog_widgets = [
        Static(
            f"[b]{right_stuff[i].strip()}[/b]\n{right_devlogs[i].text.strip()}".replace("•", ""),
            classes="right-quarter-devlogs"
        )
        for i in range(len(right_devlogs))
    ]
        yield Horizontal(
            VerticalScroll(
                Label(self.left_project, classes="left-quarter"),
                Label("By:" + usernames[0], classes="left-quarter-by"),
                Static(self.devlog_1, classes="left-quarter-devlog-and-time"),
                Static(self.time_1, classes="left-quarter-devlog-and-time"),
                Static(left_description, classes="description"),
                Horizontal(
                    Link(
                        "Go to demo",
                        url=demo_1,
                        tooltip="Click me",
                        classes="left-quarter-demo"
                    ),
                    Link(
                        "Go to repo",
                        url=repo_1,
                        tooltip="Click me",
                        classes="left-quarter-repo"
                    )
                ),
                *left_devlog_widgets,
                classes="whole-devlog"
            ),
            VerticalScroll(
                Label(self.right_project, classes="right-quarter"),
                Label("By:" + usernames[1], classes="right-quarter-by"),
                Static(self.devlog_2, classes="right-quarter-devlog-and-time"),
                Static(self.time_2, classes="right-quarter-devlog-and-time"),
                Static(right_description, classes="description"),
                Horizontal(
                    Link(
                        "Go to demo",
                        url=demo_2,
                        tooltip="Click me",
                        classes="right-quarter-demo"
                    ),
                    Link(
                        "Go to repo",
                        url=repo_2,
                        tooltip="Click me",
                        classes="right-quarter-repo"
                    )
                ),
                *right_devlog_widgets,
                classes="whole-devlog"
            ),
            classes="screen"
        )
        print(self.left_project, self.right_project, self.left_button, self.right_button, self.tie_button)
        yield Input(placeholder="Type the project you want to vote for here:", id="vote-input")
        yield Static("Write your feedback here:", classes="vote-input")
        yield Input(placeholder="Last Name", id="vote-inputs")
    def on_input_submitted(self, event: Input.Submitted) -> None:
        if event.input.id == "vote-input":
            if event.value.lower() == self.left_project.lower():
                self.driver.execute_script("arguments[0].click();", self.left_button)
            elif event.value.lower() == self.right_project.lower():
                self.driver.execute_script("arguments[0].click();", self.right_button)
            elif event.value.lower() == "tie":
                self.driver.execute_script("arguments[0].click();", self.tie_button)
            else:
                print("Invalid project name. Please enter either the left or right project name, or 'tie'.")
        elif event.input.id == "vote-inputs":
            self.feedback_form.send_keys(event.value)
            print("Vote submitted successfully!")
            self.driver.execute_script("arguments[0].click();", self.submit_button)
            Static("Vote submitted successfully!", classes="vote-success")
            if self.app:
                self.app.push_screen(Screen2())
        else:
            print("Please enter your feedback before submitting.")
class Voting(App):
    SCREENS = {"screen_one": Screen1, "screen_two": Screen2}

    def on_mount(self) -> None:
        chrome_options = Options()
        chrome_options.add_experimental_option("detach", True)
        self.driver = webdriver.Chrome(options=chrome_options)
        self.push_screen(Screen1())
if __name__ == "__main__":
    print("Welcome to the SOM CLI Voting App!")
    app = Voting()
    app.run()