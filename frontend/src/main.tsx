import {useEffect, useRef, useState} from 'react';
import {createRoot} from 'react-dom/client';
import {
  ArrowDown, ArrowLeft, ArrowRight, ArrowUp, Check, ChevronRight,
  Columns2, Download, FolderOpen, Grid2X2, Image as ImageIcon, Layers,
  LoaderCircle, Plus, Search, ShieldCheck, SlidersHorizontal, Sparkles,
  Trash2, Upload, X,
} from 'lucide-react';
import {validateFiles, move, toggle, validBrief} from './utils';
import './style.css';

type Photo = {
  id: string; width: number; height: number; duplicate_group: string;
  score?: number; reason?: string; observed_features?: string[];
  limitations?: string[]; crop_retained?: number; sharpness: number;
};
type Job = {
  status: string; completed: number; total: number; results: Photo[];
  suggested_ids?: string[]; errors: {error: string; photo_id?: string}[]; seconds?: number;
};
type View = 'studio' | 'shortlist' | 'compare' | 'privacy';
const modes = ['Business Promotion', 'Festival / Traditional', 'Professional', 'Mood / Atmosphere', 'Social Media', 'Custom'];
const examples = [
  'Warm, inviting photographs of our chocolate cake, with room for a discount message.',
  'Professional portrait candidates with simple backgrounds and balanced lighting.',
  'Cinematic travel photographs with warm light and minimal distractions.',
];
async function api(path: string, options?: RequestInit) {
  const response = await fetch('/api' + path, options);
  if (!response.ok) {
    let message = 'Request failed';
    try { const body = await response.json(); message = typeof body.detail === 'string' ? body.detail : JSON.stringify(body.detail); } catch { /* retain useful default */ }
    throw new Error(message);
  }
  return response.json();
}
const post = (body: unknown) => ({method: 'POST', headers: {'Content-Type': 'application/json'}, body: JSON.stringify(body)});

function App() {
  const [cid, setCid] = useState('');
  const [photos, setPhotos] = useState<Photo[]>([]);
  const [brief, setBrief] = useState('');
  const [mode, setMode] = useState('Business Promotion');
  const [format, setFormat] = useState('story');
  const [count, setCount] = useState(5);
  const [job, setJob] = useState<Job | null>(null);
  const [jid, setJid] = useState('');
  const [selected, setSelected] = useState<string[]>([]);
  const [error, setError] = useState('');
  const [busy, setBusy] = useState(false);
  const [model, setModel] = useState(false);
  const [tab, setTab] = useState<View>('studio');
  const [compare, setCompare] = useState<string[]>([]);
  const [filter, setFilter] = useState('all');
  const [query, setQuery] = useState('');
  const [sort, setSort] = useState('fit');
  const [dragging, setDragging] = useState(false);
  const [limits, setLimits] = useState({max_batch: 15, max_file_mb: 15});
  const input = useRef<HTMLInputElement>(null);
  const active = job?.status === 'running' || job?.status === 'queued';
  const disabled = busy || active;

  useEffect(() => {
    api('/models/status').then(x => setModel(x.available)).catch(() => {});
    api('/health').then(setLimits).catch(() => {});
  }, []);
  useEffect(() => {
    if (!jid) return;
    let stopped = false;
    const poll = async () => {
      try {
        const next = await api('/analysis/' + jid);
        if (stopped) return;
        setJob(next);
        if (['complete', 'partial', 'failed', 'canceled'].includes(next.status)) {
          setSelected(next.suggested_ids || []);
          setJid('');
        }
      } catch (e) {
        if (!stopped) { setError(String(e)); setJid(''); setJob(null); }
      }
    };
    poll();
    const timer = setInterval(poll, 1200);
    return () => { stopped = true; clearInterval(timer); };
  }, [jid]);

  const url = (id: string) => `/api/collections/${cid}/photos/${id}`;
  async function add(files: File[]) {
    if (disabled) return;
    const problem = validateFiles(files, photos.length, limits.max_batch, limits.max_file_mb);
    if (problem) { setError(problem); return; }
    if (!files.length) return;
    setBusy(true); setError('');
    try {
      let id = cid;
      if (!id) { id = (await api('/collections', {method: 'POST'})).id; setCid(id); }
      const body = new FormData();
      files.forEach(file => body.append('files', file));
      const incoming = await api(`/collections/${id}/photos`, {method: 'POST', body});
      setPhotos(previous => [...previous, ...incoming]);
      setJob(null); setSelected([]); setCompare([]); setFilter('all'); setTab('studio');
    } catch (e) { setError(String(e)); } finally { setBusy(false); }
  }
  async function loadDemo() {
    try {
      const response = await fetch('/api/demo/photo');
      if (!response.ok) throw new Error('Sample unavailable');
      const blob = await response.blob();
      await add([new File([blob], 'nasa-public-domain-sample.png', {type: 'image/png'})]);
    } catch (e) { setError(String(e)); }
  }
  async function remove(id: string) {
    setBusy(true);
    try {
      await api(`/collections/${cid}/photos/${id}`, {method: 'DELETE'});
      setPhotos(previous => previous.filter(photo => photo.id !== id));
      setJob(null); setSelected(previous => previous.filter(value => value !== id));
      setCompare(previous => previous.filter(value => value !== id));
    } catch (e) { setError(String(e)); } finally { setBusy(false); }
  }
  async function analyze() {
    if (!validBrief(brief)) { setError('Write a creative brief of at least five characters.'); return; }
    setBusy(true); setError('');
    try {
      const next = await api('/analyze', post({collection_id: cid, brief: brief.trim(), mode, format, count}));
      setJob({status: 'queued', completed: 0, total: photos.length, results: [], errors: []});
      setJid(next.id);
    } catch (e) { setError(String(e)); } finally { setBusy(false); }
  }
  async function cancelAnalysis() {
    if (!jid) return;
    try {
      await api('/analysis/' + jid + '/cancel', {method: 'POST'});
      setError('Cancellation requested. The current local model call may finish before the job stops.');
    } catch (e) { setError(String(e)); }
  }
  async function clear() {
    setBusy(true);
    try {
      if (cid) await api('/collections/' + cid, {method: 'DELETE'});
      setCid(''); setPhotos([]); setJob(null); setSelected([]); setCompare([]); setFilter('all'); setQuery('');
    } catch (e) { setError(String(e)); } finally { setBusy(false); }
  }
  async function download() {
    setBusy(true);
    try {
      const response = await fetch('/api/export', post({collection_id: cid, photo_ids: selected, format}));
      if (!response.ok) throw new Error('Export failed');
      const objectUrl = URL.createObjectURL(await response.blob());
      const anchor = document.createElement('a'); anchor.href = objectUrl; anchor.download = 'thooriga-shortlist.zip'; anchor.click();
      setTimeout(() => URL.revokeObjectURL(objectUrl), 1000);
    } catch (e) { setError(String(e)); } finally { setBusy(false); }
  }
  const assessed = job?.results || [];
  const ordered = assessed.length ? [...assessed, ...photos.filter(photo => !assessed.some(result => result.id === photo.id))] : photos;
  const similar = (photo: Photo) => photos.filter(other => other.duplicate_group === photo.duplicate_group).length > 1;
  const frameName = (id: string) => `Frame ${String(photos.findIndex(photo => photo.id === id) + 1).padStart(2, '0')}`;
  let display = tab === 'shortlist' ? selected.map(id => ordered.find(photo => photo.id === id)!).filter(Boolean) : [...ordered];
  if (tab === 'studio') {
    if (filter === 'assessed') display = display.filter(photo => photo.score !== undefined);
    if (filter === 'similar') display = display.filter(similar);
    if (sort === 'fit') display.sort((a, b) => (b.score ?? -1) - (a.score ?? -1));
    if (sort === 'upload') display.sort((a, b) => photos.findIndex(photo => photo.id === a.id) - photos.findIndex(photo => photo.id === b.id));
  }
  if (query.trim()) display = display.filter(photo => `${frameName(photo.id)} ${photo.reason || ''} ${photo.observed_features?.join(' ') || ''}`.toLowerCase().includes(query.trim().toLowerCase()));
  const ratio = ({story: '9 / 16', square: '1', portrait: '4 / 5', carousel: '1', profile: '1', original: 'auto'} as Record<string, string>)[format];
  const pageTitle = tab === 'privacy' ? 'Privacy & storage' : tab === 'shortlist' ? 'Shortlist' : tab === 'compare' ? 'Compare photographs' : 'Photo library';
  const navigate = (view: View) => { setTab(view); setQuery(''); };

  return <div className="app-shell">
    <aside className="sidebar">
      <a className="brand" href="#" onClick={() => navigate('studio')} aria-label="Thooriga home"><img src="/logo.png?v=paintbrush2" alt="Thooriga colorful paintbrush and shutter logo"/><span>thooriga<span className="brand-dot">.</span></span></a>
      <div className="workspace-switch"><span className="workspace-avatar"><img className="brand-symbol" src="/brand-icon.png?v=paintbrush2" alt="" aria-hidden="true" /></span><div><strong>Personal workspace</strong><small>Local session</small></div><ShieldCheck size={15}/></div>
      <div className="nav-label">WORKSPACE</div>
      <nav aria-label="Main navigation">
        <button className={tab === 'studio' ? 'current' : ''} onClick={() => {navigate('studio'); setFilter('all');}}><Grid2X2 size={18}/>Photo library<span className="nav-count">{photos.length}</span></button>
        <button className={tab === 'shortlist' ? 'current' : ''} onClick={() => navigate('shortlist')}><FolderOpen size={18}/>Shortlist<span className="nav-count">{selected.length}</span></button>
        <button className={tab === 'compare' ? 'current' : ''} onClick={() => navigate('compare')}><Columns2 size={18}/>Compare<span className="nav-count">{compare.length}/2</span></button>
      </nav>
      <div className="sidebar-collection"><div className="nav-label">CURRENT COLLECTION</div><div className="collection-entry"><span className="collection-dot"/>Untitled collection<span>{photos.length}</span></div><div className="capacity-label"><span>Batch capacity</span><span>{photos.length} / {limits.max_batch}</span></div><progress max={limits.max_batch} value={photos.length}/></div>
      <div className="sidebar-bottom"><div className="runtime-card"><span className="runtime-icon"><img className="brand-symbol" src="/brand-icon.png?v=paintbrush2" alt="" aria-hidden="true" /></span><div><strong>Gemma 3 · 4B</strong><small><i className={model ? 'status-dot online' : 'status-dot offline'}/>{model ? 'Ready locally' : 'Model unavailable'}</small></div></div><button className={tab === 'privacy' ? 'privacy-link current' : 'privacy-link'} onClick={() => navigate('privacy')}><ShieldCheck size={17}/>Privacy & storage<ChevronRight size={15}/></button><div className="profile-row"><span>T</span><div><strong>Local workspace</strong><small>No account required</small></div><span className="profile-status"/></div></div>
    </aside>

    <div className="workspace-shell">
      <header className="topbar"><div className="breadcrumb"><span>Workspace</span><ChevronRight size={13}/><strong>{pageTitle}</strong></div><div className="topbar-actions"><span className="local-indicator"><span className="status-dot online"/>Local session</span><button className="primary add-top" disabled={disabled} onClick={() => input.current?.click()}><Plus size={16}/>Add photos</button></div></header>
      <input ref={input} type="file" accept="image/jpeg,image/png,image/webp" multiple hidden onChange={event => {add(Array.from(event.target.files || [])); event.target.value = '';}}/>
      <main>
        <div className="page-heading"><div className="heading-icon">{tab === 'privacy' ? <ShieldCheck size={22}/> : tab === 'shortlist' ? <FolderOpen size={22}/> : tab === 'compare' ? <Columns2 size={22}/> : <ImageIcon size={22}/>}</div><div><h1>{pageTitle}</h1><p>{tab === 'privacy' ? 'Data flow, retention, and limitations' : `${photos.length} photographs · ${selected.length} selected`}</p></div><div className="heading-actions">{tab === 'studio' && photos.length > 0 && <button className="subtle" disabled={disabled} onClick={clear}><Trash2 size={14}/>Clear collection</button>}{selected.length > 0 && tab !== 'privacy' && <button className="primary" disabled={disabled} onClick={download}><Download size={15}/>Export {selected.length}</button>}</div></div>
        {error && <div className="alert" role="alert"><span>{error}</span><button aria-label="Dismiss error" onClick={() => setError('')}><X size={16}/></button></div>}
        {tab === 'privacy' ? <section className="privacy-page"><div className="privacy-card"><ShieldCheck size={24}/><h2>Local processing</h2><p>Photographs are processed by this browser, the local FastAPI backend, and Ollama on your computer. There are no cloud AI requests, analytics, facial identification, or automatic publication.</p><h3>Temporary storage</h3><p>Processing copies are saved in your system’s temporary directory. Clear the collection to delete them, or shut down the backend normally. Closing this browser alone does not delete files. A crash may leave temporary copies behind.</p><h3>Originals & exports</h3><p>Your source files remain unchanged. Exported JPEG copies omit metadata, including location fields. Original format preserves proportions, not the original file encoding. Transparent images are converted to RGB.</p><h3>Model & network</h3><p>Gemma runs at 127.0.0.1:11434 after installation. The adapter uses only loopback and disables inherited HTTP proxies. Actual offline model execution and a full network audit still need verification on your machine.</p><h3>Review limitations</h3><p>Crops are centered and do not detect subject placement. Mood is subjective. Review scores, observations, and every crop before exporting. The local API has no authentication and must not be exposed publicly.</p><button onClick={() => navigate('studio')}><ArrowLeft size={15}/>Back to photo library</button></div></section> : <div className={tab === 'studio' ? 'studio-layout' : 'review-layout'}>
          <section className="library-panel">
            <div className="library-toolbar"><div className="filter-tabs">{tab === 'studio' ? <><button className={filter === 'all' ? 'active' : ''} onClick={() => setFilter('all')}>All photos<span>{photos.length}</span></button><button className={filter === 'assessed' ? 'active' : ''} onClick={() => setFilter('assessed')}>Assessed<span>{assessed.length}</span></button><button className={filter === 'similar' ? 'active' : ''} onClick={() => setFilter('similar')}>Similar<span>{photos.filter(similar).length}</span></button></> : <span className="section-label">{tab === 'shortlist' ? 'SELECTED PHOTOGRAPHS' : 'SIDE-BY-SIDE REVIEW'}</span>}</div><span className="library-count">{display.length} items</span></div>
            {(photos.length > 0 && tab !== 'compare') && <div className="library-tools"><label className="search-box"><Search size={15}/><input aria-label="Search photographs" placeholder="Search frames or observations" value={query} onChange={event => setQuery(event.target.value)}/></label>{tab === 'studio' && <label className="sort-control"><SlidersHorizontal size={14}/><select aria-label="Sort photographs" value={sort} onChange={event => setSort(event.target.value)}><option value="upload">Upload order</option><option value="fit">Highest fit</option></select></label>}</div>}
            {active && <div className="progress-card" role="status"><LoaderCircle size={19} className="spin"/><div><strong>{job?.status === 'queued' ? 'Waiting for local model' : 'Assessing photographs'}</strong><p>{job?.completed} of {job?.total} complete · sequential local inference</p><progress max={job?.total} value={job?.completed}/></div><button className="subtle" onClick={cancelAnalysis} disabled={!jid} aria-label="Cancel analysis after current photo">Cancel</button></div>}
            {job && !active && <div className={'result-banner ' + (job.status === 'failed' ? 'failed' : '')}><img className="brand-symbol" src="/brand-icon.png?v=paintbrush2" alt="" aria-hidden="true" /><div><strong>{job.status === 'failed' ? 'The local model could not finish.' : `${job.results.length} photographs assessed`}</strong><p>{job.seconds}s elapsed · Fit scores are subjective estimates.</p>{job.errors.map((issue, index) => <p className="error-text" key={index}>{issue.error}</p>)}</div></div>}
            {tab === 'compare' ? <div className="compare-area">{compare.length < 2 ? <div className="simple-empty"><Columns2 size={32}/><h2>Select two photographs</h2><p>Use Compare on the photo cards to choose up to two frames.</p><button onClick={() => navigate('studio')}><ArrowLeft size={15}/>Photo library</button></div> : <><div className="compare-grid">{compare.map(id => <figure key={id}><img src={url(id)} alt={frameName(id) + ' comparison'}/><figcaption><strong>{frameName(id)}</strong><p>{ordered.find(photo => photo.id === id)?.reason || 'Not assessed. Original proportions shown.'}</p><button aria-pressed={selected.includes(id)} onClick={() => setSelected(previous => toggle(previous, id))}>{selected.includes(id) ? <Check size={14}/> : <Plus size={14}/>} {selected.includes(id) ? 'Selected' : 'Select photo'}</button></figcaption></figure>)}</div><button className="compare-close" onClick={() => navigate('studio')}><ArrowLeft size={15}/>Close comparison</button></>}</div> : !photos.length && tab === 'studio' ? <>
              <div className={'upload-stage ' + (dragging ? 'dragging' : '')} onDragOver={event => {event.preventDefault(); setDragging(true);}} onDragLeave={() => setDragging(false)} onDrop={event => {event.preventDefault(); setDragging(false); add(Array.from(event.dataTransfer.files));}}><div className="empty-aperture"><img className="brand-symbol" src="/brand-icon.png?v=paintbrush2" alt="" aria-hidden="true" /></div><div className="upload-heading"><h2>Add photographs</h2><p>Drag and drop files here, or browse your device.</p></div><button className="primary" disabled={disabled} onClick={() => input.current?.click()}>{busy ? <LoaderCircle size={16} className="spin"/> : <Upload size={16}/>}Choose photographs</button><span className="upload-limits">JPEG, PNG, WebP · {limits.max_file_mb} MB per file · up to {limits.max_batch} photos</span><div className="sample-divider"><span/>or<span/></div><button className="sample-button" disabled={disabled} onClick={loadDemo}><ImageIcon size={15}/>Try a public-domain sample<ArrowRight size={14}/></button><small>NASA photo · no precomputed assessments</small></div>
              <div className="empty-info"><div><span className="info-icon"><Layers size={16}/></span><div><strong>Duplicate grouping</strong><p>Similar frames remain available.</p></div></div><div><span className="info-icon"><ShieldCheck size={16}/></span><div><strong>Originals preserved</strong><p>Exports are separate JPEG copies.</p></div></div></div>
            </> : display.length === 0 ? <div className="simple-empty"><ImageIcon size={30}/><h2>{tab === 'shortlist' ? 'No selected photographs' : 'No matching photographs'}</h2><p>{tab === 'shortlist' ? 'Select photographs in your library to build this shortlist.' : 'Change the filter or search to view more frames.'}</p>{tab === 'shortlist' && <button onClick={() => navigate('studio')}>Photo library<ArrowRight size={15}/></button>}</div> : <div className="gallery">{display.map(photo => <article className={'photo-card ' + (selected.includes(photo.id) ? 'chosen' : '')} key={photo.id}>
              <div className="image-wrap" style={{aspectRatio: ratio === 'auto' ? '4 / 3' : ratio}}><img src={url(photo.id)} alt={frameName(photo.id)} loading="lazy"/><button className="select-photo" aria-label={selected.includes(photo.id) ? 'Deselect photo' : 'Select photo'} aria-pressed={selected.includes(photo.id)} onClick={() => setSelected(previous => toggle(previous, photo.id))}>{selected.includes(photo.id) ? <Check size={16}/> : <Plus size={16}/>}</button>{photo.score !== undefined && <span className="score">{Math.round(photo.score)} fit</span>}{tab === 'studio' && <button className="remove-photo" disabled={disabled} aria-label="Remove photo" onClick={() => remove(photo.id)}><Trash2 size={14}/></button>}</div>
              <div className="photo-info"><div className="photo-heading"><strong>{frameName(photo.id)}</strong><small>{photo.width} × {photo.height}</small></div><p>{photo.reason || 'Not assessed. Add a creative brief to evaluate this photograph.'}</p>{photo.observed_features && <div className="tags">{photo.observed_features.slice(0, 3).map(feature => <span key={feature}>{feature}</span>)}</div>}{similar(photo) && <small className="warning"><Layers size={11}/>Similar group · {photos.filter(other => other.duplicate_group === photo.duplicate_group).length} frames</small>}{photo.crop_retained !== undefined && photo.crop_retained < .8 && <small className="warning">Center crop keeps {Math.round(photo.crop_retained * 100)}% · review edges</small>}{photo.limitations?.map(limitation => <small className="warning" key={limitation}>{limitation}</small>)}
              <div className="card-actions">{tab === 'shortlist' ? <><button aria-label="Move photo up" disabled={selected.indexOf(photo.id) === 0} onClick={() => setSelected(previous => move(previous, previous.indexOf(photo.id), -1))}><ArrowUp size={14}/></button><button aria-label="Move photo down" disabled={selected.indexOf(photo.id) === selected.length - 1} onClick={() => setSelected(previous => move(previous, previous.indexOf(photo.id), 1))}><ArrowDown size={14}/></button><small>#{selected.indexOf(photo.id) + 1}</small></> : <button className={compare.includes(photo.id) ? 'comparing' : ''} aria-pressed={compare.includes(photo.id)} onClick={() => setCompare(previous => previous.includes(photo.id) ? previous.filter(id => id !== photo.id) : [...previous.slice(-1), photo.id])}><Columns2 size={13}/>{compare.includes(photo.id) ? 'Comparing' : 'Compare'}</button>}<a href={url(photo.id)} target="_blank" rel="noreferrer">Full frame ↗</a></div></div>
            </article>)}</div>}
            {photos.length > 0 && tab !== 'compare' && <div className="gallery-footer"><span>{format === 'original' ? 'Original proportions' : 'Center crop preview'} · subject-aware cropping unavailable</span>{compare.length === 2 && <button onClick={() => navigate('compare')}><Columns2 size={14}/>Compare two</button>}</div>}
          </section>
          {tab === 'studio' && <aside className="brief-panel"><div className="brief-title"><span className="brief-icon"><SlidersHorizontal size={18}/></span><h2>Creative brief</h2><span className="step-badge">01</span></div><div className="brief-body"><label htmlFor="brief">What are you looking for?</label><textarea id="brief" disabled={active} value={brief} maxLength={2000} onChange={event => setBrief(event.target.value)} placeholder="Describe the subject, atmosphere, intended use, and any space needed for text…"/><div className="brief-helper"><button disabled={active} onClick={() => setBrief(examples[(examples.indexOf(brief) + 1) % examples.length])}><Sparkles size={12}/>Use an example</button><span>{brief.length}/2000</span></div><div className="field-group"><label>Selection mode<select disabled={active} value={mode} onChange={event => setMode(event.target.value)}>{modes.map(value => <option key={value}>{value}</option>)}</select></label><label>Output format<select disabled={active} value={format} onChange={event => {setFormat(event.target.value); setJob(null);}}><option value="story">Instagram Story · 9:16</option><option value="square">Instagram Post · 1:1</option><option value="portrait">Portrait Post · 4:5</option><option value="carousel">Carousel · 1:1</option><option value="profile">Profile Picture · 1:1</option><option value="original">Original format</option></select></label><label>Shortlist size<select aria-label="Shortlist size" disabled={active} value={count} onChange={event => setCount(+event.target.value)}>{Array.from({length: 15}, (_, index) => index + 1).map(value => <option value={value} key={value}>{value} {value === 1 ? 'photograph' : 'photographs'}</option>)}</select></label></div><div className="crop-diagram"><div className="crop-frame"><div style={{aspectRatio: ratio === 'auto' ? '4 / 3' : ratio}}/></div><div><strong>{format === 'original' ? 'Original proportions' : format === 'story' ? '9:16 portrait' : format === 'portrait' ? '4:5 portrait' : '1:1 square'}</strong><small>{format === 'original' ? 'No crop applied' : 'Center crop · review subject edges'}</small></div></div><button className="primary analyze-button" disabled={!photos.length || disabled} onClick={analyze}>{active || busy ? <LoaderCircle size={17} className="spin"/> : <img className="brand-symbol" src="/brand-icon.png?v=paintbrush2" alt="" aria-hidden="true" />} {active ? 'Analyzing photographs' : 'Analyze collection'}<ArrowRight size={16}/></button><p className="brief-note">Custom instructions take priority over the mode preset.</p></div><div className="model-panel"><div><span className={model ? 'status-dot online' : 'status-dot offline'}/><strong>{model ? 'Gemma ready' : 'Gemma unavailable'}</strong><button disabled={busy} onClick={() => api('/models/status').then(next => setModel(next.available)).catch(e => setError(String(e)))}>Recheck</button></div><p>{model ? 'Vision inference runs locally.' : 'Start Ollama and install gemma3:4b.'}</p></div></aside>}
        </div>}
        <footer className="workspace-footer"><span><ShieldCheck size={12}/>Local processing · originals unchanged</span><button onClick={() => navigate('privacy')}>Privacy & storage<ArrowRight size={12}/></button></footer>
      </main>
    </div>
  </div>;
}

createRoot(document.getElementById('root')!).render(<App/>);
