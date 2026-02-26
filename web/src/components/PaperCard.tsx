import Link from 'next/link'
import { apiPost } from '../lib/api'

export default function PaperCard({ paper, rank }: { paper: any, rank: number }) {
  return <div style={{border:'1px solid #ccc',padding:12,marginBottom:8}}>
    <h3>{paper.title}</h3>
    <p>{(paper.authors || []).join(', ')}</p>
    <p>{paper.abstract?.slice(0, 200)}...</p>
    <button onClick={() => apiPost('/api/v1/events', { arxiv_id: paper.arxiv_id, event_type: 'click_abs', source: 'daily_digest', rank_position: rank })}>Abstract</button>{' '}
    <a href={paper.pdf_url} target="_blank" rel="noreferrer" onClick={() => apiPost('/api/v1/events', { arxiv_id: paper.arxiv_id, event_type: 'click_pdf', source: 'daily_digest', rank_position: rank })}>PDF</a>{' '}
    <button onClick={() => apiPost('/api/v1/events', { arxiv_id: paper.arxiv_id, event_type: 'save', source: 'daily_digest', rank_position: rank })}>Save</button>{' '}
    <button onClick={() => apiPost('/api/v1/events', { arxiv_id: paper.arxiv_id, event_type: 'dislike', source: 'daily_digest', rank_position: rank })}>Dislike</button>{' '}
    <Link href={`/paper/${paper.arxiv_id}`}>Details</Link>
  </div>
}
