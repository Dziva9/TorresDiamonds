from pathlib import Path
import re,json,zipfile,shutil
R=Path(__file__).resolve().parents[1];O=R.parent/'Torres_Launch_Collection';O.mkdir(exist_ok=True)
# Scope all shared catalogue/commerce rules so GHL's builder is not restyled.
def scope_css(css):
 css=re.sub(r'/\*.*?\*/','',css,flags=re.S);out='';pos=0
 while pos<len(css):
  a=css.find('{',pos)
  if a<0:out+=css[pos:];break
  header=css[pos:a].strip();depth=1;b=a+1
  while depth:
   if css[b]=='{':depth+=1
   elif css[b]=='}':depth-=1
   b+=1
  body=css[a+1:b-1]
  if header.startswith('@media') or header.startswith('@supports'):out+=header+'{'+scope_css(body)+'}'
  elif header.startswith('@'):out+=header+'{'+body+'}'
  else:out+=','.join('#torres-site '+sel.strip() for sel in header.split(','))+'{'+body+'}'
  pos=b
 return out
css=scope_css((R/'inventory.css').read_text())
base='https://sites.leadconnectorhq.com/preview/';mapping={'index':'GkpoNkcedsYPmejbXyqg','shop':'NJ3gOq7uJJfRmiHoweOF','about':'4XG3BozjpcN9mtamLIVx','custom':'ATEZPZYEkp3JlmxiElZn','consultation':'P822KIXJKfiJIf45VKdl','faq':'hccbBMf7AJCJ0QCuHRdw'}
def ghl(s):
 for key,id in mapping.items():s=s.replace(key+'.html',base+id)
 return s
config='window.TORRES_COMMERCE=window.TORRES_COMMERCE||{ghlFormUrl:""};\n'
styles='if(!document.getElementById("torres-commerce-styles")){const s=document.createElement("style");s.id="torres-commerce-styles";s.textContent='+json.dumps(css)+';document.head.append(s);}\n'
script=config+(R/'inventory-data.js').read_text()+ghl((R/'inventory.js').read_text())+'\n'+styles+(R/'commerce.js').read_text()+'\n'+(R/'anchors.js').read_text()+'\n'+(R/'review-cleanup.js').read_text()+'\n'+(R/'assets/catalog-preview-navigation.js').read_text()
(O/'03-REPLACE-CATALOGUE-SCRIPT.txt').write_text('<script>\n'+script+'\n</script>')
(O/'02-APPEND-SHOP-CSS.txt').write_text(css)
for filename,code in [('shop','01-REPLACE-SHOP-HTML.txt'),('index','04-REPLACE-HOME-HTML.txt'),('consultation','05-REPLACE-CONSULTATION-HTML.txt'),('custom','06-REPLACE-CUSTOM-HTML.txt'),('faq','07-REPLACE-FAQ-HTML.txt'),('about','08-REPLACE-ABOUT-HTML.txt')]:
 s=(R/(filename+'.html')).read_text();body=s[s.index('<body>')+6:s.index('</body>')];body=re.sub(r'<script\b.*?</script>','',body,flags=re.S)
 if '<div id="torres-site">' not in body:body='<div id="torres-site">'+body+'</div>'
 (O/code).write_text(ghl(body))
review=O/'REVIEW_SITE';review.mkdir(exist_ok=True)
for f in R.iterdir():
 if f.is_file() and f.suffix in ['.html','.css','.js']:shutil.copy2(f,review/f.name)
ss=(R/'shop.html').read_text()
for file in ['styles.css','inventory.css']:ss=ss.replace('<link rel="stylesheet" href="'+file+'">','<style>'+(R/file).read_text()+'</style>')
for file in ['inventory-data.js','script.js','inventory.js','commerce.js','anchors.js','review-cleanup.js']:ss=ss.replace('<script src="'+file+'"></script>','<script>'+(R/file).read_text()+'</script>')
for f in R.glob('*.html'):ss=ss.replace('href="'+f.name,'href="REVIEW_SITE/'+f.name)
(O/'OPEN-SHOP-PREVIEW.html').write_text(ss)
shutil.copy2(R.parent/'Torres-Website-Review.md',O/'WEBSITE-REVIEW.md')
(O/'00-CONNECTION-SETTINGS.txt').write_text('''GHL FORM CONNECTION\nIn the shared script, the very first line is:\nwindow.TORRES_COMMERCE=window.TORRES_COMMERCE||{ghlFormUrl:""};\n\nThe inquiry form is currently a styled preview that sends nothing. Supply your GHL direct form URL or embed code to replace that preview with the native form. Its custom fields and product-context mapping must be tested using the real form; do not assume iframe fields are populated from the surrounding page. Until the mapping exists, the selected product details are displayed above the form for the customer to include in the message.\n\nSHOPIFY\nNo payment provider, Shopify products or variant IDs are connected. The preview does not collect card details. Once the theme and products are configured, use Shopify native product forms, cart and checkout. GHL handles the inquiry form, CRM and follow-up; connect its Shopify integration for supported customer/order events.\n''')
(O/'READ-ME.txt').write_text('''TORRES LAUNCH COLLECTION — METAL PRICING, INQUIRY AND ORDER REVIEW\n\nREVIEW\nOpen OPEN-SHOP-PREVIEW.html. Open REVIEW_SITE/index.html to review the full website. Photos need internet access. WEBSITE-REVIEW.md contains the six-retailer analysis and recommendations.\n\nWHAT CHANGED\nEight launch listings only. All five metal choices have working prices. Your eight 14K regular CAD prices remain unchanged; other metals use Draco's published ratios (see METAL-PRICING-METHOD.json and RETAIL-PRICES-BY-METAL.csv). Product selections now include metal colour, ring size/sizing-help choice, quantity, and fixed quoted chain lengths. Silver/platinum have only white colour. Selections persist in product URLs. The bag retains configuration and selected-metal pricing and leads to an order review with an inquiry alternative.\n\nGHL UPDATE\n1. Shop page: replace its Custom HTML element with 01-REPLACE-SHOP-HTML.txt. Keep the working existing CSS.\n2. Website Settings > Body tracking: replace ONLY the previous catalogue script block with 03-REPLACE-CATALOGUE-SCRIPT.txt. It starts with window.TORRES_COMMERCE followed by window.TORRES_CATALOG. Keep unrelated site scripts. Do not add a duplicate catalogue script. This shared block supplies the new scoped CSS on all pages automatically.\n3. Home page: replace the Custom HTML element with 04-REPLACE-HOME-HTML.txt. Keep its working CSS.\n4. Consultation and Custom pages: replace their Custom HTML elements with 05 and 06 respectively. Keep their working CSS.\n5. The shared script also fixes Contact, Ordering & Aftercare, About, Diamond Education and Jewelry Guide footer destinations on existing pages. Files 07 and 08 contain the matching FAQ/About HTML for a full refresh if wanted.\n6. Save, reopen the preview, and check desktop/mobile. These files have not been deployed to your account.\n02-APPEND-SHOP-CSS.txt is included as a standalone copy; with the shared script installed, there is no need to paste it into every page.\n\nINQUIRIES AND CHECKOUT\nThe form is a styled interaction preview. It validates input but never sends or saves personal information, and does not show a fake submission confirmation. Supply the real GHL form link/embed code to connect it; see 00-CONNECTION-SETTINGS.txt. Product context appears above the inquiry. Actual GHL custom-field mapping remains to be connected/tested.\nCheckout is an order review preview. It cannot take payments. Shopify will handle product variant validation, taxes, delivery, discounts, payments and order confirmation when the store is set up. No payment details are requested here.\n\nDRAFT PRODUCT ASSUMPTIONS\nYour same-cost-by-karat/carat-tier assumption is retained provisionally. Ring photos and quoted cost/design pairings still need supplier confirmation. The linked oval bridal set has a 3ct centre / 5ct total; the separate 5ct option still flags its weight basis and exact photo as pending. Supplier chain photos show the design and do not establish the photographed length.\n\nWholesale costs and non-14K cost estimates are outside the website in Torres_Internal_Pricing. Other-metal costs are provisional estimates from retail ratios, not verified wholesale quotes. No competitor savings claims or launch discount are activated. Old products remain archived locally; old GHL product pages still require unpublishing if you no longer want them accessible directly.\n''')
with (O/'READ-ME.txt').open('a') as f:
 f.write('\nCURRENT GALLERY FEATURES\nExpanded supplier photo galleries support swipe, trackpad scrolling, mouse dragging, arrow buttons/keys, and a synchronized vertical thumbnail rail on the left. The desktop gallery stays below the header with Back to collection visible, and its height fits the available viewport. Video references are included where mapped; their source URLs remain unverified until the browser loads them. Only successfully loaded videos passing the resolution check appear. Videos play muted and loop when their active slide is at least 55% visible. They pause offscreen, on another slide, or in a background tab. Reduced-motion preferences suppress automatic playback; manual controls remain available. No new product photos or videos are generated.\n')
with zipfile.ZipFile(O.with_suffix('.zip'),'w',zipfile.ZIP_DEFLATED) as z:
 for f in O.rglob('*'):
  if f.is_file():z.write(f,Path(O.name)/f.relative_to(O))
Path('/tmp/torres-final-combined.js').write_text(script)
print('Packaged current launch, inquiry and review files; shared script bytes',len(script))
