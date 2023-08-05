## -*- coding: utf-8; -*-
<%inherit file="/master/view.mako" />
<%namespace file="/util.mako" import="view_profiles_helper" />

<%def name="extra_javascript()">
  ${parent.extra_javascript()}
  % if not instance.users and request.has_perm('users.create'):
      <script type="text/javascript">
        ## TODO: should do this differently for Buefy themes
        $(function() {
            $('#make-user').click(function() {
                if (confirm("Really make a user account for this person?")) {
                    % if not use_buefy:
                    disable_button(this);
                    % endif
                    $('form[name="make-user-form"]').submit();
                }
            });
        });
      </script>
  % endif
</%def>

<%def name="object_helpers()">
  ${parent.object_helpers()}
  ${view_profiles_helper([instance])}
</%def>

${parent.body()}

## TODO: should do this differently for Buefy themes
% if not instance.users and request.has_perm('users.create'):
    ${h.form(url('people.make_user'), name='make-user-form')}
    ${h.csrf_token(request)}
    ${h.hidden('person_uuid', value=instance.uuid)}
    ${h.end_form()}
% endif
