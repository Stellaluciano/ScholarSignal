import { useRouter } from 'next/router'
import { useEffect, useRef, useState } from 'react'
import { apiGet, apiPost } from '../../lib/api'

export default function PaperDetail(){
  const router = useRouter(); const { arxiv_id } = router.query
  const [paper, setPaper] = useState<any>(null)
  const start = useRef(Date.now())
  useEffect(()=>{ if(arxiv_id) apiGet(`/api/v1/papers/${arxiv_id}`).then(setPaper) },[arxiv_id])
  useEffect(()=>{ const fn=()=>{ if(arxiv_id) apiPost('/api/v1/events',{arxiv_id,event_type:'dwell',source:'paper_detail',dwell_ms:Date.now()-start.current})}; window.addEventListener('pagehide', fn); return ()=>window.removeEventListener('pagehide', fn)},[arxiv_id])
  if(!paper) return <div>Loading...</div>
  return <main><h1>{paper.title}</h1><p>{paper.abstract}</p><a href={paper.pdf_url} target='_blank' rel='noreferrer'>Open PDF</a></main>
}
