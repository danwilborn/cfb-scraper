import requests
from bs4 import BeautifulSoup

class Team:
    def __init__(self, name, logo, rank, record):
        self.name = name
        self.logo = logo
        self.rank = rank
        self.record = record

class Game:
    def __init__(self, date, start_time, visiting_team, home_team, visiting_score, home_score):
        self.date = date
        self.start_time = start_time
        self.visiting_team = visiting_team
        self.home_team = home_team
        self.visiting_score = visiting_score
        self.home_score = home_score

def main():
    URL = "https://www.ncaa.com/scoreboard/football/fbs"
    page = requests.get(URL)

    soup = BeautifulSoup(page.content, "html.parser")
    score_containers = soup.find_all("div", class_="gamePod_content-division")

    gamedays = dict()

    for s in score_containers:
        date = s.find("h6").text
        gamedays[date] = []
        games = s.find_all("div", class_="gamePod")
        gameday = []
        for g in games:
            teams = g.find_all("li")
            time = g.find("span", class_="game-time").text if g.find("span", class_="game-time") else None
            matchup = []
            scores = []
            for t in teams:
                name = t.find("span", class_="gamePod-game-team-name").text
                logo = t.find("img", class_="gamePod-game-team-logo")
                rank = t.find("span", class_="gamePod-game-team-rank").text
                score = t.find("span", class_="gamePod-game-team-score").text
                team = Team(name, logo, rank, None)
                matchup.append(team)
                scores.append(score)
            game = Game(date, time, matchup[0], matchup[1], scores[0], scores[1])
            gamedays[date].append(game)
    
    for date in gamedays.keys():
        for game in gamedays[date]:
            print(game.date, game.start_time)
            print(game.visiting_team.name, game.home_team.name)
            print(game.visiting_score, game.home_score)

if __name__ == "__main__":
    main()
