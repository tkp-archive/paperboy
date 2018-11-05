{%- extends 'full.tpl' -%}

{%- block html_head -%}
<style type="text/css">
    body {
        font-family: Calibri;
        text-align: justify;
        line-height: 1.1;
        font-weight: normal;
        letter-spacing: normal;
        overflow: visible;
        padding: 8px;
    }

    div#notebook {
        overflow: visible;
        border-top: none;
    }

    div.cell {
        /* fix for outlook */
        border: none !important;
    }
    div {

    }

    {%- if resources.global_content_filter.no_prompt-%}
    div#notebook-container{
      padding: 6ex 12ex 8ex 12ex;
    }
    {%- endif -%}
    @media print {
      div.cell {
        display: block;
        page-break-inside: avoid;
      } 
      div.output_wrapper { 
        display: block;
        page-break-inside: avoid; 
      }
      div.output { 
        display: block;
        page-break-inside: avoid; 
      }
    }

    div.output_png.output_subarea {
        max-width: 100% !important;
    }

    img {
        width: 100%;
        white-space: nowrap;
        padding: 0px;
        display: block;
        margin-left: auto;
        margin-right: auto;
    }

    h1 {
        background-color: #7397bc;
        color:white;
        height: 50px !important;
        padding:0px;
        margin-top:20px;
        margin-bottom: 10px;
    }

    h2 {
        border-bottom: 4px solid #7397bc;
        color: #444;
        padding: 0px;
        margin-top: 20px;
        margin-bottom: 10px;
    }

    h3 {
        color:#222;
        padding:0px;
        margin-top: 20px;
        margin-bottom: 10px;
    }

    td {
        text-align:right;
        padding:2px;
        margin-top:2px;
    }

    th {
        font-weight: normal;
        text-align: left;
        margin-top: 2px;
    }

    thead {
        background-color: #dce6f1;
        padding: 2px;
    }

    thead th {
        font-weight: bold;
        text-align: center;
        padding-left: 10px;
        padding-bottom: 2px;
        border-bottom: 1px solid #95b3d7;
    }

    tr {
        border-bottom: 1px solid #DDD;
    }

    th.pivot_row_header{}
    tr.empty_pivot_row{}
    tr.empty_pivot_row_first{}

    th.empty_pivot_row{
        font-weight: bold;
        padding-left:2px;
    }

    th.empty_pivot_row_first{
        font-weight: bold;
        border-bottom: 1px solid #95b3d7;
        padding-left: 2px;
    }

    td.empty_pivot_row{}

    td.empty_pivot_row_first{
        border-bottom: 1px solid #95b3d7;
    }

    tr.total_pivot_row {
        background-color: #dce6f1;
    }

    th.total_pivot_row {
        font-weight: bold;
        padding-left: 2px;
        border-top: 1px solid #95b3d7;
    }

    td.total_pivot_row {
        border-top: 1px solid #95b3d7;
        font-weight: bold;
    }

    table {
        margin-top: 10px;
        margin-left: 10px;
        padding-bottom: 20px;
        padding:0px;
        white-space: nowrap;
        border-collapse: collapse;
        font-family: Calibri, Arial;
        font-size: 9px;
        letter-spacing: normal;
        mso-displayed-decimal-separator: "\.";
        mso-displayed-thousand-separator: "\,";
        table-layout: auto;
        width:600px;
    }

    .header {
        font-size: 0.75em;
    }

    .footer {
        font-size: 0.75em;
    }
</style>
{{ super() }}
<div class="header"></div>
{%- endblock html_head -%}

{% block footer %}
<div class="footer"></div>
{{ super() }}
{%- endblock footer %}

{% block in_prompt -%}
{%- endblock in_prompt %}

{% block empty_in_prompt -%}
{%- endblock empty_in_prompt %}

{% block output_area_prompt %}
{% endblock output_area_prompt %}


