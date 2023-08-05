## -*- coding: utf-8; -*-
<%namespace file="/grids/nav.mako" import="grid_index_nav" />
<%namespace file="/feedback_dialog_buefy.mako" import="feedback_dialog" />
<%namespace file="/autocomplete.mako" import="tailbone_autocomplete_template" />
<%namespace name="base_meta" file="/base_meta.mako" />
<!DOCTYPE html>
<html lang="en">
  <head>
    <meta http-equiv="content-type" content="text/html; charset=UTF-8" />
    <title>${base_meta.global_title()} &raquo; ${capture(self.title)|n}</title>
    ${base_meta.favicon()}
    ${self.header_core()}

    % if background_color:
        <style type="text/css">
          body, .navbar, .footer {
              background-color: ${background_color};
          }
        </style>
    % endif

    % if not request.rattail_config.production():
        <style type="text/css">
          body, .navbar, .footer {
            background-image: url(${request.static_url('tailbone:static/img/testing.png')});
          }
        </style>
    % endif

    ${self.head_tags()}
  </head>

  <body>

    ## TODO: should move template to JS, then can postpone the JS
    ${tailbone_autocomplete_template()}
    ${h.javascript_link(request.static_url('tailbone:static/js/tailbone.buefy.autocomplete.js') + '?ver={}'.format(tailbone.__version__))}

    <header>

      <nav class="navbar" role="navigation" aria-label="main navigation">

        <div class="navbar-brand">
          <a class="navbar-item" href="${url('home')}">
            ${base_meta.header_logo()}
            ${base_meta.global_title()}
          </a>
          <a role="button" class="navbar-burger" aria-label="menu" aria-expanded="false">
            <span aria-hidden="true"></span>
            <span aria-hidden="true"></span>
            <span aria-hidden="true"></span>
          </a>
        </div>

        <div class="navbar-menu">
          <div class="navbar-start">

            % for topitem in menus:
                % if topitem.is_link:
                    ${h.link_to(topitem.title, topitem.url, target=topitem.target, class_='navbar-item')}
                % else:
                    <div class="navbar-item has-dropdown is-hoverable">
                      <a class="navbar-link">${topitem.title}</a>
                      <div class="navbar-dropdown">
                        % for subitem in topitem.items:
                            % if subitem.is_sep:
                                <hr class="navbar-divider">
                            % else:
                                ${h.link_to(subitem.title, subitem.url, class_='navbar-item', target=subitem.target)}
                            % endif
                        % endfor
                      </div>
                    </div>
                % endif
            % endfor

          </div><!-- navbar-start -->
          <div class="navbar-end">

            ## User Menu
            % if request.user:
                <div class="navbar-item has-dropdown is-hoverable">
                  % if messaging_enabled:
                      <a class="navbar-link ${'root-user' if request.is_root else ''}">${request.user}${" ({})".format(inbox_count) if inbox_count else ''}</a>
                  % else:
                      <a class="navbar-link ${'root-user' if request.is_root else ''}">${request.user}</a>
                  % endif
                  <div class="navbar-dropdown">
                    % if request.is_root:
                        ${h.link_to("Stop being root", url('stop_root'), class_='navbar-item root-user')}
                    % elif request.is_admin:
                        ${h.link_to("Become root", url('become_root'), class_='navbar-item root-user')}
                    % endif
                    % if messaging_enabled:
                        ${h.link_to("Messages{}".format(" ({})".format(inbox_count) if inbox_count else ''), url('messages.inbox'), class_='navbar-item')}
                    % endif
                    ${h.link_to("Change Password", url('change_password'), class_='navbar-item')}
                    ${h.link_to("Logout", url('logout'), class_='navbar-item')}
                  </div>
                </div>
            % else:
                ${h.link_to("Login", url('login'), class_='navbar-item')}
            % endif

          </div><!-- navbar-end -->
        </div>
      </nav>

      <nav class="level" style="margin: 0.5rem auto;">
        <div class="level-left">

          ## Current Context
          <div id="current-context" class="level-item">
            % if master:
                % if master.listing:
                    <span>${index_title}</span>
                % else:
                    ${h.link_to(index_title, index_url)}
                    % if parent_url is not Undefined:
                        <span>&raquo;</span>
                        ${h.link_to(parent_title, parent_url)}
                    % elif instance_url is not Undefined:
                        <span>&raquo;</span>
                        ${h.link_to(instance_title, instance_url)}
                    % endif
                    % if master.viewing and grid_index:
                        ${grid_index_nav()}
                    % endif
                % endif
            % elif index_title:
                <span>${index_title}</span>
            % endif
          </div>

          % if expose_db_picker is not Undefined and expose_db_picker:
              <div class="level-item">
                <p>DB:</p>
              </div>
              <div class="level-item">
                ${h.form(url('change_db_engine'))}
                ${h.csrf_token(request)}
                ${h.hidden('engine_type', value=master.engine_type_key)}
                <div class="select">
                  ${h.select('dbkey', db_picker_selected, db_picker_options, id='db-picker')}
                </div>
                ${h.end_form()}
              </div>
          % endif

        </div><!-- level-left -->
        <div class="level-right">

          ## Quickie Lookup
          % if quickie is not Undefined and quickie and request.has_perm(quickie.perm):
              <div class="level-item">
                ${h.form(quickie.url, method="get")}
                <div class="level">
                  <div class="level-right">
                    <div class="level-item">
                      ${h.text('entry', placeholder=quickie.placeholder, autocomplete='off')}
                    </div>
                    <div class="level-item">
                      <button type="submit" class="button is-primary">
                        <span class="icon is-small">
                          <i class="fas fa-search"></i>
                        </span>
                        <span>Lookup</span>
                      </button>
                    </div>
                  </div>
                </div>
                ${h.end_form()}
              </div>
          % endif

          ## Theme Picker
          % if expose_theme_picker and request.has_perm('common.change_app_theme'):
              <div class="level-item">
                ${h.form(url('change_theme'), method="post")}
                ${h.csrf_token(request)}
                Theme:
                <div class="theme-picker">
                  <div class="select">
                    ${h.select('theme', theme, options=theme_picker_options, id='theme-picker')}
                  </div>
                </div>
                ${h.end_form()}
              </div>
          % endif

          ## Help Button
          % if help_url is not Undefined and help_url:
              <div class="level-item">
                ${h.link_to("Help", help_url, target='_blank', class_='button')}
              </div>
          % endif

          ## Feedback Button / Dialog
          ${h.javascript_link(request.static_url('tailbone:static/themes/falafel/js/tailbone.feedback.js') + '?ver={}'.format(tailbone.__version__))}
          ${feedback_dialog()}
          <div id="feedback-app">
            <feedback-form action="${url('feedback')}">
            </feedback-form>
          </div>
          <script type="text/javascript">
            new Vue({el: '#feedback-app'})
          </script>

        </div><!-- level-right -->
      </nav><!-- level -->
    </header>

    ## Page Title
    <section id="content-title" class="hero is-primary">
      <div class="container">
        % if capture(self.content_title):

            % if show_prev_next is not Undefined and show_prev_next:
                <div style="float: right;">
                  % if prev_url:
                      ${h.link_to(u"« Older", prev_url, class_='button autodisable')}
                  % else:
                      ${h.link_to(u"« Older", '#', class_='button', disabled='disabled')}
                  % endif
                  % if next_url:
                      ${h.link_to(u"Newer »", next_url, class_='button autodisable')}
                  % else:
                      ${h.link_to(u"Newer »", '#', class_='button', disabled='disabled')}
                  % endif
                </div>
            % endif

            <h1 class="title">${self.content_title()}</h1>
        % endif
      </div>
    </section>

    <div class="content-wrapper">

    ## Page Body
    <section id="page-body">

      % if request.session.peek_flash('error'):
          % for error in request.session.pop_flash('error'):
              <div class="notification is-warning">
                <!-- <button class="delete"></button> -->
                ${error}
              </div>
          % endfor
      % endif

      % if request.session.peek_flash():
          % for msg in request.session.pop_flash():
              <div class="notification is-info">
                <!-- <button class="delete"></button> -->
                ${msg}
              </div>
          % endfor
      % endif

      ${self.body()}
    </section>

    ## Footer
    <footer class="footer">
      <div class="content">
        ${base_meta.footer()}
      </div>
    </footer>

    </div><!-- content-wrapper -->

  </body>
</html>

<%def name="title()"></%def>

<%def name="content_title()">
  ${self.title()}
</%def>

<%def name="header_core()">

  ${self.core_javascript()}
  ${self.extra_javascript()}
  ${self.core_styles()}
  ${self.extra_styles()}

  ## TODO: should this be elsewhere / more customizable?
  % if dform is not Undefined:
      <% resources = dform.get_widget_resources() %>
      % for path in resources['js']:
          ${h.javascript_link(request.static_url(path))}
      % endfor
      % for path in resources['css']:
          ${h.stylesheet_link(request.static_url(path))}
      % endfor
  % endif
</%def>

<%def name="core_javascript()">
  ${self.jquery()}
  ${self.vuejs()}
  ${self.buefy()}
  ${self.fontawesome()}

  ## some commonly-useful logic for detecting (non-)numeric input
  ${h.javascript_link(request.static_url('tailbone:static/js/numeric.js') + '?ver={}'.format(tailbone.__version__))}

  ## Tailbone / Buefy stuff
  ${h.javascript_link(request.static_url('tailbone:static/js/tailbone.buefy.datepicker.js') + '?ver={}'.format(tailbone.__version__))}
  ${h.javascript_link(request.static_url('tailbone:static/js/tailbone.buefy.numericinput.js') + '?ver={}'.format(tailbone.__version__))}
  ${h.javascript_link(request.static_url('tailbone:static/js/tailbone.buefy.oncebutton.js') + '?ver={}'.format(tailbone.__version__))}
  ${h.javascript_link(request.static_url('tailbone:static/js/tailbone.buefy.timepicker.js') + '?ver={}'.format(tailbone.__version__))}
  ${h.javascript_link(request.static_url('tailbone:static/js/tailbone.buefy.grid.js') + '?ver={}'.format(tailbone.__version__))}

  <script type="text/javascript">
    var session_timeout = ${request.get_session_timeout() or 'null'};
    var logout_url = '${request.route_url('logout')}';
    var noop_url = '${request.route_url('noop')}';
    % if expose_db_picker is not Undefined and expose_db_picker:
        $(function() {
            $('#db-picker').change(function() {
                $(this).parents('form:first').submit();
            });
        });
    % endif
    % if expose_theme_picker and request.has_perm('common.change_app_theme'):
        $(function() {
            $('#theme-picker').change(function() {
                $(this).parents('form:first').submit();
            });
        });
    % endif
    $(function() {
        ## NOTE: this code was copied from
        ## https://bulma.io/documentation/components/navbar/#navbar-menu
        $('.navbar-burger').click(function() {
            $('.navbar-burger').toggleClass('is-active');
            $('.navbar-menu').toggleClass('is-active');
        });
    });
  </script>
</%def>

<%def name="jquery()">
  ## jQuery 1.12.4
  ${h.javascript_link('https://code.jquery.com/jquery-1.12.4.min.js')}
</%def>

<%def name="vuejs()">
  ## Vue.js (latest)
  ${h.javascript_link('https://unpkg.com/vue')}

  ## vue-resource
  ## (needed for e.g. this.$http.get() calls, used by grid at least)
  ${h.javascript_link('https://cdn.jsdelivr.net/npm/vue-resource@1.5.1')}
</%def>

<%def name="buefy()">
  ## Buefy (latest)
  ${h.javascript_link('https://unpkg.com/buefy/dist/buefy.min.js')}
</%def>

<%def name="fontawesome()">
  <script defer src="https://use.fontawesome.com/releases/v5.3.1/js/all.js"></script>
</%def>

<%def name="extra_javascript()"></%def>

<%def name="core_styles()">

  ${self.buefy_styles()}

  ${h.stylesheet_link(request.static_url('tailbone:static/themes/bobcat/css/base.css') + '?ver={}'.format(tailbone.__version__))}
  ${h.stylesheet_link(request.static_url('tailbone:static/themes/falafel/css/layout.css') + '?ver={}'.format(tailbone.__version__))}
  ${h.stylesheet_link(request.static_url('tailbone:static/css/grids.css') + '?ver={}'.format(tailbone.__version__))}
  ${h.stylesheet_link(request.static_url('tailbone:static/themes/falafel/css/grids.css') + '?ver={}'.format(tailbone.__version__))}
  ${h.stylesheet_link(request.static_url('tailbone:static/themes/falafel/css/grids.rowstatus.css') + '?ver={}'.format(tailbone.__version__))}
##   ${h.stylesheet_link(request.static_url('tailbone:static/css/filters.css') + '?ver={}'.format(tailbone.__version__))}
  ${h.stylesheet_link(request.static_url('tailbone:static/themes/falafel/css/filters.css') + '?ver={}'.format(tailbone.__version__))}
  ${h.stylesheet_link(request.static_url('tailbone:static/themes/bobcat/css/forms.css') + '?ver={}'.format(tailbone.__version__))}
  ${h.stylesheet_link(request.static_url('tailbone:static/themes/falafel/css/forms.css') + '?ver={}'.format(tailbone.__version__))}
  ${h.stylesheet_link(request.static_url('tailbone:static/css/diffs.css') + '?ver={}'.format(tailbone.__version__))}

  <style type="text/css">
    .filters .filter-fieldname {
        min-width: ${filter_fieldname_width};
        justify-content: left;
    }
    .filters .filter-verb {
        min-width: ${filter_verb_width};
    }
  </style>
</%def>

<%def name="buefy_styles()">
  ## Buefy 0.7.4
  ${h.stylesheet_link('https://unpkg.com/buefy@0.7.4/dist/buefy.min.css')}
</%def>

## TODO: this is only being referenced by the progress template i think?
## (so, should make a Buefy progress page at least)
<%def name="jquery_theme()">
  ${h.stylesheet_link('https://code.jquery.com/ui/1.11.4/themes/dark-hive/jquery-ui.css')}
</%def>

<%def name="extra_styles()"></%def>

<%def name="head_tags()"></%def>

<%def name="wtfield(form, name, **kwargs)">
  <div class="field-wrapper${' error' if form[name].errors else ''}">
    <label for="${name}">${form[name].label}</label>
    <div class="field">
      ${form[name](**kwargs)}
    </div>
  </div>
</%def>

<%def name="simple_field(label, value)">
  ## TODO: keep this? only used by personal profile view currently
  ## (although could be useful for any readonly scenario)
  <div class="field-wrapper">
    <div class="field-row">
      <label>${label}</label>
      <div class="field">
        ${'' if value is None else value}
      </div>
    </div>
  </div>
</%def>
