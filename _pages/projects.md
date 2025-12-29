---
layout: page
title: projects
permalink: /projects/
description: projects of the lab
nav: true
nav_order: 3
display_categories: [Research Projects, Research Topics]
horizontal: true
---

<!-- pages/projects.md -->
<div class="projects">

  <!-- Projects Header (Consistent with People/Home) -->
  <div class="text-center mt-5 mb-5">
    <h1 class="font-weight-bold" style="letter-spacing: 2px;">PROJECTS</h1>
    <p class="mx-auto text-muted" style="max-width: 600px;">
      Our research projects spanning various domains.
    </p>
  </div>
{% if site.enable_project_categories and page.display_categories %}
  <!-- Display categorized projects -->
  {% for category in page.display_categories %} 
  <a id="{{ category }}" href=".#{{ category }}" style="text-decoration: none; color: inherit;">
    <div class="text-center mb-4 mt-5">
      <h2 class="font-weight-bold text-uppercase" style="letter-spacing: 1px;">{{ category }}</h2>
      <hr style="width: 50px; border-top: 2px solid #333; margin: 15px auto;">
    </div>
  </a>
  {% assign categorized_projects = site.projects | where: "category", category %}
  {% assign sorted_projects = categorized_projects | sort: "importance" %}
  <!-- Generate list-style items for each project -->
  {% if page.horizontal %}
  <div class="container">
    <div class="row row-cols-1">
    {% for project in sorted_projects %}
      {% include projects_horizontal.liquid %}
    {% endfor %}
    </div>
  </div>
  {% else %}
  <div class="row row-cols-1">
    {% for project in sorted_projects %}
      {% include projects.liquid %}
    {% endfor %}
  </div>
  {% endif %}
  {% endfor %}

{% else %}

<!-- Display projects without categories -->

{% assign sorted_projects = site.projects | sort: "importance" %}

  <!-- Generate list-style items for each project -->

{% if page.horizontal %}

  <div class="container">
    <div class="row row-cols-1">
    {% for project in sorted_projects %}
      {% include projects_horizontal.liquid %}
    {% endfor %}
    </div>
  </div>
  {% else %}
  <div class="row row-cols-1">
    {% for project in sorted_projects %}  
      {% include projects.liquid %}
    {% endfor %}
  </div>
  {% endif %}
{% endif %}
</div>
