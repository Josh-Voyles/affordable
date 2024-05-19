## Contributing to Home-Choice-Pro

Create a copy of the repository on your local machine via terminal:

```bash
cd Desktop  # if wanting folder on desktop

git clone https://github.com/Josh-Voyles/Home-Choice-Pro

cd Home-Choice-Pro
```

Before creating a new branch, ALWAYS ensure latest development branch

```bash
git pull origin develop
```

Create issue on Github for new feature or bug OR take note of issue number

```bash
git branch feature-or-bugfix-name

git checkout feature-or-bugfix-name

# open project in your editor
# for example VS Code
code .
```

Again, make sure you're working on a specific issue

Once you're done with your edits, save and add changes to staging

For example, if working on README.md file

```bash
git add README.md
```

Now commit your changes

```bash
git commit -m "See: #<issue_number> <your_commit_message>"
```

Now let's push your branch to Github

```bash
git push origin feature-or-bugfix-name
```

Head to the Github project, and open new pull request to develop branch

After the project has been merged, make sure you delete your local repository that you pushed.

```bash
git checkout develop  # switch to develop branch first

git branch -d feature-or-bugfix-name
```
