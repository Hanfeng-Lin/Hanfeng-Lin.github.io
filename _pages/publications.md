---
layout: archive
title: "Publications"
permalink: /publications/
author_profile: true
---

{% if author.googlescholar %}
  You can also find my articles on <u><a href="{{author.googlescholar}}">my Google Scholar profile</a>.</u>
{% endif %}

{% include base_path %}

{% comment %}
  Entries that carry a cover image are shown first, then the rest.
  Both groups run newest first. An entry joins the top group simply by
  containing an image, using the same detection as the thumbnail in
  _includes/archive-single.html -- no front matter flag needed.
{% endcomment %}

{% assign all_pubs = site.publications | sort: "date" | reverse %}

{% for post in all_pubs %}
  {% capture pub_html %}{{ post.excerpt | markdownify }}{{ post.content | markdownify }}{% endcapture %}
  {% if pub_html contains '<img' %}
    {% include archive-single.html %}
  {% endif %}
{% endfor %}

{% for post in all_pubs %}
  {% capture pub_html %}{{ post.excerpt | markdownify }}{{ post.content | markdownify }}{% endcapture %}
  {% unless pub_html contains '<img' %}
    {% include archive-single.html %}
  {% endunless %}
{% endfor %}
