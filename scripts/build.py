#!/usr/bin/env python3
"""Build CORA's static site with the retained CLeAR template, using Python only."""
from pathlib import Path
from html import escape
from datetime import date
from render_people import participant_catalog, render_participants, render_people
import argparse, json, re, shutil

ROOT = Path(__file__).resolve().parents[1]
parser = argparse.ArgumentParser()
parser.add_argument('--base-path', default='')
parser.add_argument('--output', default=str(ROOT/'dist'))
args = parser.parse_args()
base = '/' + args.base_path.strip('/') if args.base_path.strip('/') else ''
if base and not re.fullmatch(r'/[A-Za-z0-9._/-]+', base): raise SystemExit('Invalid base path')
out = Path(args.output).resolve()
protected = [ROOT/n for n in ('data','assets','vendor','templates','scripts','docs','.github','.openai','.git')]
if out == ROOT or out in ROOT.parents or any(out==p or p in out.parents or out in p.parents for p in protected):
 raise SystemExit('Output must be separate from source folders and their ancestors')
if out.exists(): shutil.rmtree(out)
out.mkdir(parents=True)
for name in ('assets','vendor'): shutil.copytree(ROOT/name, out/name)
shutil.copy2(ROOT/'LICENSE', out/'LICENSE')
facts = json.loads((ROOT/'data/verified-facts.json').read_text())
content = json.loads((ROOT/'data/content.json').read_text())
lab, pi = facts['lab'], facts['pi']
roster = json.loads((ROOT/'data/people.json').read_text())
phd_count = sum(p['category'] == 'phd' for p in roster['people'])
ms_count = sum(p['category'] == 'ms' for p in roster['people'])
template = (ROOT/'templates/layout.html').read_text()
E = lambda x: escape(str(x), quote=True)
U = lambda path: base + path
def link(url, text, cls=''):
 return f'<a href="{E(url)}"'+(f' class="{cls}"' if cls else '')+f'>{E(text)}</a>'
def local(path,text): return link(U(path),text)
def heading(text): return f'<h1 class="page-heading">{E(text)}</h1>'
nav = [('Home','/'),('About','/about/'),('Research','/research/'),('Projects','/projects/'),('Papers','/publications/'),('People','/people/'),('Teaching','/teaching/'),('Contact','/contact/')]
pages = []
def page(path,title,body,active=None):
 active = active or path
 nav_html=''.join(f'<li'+(' class="active"' if route==active else '')+'><a href="'+U(route)+'"'+(' aria-current="page"' if route==active else '')+'>'+name+'</a></li>' for name,route in nav)
 html=template
 for key,value in {'title':E(title),'base':base,'nav':nav_html,'body':body}.items(): html=html.replace('{{'+key+'}}',value)
 dest = out/('index.html' if path=='/' else path.strip('/')+'/index.html')
 if path=='/404.html': dest=out/'404.html'
 dest.parent.mkdir(parents=True,exist_ok=True);dest.write_text(html)
 pages.append(str(dest.relative_to(out)))

def social_link(url,label,icon):
 return f'<a href="{E(url)}"><i class="fa {icon}" aria-hidden="true"></i> {E(label)}</a>'
social='<p class="home-links">'+social_link(lab['github'],'GitHub','fa-github')+' '+social_link(lab['scholar'],'Google Scholar','fa-graduation-cap')+' '+social_link('mailto:'+pi['email'],pi['email'],'fa-envelope-o')+'</p>'
news=''.join('<li><span class="news-date">'+E(n['date'])+'</span> — '+link(n['url'],n['title'])+'<br>'+E(n['text'])+'</li>' for n in facts['news'])
profiles_by_name = participant_catalog(roster)
research_items = ''.join(
 f'<li data-research-id="{E(area["id"])}">'
 + local('/research/#' + area['id'], area['title'])
 + '<p>' + E(area['short']) + '</p>'
 + render_participants(area['participants'], profiles_by_name, E, local)
 + '</li>'
 for area in content['research']
)
home=f'''<img class="hero-image" src="{U('/assets/cora-autonomy.svg')}" width="1000" height="580" alt="CORA: computational methods connecting ground, aerial and space robotics">
<h1 class="hero-title">Computational Robotics and Autonomy</h1>
<p class="hero-subtitle"><span>{E(pi['department'])}</span><span>Inha University · Incheon, Republic of Korea</span><span lang="ko">인하대학교 계산로보틱스 및 자율시스템 연구실</span></p>
{social}<div class="news-box"><h2 class="page-heading">Research highlights</h2><ul>{news}</ul></div>
<section class="section"><h2 class="page-heading">Research areas</h2><p>{E(content['mission'])}</p><ul class="research-list home-research-list">{research_items}</ul></section>
<section><h2 class="page-heading">Research and education projects</h2><p>Explore our international collaborations, research projects, and graduate education programs. {local('/projects/','View our projects')}.</p></section>
<section><h2 class="page-heading">Our people</h2><p>Our team includes the principal investigator, {phd_count} Ph.D. students, and {ms_count} M.S. students. {local('/people/','Meet our researchers and alumni')}.</p></section>
<section><h2 class="page-heading">Research with us</h2><p>Interested in graduate research, undergraduate research, or collaboration? {local('/contact/','Get in touch with CORA Lab')}.</p></section>'''
page('/','Home',home)

about=heading('About us')+f'''<p>The <strong>Computational Robotics and Autonomy (CORA) Lab</strong> at <a href="https://www.inha.ac.kr/">Inha University</a> develops computational methods for intelligent autonomous systems. The lab is led by {local('/people/kwangki-kim/',pi['name'])}.</p><p>{E(content['mission'])}</p>
<h2 class="page-heading">Research approach</h2><ul class="research-list">'''+''.join('<li>'+E(x)+'</li>' for x in content['approach'])+f'''</ul><p lang="ko">CORA Lab은 최적화, 확률적 추론, 학습 기법을 결합하여 로봇의 인지·추정·계획·제어 문제를 연구합니다. 수학적 방법론을 실제 로봇과 임베디드 시스템에서 검증하며, 신뢰할 수 있는 자율시스템 구현을 목표로 합니다.</p>
<h2 class="page-heading">International collaboration</h2><p><strong>SafeRL-HRC</strong> brings together safe robot learning, constrained reinforcement learning, and formal verification for human–robot collaboration. The Japan–Korea project with the Nara Institute of Science and Technology runs in FY2025–FY2028. {link(facts['project']['source'],'Project overview')}.</p>
<h2 class="page-heading">Open research</h2><p>Explore our {local('/publications/','selected publications')} and {link(lab['github'],'open-source repositories')}, including code for motion planning and multi-robot state estimation.</p>'''
page('/about/','About',about)

research=heading('Research')+'<p>From mathematical structure to real-time autonomous behavior.</p>'
research+='<nav class="research-jump-links" aria-label="Research themes"><ol>'
research+=''.join('<li>'+local('/research/#'+r['id'],r['title'])+'</li>' for r in content['research'])
research+='</ol></nav>'
for r in content['research']:
 research+=f'<section class="section research-section" id="{E(r["id"])}" aria-labelledby="{E(r["id"])}-title">'
 research+=''.join(f'<span class="research-anchor" id="{E(alias)}" aria-hidden="true"></span>' for alias in r.get('aliases',[]))
 research+=f'<h2 class="page-heading" id="{E(r["id"])}-title">{E(r["title"])}</h2>'
 if r.get('participants'):
  research += render_participants(r['participants'], profiles_by_name, E, local)
 research+=f'<p>{E(r["body"])}</p>'
 if r.get('body_ko'):
  research+=f'<p class="research-description-ko" lang="ko">{E(r["body_ko"])}</p>'
 research+=f'<p class="research-topics"><strong>Topics:</strong> {E(", ".join(r["topics"]))}</p>'
 if r.get('image'):
  research+=f'<figure class="research-figure compact"><img src="{U("/assets/"+r["image"])}" alt="{E(r["caption"])}" loading="lazy"><figcaption>{E(r["caption"])} · {link(r["image_source"],"Source and project details")}</figcaption></figure>'
 if r.get('links'):
  research+='<p class="research-links">'+' · '.join((local(l['url'],l['label']) if l['url'].startswith('/') else link(l['url'],l['label'])) for l in r['links'])+'</p>'
 research+='</section>'
page('/research/','Research',research)

from render_projects import render_projects
projects = json.loads((ROOT/'data/projects.json').read_text())
render_projects(projects, E, U, link, heading, page)

catalog_path=ROOT/'data/publications.json'
catalog=json.loads(catalog_path.read_text()) if catalog_path.exists() else {'records':facts['publications']}
publications=sorted(catalog['records'],key=lambda p:(-(p.get('year') or 0),p['title'].casefold()))
years=sorted({p['year'] for p in publications if p.get('year')},reverse=True)
has_undated=any(not p.get('year') for p in publications)
types=sorted({p.get('type') or 'Other' for p in publications})
scholar_url=lab['scholar']
papers=heading('Publications')+'<p>Research publications and conference contributions by Kwang-Ki K. Kim and collaborators. Visit '+link(scholar_url,'Google Scholar')+' for the citation record.</p>'
updated_on = catalog.get('metadata', {}).get('updated_date') or catalog.get('metadata', {}).get('verified_date')
update_note = ''
if updated_on:
 updated = date.fromisoformat(updated_on)
 update_note = f' · Updated {updated.day} {updated:%B %Y}'
papers += ('<p class="bibliography-note">Sources: CV, ' + link(pi['orcid'], 'ORCID')
           + ', publisher records, and the lab bibliography' + E(update_note) + '.</p>')
papers+='<form class="paper-controls" hidden><div class="search-field"><label for="paper-search">Search title, author, or venue</label><input id="paper-search" type="search" placeholder="e.g. trajectory, estimation, Kim" autocomplete="off"></div><div><label for="paper-year">Year</label><select id="paper-year"><option value="">All years</option>'+''.join(f'<option value="{y}">{y}</option>' for y in years)+('<option value="undated">Undated</option>' if has_undated else '')+'</select></div><div><label for="paper-type">Type</label><select id="paper-type"><option value="">All types</option>'+''.join(f'<option value="{E(t)}">{E(t)}</option>' for t in types)+'</select></div><button type="reset">Clear</button></form><p class="filter-status" id="filter-status" role="status" aria-live="polite">'+str(len(publications))+' publications</p><div class="no-results" id="no-results" hidden><p>No matching publications. Try another keyword or clear the filters.</p></div><hr>'
for y in years+([None] if has_undated else []):
 papers+=f'<section class="paper-group"><h2 class="page-heading">{y or "Undated"}</h2><ul class="paper-list">'
 for p in [p for p in publications if p.get('year')==y]:
  volume=str(p.get('volume') or '')+('('+str(p['issue'])+')' if p.get('issue') else '')
  details=', '.join(str(x) for x in [volume,p.get('pages') or p.get('article')] if x)
  venue=('<em>'+E(p['venue'])+'</em>') if p.get('venue') else ''
  venue=', '.join(x for x in [venue,E(details)] if x)
  links=[]
  if p.get('doi'):links.append(link('https://doi.org/'+p['doi'],'DOI'))
  elif p.get('url'):links.append(link(p['url'],p.get('url_label') or ('Preprint' if p.get('type')=='Preprint' else 'Paper')))
  if p.get('preprint') and p['preprint']!=p.get('url'):links.append(link(p['preprint'],'Preprint'))
  if p.get('code'):links.append(link(p['code'],'Code'))
  authors=E(p.get('authors') or '')
  lead=(authors+' ' if authors else '')+(f'({y}). ' if y else '')
  status_label=('<span class="paper-type">'+E(p.get('presentation_type') or 'Presentation')+'</span>' if p.get('status')=='Presented' else '')
  papers+=f'<li class="paper" id="{E(p["id"])}" data-year="{y or "undated"}" data-type="{E(p.get("type") or "Other")}">{lead}<span class="paper-title">{E(p["title"])}</span>.'+(' '+venue+'.' if venue else '')+f'<div class="paper-links"><span class="paper-type">{E(p.get("type") or "Other")}</span>'+status_label+''.join(links)+'</div></li>'
 papers+='</ul></section>'
page('/publications/','Papers',papers)

render_people(roster, pi, lab, E, U, link, local, heading, page, research=content['research'])

teaching=heading('Teaching')+'<p>Mathematical foundations and practical software for robotics and autonomy.</p>'
for c in content['courses']:
 teaching+=f'<section class="course"><h2>{E(c["title"])}</h2><p>{E(c["description"])}</p><p><strong>Topics:</strong> {E(", ".join(c["topics"]))}</p></section>'
teaching+='<hr><h2 class="page-heading">Course access</h2><p>Enrolled students should use the course links and learning management system provided by the instructor for materials, assignments, and announcements.</p><h2 class="page-heading">Open-source learning resources</h2><ul class="research-list">'
for r in content['resources']:teaching+='<li>'+link(r['url'],r['name'])+' — '+E(r['description'])+'</li>'
teaching+='</ul>'
page('/teaching/','Teaching',teaching)

contact=heading('Contact')+f'''<h2 class="page-heading">Computational Robotics and Autonomy Lab</h2><p>{E(pi['department'])}<br>Inha University<br>100 Inha-ro, Michuhol-gu, Incheon 22212<br>Republic of Korea</p><p class="contact-email">{link('mailto:'+pi['email'],pi['email'])}</p><p>Principal Investigator: {local('/people/kwangki-kim/',pi['name'])}</p><hr><h2 class="page-heading">Prospective students</h2><p>If you are interested in research with CORA Lab, please email a short introduction, your CV, research interests, and intended degree and start term. You may also include a project portfolio or links to relevant code.</p><p lang="ko">대학원 진학, 학부 연구 참여 및 공동연구에 관심이 있으시면 연구 관심 분야와 간단한 자기소개를 이메일로 보내 주세요.</p><h2 class="page-heading">Research collaboration</h2><p>For academic or industry collaboration, share the technical problem, intended application, and possible scope of joint research.</p><p>{link(lab['github'],'GitHub')} · {link(lab['scholar'],'Google Scholar')} · {link(pi['faculty_url'],'Inha faculty profile')}</p>'''
page('/contact/','Contact',contact)

credits=heading('Site credits')+'<p>This CORA Lab site adapts the typography, responsive navigation, and page structure of the '+link('https://clearoboticslab.github.io/','CLeAR Robotics Lab website')+'. The original template license is preserved in '+local('/LICENSE','LICENSE')+'.</p><p>CORA artwork was created for this site. People profiles and portraits are provided by CORA Lab in the supplied website source. Research images are from CORA’s public project repositories and are linked next to the figures.</p><p>Rendering dependencies and their notices are included in '+local('/vendor/licenses/README.md','third-party license notices')+'.</p>'
page('/credits/','Site credits',credits)
page('/404.html','Page not found',heading('Page not found')+'<p>The requested page could not be found. '+local('/','Return to the CORA Lab homepage')+'.</p>')
(out/'.nojekyll').touch()
print(json.dumps({'pages':len(pages),'publications':len(publications),'base_path':base,'output':str(out)}))
