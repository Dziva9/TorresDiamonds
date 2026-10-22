(function(){
'use strict';
if(window.torresAnchorsRuntime)return;window.torresAnchorsRuntime=true;
let pending=location.hash.slice(1),frame=0,userMoved=false;
const ids=['contact','ordering','about','diamond-education'];
const footerTargets={'Contact':'contact','Ordering & Aftercare':'ordering','Diamond Education':'diamond-education','Jewelry Guide':'diamond-education','About':'about'};
function root(){return document.querySelector('#torres-site')||document.body;}
function prepare(){
 const site=root();if(!site)return;
 site.querySelectorAll('.navicons .iconbtn').forEach(button=>{if(button.querySelector('svg'))return;const label=button.getAttribute('aria-label');let shape='';if(label==='Browse jewelry')shape='<circle cx="10.5" cy="10.5" r="6.5"/><path d="M16 16L21 21"/>';if(label==='Get help choosing')shape='<path d="M9 8a3 3 0 116 0c0 2-3 2-3 5"/><path d="M12 17h.01"/>';if(shape)button.innerHTML='<svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.7" stroke-linecap="round" aria-hidden="true">'+shape+'</svg>';});
 site.querySelectorAll('footer a[href]').forEach(a=>{const id=footerTargets[a.textContent.trim()];if(!id)return;try{const url=new URL(a.getAttribute('href'),location.href);url.hash=id;if(a.href!==url.href)a.href=url.href;}catch(e){}});
 const path=location.pathname.toLowerCase();
 if(path.includes('consultation')||path.includes('p822kixjkfijif45vkdl')){const h=site.querySelector('.consult-box > .info-card h3');if(h&&!h.id)h.id='contact';}
 if(path.includes('about')||path.includes('4xg3bozjpcn9mtamlivx')){const h=site.querySelector('.page-hero h1');if(h&&!h.id)h.id='about';}
 if(path.includes('faq')||path.includes('hccbbmf7ajcj0qcuhrdw')){const h=site.querySelector('.page-hero h1');if(h&&!h.id)h.id='diamond-education';}
 const order=site.querySelector('#ordering');if(order&&!/^H[1-6]$/.test(order.tagName)){const heading=order.closest('section')?.querySelector('h2');if(heading){order.removeAttribute('id');heading.id='ordering';}}
 ids.forEach(id=>{const target=document.getElementById(id);if(target){target.style.scrollMarginTop=(offset()+24)+'px';if(!target.hasAttribute('tabindex'))target.setAttribute('tabindex','-1');}});
}
function offset(){let edge=0;root()?.querySelectorAll('.header').forEach(h=>{const position=getComputedStyle(h).position;if(position==='sticky'||position==='fixed'){const rect=h.getBoundingClientRect();if(rect.bottom>0)edge=Math.max(edge,Math.max(0,rect.top)+rect.height);}});return edge;}
function scroll(id,smooth,focus){const el=document.getElementById(id);if(!el)return false;const reduce=matchMedia('(prefers-reduced-motion: reduce)').matches;const top=Math.max(0,el.getBoundingClientRect().top+window.scrollY-offset()-24);window.scrollTo({top,behavior:smooth&&!reduce?'smooth':'instant'});if(focus)el.focus({preventScroll:true});return true;}
function attempt(){frame=0;prepare();if(pending&&!['all','rings','bridal','tennis','chains','engagement'].includes(pending)&&scroll(pending,false,true)){const id=pending;pending='';document.fonts?.ready.then(()=>{if(!userMoved&&location.hash==='#'+id)scroll(id,false,false);});}}
function schedule(){if(!frame)frame=requestAnimationFrame(attempt);}
document.addEventListener('click',e=>{const a=e.target.closest?.('a[href]');if(!a||e.defaultPrevented||e.button!==0||e.metaKey||e.ctrlKey||e.shiftKey||e.altKey||a.target==='_blank')return;let url;try{url=new URL(a.href,location.href);}catch(err){return;}const id=url.hash.slice(1);if(!id||['all','rings','bridal','tennis','chains','engagement'].includes(id)||url.origin!==location.origin||url.pathname!==location.pathname||url.search!==location.search)return;prepare();if(!document.getElementById(id))return;e.preventDefault();userMoved=true;history.pushState(null,'',url);scroll(id,true,true);});
window.addEventListener('hashchange',()=>{pending=location.hash.slice(1);userMoved=false;schedule();});
window.addEventListener('resize',prepare,{passive:true});
['wheel','touchstart','keydown'].forEach(type=>window.addEventListener(type,()=>{userMoved=true;},{passive:true}));
if(document.readyState==='loading')document.addEventListener('DOMContentLoaded',schedule,{once:true});else schedule();
document.addEventListener('hydrationDone',schedule);
if(document.body)new MutationObserver(()=>{if(pending||!root()?.querySelector('footer a[href*="#contact"]'))schedule();}).observe(document.body,{childList:true,subtree:true});
})();
