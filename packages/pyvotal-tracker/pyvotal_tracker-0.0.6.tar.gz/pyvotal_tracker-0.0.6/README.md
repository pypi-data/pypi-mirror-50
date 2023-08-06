# Pyvotal Tracker

## Description

Pivotal Tracker module for python


## Usage

```
from pyvotal_tracker import PivotalTracker

pivotal = PivotalTracker("Your API Token")

story = pivotal.get_story("project_id", "story_id")
print(story['description')

```

