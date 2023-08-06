## -*- coding: utf-8; mode: html; -*-
<%inherit file="tailbone:templates/home.mako" />

<%def name="title()">Home</%def>

<div class="logo">

## ${h.image(request.static_url('rattail_tutorial.web:static/img/rattail_tutorial.jpg'), "Rattail Tutorial Logo", id='logo', width=500)}
${h.image(request.static_url('tailbone:static/img/home_logo.png'), "Rattail Logo")}

</div>

<h1 style="text-align: center;">Welcome to Rattail Tutorial</h1>

