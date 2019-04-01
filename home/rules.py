import rules


@rules.predicate
def is_project_owner(user, project):
    return user == project.owner


@rules.predicate
def is_project_editor(user, project):  # user must always be the first parameter
    return False  # TODO add editors


@rules.predicate
def project_visible(user, project):  # user must always be the first parameter
    return project.visible

@rules.predicate
def is_staff(user):
    return user.is_staff


rules.add_perm('projects.is_owner', is_project_owner)
rules.add_perm('projects.edit_project', is_project_owner | is_project_editor)
rules.add_perm('projects.delete_project', is_project_owner)
rules.add_perm('projects.can_view', project_visible | is_project_owner | is_project_editor)

rules.add_perm('common.is_staff', is_staff)