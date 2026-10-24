import asyncio, io, zipfile, shutil
from unittest.mock import patch
import httpx, pytest
from PIL import Image, ImageDraw, ImageEnhance
from fastapi.testclient import TestClient
from backend import app as m
client=TestClient(m.app)
@pytest.fixture(autouse=True)
def isolate_test_collections():
    yield
    for cid in list(m.collections):
        shutil.rmtree(m.ROOT / cid, ignore_errors=True)
    m.collections.clear()
    m.jobs.clear()
    m.cache.clear()
def pic(size=(400,300),fmt='JPEG',exif=False):
    im=Image.new('RGB',size,'tan'); d=ImageDraw.Draw(im); d.rectangle((20,30,150,180),fill='brown'); d.ellipse((200,20,300,160),fill='green'); b=io.BytesIO()
    e=Image.Exif(); e[34853]={1:'N',2:(1.,2.,3.)} if exif else {}
    im.save(b,format=fmt,exif=e); return b.getvalue()
def create(): return client.post('/api/collections').json()['id']
def upload(c,data=None,name='photo.jpg'): return client.post(f'/api/collections/{c}/photos',files=[('files',(name,data or pic(),'image/jpeg'))])
def test_upload_preview_and_original_untouched():
    c=create(); source=pic(); r=upload(c,source); assert r.status_code==200
    p=r.json()[0]; assert p['width']==400 and 'path' not in p
    assert client.get(f'/api/collections/{c}/photos/{p["id"]}').status_code==200
    assert source==pic()
@pytest.mark.parametrize('data',[b'not an image',pic(fmt='GIF')])
def test_bad_upload(data): assert upload(create(),data).status_code==415
def test_size_limit():
    with patch.object(m,'MAX_BYTES',10): assert upload(create()).status_code==413
def test_batch_limit():
    c=create()
    with patch.object(m,'MAX_BATCH',1):
        assert upload(c).status_code==200
        assert upload(c).status_code==422
def test_empty_and_prompt():
    c=create(); assert client.post('/api/analyze',json={'collection_id':c,'brief':'a dessert'}).status_code==422
    assert client.post('/api/analyze',json={'collection_id':c,'brief':'x'}).status_code==422
def test_duplicates_resized_recompressed():
    c=create(); first=upload(c).json()[0]; im=Image.open(io.BytesIO(pic())); im=im.resize((800,600)); b=io.BytesIO(); im.save(b,format='JPEG',quality=65)
    second=upload(c,b.getvalue()).json()[0]; assert first['duplicate_group']==second['duplicate_group']
def test_crop_dimensions():
    for ratio in (9/16,1,4/5):
        a,b,c,d=m.crop_box(1200,800,ratio); assert abs((c-a)/(d-b)-ratio)<.002
        assert 0<=a<c<=1200 and 0<=b<d<=800
def test_rank_relevance_and_no_blur_penalty():
    assert m.rank({'relevance':4,'suitability':4},1,1,False)==100
    assert m.rank({'relevance':0,'suitability':4},1,1,False)==40
    assert m.rank({'relevance':4,'suitability':4},1,1,True)==95
@pytest.mark.parametrize('raw',['{}','{"relevance":9}','not json'])
def test_malformed_schema(raw):
    with pytest.raises(ValueError): m.Assessment.model_validate_json(raw)
def test_export_metadata_safe_names_and_cleanup():
    c=create(); p=upload(c,pic(exif=True),'../../private.jpg').json()[0]
    r=client.post('/api/export',json={'collection_id':c,'photo_ids':[p['id']],'format':'square'}); assert r.status_code==200
    z=zipfile.ZipFile(io.BytesIO(r.content)); assert z.namelist()==['thooriga-01.jpg']
    im=Image.open(z.open(z.namelist()[0])); assert im.size==(300,300) and not im.getexif()
    assert client.post('/api/export',json={'collection_id':c,'photo_ids':['../../etc/passwd']}).status_code==404
    assert client.delete('/api/collections/'+c).status_code==200
    assert not (m.ROOT/c).exists()
    assert client.get(f'/api/collections/{c}/photos/{p["id"]}').status_code==404
def test_origin_and_host_guards():
    assert client.post('/api/collections',headers={'origin':'https://evil.example'}).status_code==403
    assert client.get('/api/health',headers={'host':'evil.example'}).status_code==403
def test_model_missing_and_timeout():
    for exc in (httpx.ConnectError('offline'),httpx.ReadTimeout('timeout')):
        async def fail(*args,**kwargs): raise exc
        with patch.object(httpx.AsyncClient,'get',fail): assert not client.get('/api/models/status').json()['available']
def test_analysis_success_interface_and_failure():
    c=create(); upload(c)
    assessment={'relevance':4,'suitability':3,'observed_features':['test fixture only'],'reason':'Contract test; not real inference.','limitations':[],'suggested_use':'square'}
    async def good(*a): return assessment
    with patch.object(m,'assess',good):
        jid=client.post('/api/analyze',json={'collection_id':c,'brief':'test fixture brief'}).json()['id']
        j=client.get('/api/analysis/'+jid).json(); assert j['status']=='complete' and len(j['results'])==1
    async def bad(*a): raise httpx.ReadTimeout('timeout')
    with patch.object(m,'assess',bad):
        jid=client.post('/api/analyze',json={'collection_id':c,'brief':'a different brief'}).json()['id']
        j=client.get('/api/analysis/'+jid).json(); assert j['status']=='failed' and not j['results'] and j['errors']
def test_ollama_request_is_loopback_and_resized():
    c=create(); p=upload(c,pic((1600,1200))).json()[0]
    captured=[]
    async def send(self,url,**kw):
        captured.append((url,kw['json'])); return httpx.Response(200,request=httpx.Request('POST',url),json={'message':{'content':'{"relevance":3,"suitability":3,"observed_features":["fixture"],"reason":"fixture","limitations":[],"suggested_use":"square"}'}})
    with patch.object(httpx.AsyncClient,'post',send): asyncio.run(m.assess(m.photo(c,p['id'])['path'],'test brief','Custom','square'))
    import base64
    url,body=captured[0]; assert url=='http://127.0.0.1:11434/api/chat' and body['model']=='gemma3:4b'
    im=Image.open(io.BytesIO(base64.b64decode(body['messages'][0]['images'][0]))); assert max(im.size)<=896

def test_slight_brightness_duplicate():
    c=create(); a=upload(c).json()[0]; im=ImageEnhance.Brightness(Image.open(io.BytesIO(pic()))).enhance(1.05); b=io.BytesIO(); im.save(b,format='JPEG')
    other=upload(c,b.getvalue()).json()[0]; assert a['duplicate_group']==other['duplicate_group']
def test_blank_api_brief():
    assert client.post('/api/analyze',json={'collection_id':create(),'brief':'      '}).status_code==422

def test_public_domain_demo_has_decodable_photo_no_assessment():
    r=client.get('/api/demo/photo'); assert r.status_code==200
    im=Image.open(io.BytesIO(r.content)); assert im.size==(512,512)

def test_collection_quota_is_enforced_without_losing_existing_data():
    existing = len(m.collections)
    with patch.object(m, 'MAX_COLLECTIONS', existing):
        r = client.post('/api/collections')
    assert r.status_code == 429
    assert len(m.collections) == existing


def test_cancel_queued_analysis_skips_inference_and_keeps_source_photos():
    c = create()
    upload(c)
    jid = 'queued-test-cancel'
    m.jobs[jid] = {'id': jid, 'collection_id': c, 'status': 'queued',
                   'completed': 0, 'total': 1, 'results': [], 'errors': [],
                   'cancel_requested': False}
    response = client.post(f'/api/analysis/{jid}/cancel')
    assert response.status_code == 200 and response.json()['cancel_requested']
    async def must_not_run(*args):
        raise AssertionError('Canceled job must not invoke the model')
    with patch.object(m, 'assess', must_not_run):
        asyncio.run(m.run(jid, m.Analyze(collection_id=c, brief='test cancellation')))
    assert m.jobs[jid]['status'] == 'canceled'
    assert m.jobs[jid]['completed'] == 0
    assert len(m.collections[c]) == 1
    assert client.post('/api/analysis/not-a-job/cancel').status_code == 404


def test_export_rejects_duplicate_photo_ids():
    c = create()
    p = upload(c).json()[0]
    r = client.post('/api/export', json={'collection_id': c, 'photo_ids': [p['id'], p['id']]})
    assert r.status_code == 422


def test_phash_is_stable_and_can_compare_similar_images():
    sample = Image.open(io.BytesIO(pic()))
    a = m.perceptual_hash(sample)
    modified = ImageEnhance.Brightness(sample).enhance(1.06)
    b = m.perceptual_hash(modified)
    assert isinstance(a, int)
    assert 0 <= m.hash_distance(f'{a:016x}', f'{b:016x}') <= m.DUP_THRESHOLD


def test_diverse_shortlist_prefers_best_representative_regardless_of_upload_order():
    def candidate(name, score, group):
        return {'id': name, 'score': score, 'duplicate_group': group}
    scores = [candidate('weaker-first', 61, 'one'), candidate('different', 75, 'two'), candidate('stronger-second', 95, 'one')]
    ordered, suggested = m.finalize_rankings(scores, 2)
    assert suggested == ['stronger-second', 'different']
    assert ordered[0]['id'] == 'stronger-second'
    assert next(x for x in ordered if x['id'] == 'weaker-first')['score'] == 56


def test_results_keep_alternative_when_shortlist_exceeds_unique_groups():
    scores = [{'id':i, 'score':v, 'duplicate_group':g} for i,v,g in [('a',90,'one'), ('b',88,'one'), ('c',80,'two')]]
    ordered, suggested = m.finalize_rankings(scores, 3)
    assert len(ordered) == 3
    assert suggested == ['a', 'c', 'b']


def test_private_digest_not_exposed_to_browser():
    c = create(); p = upload(c).json()[0]
    assert 'digest' not in p and 'path' not in p and 'hash' not in p
    assert 'digest' not in client.get(f'/api/collections/{c}/photos').json()[0]


def test_response_disables_caching_and_sniffing():
    r = client.get('/api/health')
    assert r.headers.get('cache-control') == 'no-store'
    assert r.headers.get('x-content-type-options') == 'nosniff'


def test_job_history_is_bounded_and_pruned_before_next_analysis():
    c = create(); upload(c)
    with patch.object(m, 'MAX_JOBS', 8):
        snapshot = dict(m.jobs)
        try:
            m.jobs.clear()
            for i in range(8):
                m.jobs[f'finished-{i}'] = {'collection_id':c, 'status':'complete'}
            async def good(*args):
                return {'relevance':4, 'suitability':4, 'observed_features':['test fixture'], 'reason':'test fixture', 'limitations':[], 'suggested_use':'story'}
            with patch.object(m, 'assess', good):
                r = client.post('/api/analyze', json={'collection_id':c, 'brief':'test quota pruning'})
            assert r.status_code == 200
            assert len(m.jobs) <= 8
        finally:
            m.jobs.clear(); m.jobs.update(snapshot)
