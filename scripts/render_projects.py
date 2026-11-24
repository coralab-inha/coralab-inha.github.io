"""Render CORA’s project directory and individual program pages."""


def render_projects(catalog, E, U, link, heading, page):
    projects = catalog['projects']
    overview = heading('Projects')
    overview += '<div class="projects-intro"><p>' + E(catalog['intro_en']) + '</p>'
    overview += '<p lang="ko">' + E(catalog['intro_ko']) + '</p></div>'
    overview += '<nav class="projects-jump-links" aria-label="Project sections">'
    overview += ''.join(link(U('/projects/#' + p['id']), p['short_label']) for p in projects)
    overview += '</nav>'

    for project in projects:
        identifier = project['id']
        route = '/projects/' + identifier + '/'
        program = project['program_label']
        project_title = project['title_en']
        korean_title = '<p class="project-title-ko" lang="ko">' + E(project['title_ko']) + '</p>'
        context = '<p class="project-category">' + E(program) + ' · ' + E(project['category']) + '</p>'
        summary = '<p class="project-overview">' + E(project['overview_en']) + '</p>'
        summary += '<p class="project-overview" lang="ko">' + E(project['overview_ko']) + '</p>'

        overview += f'<section class="project-section" id="{E(identifier)}" data-project-id="{E(identifier)}">'
        overview += context + '<h2 class="project-title">' + link(U(route), project_title) + '</h2>'
        overview += korean_title + summary + '</section>'

        detail = '<p class="profile-back">' + link(U('/projects/#' + identifier), '← All projects') + '</p>'
        detail += f'<article data-project-detail="{E(identifier)}">'
        detail += context + heading(project_title) + korean_title + summary
        if project.get('scope_ko'):
            detail += '<p lang="ko">' + E(project['scope_ko']) + '</p>'
        if project.get('metadata'):
            detail += '<dl class="project-metadata">'
            for item in project['metadata']:
                detail += '<dt>' + E(item['label']) + '</dt><dd>' + E(item['value']) + '</dd>'
            detail += '</dl>'
        if project.get('focus'):
            detail += '<h2 class="project-focus-heading">Research &amp; education focus</h2><ul class="research-list project-focus" lang="ko">'
            detail += ''.join('<li>' + E(item) + '</li>' for item in project['focus']) + '</ul>'
        if project.get('links'):
            detail += '<h2 class="project-focus-heading">Program resources</h2><ul class="research-list">'
            detail += ''.join('<li>' + link(item['url'], item['label']) + '</li>' for item in project['links']) + '</ul>'
        if project.get('related_links'):
            detail += '<p class="project-related"><span>Explore:</span> '
            detail += ' · '.join(link(U(item['url']) if item['url'].startswith('/') else item['url'], item['label']) for item in project['related_links'])
            detail += '</p>'
        page(route, project_title, detail + '</article>', active='/projects/')

    page('/projects/', 'Projects', overview)
