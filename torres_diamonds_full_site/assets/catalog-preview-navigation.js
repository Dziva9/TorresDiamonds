
(function(){
 if(location.hostname!=='sites.leadconnectorhq.com'||window.torresCatalogNavigation)return;
 window.torresCatalogNavigation=true;
 const mapping={"/product":"shoreline-engagement-ring-3ct","/preview/gFkcTwvXD00bPvSzeuvY":"shoreline-engagement-ring-3ct","/product-emerald":"aurelia-bridal-set-3ct","/preview/9XMCazCWJvJmeab7jY5T":"aurelia-bridal-set-3ct","/product-radiant":"shoreline-engagement-ring-5ct","/preview/mBohSqn3N04ndiMf6cXZ":"shoreline-engagement-ring-5ct","/product-tennis":"harbour-tennis-bracelet-5ct","/preview/Dtd67TDYAeQbiWTl7VIS":"harbour-tennis-bracelet-5ct","/product-pendant":"not-in-current-collection","/preview/BCcC9fFI2ipjBcW5Jkgo":"not-in-current-collection","/product-studs":"not-in-current-collection","/preview/LVvTS2LwwFPjnSsVTgTN":"not-in-current-collection","/product-chain":"solara-tennis-chain-15ct-16in","/preview/Mo5MGrjyoPMhshuV6w3K":"solara-tennis-chain-15ct-16in","/product-emerald-bracelet":"harbour-tennis-bracelet-3ct","/preview/J0x3GPRSp5e4ZRTXCMnR":"harbour-tennis-bracelet-3ct"};
 const shop='https://sites.leadconnectorhq.com/preview/NJ3gOq7uJJfRmiHoweOF';
 function updateLink(link){
  let url;try{url=new URL(link.getAttribute('href'),location.href);}catch(e){return;}
  if(url.origin!==location.origin)return;
  const path=url.pathname.replace(/\.html$/,'').replace(/\/$/,'');
  const piece=mapping[path];if(!piece)return;
  link.href=shop+'?piece='+encodeURIComponent(piece);
 }
 function updateAll(){document.querySelectorAll('#torres-site a[href]').forEach(updateLink);}
 updateAll();document.addEventListener('DOMContentLoaded',updateAll);document.addEventListener('hydrationDone',updateAll);
 document.addEventListener('click',function(event){const link=event.target.closest&&event.target.closest('#torres-site a[href]');if(link)updateLink(link);},true);
})();
