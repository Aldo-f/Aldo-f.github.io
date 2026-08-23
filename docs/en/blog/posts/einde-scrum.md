---
title: "End of Scrum"
date: 2019-04-17T18:30:00+02:00
categories:
  - Scrum
  - VDAB
---

It's Wednesday now, the 5th day after the scrum week.

To me it felt like it went by far too fast.
Not that the project wasn't finished - with the minimal functionality - but simply, it's hard to consider a project as "done".

## How did it go?
First we felt out who would take on which parts; we mostly worked per page/feature.

### Who did what?
* Griet:
  * Pages: registration, own profile, edit profile, view user, ...
  * Functionality: input validation, adding a photo, displaying the zodiac sign, ...
* Mesut:
  * Pages: messages, index, navigation
  * Functionality: everything related to messages (posting, reading, sorting, deleting, starting)
* Wouter:
  * Pages: search, navigation
  * Functionality: everything related to search (number per page, searching by ..., ) and the pagination at the bottom.
* Aldo:
  * Pages: navigation, registration, login (in navbar), own profile, ...
  * Functionality: login, localStorage, favorites, lovecoins (actions and adjustments), ...

### What went well?
* Communication; as far as I'm concerned this went very smoothly, everyone knew what the others were doing (even if only partially), questions could be asked of each other, and we almost never had to wait on each other (code-wise).

  Mostly thanks to the daily standup, and the extra mid-week demos we scheduled.
* The CSS; by using Bootstrap a large part of UI and UX was already solved, so as developers we had little left to think about or adjust.


### What could be better?
* The designation of Scrum Master and Product Owner; no real distinction was made between group members.

  At least not on paper.
* Indicating how many story points per feature; this wasn't always done, and it's hard to stick to.

  Also, things were sometimes subdivided too much (CSS &amp; code).
* Because of the shorter period it was difficult to know clearly what could be included in each sprint (the 1<sup>st</sup> lasted 1.5 days)

  At the interim demo (on Thursday) it was once again clearly discussed what could still be added, and what had to be cancelled.
* A bit more commenting in the code, especially when others want to add things.
* In my eyes the demo was not a complete result; the small bugs that were still found, the feature that wasn't nicely finished (the favorites). Plenty could still be improved to deliver a nicer, better result.

  Afterwards some adjustments were made and merged into the master branch.


## What do I take away?
Every project needs a solid base codebase before anyone can work further on their feature. Only after this base can work continue. Also, knowing better where each group member stands (not everyone knew Bootstrap) can be a great added value in other projects.

## More info:
The code for this project can be found on GitHub and GitLab.

Everything was pushed to GitLab, where merge requests were accepted or declined (usually in the develop branch).

Later, always just before a small demo, the code was merged into the master branch. After which both the develop and master branches were automatically pushed to GitHub.
So that a GitHub Page could be made from master there.


[gitlab.com/vdab-flexidating](https://gitlab.com/vdab-flexidating/flexidating/tags/Demo-2)

[github.com/vdab-flexidating](https://github.com/vdab-flexidating/vdab-flexidating.github.io/releases/tag/Demo-2)

[vdab-flexidating.github.io](https://vdab-flexidating.github.io/)
