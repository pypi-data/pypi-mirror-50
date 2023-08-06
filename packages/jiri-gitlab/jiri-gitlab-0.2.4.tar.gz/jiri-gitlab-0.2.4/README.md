# jiri-gitlab

This is a small utility that creates a [jiri manifest file](https://fuchsia.googlesource.com/jiri/) 
from Gitlab projects.

Use this if you want a complete and updated set of repositories from your private gitlab instance 
on your machine.

## Install

`pip3 install --user jiri-gitlab`

## Instructions

Ensure you've followed [the Jiri bootstrapping guide](https://fuchsia.googlesource.com/jiri/#quickstart).

Then, create a file called `~/.python-gitlab.cfg` in your home directory and add:

```cfg
[company-name-here]
url = https://your-gitlab-url/
private_token = your-private-token

```

You need to create a private token with read access to your repositories.

Once you've done that, run:

```
cd $MY_ROOT # Or wherever you've defined your project directory to be
jiri-gitlab --auth company-name-here "*" > .jiri_manifest
```

This will produce an XML file that Jiri can consume to pull all your projects:

```
jiri update -gc=true
```

There is also a utility tool to list projects:

```
jiri-list ~/projects/.jiri_manifest
```

You can combine this with `fzf` for quick project navigation:

```
jiri-list ~/projects/.jiri_manifest | fzf --ansi --preview "mdcat {}/README.md"
```
