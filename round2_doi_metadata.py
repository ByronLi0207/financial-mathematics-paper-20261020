import json,urllib.request,urllib.parse
for doi in ['10.1016/0304-405X(81)90020-9','10.1016/0304-405X(95)00832-Y','10.1111/0022-1082.00067']:
 url='https://api.crossref.org/works/'+urllib.parse.quote(doi,safe='');req=urllib.request.Request(url,headers={'User-Agent':'ResearchMetadataVerification/1.0'})
 with urllib.request.urlopen(req,timeout=45) as r:
  m=json.load(r)['message'];print(json.dumps(dict(url=url,status=r.status,DOI=m['DOI'],title=m['title'],authors=m['author'],journal=m['container-title'],volume=m.get('volume'),issue=m.get('issue'),page=m.get('page'),published_print=m.get('published-print')),ensure_ascii=False))
