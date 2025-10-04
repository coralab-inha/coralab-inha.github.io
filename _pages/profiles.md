---
layout: page
title: people
permalink: /people/
description: Members of the Lab
nav: true
nav_order: 2
display_categories: [professor, phd, msphd, master, intern]
horizontal: false
---

<!-- pages/people.md -->
<div class="people">
{% if page.display_categories %}
  <!-- Display categorized members -->
  {% for category in page.display_categories %}
  <a id="{{ category }}" href=".#{{ category }}">
    <h2 class="category">{{ category | capitalize }}</h2>
  </a>

  {% assign categorized_people = site.people | where: "category", category %}

  <div class="container mt-3">
    <div class="row row-cols-1 row-cols-md-3 g-4">
      {% for person in categorized_people %}
      <div class="col">
        <div class="card h-100 shadow-sm border-0">
          <a href="{{ person.url }}" style="text-decoration:none; color:inherit;">
            {% if person.image %}
              <img src="{{ person.image }}" class="card-img-top rounded" alt="{{ person.title }}">
            {% endif %}
            <div class="card-body">
              <h5 class="card-title text-center fw-bold">{{ person.title }}</h5>
              {% if person.position %}
                <p class="card-text text-center text-muted">{{ person.position }}</p>
              {% endif %}
              {% if person.course %}
                <p class="card-text text-center small">{{ person.course }}</p>
              {% endif %}
            </div>
          </a>
        </div>
      </div>
      {% endfor %}
    </div>
  </div>

  {% endfor %}
{% endif %}
</div>
