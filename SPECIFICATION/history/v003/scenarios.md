# livespec-ai.org — scenarios

Acceptance scenarios in Gherkin form. Each Gherkin keyword line is
preceded and followed by a blank line so that every step renders as
its own Markdown paragraph under GitHub-Flavored Markdown.

## Scenario: Visitor reads the homepage

Given a visitor opens `https://livespec-ai.org/`

When the page loads

Then the visitor sees an introduction to Chad Woolley ("thewoolleyman")

And the visitor sees livespec described as an experimental work in progress

And the visitor sees the two goals: the specification–implementation feedback loop, and turning quality dials toward 11 within the fast/cheap/right trade-off

And the visitor sees a project-state summary made mostly of links to the livespec GitHub repositories

And the visitor sees a link to the blog

## Scenario: Visitor follows a project-state link

Given a visitor is on the homepage

When the visitor follows the link to the livespec installation documentation

Then the visitor arrives at that documentation in the `thewoolleyman/livespec` GitHub repository

## Scenario: Visitor browses the blog

Given a visitor opens `https://livespec-ai.org/blog/`

When the page loads

Then the visitor sees a list of blog entries, newest first, each with its title and publication date

When the visitor selects the placeholder entry

Then the visitor arrives at `/blog/<slug>/` showing the entry's title, publication date, and placeholder text

And the entry links back to `/blog/` and `/`

## Scenario: Visitor uses a phone

Given a visitor opens any page on a 360-pixel-wide screen

When the page loads

Then all content is readable without horizontal scrolling

And prose paragraphs are left-justified

## Scenario: Visitor browses with JavaScript disabled

Given a visitor's browser has JavaScript disabled

When the visitor opens any page

Then all content and navigation work

## Scenario: Visitor uses the www or http address

Given a visitor requests `http://www.livespec-ai.org/blog/`

When the request completes

Then the visitor lands on `https://livespec-ai.org/blog/`

## Scenario: Search engine indexes the site

Given a crawler fetches `https://livespec-ai.org/robots.txt`

When the crawler follows the referenced sitemap

Then the sitemap lists the homepage, the blog index, and every blog entry with their last-modified dates

And each listed page carries a title, description, and canonical URL
