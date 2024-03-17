#!/usr/bin/python3

"""
    Forgejo / Gitea Stats Generator
    Copyright (C) 2022 Jacob Strieb
    Copyright (C) 2024 Tuxilio

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program.  If not, see <https://www.gnu.org/licenses/>.
"""

import os
import re
from typing import Dict, List, Optional, Set, Tuple, Any, cast
import json
import sys

import requests


###############################################################################
# Main Classes
###############################################################################


class Queries(object):
    """
    Class with functions to query the Forgejo / Gitea API.
    """

    def __init__(self, username: str, access_token: str, git_url: str):
        self.username = username
        self.access_token = access_token
        self.git_url = git_url

    def query(self, query: str) -> Dict:
        """
        Make a request to the Forgejo / Gitea API using the authentication token from
        the environment
        :param query: string query to be sent to the API
        :return: JSON output
        """
        headers = {
            "accept": "application/json"
        }

        generated_query = self.git_url + "/api/v1" + query + "?token=" + self.access_token

        response = requests.get(generated_query, headers=headers)

        if response.status_code != 200:
            print("Error while making the request. Status code:", response.status_code)
            sys.exit(1)

        return response.json()

class Stats(object):
    """
    Retrieve and store statistics about Forgejo / Gitea usage.
    """

    def __init__(self, username: str, access_token: str, git_url: str, exclude_repos: Optional[Set] = None, exclude_langs: Optional[Set] = None, ignore_forked_repos: bool = False):
        self.username = username
        self.git_url = git_url
        self._ignore_forked_repos = ignore_forked_repos
        self._exclude_repos = set() if exclude_repos is None else exclude_repos
        self._exclude_langs = set() if exclude_langs is None else exclude_langs
        self.queries = Queries(username, access_token, git_url)

        self._name: Optional[str] = None
        self._stargazers: Optional[int] = None
        self._forks: Optional[int] = None
        self._total_contributions: Optional[int] = None
        self._languages: Optional[Dict[str, Any]] = None
        self._repos: Optional[Set[str]] = None
        self._repo_list: Optional[Set[str]] = None
        self._lines_changed: Optional[Tuple[int, int]] = None
        self._views: Optional[int] = None
        self._streak: Optional[int] = None

    def get_stats(self) -> None:
        """
        Get lots of summary statistics. This is the main program for getting statistics.
        """

        self.name()
        self.repo_list()
        self.stargazers()
        self.forks()
        self.contributions()
        self.languages()
        self.streak()

        print_data = [
            ["User:", self._name],
            ["Repos:", self._repo_list],
            ["Stars:", self._stargazers],
            ["Forks:", self._forks],
            ["Lines changed:", self._lines_changed],
            ["Contributions:", self._total_contributions],
            ["Languages:", self._languages]
            ["Streak:", self._streak]
        ]

        max_len = max(len(row[0]) for row in print_data)

        for row in print_data:
            print(row[0].ljust(max_len) + "     " + str(row[1]))

    def name(self) -> str:
        """
        :return: Forgejo / Gitea user's name (e.g., Tuxilio)
        """
        
        if self._name is not None:
            return self._name

        response =  self.queries.query("/users/" + self.username)

        self._name = response['full_name']

        if self._name is None or self._name == "":
            self._name = self._name = response['username']

        return self._name

    def repo_list(self) -> str:
        """
        :return: Forgejo / Gitea repo list (e.g., [repo1, repo2])
        """
        
        if self._repo_list is not None:
            return self._repo_list

        self._repo_list = []

        response =  self.queries.query("/users/" + self.username + "/repos")

        for repo in response:
            self._repo_list.append(repo['name'])

        return self.repo_list

    def stargazers(self) -> str:
        """
        :return: Forgejo / Gitea total stargazers (e.g., 24)
        """
        
        if self._stargazers is not None:
            return self._stargazers

        self._stargazers = 0

        for i in self._repo_list:
            response =  self.queries.query("/repos/" + self.username + "/" + i + "/stargazers")

            for a in response:
                self._stargazers += 1

        return self._stargazers

    def forks(self) -> str:
        """
        :return: Forgejo / Gitea total forks (e.g., 12)
        """
        
        if self._forks is not None:
            return self._forks

        self._forks = 0

        for i in self._repo_list:
            response =  self.queries.query("/repos/" + self.username + "/" + i + "/forks")

            for a in response:
                self._forks += 1

        return self._forks

    def contributions(self) -> str:
        """
        :return: Forgejo / Gitea total lines changed (e.g., 35011)
        :return: Forgejo / Gitea total contributions (e.g., 514)
        """
        
        if self._lines_changed is not None and self._total_contributions is not None:
            return self._lines_changed, self._total_contributions

        self._lines_changed = 0
        self._total_contributions = 0

        for i in self._repo_list:
            response =  self.queries.query("/repos/" + self.username + "/" + i + "/commits")

            for a in response:
                self._total_contributions += 1
                self._lines_changed += a['stats']['total']

        return self._lines_changed, self._total_contributions

    def languages(self) -> str:
        """
        :return: Most used languages (e.g., ["Py"thon":20, "Java":80])
        """
        
        if self._languages is not None:
            return self._languages

        language_data = {}

        for i in self._repo_list:
            response =  self.queries.query("/repos/" + self.username + "/" + i + "/languages")

            for language, bytes in response.items():
                if language in language_data:
                    language_data[language] += bytes
                else:
                    language_data[language] = bytes

        total_bytes = sum(language_data.values())

        self._languages = {language: round(bytes / total_bytes * 100, 2) for language, bytes in language_data.items()}

        return self._languages

    
    def streak(self):
        """
        :return: Streak length
        """
        if self._streak is not None:
            return self._streak

        self._streak = 0
        last_timestamp = None

        response = self.queries.query("/users/" + self.username + "/heatmap")

        for day in response:
            if last_timestamp is not None:
                if day['timestamp'] - last_timestamp > 900:
                    self._streak = 0
            if day['contributions'] > 0:
                self._streak += 1
            else:
                break

            last_timestamp = day['timestamp']

        return self._streak

class Generate(object):
    """
    Class for generating images from data generated in stats
    """
    def __init__(self, stats, exclude_repos: Optional[Set] = None, exclude_langs: Optional[Set] = None, ignore_forked_repos: bool = False):
        self.stats = stats

    def generate_output_folder(self) -> None:
        """
        Create the output folder if it does not already exist
        """
        
        if not os.path.isdir("generated"):
            os.mkdir("generated")

    def generate_overview(self) -> None:
        """
        Generate an SVG badge with summary statistics
        """
        
        with open("templates/overview.svg", "r") as f:
            output = f.read()

        output = re.sub("{{ name }}", self.stats._name, output)
        output = re.sub("{{ stars }}", f"{self.stats._stargazers:,}", output)
        output = re.sub("{{ forks }}", f"{self.stats._forks:,}", output)
        output = re.sub("{{ contributions }}", f"{self.stats._total_contributions:,}", output)
        changed = sum(self.stats._lines_changed) if isinstance(self.stats._lines_changed, tuple) else self.stats._lines_changed
        output = re.sub("{{ lines_changed }}", f"{changed:,}", output)

        """views_str = f"{self.stats._views:,}" if self.stats._views is not None else "N/A"
        output = re.sub("{{ views }}", views_str, output)
        repos_len = len(self.stats._repos) if self.stats._repos is not None else 0
        output = re.sub("{{ repos }}", f"{repos_len:,}", output)"""

        self.generate_output_folder()
        with open("generated/overview.svg", "w") as f:
            f.write(output)


    def generate_languages(self) -> None:
        """
        Generate an SVG badge with summary languages used
        """
        
        with open("templates/languages.svg", "r") as f:
            output = f.read()

        with open('colors.json') as d:
            color_data = json.load(d)

        progress = ""
        lang_list = ""

        # Sort languages based on their percentage
        sorted_languages = sorted(
            self.stats._languages.items(),
            reverse=True,
            key=lambda t: t[1]  # Sort based on the language percentage directly
        )

        delay_between = 150
        for i, (lang, data) in enumerate(sorted_languages):
            if lang in color_data:
                color = color_data[lang]['color']
            else:
                color = "#000000"

            progress += (
                f'<span style="background-color: {color};'
                f'width: {data:0.3f}%;" '
                f'class="progress-item"></span>'
            )
            lang_list += f"""
<li style="animation-delay: {i * delay_between}ms;">
<svg xmlns="http://www.w3.org/2000/svg" class="octicon" style="fill:{color};"
viewBox="0 0 16 16" version="1.1" width="16" height="16"><path
fill-rule="evenodd" d="M8 4a4 4 0 100 8 4 4 0 000-8z"></path></svg>
<span class="lang">{lang}</span>
<span class="percent">{data:0.2f}%</span>
</li>
"""

        output = re.sub(r"{{ progress }}", progress, output)
        output = re.sub(r"{{ lang_list }}", lang_list, output)

        self.generate_output_folder()
        with open("generated/languages.svg", "w") as f:
            f.write(output)

###############################################################################
# Main Function
###############################################################################


def main() -> None:
    """
    Main program
    """
    
    access_token = os.getenv("ACCESS_TOKEN")
    user = os.getenv("USER")
    git_url = os.getenv("GIT_URL")

    print("Generating stats for user " + user)
    if access_token is None or user is None:
        raise RuntimeError(
            "ACCESS_TOKEN and USERNAME environment variables cannot be None!"
        )

    stats = Stats(user, access_token, git_url)
    stats.get_stats()

    generate = Generate(stats)
    generate.generate_overview()
    generate.generate_languages()

if __name__ == "__main__":
    main()
