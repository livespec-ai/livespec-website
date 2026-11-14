-- Rewrite relative links to Markdown sources (foo/index.md[#frag]) into links
-- to their rendered pages (foo/index.html[#frag]), in Markdown links and in raw
-- HTML href attributes. Links with a URL scheme, protocol-relative links and
-- root-absolute links are left alone. Rule: SPECIFICATION/non-functional-requirements.md.

local function rewrite(url)
  if url:match("^%a[%w+.-]*:") or url:sub(1, 1) == "/" then
    return url
  end
  local path, rest = url:match("^([^?#]*)(.*)$")
  if path:match("%.md$") then
    return path:sub(1, -4) .. ".html" .. rest
  end
  return url
end

local function rewrite_html(text)
  text = text:gsub('(href%s*=%s*")([^"]*)(")', function(a, url, b) return a .. rewrite(url) .. b end)
  return (text:gsub("(href%s*=%s*')([^']*)(')", function(a, url, b) return a .. rewrite(url) .. b end))
end

function Link(el)
  el.target = rewrite(el.target)
  return el
end

local function raw(el)
  if el.format == "html" then
    el.text = rewrite_html(el.text)
    return el
  end
end

RawInline = raw
RawBlock = raw
