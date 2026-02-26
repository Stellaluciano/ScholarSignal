import { useEffect, useState } from 'react'
import PaperCard from '../components/PaperCard'
import { apiGet } from '../lib/api'

export default function Today() {
  const [papers, setPapers] = useState<any[]>([])
  useEffect(() => {
    apiGet('/api/v1/digests/today').then(async (d) => {
      const ids = d?.arxiv_ids || []
      const full = await Promise.all(ids.map((id: string) => apiGet(`/api/v1/papers/${id}`)))
      setPapers(full)
    })
  }, [])
  return <main><h1>Today</h1>{papers.map((p, i) => <PaperCard key={p.arxiv_id} paper={p} rank={i + 1} />)}</main>
}
