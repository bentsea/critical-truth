---
title: "{% if subjectItem %}{{ subjectItem.title }} ({{ subjectItem.release_year }}){% else %}{{ title }}{% endif %}"
blurb: ""
categories: [{% if subjectItem %}review,movie,{{ subjectItem.categories | join(',') }}{% else %}editorial{% endif %}]
image: {% if subjectItem %}{{ subjectItem.cover_image }}{% endif %}
author: {{ author_username }}
youtube: {% if review  == true %}
reviewInfo:
   final-verdict: ""
   rating: {% endif %}{% if subjectItem %}
subjectInfo:
   type: {{ subjectItem.type }}
   name: "{{ subjectItem.title }}"
   sameAs: "{{ subjectItem.imdb_url }}"
   image: "https://image.tmdb.org/t/p/original{{ subjectItem.poster_path }}"
   director: "{{ subjectItem.director }}"
   dateCreated: "{{ subjectItem.release_date }}"{% endif %}
published: False
---



