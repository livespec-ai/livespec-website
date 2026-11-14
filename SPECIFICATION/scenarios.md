# livespec-ai.org — scenarios

Acceptance scenarios in Gherkin form. Each Gherkin keyword line is
preceded and followed by a blank line so that every step renders as
its own Markdown paragraph under GitHub-Flavored Markdown.

## Scenario: Visitor reads the homepage

Given a visitor opens `https://livespec-ai.org/`

When the page loads

Then the visitor sees a description of what livespec is

And the visitor sees a link to the blog

And the visitor sees the project goals

And the visitor sees links to the livespec GitHub repositories, including the core README, installation documentation, and specification

And the visitor sees an introduction to Chad Woolley ("thewoolleyman")

## Scenario: Visitor follows a repository link

Given a visitor is on the homepage

When the visitor follows the link to the livespec installation documentation

Then the visitor arrives at that documentation in the `thewoolleyman/livespec` GitHub repository

## Scenario: Visitor browses the blog

Given a visitor opens `https://livespec-ai.org/blog/`

When the page loads

Then the visitor sees a list of blog entries, newest first, each with its title and publication date

When the visitor selects an entry

Then the visitor arrives at `/blog/<slug>/` showing the entry's title, author, publication date, and body

And if the entry is a placeholder, it is clearly marked as a placeholder

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
