const menuBtn=document.getElementById('menuBtn'),drawer=document.getElementById('drawer'),closeDrawer=document.getElementById('closeDrawer');menuBtn?.addEventListener('click',()=>drawer.classList.add('open'));closeDrawer?.addEventListener('click',()=>drawer.classList.remove('open'));drawer?.querySelectorAll('a').forEach(a=>a.addEventListener('click',()=>drawer.classList.remove('open')));document.querySelectorAll('.faq-q').forEach(btn=>{btn.addEventListener('click',()=>{const panel=btn.nextElementSibling,open=panel.style.maxHeight;document.querySelectorAll('.faq-a').forEach(p=>p.style.maxHeight=null);document.querySelectorAll('.faq-q span').forEach(s=>s.textContent='＋');if(!open){panel.style.maxHeight=panel.scrollHeight+'px';btn.querySelector('span').textContent='−'}})});document.querySelectorAll('.choice').forEach(btn=>{btn.addEventListener('click',()=>{const group=btn.parentElement;group.querySelectorAll('.choice').forEach(x=>x.classList.remove('active'));btn.classList.add('active')})});
const filterButtons=[...document.querySelectorAll('[data-filter]')];
function filterProducts(){
 if(!filterButtons.length)return;
 const requested=location.hash.slice(1)||'all';
 const active=filterButtons.some(b=>b.dataset.filter===requested)?requested:'all';
 filterButtons.forEach(b=>b.setAttribute('aria-pressed',String(b.dataset.filter===active)));
 document.querySelectorAll('[data-category]').forEach(card=>{card.hidden=active!=='all'&&card.dataset.category!==active;});
}
filterButtons.forEach(b=>b.addEventListener('click',()=>{location.hash=b.dataset.filter;filterProducts();}));
window.addEventListener('hashchange',filterProducts);filterProducts();

// Real image galleries: thumbnails, quick look, keyboard navigation, swipe and zoom.
const photoDialog=document.createElement('dialog');
photoDialog.className='photo-dialog';
photoDialog.setAttribute('aria-labelledby','photo-title');
photoDialog.innerHTML='<div class="photo-toolbar"><h2 id="photo-title"></h2><button type="button" class="iconbtn photo-close" aria-label="Close photo gallery">×</button></div><div class="photo-stage"><img alt=""></div><div class="photo-controls"><button type="button" class="iconbtn photo-prev" aria-label="Previous photo">←</button><p class="photo-count" aria-live="polite"></p><button type="button" class="photo-zoom pill" aria-pressed="false">Zoom in</button><button type="button" class="iconbtn photo-next" aria-label="Next photo">→</button></div><p class="photo-tip">Click the photo to zoom · Use arrow keys or swipe to change views</p>';
document.body.append(photoDialog);
const photoImage=photoDialog.querySelector('.photo-stage img');
const photoStage=photoDialog.querySelector('.photo-stage');
let galleryImages=[],galleryIndex=0,galleryTitle='',previousOverflow='';
function renderPhoto(){
 photoStage.classList.remove('is-zoomed');
 const zoom=photoDialog.querySelector('.photo-zoom');zoom.textContent='Zoom in';zoom.setAttribute('aria-pressed','false');
 photoImage.src=galleryImages[galleryIndex];
 photoImage.alt=galleryTitle+' — view '+(galleryIndex+1);
 photoDialog.querySelector('.photo-count').textContent=(galleryIndex+1)+' / '+galleryImages.length;
 photoDialog.querySelectorAll('.photo-prev,.photo-next').forEach(button=>button.disabled=galleryImages.length<2);
}
function changePhoto(direction){galleryIndex=(galleryIndex+direction+galleryImages.length)%galleryImages.length;renderPhoto();}
document.querySelectorAll('[data-gallery]').forEach(button=>{
 button.addEventListener('click',()=>{
  galleryImages=JSON.parse(button.dataset.gallery);
  galleryIndex=Number(button.dataset.index||0);
  galleryTitle=button.dataset.title;
  photoDialog.querySelector('#photo-title').textContent=galleryTitle;
  renderPhoto();previousOverflow=document.body.style.overflow;
  document.body.style.overflow='hidden';photoDialog.showModal();
 });
});
photoDialog.querySelector('.photo-close').addEventListener('click',()=>photoDialog.close());
photoDialog.addEventListener('close',()=>{document.body.style.overflow=previousOverflow;photoStage.classList.remove('is-zoomed');});
photoDialog.addEventListener('click',event=>{if(event.target===photoDialog){const r=photoDialog.getBoundingClientRect();if(event.clientX<r.left||event.clientX>r.right||event.clientY<r.top||event.clientY>r.bottom)photoDialog.close();}});
photoDialog.querySelector('.photo-prev').addEventListener('click',()=>changePhoto(-1));
photoDialog.querySelector('.photo-next').addEventListener('click',()=>changePhoto(1));
photoDialog.addEventListener('keydown',event=>{if(event.key==='ArrowLeft'){event.preventDefault();changePhoto(-1);}if(event.key==='ArrowRight'){event.preventDefault();changePhoto(1);}});
function togglePhotoZoom(){photoStage.classList.toggle('is-zoomed');const zoomed=photoStage.classList.contains('is-zoomed');const button=photoDialog.querySelector('.photo-zoom');button.textContent=zoomed?'Zoom out':'Zoom in';button.setAttribute('aria-pressed',String(zoomed));}
photoImage.addEventListener('click',togglePhotoZoom);
photoDialog.querySelector('.photo-zoom').addEventListener('click',togglePhotoZoom);
let photoTouchX=null;
photoStage.addEventListener('touchstart',event=>{photoTouchX=event.touches[0].clientX;},{passive:true});
photoStage.addEventListener('touchend',event=>{if(photoTouchX===null)return;const delta=event.changedTouches[0].clientX-photoTouchX;if(Math.abs(delta)>55){changePhoto(delta<0?1:-1);}photoTouchX=null;},{passive:true});
document.querySelectorAll('[data-product-gallery]').forEach(gallery=>{
 gallery.querySelectorAll('.gallery-thumb').forEach(thumb=>thumb.addEventListener('click',()=>{
  const main=gallery.querySelector('.gallery-main');
  main.querySelector('img').src=thumb.dataset.image;
  main.querySelector('img').alt=thumb.querySelector('img').alt;
  main.dataset.index=thumb.dataset.index;
  gallery.querySelectorAll('.gallery-thumb').forEach(t=>{t.classList.toggle('selected',t===thumb);t.setAttribute('aria-pressed',String(t===thumb));});
 }));
});


(function () {
  if (window.torresProfessionalIcons) return;
  window.torresProfessionalIcons = true;
  const NS = 'http://www.w3.org/2000/svg';
  const shapes = {
    search: ['circle:cx=10,cy=10,r=6', 'path:d=M14.5 14.5L20 20'],
    expand: ['path:d=M8 3H3V8M16 3H21V8M21 16V21H16M8 21H3V16'],
    right: ['path:d=M4 12H20M13 5L20 12L13 19'],
    left: ['path:d=M20 12H4M11 5L4 12L11 19']
  };
  function icon(name) {
    const svg = document.createElementNS(NS, 'svg');
    svg.setAttribute('viewBox', '0 0 24 24');
    svg.setAttribute('width', '16');
    svg.setAttribute('height', '16');
    svg.setAttribute('fill', 'none');
    svg.setAttribute('stroke', 'currentColor');
    svg.setAttribute('stroke-width', '1.6');
    svg.setAttribute('stroke-linecap', 'round');
    svg.setAttribute('stroke-linejoin', 'round');
    svg.setAttribute('aria-hidden', 'true');
    svg.setAttribute('focusable', 'false');
    svg.setAttribute('style', 'display:inline-block;width:16px;height:16px;flex-shrink:0;vertical-align:-2px;margin:0 3px;');
    shapes[name].forEach(function (spec) {
      const colon = spec.indexOf(':');
      const el = document.createElementNS(NS, spec.slice(0, colon));
      const attrs = spec.slice(colon + 1);
      if (spec.startsWith('path:')) el.setAttribute('d', attrs.slice(2));
      else attrs.split(',').forEach(function (attr) {
        const pair = attr.split('='); el.setAttribute(pair[0], pair[1]);
      });
      svg.appendChild(el);
    });
    return svg;
  }
  function updateIcons() {
    const root = document.getElementById('torres-site');
    if (!root) return;
    root.querySelectorAll('.quick-view > span').forEach(function (span) {
      if (span.dataset.torresIcon) return;
      span.replaceChildren(icon('search'));
      span.dataset.torresIcon = 'search';
    });
    const walker = document.createTreeWalker(root, NodeFilter.SHOW_TEXT);
    const nodes = [];
    while (walker.nextNode()) {
      const node = walker.currentNode;
      if (/[↗→←]/.test(node.nodeValue) && !node.parentElement.closest('script,style,textarea,svg')) nodes.push(node);
    }
    nodes.forEach(function (node) {
      const fragment = document.createDocumentFragment();
      node.nodeValue.split(/([↗→←])/).forEach(function (part) {
        const name = {'↗':'expand', '→':'right', '←':'left'}[part];
        fragment.appendChild(name ? icon(name) : document.createTextNode(part));
      });
      node.replaceWith(fragment);
    });
  }
  let queued = false;
  function schedule() {
    if (queued) return;
    queued = true;
    requestAnimationFrame(function () { queued = false; updateIcons(); });
  }
  function start() {
    updateIcons();
    if (document.body && !window.torresIconObserver) {
      window.torresIconObserver = new MutationObserver(schedule);
      window.torresIconObserver.observe(document.body, {childList:true, subtree:true});
    }
  }
  if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', start, {once:true});
  else start();
  document.addEventListener('hydrationDone', start);
})();

