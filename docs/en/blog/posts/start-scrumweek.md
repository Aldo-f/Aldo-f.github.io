---
title: "Start of the Scrum Week"
date: 2019-04-08T21:34:04+02:00
categories:
    - Scrum
    - VDAB
---

For the VDAB php developer training course, the scrum week started today.
Two groups were formed, of 3 and 4 people.

The goal is to build a FlexDating app this week,
mostly by reusing existing code that fetches users from another server.
Those responses are then used to create the front-end of a website.

To get a bit of a feel for the whole group, today we chose to give pair programming a chance.
This to map out the weaknesses and strengths of all group members.

Today we discussed in broad lines how we would approach the project.
Some points that came up:
* Use Bootstrap to present the received data in an orderly way.
* Priorities
    * Login
    * Registration
    * Home page
    * Search page

The login is especially important in this sprint, since in principle no (or very little) user data may be seen before the user has signed in themselves.


Problems I ran into today:
* Setting up a git server doesn't always go smoothly.
    * Creating a group that everyone became a member of, so that all members would have maximum ownership of the code
    * Creating a clear workflow around it, one that is actually followed, is not always easy.

  Probably the first time for each of us collaborating on a project.

  In our group, for example, we didn't fork from <code>develop</code> a 2<sup>nd</sup> time to complete the registration, but did it directly on the develop branch.
* During pair programming I was told - and I noticed myself - that the distribution of weaknesses and strengths wasn't entirely compensated. I think pair programming only really adds value when the differences show themselves more clearly. Maybe do it again later in the project, but then switch around.
* Does pair programming actually add value, speed-wise, after there's already a strong foundation?


What can be better by tomorrow and what do I want to keep?
* Now that we have the base code, and everyone's way of working (having also discovered some strengths and weaknesses), it seems good to spend the next days with this base code each finishing their assigned feature. The current features (index.html and registration.html) are not yet done. Is it best to have the groups finish them, or can the groups already split up during a feature? Perhaps a clear scrum-master and product-owner could be chosen who try to keep this on track over the next few days.
* Pausing pair programming for now?
* Communicating more with each other is always an added value; after a basic JavaScript course it's hard to know every existing function already. Being able to look together at solving a problem does help speed here.


Later I made a mirror of the GitLab on GitHub, and a GitHub Page was made from it.
That website can be found [here](https://vdab-flexidating.github.io/).
(it always shows master)
