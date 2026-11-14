# livespec-ai.org — scenarios

Acceptance scenarios in Gherkin form. Each Gherkin keyword line is
preceded and followed by a blank line so that every step renders as
its own Markdown paragraph under GitHub-Flavored Markdown.

## Scenario: Visitor reads the homepage

Given a visitor opens `https://livespec-ai.org/`

When the page loads

Then the visitor first sees livespec described as a "dark" software factory and an experimental work in progress, with a link to "The Software Factory: A Practitioner's Guide" on thewoolleyweb.com

And the visitor next sees a link to the blog

And the visitor next sees the three goals: the specification–implementation feedback loop, turning quality dials toward 11 within the fast/cheap/right trade-off, and finding the minimal human attention the factory needs

And the visitor next sees a project-state summary made mostly of links to the livespec GitHub repositories

And the visitor finally sees who is responsible for livespec: an introduction to Chad Woolley ("thewoolleyman")

## Scenario: Visitor follows a project-state link

Given a visitor is on the homepage

When the visitor follows the link to the livespec installation documentation

Then the visitor arrives at that documentation in the `thewoolleyman/livespec` GitHub repository

## Scenario: Visitor browses the blog

Given a visitor opens `https://livespec-ai.org/blog/`

When the page loads

Then the visitor sees a list of blog entries, newest first, each with its title and publication date

When the visitor selects a placeholder entry

Then the visitor arrives at `/blog/<slug>/` showing the entry's title, author, publication date, and placeholder text

And the entry links back to `/blog/` and `/`

## Scenario: Visitor uses a phone

Given a visitor opens any page on a 360-pixel-wide screen

When the page loads

Then all content is readable without horizontal scrolling

And prose paragraphs are start-aligned in a single readable column

## Scenario: Visitor browses with JavaScript disabled

Given a visitor's browser has JavaScript disabled

When the visitor opens any page

Then all content and navigation work

## Scenario: Visitor uses the www or http address

Given a visitor requests `http://www.livespec-ai.org/blog/`

When the request completes

Then the visitor lands on `https://livespec-ai.org/blog/`

## Scenario: Maintainer reviews the site from the filesystem

Given a maintainer opens `site/index.html` from a local checkout via a `file://` URL

When the page loads and the maintainer follows the header, body, and footer links

Then every page renders with the site stylesheet

And every internal link opens the target page rather than a directory listing

## Scenario: Search engine indexes the site

Given a crawler fetches `https://livespec-ai.org/robots.txt`

When the crawler follows the referenced sitemap

Then the sitemap lists the homepage, the blog index, and every blog entry with their last-modified dates

And each listed page carries a title, description, and canonical URL
