import { useEffect, useState } from 'react'
import PaperCard from '../components/PaperCard'
import { apiGet } from '../lib/api'

export default function Explore(){
  const [papers,setPapers]=useState<any[]>([])
  useEffect(()=>{apiGet('/api/v1/papers?limit=20').then(setPapers)},[])
  return <main><h1>Explore</h1>{papers.map((p,i)=><PaperCard key={p.arxiv_id} paper={p} rank={i+1} />)}</main>
}
