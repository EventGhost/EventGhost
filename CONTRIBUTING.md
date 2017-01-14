# I need help with EventGhost

Then you're in the wrong place. Support requests should be posted on [our forum](http://www.eventghost.org/forum/), either in [General Support](http://www.eventghost.org/forum/viewforum.php?f=2), or, if you need support for a specific plugin, in that plugin's thread in [Plugin Support](http://www.eventghost.org/forum/viewforum.php?f=9). Be sure to search before posting, as the most timely answer to your question will always be the one that's already there.


# I want to report a bug

Great! Bugs are, unfortunately, a fact of software development life, but with your help, we can make EventGhost better for everyone.

### Do I need to report this at all?

Before continuing, be sure to:

* Search [our issue tracker](https://github.com/EventGhost/EventGhost/issues?q=) to see if your bug has already been identified. If you find a match, +1s aren't helpful to us, but any further light you can shed on the issue absolutely is.
* Try [the latest stable version](http://www.eventghost.org/downloads/) and [the latest development version](https://ci.appveyor.com/project/topic2k/eventghost/branch/master/artifacts). Your bug might already be fixed!

### Things to include in your bug report

* If your bug report is about a specific plugin, the plugin name enclosed in square brackets (for example, "[Keyboard]") should come first in your title.
* The exact versions of EventGhost and Windows you're running.
* A detailed list of steps to reproduce. If we can't reproduce your bug, we probably won't be able to fix it.
* Any and all tracebacks and error messages.


# I want to write a plugin

Great! EventGhost would be nothing without our vibrant community of plugin developers, so we're glad to have you aboard.

### Getting started

If you're new to EventGhost plugin development, your first stop should be the "Writing Plugins" section of our user manual, `EventGhost.chm`. Still stumped? Check out the [Coding Corner](http://www.eventghost.org/forum/viewforum.php?f=10) section of [our forum](http://www.eventghost.org/forum/).

### Publishing your work

Note that we no longer accept new plugins for inclusion in EventGhost. Long-term, our goal is to remove *all* non-core plugins from the distribution and make them available in-app, on-demand through an [online plugin repository](https://github.com/EventGhost/EventGhost/issues/4), where you'll one day be able to offer your plugins right alongside ours. Until then, please share your work in the [Plugin Support](http://www.eventghost.org/forum/viewforum.php?f=9) section of [our forum](http://www.eventghost.org/forum/).


# I want to contribute code

Great! While not every pull request will meet our quality standards or align with our design philosophy, we welcome contributions from the community with open arms.

### What's this "Git" thing I keep hearing about?

If you're new to Git, we recommend the following:

* Install [TortoiseGit](https://tortoisegit.org/download/) and read through its [Daily Use Guide](https://tortoisegit.org/docs/tortoisegit/tgit-dug.html). TortoiseGit integrates directly into Windows, and you operate it by right-clicking on files and folders in your repo. It's a great Git client for both beginners and experts alike.
* To get a better feel for Git's command-line tools, run through [GitHub's 15-minute interactive Git tutorial](https://try.github.io/).
* Read the first three chapters of [*Pro Git*](https://git-scm.com/book). Written by GitHub's co-founder, *Pro Git* is the gold standard of Git books, and is available free of charge at the link provided.

### Setting up your editor

Before you begin working on EventGhost, please install the following plugins in your code editor/IDE:

* [`EditorConfig`](http://editorconfig.org/)
* [`flake8`](https://flake8.readthedocs.io/)

These plugins will help guide you to producing the highest quality code possible. If you're not using `EditorConfig` or your code doesn't fully validate with `flake8`, don't be surprised when your pull request is rejected and you're pointed back to this document.

Still using Notepad or another program without plugin support? Check out [Visual Studio Code](https://code.visualstudio.com/docs/languages/python), which is free, comes with full Git integration, and has a robust Python plugin with debugging(!).

### Commits count!

Good commits are just as important as good code. Every developer worth his or her salt should read and internalize the following two articles:

* [Developer Tip: Keep Your Commits "Atomic"](http://www.freshconsulting.com/atomic-commits/)
* [How to Write a Git Commit Message](http://chris.beams.io/posts/git-commit/)

For the good of the project, pull requests containing commits that don't comply with these guidelines may be rejected.

### Things to include in your pull request

* If your pull request is for a specific plugin, the plugin name enclosed in square brackets (for example, "[Keyboard]") should come first in your title. Don't do this for commit titles.
* If your pull request fixes an issue on [our issue tracker](https://github.com/EventGhost/EventGhost/issues), use the [closes/fixes/resolves syntax](https://help.github.com/articles/closing-issues-via-commit-messages/) in the body to denote this.
* If your pull request makes changes pertinent to plugin developers, be sure to outline those changes in the body.

### Reasons your pull request might be rejected

* Your code wasn't up to par. In this case, we'll usually provide a list of changes we want made. Be sure to post a follow-up comment after adding new commits to your pull request, as GitHub doesn't notify us on new commits.
* Your code didn't align with our design philosophy. Try not to take it personally if this happens -- we're only doing what we think is best for everyone.
* Your code was too sloppy. Read the [Setting up your editor](#setting-up-your-editor) section above and try again.
* Your commits weren't up to par. Read the [Commits count!](#commits-count) section above and try again.
* Your coding style didn't match ours. Read the [Coding Style Guidelines](https://github.com/EventGhost/EventGhost/blob/master/_build/data/docs/codingstyle.rst) section of our manual and try again.
* Your code didn't work. Setting up a build environment is now easier than ever -- just run `python Build.py --make-env` from an administrative command prompt -- so there's no excuse for not testing your work.
* You added yourself to a plugin's author list without doing substantial work on that plugin. Fixing a bug doesn't make you an author.
* Your pull request contained merge commits. To remove merge commits from an existing branch, run `git rebase upstream/master && git push --force`. To ensure you don't get merge commits in the future, run `git config --global pull.rebase true`.
