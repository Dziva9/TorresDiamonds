(function(){
'use strict';
if(window.torresSupplierReviewCleanup)return;window.torresSupplierReviewCleanup=true;
const selector='.reviews,.review-card,.testimonials,.testimonial,.testimonial-card,.jdgm-widget,.yotpo-main-widget,.loox-reviews-default,[data-testimonials],[data-customer-reviews]';
let queued=false;
function clean(){queued=false;const root=document.querySelector('#torres-site');if(!root)return;root.querySelectorAll(selector).forEach(block=>{if(!/\bdraco\b/i.test(block.textContent||''))return;const section=block.closest('section');const heading=section?.querySelector('h2');if(section&&heading&&/review|testimonial|customer.*say|customer.*love|customer.*stor/i.test(heading.textContent)&&!section.querySelector('.product-card,.category-card,[data-torres-catalog],form,iframe'))section.remove();else block.remove();});}
function schedule(){if(!queued){queued=true;requestAnimationFrame(clean);}}
if(document.readyState==='loading')document.addEventListener('DOMContentLoaded',schedule,{once:true});else schedule();
document.addEventListener('hydrationDone',schedule);
if(document.body)new MutationObserver(schedule).observe(document.body,{childList:true,subtree:true});
})();
