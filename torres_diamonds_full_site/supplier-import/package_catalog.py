from pathlib import Path
import json,re,html,csv,ast,zipfile,shutil
ROOT=Path(__file__).resolve().parents[1]
products=json.loads((ROOT/'assets/full-catalog.json').read_text())
original=(ROOT.parent/'torres_diamonds_before_full_catalog/shop.html').read_text()
header=original[original.index('<header'):original.index('<section class="page-hero">')]
tail=original[original.index('<section class="section signup">'):original.index('<script src="script.js">')]
def esc(s):return html.escape(str(s),quote=True)
def icon(name):
 shapes={'search':'<circle cx="10.5" cy="10.5" r="6.5"/><path d="M16 16L21 21"/>','bag':'<path d="M5 7H19L20 21H4L5 7Z"/><path d="M8 8V6A4 4 0 0116 6V8"/>'}
 return '<svg class="inventory-icon" width="17" height="17" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.6" stroke-linecap="round" aria-hidden="true">'+shapes[name]+'</svg>'
def card(p):
 return '<article class="inventory-card"><div class="inventory-photo"><a href="?piece='+esc(p['id'])+'" data-piece="'+esc(p['id'])+'"><img src="'+esc(p['photos'][0])+'" alt="'+esc(p['name'])+'" loading="lazy"></a><button type="button" class="inventory-look" data-look="'+esc(p['id'])+'">'+icon('search')+'Quick look</button></div><div class="inventory-card-copy"><a class="inventory-card-title" data-piece="'+esc(p['id'])+'" href="?piece='+esc(p['id'])+'">'+esc(p['name'])+'</a><p class="inventory-card-spec">'+esc(p['shortSpec'])+'</p><span class="inventory-card-price">'+('Demo from ${:,.2f} CAD'.format(p['price']) if p['price'] else 'Price to be confirmed')+'</span></div></article>'
static='<section class="inventory-intro"><div class="wrap"><div class="eyebrow">The Torres Collection</div><h1>Find your next favourite.</h1><p>Explore diamond jewelry, signature settings, and pieces for the moments that matter. Find a style you love, then make the details your own.</p><div class="inventory-meta">Demo collection · Final selections and Torres pricing to be confirmed</div></div></section><section class="inventory-main"><div class="wrap"><div class="inventory-grid">'+''.join(card(p) for p in products[:12])+'</div><noscript><p>Enable JavaScript to search the full collection and explore individual pieces.</p></noscript></div></section>'
body=header+'<main data-torres-catalog>'+static+'</main>'+tail
(ROOT/'shop.html').write_text('<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>The Collection — Torres Diamonds</title><meta name="description" content="Explore the Torres Diamonds demo collection of diamond rings, bracelets, earrings, necklaces and pendants. Compare designs and discover your favourite pieces."><link rel="stylesheet" href="styles.css"><link rel="stylesheet" href="inventory.css"></head><body><div id="torres-site">'+body+'</div><script src="inventory-data.js"></script><script src="script.js"></script><script src="inventory.js"></script></body></html>')
# New catalogue entries are handled on one shop page, including in GHL Preview.
PREVIEW={'index':'GkpoNkcedsYPmejbXyqg','about':'4XG3BozjpcN9mtamLIVx','custom':'ATEZPZYEkp3JlmxiElZn','shop':'NJ3gOq7uJJfRmiHoweOF','consultation':'P822KIXJKfiJIf45VKdl','faq':'hccbBMf7AJCJ0QCuHRdw'}
base='https://sites.leadconnectorhq.com/preview/'
ghl_body=body
for key,id in PREVIEW.items():
 ghl_body=ghl_body.replace('href="'+key+'.html"','href="'+base+id+'"').replace('href="'+key+'.html#','href="'+base+id+'#')
# Preserve the official photo source/reference data in CSV and JSON, but ship only UI fields in the browser payload.
public=[{k:v for k,v in p.items() if k not in ['sourceName','sourceUrl','sourceHandle','capturedDate']} for p in products]
data='window.TORRES_CATALOG='+json.dumps(public,ensure_ascii=False,separators=(',',':')).replace('<','\\u003c')+';\n'
script=(ROOT/'inventory.js').read_text()
script=script.replace('href="consultation.html"','href="'+base+PREVIEW['consultation']+'"').replace('href="custom.html"','href="'+base+PREVIEW['custom']+'"')
# Scope just the new inventory stylesheet; leave the user's existing GHL site CSS intact.
tree=ast.parse(Path('/tmp/package_torres_ghl.py').read_text());mod=ast.Module(body=[x for x in tree.body if isinstance(x,ast.FunctionDef) and x.name in ['end_brace','scope']],type_ignores=[])
ns={'re':re};exec(compile(mod,'css-scoper','exec'),ns)
newcss=ns['scope'](re.sub(r'/\*.*?\*/','',(ROOT/'inventory.css').read_text(),flags=re.S))
out=ROOT.parent/'Torres_Full_Catalog_Demo';out.mkdir(exist_ok=True)
(out/'01-SHOP-HTML.txt').write_text('<div id="torres-site">'+ghl_body+'</div>')
(out/'02-CATALOG-CSS-APPEND.txt').write_text(newcss)
(out/'03-CATALOG-SCRIPT-SITE-WIDE.txt').write_text('<script>\n'+data+script+'\n'+(ROOT/'assets/catalog-preview-navigation.js').read_text()+'\n</script>')
shutil.copy2(ROOT/'assets/catalog-review.csv',out/'CATALOG-SELECTION.csv')
shutil.copy2(ROOT/'assets/full-catalog.json',out/'SOURCE-TO-TORRES-CATALOG.json')
shutil.copy2(ROOT/'supplier-import/audit.json',out/'IMPORT-AUDIT.json')
# A single local HTML file with embedded CSS/data/scripts makes the entire catalogue easy to review.
standalone='<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>The Collection — Torres Diamonds</title><style>'+(ROOT/'styles.css').read_text()+'\n'+(ROOT/'inventory.css').read_text()+'</style></head><body><div id="torres-site">'+body+'</div><script>'+data+'</script><script>'+(ROOT/'script.js').read_text()+'</script><script>'+(ROOT/'inventory.js').read_text()+'</script></body></html>'
# Keep the full existing site alongside the one-file catalogue for working review navigation.
review=out/'REVIEW_SITE';review.mkdir(exist_ok=True)
for file in ROOT.iterdir():
 if file.is_file() and file.suffix in ['.html','.css','.js']:shutil.copy2(file,review/file.name)
shutil.copytree(ROOT/'assets',review/'assets',dirs_exist_ok=True)
for file in ROOT.glob('*.html'):
 standalone=standalone.replace('href="'+file.name+'"','href="REVIEW_SITE/'+file.name+'"').replace('href="'+file.name+'#','href="REVIEW_SITE/'+file.name+'#')
(out/'OPEN-CATALOG-PREVIEW.html').write_text(standalone)
with (out/'PHOTO-SOURCES.csv').open('w',newline='') as f:
 w=csv.writer(f);w.writerow(['Torres product','View','Image URL','Supplier product URL'])
 for p in products:
  for i,url in enumerate(p['photos'],1):w.writerow([p['name'],i,url,p['sourceUrl']])
(out/'START-HERE.txt').write_text('''TORRES FULL CATALOGUE DEMO

REVIEW FIRST
Open OPEN-CATALOG-PREVIEW.html in a browser. The entire catalogue is in this one file; no local server is required for catalogue browsing, search, product views, gallery or demo bag. The rest of the existing website is included in REVIEW_SITE for local navigation. Product photos and Google Fonts require internet access.

UPDATE THE EXISTING GHL SHOP PAGE ONLY
1. Open your existing Shop page in GHL. Replace its Custom HTML element contents with ALL of 01-SHOP-HTML.txt.
2. Keep the Shop page's existing working Custom CSS and paste ALL of 02-CATALOG-CSS-APPEND.txt at the bottom.
3. In website Settings > Body tracking code, append ALL of 03-CATALOG-SCRIPT-SITE-WIDE.txt ONCE. Keep your existing site scripts and navigation patch. Do not also paste this new catalogue script into each page footer.
4. Save, then open the Shop preview in a new tab. The script only initializes on pages containing this new catalogue element.

ONE SHOP PAGE, ALL PRODUCTS
Each product opens as a view on the same Shop page, using ?piece=the-product-id. The browser Back button returns to the collection. Search, categories, price sorting, more results, photo galleries and the demo bag operate within this page. You DO NOT need to create hundreds of new GHL pages or gather additional preview IDs.
Existing links to the eight older demo product pages are also redirected into this catalogue by the new shared script.\nThe existing Shop preview URL is https://sites.leadconnectorhq.com/preview/NJ3gOq7uJJfRmiHoweOF . Product-view links automatically retain the current page path, so they work in that preview and later on your published Shop page.

CHOOSING INVENTORY
CATALOG-SELECTION.csv includes a Keep? column, Torres names, source listing names, source product URLs, demo reference prices, photo URLs and a Notes column. Open it in Excel or Sheets and mark the pieces you want. SOURCE-TO-TORRES-CATALOG.json preserves the underlying mapping.

PRICES AND PURCHASES
Displayed prices are demonstration reference prices observed on supplier product pages, not wholesale costs or approved Torres retail prices. Catalogue-card snapshots and detail pages sometimes disagree; the detail-page price is preferred. Final pricing for a selected metal/size must be confirmed.
The demo bag supports adding pieces, quantities, removing items, and a reference subtotal. It saves to the current browser where storage is available. Checkout is intentionally disabled: no order is submitted and no payment is taken. Rings and jewelry are not inventory reservations.

PHOTOS AND COPY
Product images reference the supplier's original image URLs. They are NOT downloaded local copies; network restrictions in the build environment prevented that. Photo source URLs are included for later upload to your own media storage. Only product imagery is used; Draco's homepage lifestyle photo is not used.
Product names are Torres-inspired. Descriptions are rewritten from product design information. Product specifications are retained where explicitly available. Draco reviews, price-saving percentages, promotional programmes, founder claims, return terms and shipping guarantees are not carried over.

COMPARISONS
Competitor comparison work is deferred as requested. No Blue Nile or other competitor price/savings claim is added by this package.

STATUS
The import audit records coverage of the refreshed collection pages and separates older broken links from that current coverage. This is demo content, not a verified live-stock feed. No changes were deployed to your GHL account. GHL Preview rendering still requires checking in your account.
''')
with zipfile.ZipFile(out.with_suffix('.zip'),'w',zipfile.ZIP_DEFLATED) as z:
 for f in out.rglob('*'):
  if f.is_file():z.write(f,Path(out.name)/f.relative_to(out))
print('Packaged',len(products),'products at',out)
