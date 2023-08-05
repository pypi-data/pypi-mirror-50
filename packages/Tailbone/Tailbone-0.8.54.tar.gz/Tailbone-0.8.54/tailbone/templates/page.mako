## -*- coding: utf-8; -*-
<%inherit file="/base.mako" />

<%def name="context_menu_items()"></%def>

<%def name="page_content()"></%def>

<%def name="render_this_page()">
  <div style="display: flex; justify-content: space-between;">

    <div class="this-page-content">
      ${self.page_content()}
    </div>

    <ul id="context-menu">
      ${self.context_menu_items()}
    </ul>

  </div>
</%def>

<%def name="render_this_page_buefy()">
  <script type="text/x-template" id="this-page-template">
    <div>
      ${self.render_this_page()}
    </div>
  </script>

  <div id="this-page-app">
    <this-page></this-page>
  </div>
</%def>

<%def name="modify_this_page()">
  ## NOTE: if you override this, must use <script> tags
</%def>

<%def name="declare_page_vars()">
  <script type="text/javascript">

    let ThisPage = {
        template: '#this-page-template',
        methods: {}
    }

    let ThisPageData = {}

  </script>
</%def>

<%def name="finalize_page_components()">
  ## NOTE: if you override this, must use <script> tags
</%def>

<%def name="make_this_page_app()">
  ${self.declare_page_vars()}
  ${self.modify_this_page()}
  ${self.finalize_page_components()}
  <script type="text/javascript">

    ThisPage.data = function() { return ThisPageData }

    Vue.component('this-page', ThisPage)

    new Vue({
        el: '#this-page-app'
    })

  </script>
</%def>


% if use_buefy:
    ${self.render_this_page_buefy()}
    ${self.make_this_page_app()}
% else:
    ${self.render_this_page()}
% endif
