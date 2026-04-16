
import { useState } from 'react'
export default function App(){
  const [msgs,setMsgs]=useState([])
  const [txt,setTxt]=useState('')
  return (
    <div style={{padding:20}}>
      <h2>ChatApp</h2>
      {msgs.map((m,i)=><div key={i}>{m}</div>)}
      <input value={txt} onChange={e=>setTxt(e.target.value)} />
      <button onClick={()=>{setMsgs([...msgs,txt]);setTxt('')}}>Senden</button>
    </div>
  )
}
