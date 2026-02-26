import { signIn, signOut, useSession } from 'next-auth/react'

export default function Settings(){
  const { data } = useSession()
  return <main><h1>Settings</h1>
    <button onClick={()=>signIn('github')}>Sign in GitHub</button>
    <button onClick={()=>signIn('google')}>Sign in Google</button>
    {data && <button onClick={()=>signOut()}>Sign out</button>}
  </main>
}
