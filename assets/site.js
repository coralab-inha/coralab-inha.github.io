/* Progressive enhancement: every publication remains readable without JavaScript. */
(() => {
 const controls = document.querySelector('.paper-controls:not(.people-controls)');
 if (!controls) return;
 controls.hidden = false;
 const search = document.querySelector('#paper-search');
 const year = document.querySelector('#paper-year');
 const type = document.querySelector('#paper-type');
 const papers = [...document.querySelectorAll('.paper')];
 const groups = [...document.querySelectorAll('.paper-group')];
 const status = document.querySelector('#filter-status');
 const empty = document.querySelector('#no-results');
 function filter() {
  const words = search.value.toLocaleLowerCase().trim().split(/\s+/).filter(Boolean);
  let count = 0;
  papers.forEach(paper => {
   const match = (!year.value || paper.dataset.year === year.value) && (!type.value || paper.dataset.type === type.value) && words.every(word => paper.textContent.toLocaleLowerCase().includes(word));
   paper.hidden = !match;
   if (match) count++;
  });
  groups.forEach(group => { group.hidden = ![...group.querySelectorAll('.paper')].some(p => !p.hidden); });
  status.textContent = `${count} of ${papers.length} publications`;
  empty.hidden = count !== 0;
 }
 search.addEventListener('input', filter);
 year.addEventListener('change', filter);
 type.addEventListener('change', filter);
 controls.addEventListener('reset', () => { search.value = ''; year.value = ''; type.value = ''; filter(); search.focus(); });
 controls.addEventListener('submit', e => e.preventDefault());
 filter();
})();

/* People stay readable and profile links work without JavaScript. */
(() => {
 const controls = document.querySelector('.people-controls');
 if (!controls) return;
 const input = document.querySelector('#people-search');
 const people = [...document.querySelectorAll('.people-section [data-person-id]')];
 const sections = [...document.querySelectorAll('.people-section')];
 const status = document.querySelector('#people-status');
 const empty = document.querySelector('#people-no-results');
 controls.hidden = false;
 status.hidden = false;
 function filter() {
  const terms = input.value.toLocaleLowerCase().trim().split(/\s+/).filter(Boolean);
  let count = 0;
  people.forEach(person => {
   const text = (person.dataset.search || person.textContent).toLocaleLowerCase();
   person.hidden = !terms.every(term => text.includes(term));
   if (!person.hidden) count++;
  });
  sections.forEach(section => {
   section.hidden = ![...section.querySelectorAll('[data-person-id]')].some(person => !person.hidden);
  });
  status.textContent = `${count} of ${people.length} people`;
  empty.hidden = count !== 0;
 }
 input.addEventListener('input', filter);
 controls.addEventListener('reset', () => { input.value = ''; filter(); input.focus(); });
 controls.addEventListener('submit', event => event.preventDefault());
 document.querySelectorAll('.people-jump-links a').forEach(anchor => anchor.addEventListener('click', () => {
  if (input.value) { input.value = ''; filter(); }
 }));
 filter();
})();
