---
layout: page
title: people
permalink: /people/
description: people in the design research collective
nav: true
nav_order: 2
---

<div class="container">
  <div class="row">
    {% assign active_people = site.people | where_exp: "item", "item.category != 'alumni'" %}
    
    {% comment %} 
      Start with Professor/Director 
    {% endcomment %}
    {% assign professors = site.people | where: "category", "professor" %}
    {% for person in professors %}
    <div class="col-md-4 mb-5 text-center">
      <a href="{{ person.url | relative_url }}" style="text-decoration: none; color: inherit;">
        <div class="mb-3">
          <img src="{{ person.image }}" alt="{{ person.title }}" class="img-fluid shadow-sm" style="width: 250px; height: 250px; object-fit: cover; border-radius: 2px;">
        </div>
        <h5 class="font-weight-bold text-uppercase mb-1" style="color: #2c3e50;">{{ person.title }}</h5>
        <div class="font-italic text-muted mb-1">{{ person.role }}</div>
        <div style="color: #3498db;">{{ person.email }}</div>
      </a>
    </div>
    {% endfor %}

    {% comment %} 
      Then PhDs 
    {% endcomment %}
    {% assign phds = site.people | where: "category", "phd" %}
    {% for person in phds %}
    <div class="col-md-4 mb-5 text-center">
      <a href="{{ person.url | relative_url }}" style="text-decoration: none; color: inherit;">
        <div class="mb-3">
          <img src="{{ person.image }}" alt="{{ person.title }}" class="img-fluid shadow-sm" style="width: 250px; height: 250px; object-fit: cover; border-radius: 2px;">
        </div>
        <h5 class="font-weight-bold text-uppercase mb-1" style="color: #2c3e50;">{{ person.title }}</h5>
        <div class="font-italic text-muted mb-1">{{ person.role }}</div>
        <div style="color: #3498db;">{{ person.email }}</div>
      </a>
    </div>
    {% endfor %}

    {% comment %} 
      Then Masters 
    {% endcomment %}
    {% assign masters = site.people | where: "category", "master" %}
    {% for person in masters %}
    <div class="col-md-4 mb-5 text-center">
      <a href="{{ person.url | relative_url }}" style="text-decoration: none; color: inherit;">
        <div class="mb-3">
          <img src="{{ person.image }}" alt="{{ person.title }}" class="img-fluid shadow-sm" style="width: 250px; height: 250px; object-fit: cover; border-radius: 2px;">
        </div>
        <h5 class="font-weight-bold text-uppercase mb-1" style="color: #2c3e50;">{{ person.title }}</h5>
        <div class="font-italic text-muted mb-1">{{ person.role }}</div>
        <div style="color: #3498db;">{{ person.email }}</div>
      </a>
    </div>
    {% endfor %}

    {% comment %} 
      Then Undergrads 
    {% endcomment %}
    {% assign undergrads = site.people | where: "category", "undergraduate" %}
    {% for person in undergrads %}
    <div class="col-md-4 mb-5 text-center">
      <a href="{{ person.url | relative_url }}" style="text-decoration: none; color: inherit;">
        <div class="mb-3">
          <img src="{{ person.image }}" alt="{{ person.title }}" class="img-fluid shadow-sm" style="width: 250px; height: 250px; object-fit: cover; border-radius: 2px;">
        </div>
        <h5 class="font-weight-bold text-uppercase mb-1" style="color: #2c3e50;">{{ person.title }}</h5>
        <div class="font-italic text-muted mb-1">{{ person.role }}</div>
        <div style="color: #3498db;">{{ person.email }}</div>
      </a>
    </div>
    {% endfor %}

  </div>

  <!-- Alumni Section -->
  <div class="mt-5 mb-5 pt-5 border-top">
    <h3 class="font-weight-bold mb-4 text-uppercase text-center">ALUMNI</h3>
    <ul class="list-unstyled mx-auto" style="max-width: 800px; font-size: 1.1rem; line-height: 1.8;">
      <li class="mb-2">1. <strong>Samuel Doe</strong>, MS 2019, now PhD Student at University of Pittsburgh.</li>
      <li class="mb-2">2. <strong>Christina Murphy</strong>, MS 2020, now Composite Application Engineer @ Pratt & Whitney.</li>
      <li class="mb-2">3. <strong>Jacob Robson</strong>, MS 2020, now Engineer @ Rockwell.</li>
    </ul>
  </div>
</div>
