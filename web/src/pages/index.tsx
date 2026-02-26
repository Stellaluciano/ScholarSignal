import { useEffect } from 'react'
import { useRouter } from 'next/router'
export default function Home(){ const r = useRouter(); useEffect(()=>{r.replace('/today')},[r]); return null }
