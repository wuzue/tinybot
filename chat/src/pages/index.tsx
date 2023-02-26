import Head from 'next/head'
import Image from 'next/image'
import { Inter } from '@next/font/google'
import styles from '@/styles/Home.module.css'
import { useEffect, useState, useRef, MutableRefObject } from 'react'
import ScrollToBottom from "react-scroll-to-bottom";
import { request } from 'http'

const inter = Inter({ subsets: ['latin'] })

export default function Home() {

  const [messages, setMessages] = useState<any>([])
  const messagesEndRef = useRef() as MutableRefObject<HTMLDivElement>
  const [typing, setTyping] = useState(false)
  const inputElementRef = useRef() as MutableRefObject<HTMLTextAreaElement>
  const [botResponse, setBotResponse] = useState('');
  const [isGeneratingBotResponse, setIsGeneratingBotResponse] = useState(false);

  // THIS IS THE FUNCTION PRIOR TO USING FLASK
  // async function generateBotResponse(message: string){
  //   setIsGeneratingBotResponse(true);
  //   const endPointUrl = "http://localhost:5072/weather";
  //   const locationMatch = message.match(/temperature in (.+)/i);
  //   if(locationMatch && locationMatch[1]){
  //     const location = locationMatch[1];
  //     const apiUrl = `${endPointUrl}?message=${location}`;
  //     try{
  //       const response = await fetch(apiUrl);
  //       const data = await response.text();
  //       setBotResponse(data);
  //     }catch(error){
  //       console.log(`Error calling weather api, ${error}`);
  //       setBotResponse(`I am sorry, there was an error retrieving that information for you.`);
  //     }
  //   } else {
  //     setBotResponse(`I am sorry, I don't know what you mean by ${message}`);
  //   }
  //   setIsGeneratingBotResponse(false);
  // }

  async function generateBotResponse(message: string){
    setIsGeneratingBotResponse(true);
    const endPointUrl = "http://127.0.0.1:5072/api/messages";
    const requestOptions = {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ "message": message })
    };
    try {
      const response = await fetch(endPointUrl, requestOptions);
      console.log('sent post request to C# server');
      const data = await response.text();
      const styledResponse = data
      setBotResponse(styledResponse)
      // setBotResponse(`Processed message:\n${data}`);
    } catch (error) {
      console.log(`Error calling API, ${error}`);
      setBotResponse(`I am sorry, there was an error retrieving that information for you.`);
    }
    setIsGeneratingBotResponse(false);
  } 

  //handles the message exchange system, checks whose turn it is...
  const handleMessages = async () => {
  const inputElement = (document.getElementById('message-input') as HTMLInputElement | HTMLTextAreaElement)
  const messageText = inputElement.value.trim()
  if(messageText){
    const newMessage = { text: messageText, from: 'user'}
    setMessages((prevMessages: any[]) => [...prevMessages, newMessage])
    inputElement.value = ''
    await generateBotResponse(messageText);
  }
  inputElement.focus()
}

  //update messages with new bot response when botResponse state changes
  useEffect(() => {
  if (botResponse) {
    const newBotMessage = { text: botResponse, from: 'bot'}
    setMessages((prevMessages:any[]) => [...prevMessages, newBotMessage])
  }
  }, [botResponse])

  //set focus on the textarea by default - when starting the app.
  useEffect(() => {
    inputElementRef.current.focus()
  }, [])
    
  //scroll view as text scrolls down
  useEffect(() => {
    messagesEndRef.current.scrollIntoView({ behavior: 'smooth' })
  }, [messages])

  return (
    <>
      <Head>
        <title>Gepeteco</title>
        <meta name="description" content="Generated by create next app" />
        <meta name="viewport" content="width=device-width, initial-scale=1" />
        <link rel="icon" href="/favicon.ico" />
      </Head>
      <main className='bg-[#343541]'>
        <div className="flex flex-col h-screen w-[50%] m-auto">
            <div className="flex-grow bg-[#343541]" id='screen' style={{overflowY: 'scroll'}}>
              {messages.map((message:any, index: number) => (
                <div key={index} className={`flex ${message.from === 'user' ? 'justify-end bg-[#343541]' : 'justify-start bg-[#444654]'}`}>
                  <span className='flex h-[3rem] inline-block w-auto p-2 rounded-full text-[ghostwhite] m-2'>
                    {message.text}
                  </span>
                </div>
              ))}
              <div ref={messagesEndRef}/>
            </div>
          <div className="p-4 flex bg-[#444654] rounded-[5px] mt-[1rem]">
          <textarea onKeyDown={(e) => { if(e.key === 'Enter'){ e.preventDefault(); handleMessages()}}} ref={inputElementRef} id='message-input' className="text-[ghostwhite] w-full h-16 border border-gray-300 bg-[#444654] rounded-md resize-none p-2" placeholder="Type your message"></textarea>
          <button className="bg-blue-500 text-white px-4 py-2 rounded-md ml-2 shadow-[0px_8px_24px_rgb(0,0,0,12%)]" onClick={handleMessages}>Send</button>
        </div>
        </div>
      </main>
    </>
  )
}