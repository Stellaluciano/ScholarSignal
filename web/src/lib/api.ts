export const apiBase = process.env.NEXT_PUBLIC_API_BASE_URL || 'http://localhost:8000'

export async function apiGet(path: string) {
  const res = await fetch(`${apiBase}${path}`, { credentials: 'include' })
  return res.json()
}

export async function apiPost(path: string, body: unknown) {
  const res = await fetch(`${apiBase}${path}`, {
    method: 'POST',
    credentials: 'include',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(body)
  })
  return res.json()
}
