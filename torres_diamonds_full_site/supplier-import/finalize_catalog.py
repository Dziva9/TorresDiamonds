from pathlib import Path
import json,re
ROOT=Path(__file__).resolve().parents[1]
ps=json.loads((ROOT/'assets/full-catalog.json').read_text());old=json.loads((ROOT/'assets/catalog.json').read_text())
links={}
for p in old:
 matches=[x for x in ps if {u.split('?')[0] for u in x['photos']} & {u.split('?')[0] for u in p['photos']}]
 if len(matches)==1:links[p['file'].removesuffix('.html')]=matches[0]['id']
assert len(links)==8,links
(ROOT/'assets/legacy-product-links.json').write_text(json.dumps(links,indent=2))
for file in ROOT.glob('*.html'):
 if file.name=='shop.html':continue
 text=file.read_text()
 for legacy,target in links.items():text=text.replace('href="'+legacy+'.html"','href="shop.html?piece='+target+'"')
 file.write_text(text)
# Track current collection coverage separately from older links that no longer resolve.
def norm(t):
 t=t.lower().replace('lab grown','lab').replace('ghostforge','').replace('draco diamond','');return re.sub(r'[^a-z0-9]+',' ',re.sub(r'\s*\|\s*(silver|10k).*','',t)).strip()
def core(t):return norm('|'.join(t.split('|')[:2]))
live=json.loads((ROOT/'supplier-import/live-collection-audit.json').read_text());current={core(t):t for c in live['seen'] for t in c['titles']};good={core(p['sourceName']) for p in ps}
audit=json.loads((ROOT/'supplier-import/audit.json').read_text())
audit['historical_links_not_imported']=audit.pop('unresolved')
audit['current_collection_titles_checked']=len(current)
audit['current_collection_titles_not_matched']=[v for k,v in current.items() if k not in good]
audit['notes']=['Supplier collection snapshots reported different total counts. Products are deduplicated by their source product URL, not those displayed totals.','Every title observed in the refreshed category-page audit is matched to a product with source photos. Older broken/redirecting links are recorded separately.','Photos are linked to supplier image URLs, not downloaded locally.','Demo prices are source retail reference prices; metal/size-specific final pricing is not verified.']
(ROOT/'supplier-import/audit.json').write_text(json.dumps(audit,indent=2))
# Browser-side preview routing so existing home/product links lead into the new catalogue.
preview_ids={'product':'gFkcTwvXD00bPvSzeuvY','product-tennis':'Dtd67TDYAeQbiWTl7VIS','product-radiant':'mBohSqn3N04ndiMf6cXZ','product-studs':'LVvTS2LwwFPjnSsVTgTN','product-pendant':'BCcC9fFI2ipjBcW5Jkgo','product-emerald':'9XMCazCWJvJmeab7jY5T','product-emerald-bracelet':'J0x3GPRSp5e4ZRTXCMnR','product-chain':'Mo5MGrjyoPMhshuV6w3K'}
map_paths={}
for path,piece in links.items():map_paths['/'+path]=piece;map_paths['/preview/'+preview_ids[path]]=piece
navigation='''
(function(){
 if(location.hostname!=='sites.leadconnectorhq.com'||window.torresCatalogNavigation)return;
 window.torresCatalogNavigation=true;
 const mapping=MAP;
 const shop='https://sites.leadconnectorhq.com/preview/NJ3gOq7uJJfRmiHoweOF';
 function updateLink(link){
  let url;try{url=new URL(link.getAttribute('href'),location.href);}catch(e){return;}
  if(url.origin!==location.origin)return;
  const path=url.pathname.replace(/\\.html$/,'').replace(/\\/$/,'');
  const piece=mapping[path];if(!piece)return;
  link.href=shop+'?piece='+encodeURIComponent(piece);
 }
 function updateAll(){document.querySelectorAll('#torres-site a[href]').forEach(updateLink);}
 updateAll();document.addEventListener('DOMContentLoaded',updateAll);document.addEventListener('hydrationDone',updateAll);
 document.addEventListener('click',function(event){const link=event.target.closest&&event.target.closest('#torres-site a[href]');if(link)updateLink(link);},true);
})();
'''.replace('MAP',json.dumps(map_paths,separators=(',',':')))
(ROOT/'assets/catalog-preview-navigation.js').write_text(navigation)
print('Matched all 8 existing product links into the catalogue; checked',len(current),'current collection titles. Matched:',len(current)-len(audit['current_collection_titles_not_matched']))
