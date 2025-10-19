---
layout: page
title: people
permalink: /people/
description: Members of the Lab
nav: true
nav_order: 2
display_categories: [professor, phd, master, undergraduate, alumni]
horizontal: false
---

<!-- pages/people.md -->
<div class="people">
{% if page.display_categories %}
  {% for category in page.display_categories %}
  <h2 class="category mt-4 mb-3">{{ category | capitalize }}</h2>

  {% assign categorized_people = site.people | where: "category", category %}

  <div class="container">
    {% for person in categorized_people %}
    <a href="{{ person.url }}" style="text-decoration: none; color: inherit;">
      <div class="card mb-3 shadow-sm border-0 hover-shadow" style="max-width: 900px; margin: 0 auto; transition: transform 0.2s;">
        <div class="row g-0 align-items-center">
          <div class="col-md-3 text-center">
            {% if person.image %}
              <img src="{{ person.image }}" class="img-fluid rounded-start" alt="{{ person.title }}" style="width: 100%; height: auto; border-radius: 12px;">
            {% else %}
              <div style="background-color: #f0f0f0; width: 100%; height: 100%; border-radius: 12px; display: flex; align-items: center; justify-content: center;">
                <span class="text-muted">No Image</span>
              </div>
            {% endif %}
          </div>
          <div class="col-md-9">
            <div class="card-body">
              <h5 class="card-title fw-bold mb-2">{{ person.title }}</h5>
              {% if person.interests %}
                <p class="card-text text-muted mb-0">{{ person.interests }}</p>
              {% endif %}
            </div>
          </div>
        </div>
      </div>
    </a>
    {% endfor %}
  </div>

  {% endfor %}
{% endif %}
</div>

<style>
.card:hover {
  transform: translateY(-3px);
  box-shadow: 0 4px 12px rgba(0,0,0,0.15);
}
</style>
