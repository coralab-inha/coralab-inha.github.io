"""Render the supplied CORA roster within the retained CLeAR page frame."""


def participant_name(label):
    """The original label is displayed unchanged; parentheses are ignored for lookup."""
    return label[1:-1] if label.startswith('(') and label.endswith(')') else label


def participant_catalog(roster):
    catalog = {}
    for person in roster['people']:
        name = person.get('research_name_ko')
        if not name or person['category'] == 'alumni':
            continue
        if name in catalog:
            raise ValueError(f'Ambiguous research profile name: {name}')
        catalog[name] = person['id']
    return catalog


def render_participants(participants, profiles_by_name, E, local):
    if not participants:
        return ''
    labels = []
    for label in participants:
        identifier = profiles_by_name.get(participant_name(label))
        labels.append(local('/people/' + identifier + '/', label) if identifier else E(label))
    return '<p class="research-participants" lang="ko"><strong>참여연구원</strong> <span>' + ', '.join(labels) + '</span></p>'


def render_people(roster, pi, lab, E, U, link, local, heading, page, research=()):
    people = roster['people']
    topics_by_name = {}
    for topic in research:
        for label in topic.get('participants', []):
            topics_by_name.setdefault(participant_name(label), []).append((topic, label))
    groups = [(c, [p for p in people if p['category'] == c['key']])
              for c in roster['categories']]
    groups = [(c, members) for c, members in groups if members]
    name = lambda p: p.get('display_name') or p['title']
    route = lambda p: '/people/' + p['id'] + '/'
    role = lambda p: (p.get('position') or '').strip() or p.get('role', '')

    body = heading('People')
    body += '<p>Meet the researchers and alumni of the Computational Robotics and Autonomy Lab.</p>'
    body += '<nav class="people-jump-links" aria-label="People categories">'
    for category, members in groups:
        body += local('/people/#' + category['key'], category['title'] + ' (' + str(len(members)) + ')')
    body += '</nav>'
    body += '''<form class="people-controls paper-controls" hidden>
    <div class="search-field"><label for="people-search">Search by name, research topic, interest, or email</label>
    <input id="people-search" type="search" placeholder="e.g. Multi-Robot Systems, 김건우" autocomplete="off"></div>
    <button type="reset">Clear</button></form>
    <p id="people-status" class="filter-status" role="status" aria-live="polite" hidden></p>
    <div id="people-no-results" class="no-results" hidden><p>No matching people. Try another keyword or clear the search.</p></div>'''

    for category, members in groups:
        key = category['key']
        body += f'<section class="people-section" id="{E(key)}" data-people-category="{E(key)}">'
        body += '<h2 class="page-heading">' + E(category['title']) + '</h2>'
        if key == 'alumni':
            body += '<ul class="alumni-list">'
            for p in members:
                body += f'<li data-person-id="{E(p["id"])}"><span lang="ko">{E(name(p))}</span></li>'
            body += '</ul>'
        else:
            body += '<div class="people-grid">'
            for p in members:
                interests = '; '.join(p.get('research_interests', []))
                korean_name = p.get('research_name_ko', '')
                topics = [topic['title'] for topic, _ in topics_by_name.get(korean_name, [])]
                search = ' '.join([p['title'], name(p), korean_name, role(p), p.get('email', ''), interests, *topics])
                body += f'<article class="person-card" data-person-id="{E(p["id"])}" data-search="{E(search)}">'
                body += f'<a class="list-post-title" href="{U(route(p))}"><img class="profile-thumbnail" src="{U(p["image"])}" width="200" height="200" alt="Portrait of {E(p["title"])}" loading="lazy"><span class="name">{E(name(p))}</span></a>'
                if korean_name:
                    body += '<p class="person-role" lang="ko">' + E(korean_name) + '</p>'
                if role(p):
                    body += '<p class="person-role">' + E(role(p)) + '</p>'
                if p.get('email'):
                    body += '<p class="person-email">' + link('mailto:' + p['email'], p['email']) + '</p>'
                if interests:
                    body += '<p class="person-interests">' + E(interests) + '</p>'
                if p.get('current_role'):
                    body += '<p class="person-interests">Now: ' + E(p['current_role']) + '</p>'
                body += '</article>'
            body += '</div>'
        body += '</section>'
    body += '<hr><h2 class="page-heading">Join CORA Lab</h2><p>Our work connects robotics, control, optimization, and learning. Prospective students and collaborators are welcome to ' + local('/contact/', 'contact the principal investigator') + ' with their research interests.</p>'
    page('/people/', 'People', body)

    for p in people:
        if p['category'] == 'alumni':
            continue
        profile = '<p class="profile-back">' + local('/people/#' + p['category'], '← People / ' + next(c['title'] for c, _ in groups if c['key'] == p['category'])) + '</p>'
        profile += heading(name(p))
        profile += f'<div class="profile-intro member-profile" data-person-id="{E(p["id"])}"><img class="profile-photo" src="{U(p["image"])}" alt="Portrait of {E(p["title"])}" width="200" height="240">'
        if p['category'] == 'professor':
            profile += f'<p><strong>Principal Investigator, CORA Lab</strong><br>{E(pi["title"])}<br>{E(pi["department"])}<br>Inha University</p><p lang="ko">김광기 · 인하대학교</p>'
        else:
            position = '<strong>' + E(role(p)) + '</strong><br>' if role(p) else ''
            profile += '<p>' + position + 'Computational Robotics and Autonomy Lab<br>Inha University</p>'
            if p.get('research_name_ko'):
                profile += '<p lang="ko">' + E(p['research_name_ko']) + '</p>'
        if p.get('email'):
            profile += '<p class="profile-email">' + link('mailto:' + p['email'], p['email']) + '</p>'
        if p['category'] == 'professor':
            profile += '<p>' + link(lab['scholar'], 'Google Scholar') + ' · ' + link(pi['orcid'], 'ORCID') + '<br>' + link(pi['faculty_url'], 'Faculty directory') + '</p>'
        for field, label in [('website', 'Website'), ('contact_note', 'Note'), ('current_role', 'Now')]:
            if p.get(field):
                profile += '<p>' + (link(p[field], label) if field == 'website' else E(label + ': ' + p[field])) + '</p>'
        profile += '</div>'

        assignments = topics_by_name.get(p.get('research_name_ko'), [])
        if assignments:
            profile += '<section class="profile-section profile-topics"><h2 class="page-heading">Research topics</h2><ul class="research-list">'
            for topic, label in assignments:
                qualifier = ' <span lang="ko">' + E(label) + '</span>' if label != participant_name(label) else ''
                profile += '<li>' + local('/research/#' + topic['id'], topic['title']) + qualifier + '</li>'
            profile += '</ul></section>'
        if p.get('education'):
            profile += '<section class="profile-section"><h2 class="page-heading">Education</h2><ul class="education-list">'
            for edu in p['education']:
                profile += '<li><strong>' + E(edu['degree']) + '</strong><br>' + E(edu['institution'])
                if edu.get('year'):
                    profile += ' <span class="education-period">· ' + E(edu['year']) + '</span>'
                profile += '</li>'
            profile += '</ul></section>'
        if p.get('research_interests'):
            profile += '<section class="profile-section"><h2 class="page-heading">Research interests</h2><ul class="research-list">'
            profile += ''.join('<li>' + E(x) + '</li>' for x in p['research_interests']) + '</ul></section>'
        elif p['category'] == 'professor':
            profile += '<section class="profile-section"><h2 class="page-heading">Research interests</h2><p>Optimization-based motion planning and control; state estimation and sensor fusion; safe robot learning; energy-aware autonomous systems.</p><p>' + E(pi['name']) + ' leads the Computational Robotics and Autonomy Lab, connecting mathematical methods with practical robot autonomy. ' + local('/publications/', 'Selected publications') + " describe the group's work in trajectory optimization, multi-robot estimation, and data-driven control.</p></section>"
        if p.get('selected_publications'):
            profile += '<section class="profile-section"><h2 class="page-heading">Selected publications</h2><ul class="member-publications">'
            for pub in p['selected_publications']:
                profile += '<li>' + E(pub.get('authors', '').rstrip('. ')) + '. <strong>' + E(pub['title']) + '</strong>. <em>' + E(pub.get('journal', '')) + '</em>.'
                links = [link(pub[k], label) for k, label in [('paper', 'Paper'), ('link', 'Project')] if pub.get(k)]
                if links:
                    profile += '<div class="paper-links">' + ' '.join(links) + '</div>'
                profile += '</li>'
            profile += '</ul></section>'
        page(route(p), name(p), profile, '/people/')
