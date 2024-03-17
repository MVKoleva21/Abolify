import { Button } from "@/components/ui/button";
import searchIcon from "/public/search-icon.png";
import { useState, useEffect } from "react";
import ChatEntry from "@/components/ChatEntry";
import { Textarea } from "@/components/ui/textarea";
import planeIcon from "/public/plane.png";
import abolifyBotBig from '/public/bg-bot-thingy.png';
import { ScrollArea } from "@/components/ui/scroll-area";
import { Avatar, AvatarFallback, AvatarImage } from "@/components/ui/avatar";
import axios from "axios";
import Cookie from "js-cookie";
import {Dialog, DialogContent, DialogHeader, DialogTitle, DialogTrigger} from "@/components/ui/dialog"; 
import { Input } from '@/components/ui/input';
import Cookies from 'js-cookie';

interface ChatEntryType {
    name: string;
}

export default function Chat() {
    const [theme, setTheme] = useState<'light' | 'dark'>('light'); // Default theme is light
    const [_, setThemeApplied] = useState<boolean>(false);

    useEffect(() => {
        const applyTheme = () => {
            document.body.className = theme === 'dark' ? 'dark' : ''; // Add 'dark' class to body for dark mode
        };

        applyTheme();
        setThemeApplied(true);
    }, [theme]);

    const handleThemeChange = () => {
        const newTheme = theme === 'light' ? 'dark' : 'light';
        setTheme(newTheme);
    };

    const [user, setUser] = useState<string>()
    const [chatHistory, setChatHistory] = useState<any>([])
    const [chat, setChat] = useState<any>(Cookies.get('chat'))
    const [chatMessages, setChatMessages] = useState<any>([])

    useEffect(() => {
        axios.get(`${import.meta.env.VITE_BACKEND_URL}/user`, {
            headers: {
                    'Authorization': `Bearer ${localStorage.getItem('token')}`
                }
            })
            .then((res) => {
                setUser(res.data)
            })
    }, [])

    useEffect(() => {
        if(chat == null)
            return

        axios.get(`${import.meta.env.VITE_BACKEND_URL}/chat/${chat}`, {
            headers: {
                    'Authorization': `Bearer ${localStorage.getItem('token')}`
            }}).then((res) => {
                Cookies.set('chat', chat)
                setChatMessages(res.data['messages'])
            })
    }, [chat])

    useEffect(() => {
        if(user === 'none')
            return

        axios.get(`${import.meta.env.VITE_BACKEND_URL}/user/chats`, {
            headers: {
                'Authorization': `Bearer ${localStorage.getItem('token')}`
            }
        }).then(async res => {
            setChatHistory(res.data.reverse())
        })}, [user])

    const [newChatName, setNewChatName] = useState<string>('')
    let handelNewChat = () => {
        let data = {
            alias: newChatName
        }

        axios.post(`${import.meta.env.VITE_BACKEND_URL}/chat`, data, {
            headers: {
                'Authorization': `Bearer ${localStorage.getItem('token')}`
            }
        })
        .then((res) => {
            Cookies.set('chat', res.data['id'])
            window.location.reload()
        })
    }

    let [message, setMessage] = useState<string>('')
    const handelNewMessage = (e: any) => {
        e.preventDefault()

        let data = {
            content: message,
            chat_id: chat
        }

        axios.post(`${import.meta.env.VITE_BACKEND_URL}/message`, data, {
            headers: {
                'Authorization': `Bearer ${localStorage.getItem('token')}`
            }
        })
        .then(() => {
            window.location.reload()
        })
    }

    return (
        <>
            <div className={`min-w-screen overflow-hidden h-screen ${theme === 'dark' ? 'bg-gradient-to-b from-[#1E1E1E] to-[#6618E7]' : 'bg-gradient-to-b from-[#FAD987] to-[#EA3FC5]'} flex`}>
                <div className={`w-1/5 ${theme === 'dark' ? 'bg-white text-black' : 'bg-black text-white'} min-h-[80%] items-center flex flex-col my-5 ml-5 rounded-2xl`}>
                        <div className="w-[90%] h-full mt-12 flex flex-col items-center">
                            <div className="flex gap-4 items-center border border-pink-50 w-full p-2 px- 4 rounded-[36px]">
                                <Avatar>
                                    <AvatarImage src="" />
                                    <AvatarFallback>IS</AvatarFallback>
                                </Avatar>
                                <h1>{user}</h1>
                            </div>
    
                            <div className="container-switch">
                                <span>Change Theme </span>
                                    <label className="switch">
                                        <input type="checkbox" onChange={handleThemeChange} checked={theme === 'dark'} />
                                        <span className="slider"></span>
                                    </label>
                            </div>

                            <div className="flex items-center w-full gap-2 mt-[36px]">
                                <Dialog>
                                    <DialogTrigger asChild>
                                        <Button className={`${theme === 'dark' ? 'bg-gradient-to-r from-[#1E1E1F] to-[#6218DC] text-white' : 'bg-gradient-to-r from-[#FAD987] to-[#EA3FC5] text-black'} p-6 w-full rounded-[36px]'} font-black`}>+ New chat</Button>
                                    </DialogTrigger >
                                    <DialogContent className="sm:max-w-[425px] bg-black text-white">
                                        <DialogHeader>
                                            <DialogTitle>New Chat</DialogTitle>
                                        </DialogHeader>
                                        <div>
                                            <Input placeholder="Enter chat name" className="p-6" onChange={(e) => setNewChatName(e.target.value)}/>
                                        </div>
                                        <Button onClick={handelNewChat}>New Chat</Button>
                                    </DialogContent >
                                </Dialog>

                                <Button size="icon" className="rounded-full h-full w-[64px]"><img src={searchIcon} alt="" /></Button>
                            </div>
                            <div className="flex gap-8 items-center my-[24px] py-[20px] relative before:content-[''] before:absolute before:top-0 before:left-0 before:w-full before:h-[1px] before:bg-zinc-600 after:content-[''] after:absolute after:bottom-0 after:left-0 after:w-full after:h-[1px] after:bg-zinc-600">
                                <p>You conversations</p>
                                <Button variant="link" className={`${theme === 'dark' ? 'text-purple-500' : 'text-pink-500'}`}>Clear All</Button>
                            </div>
                            <ScrollArea className="h-full flex flex-col overflow-auto">
                                {
                                    chatHistory.map((chat: any) => {
                                        return <ChatEntry onclick={() => setChat(chat[0])} chatTitle={chat[2]} />
                                    })
                                }
                            </ScrollArea>
                        </div>
                    </div>
                    <div className="w-4/5 min-h-[80%] items-center flex flex-col m-5 relative rounded-2xl text-white">
                    <div className={`${theme === 'dark' ? 'text-white' : 'text-black'} w-full h-5/6 flex flex-col p-4 ml-[300px] gap-2`}>
                        <img className="absolute top-[50%] left-[50%] translate-x-[-50%] translate-y-[-50%] mix-blend-overlay select-none" draggable="false" src={abolifyBotBig} alt="" />
                    
                            <ScrollArea className="gap-2 flex flex-col font-bold bg-black p-8 rounded-3xl w-[70%]">
                                {

                                    chatMessages.map((message: any, index: any) => {
                                        if(index % 2 == 0)
                                            return <div className="w-[70%] h-[12%] rounded-xl flex gap-5 p-3 items-center">
                                                <p className="text-white break-words">{message[2]}</p>
                                            </div>
                                        else
                                            return <div className="w-[70%] h-[12%] rounded-xl flex gap-5 p-3 items-center">
                                                <p className="text-white ml-10 mt-[-10px] break-words">{message[2]}</p>
                                            </div>
                                    })
                                }
                            </ScrollArea>
                    
                    </div>

                    <form onSubmit={handelNewMessage} className={`${theme === 'dark' ? 'bg-white text-black' : 'bg-black text-white' } w-[70%] h-[12%] rounded-[36px] flex gap-5 p-6 items-center`}>
                        <Textarea onChange={(e) => setMessage(e.target.value)} className="resize-none border-none" /> 
                        <Button size="icon" className={`${theme === 'dark' ? ' bg-[#5661F6] hover:bg-[#5331F3]' : ' bg-[#EA3FC5] hover:bg-[#d34db6]'} rounded-full w-14 h-14`}><img src={planeIcon} alt="" /></Button>
                    </form>
                </div>
            </div>
        </>
    );
}
