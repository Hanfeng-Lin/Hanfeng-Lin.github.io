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

{% assign featured = site.publications | where: "featured", true %}
{% assign rest = site.publications | where_exp: "item", "item.featured != true" %}

{% for post in featured %}
  {% include archive-single.html %}
{% endfor %}

{% for post in rest reversed %}
  {% include archive-single.html %}
{% endfor %}



  <script>
        document.ready = function () {
            var tree = document.querySelector("#main>.archive article");
            var child = tree.children[1];
            tree.removeChild(child);
        }()
  </script>
