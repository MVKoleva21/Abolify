import { Button } from "@/components/ui/button"
import searchIcon from "/public/search-icon.png"
import { useState } from "react"
import ChatEntry from "@/components/ChatEntry"
import { Textarea } from "@/components/ui/textarea"
import planeIcon from "/public/plane.png"
import abolifyBotBig from '/public/bg-bot-thingy.png'
import { ScrollArea } from "@/components/ui/scroll-area"
import { Avatar, AvatarFallback, AvatarImage } from "@/components/ui/avatar"

interface ChatEntryType {
    name: String
}

export default function Chat() {
    let [isChatEmpty, setIsChatEmpty] = useState<bool>(true)

    let [chats, setChats] = useState<ChatEntryType[]>([
        {
            "name": "Create a react site using..."
        },
        {
            "name": "Fix this code.."
        },
        {
            "name": "What is UI UX design?"
        }
    ])

    return (
        <>
            <div className="min-w-screen h-screen bg-gradient-to-b from-[#1E1E1E] to-[#6618E7] flex">
                <div className="w-1/5 bg-white min-h-[80%] items-center flex flex-col my-5 ml-5 rounded-2xl">
                    <div className="w-[90%] h-full mt-12 flex flex-col items-center">

                        <div className="flex gap-4 items-center border border-pink-50 w-full p-2 px-4 rounded-[36px]">
                            <Avatar>
                                <AvatarImage src="" /> 
                                <AvatarFallback>IS</AvatarFallback>
                            </Avatar>

                            <h1>Ivan Stoychev</h1>
                        </div> 

                        <div className="flex items-center w-full gap-2 mt-[36px]">
                            <Button className="p-6 w-full rounded-[36px] bg-gradient-to-r from-[#1E1E1F] to-[#6218DC]">+ New chat</Button>
                            <Button size="icon" className="rounded-full h-full w-[64px]"><img src={searchIcon} alt="" /></Button>
                        </div>

                        <div className="flex gap-8 items-center my-[24px] py-[20px] relative before:content-[''] before:absolute before:top-0 before:left-0 before:w-full before:h-[1px] before:bg-purple-800 after:content-[''] after:absolute after:bottom-0 after:left-0 after:w-full after:h-[1px] after:bg-purple-800">
                            <p>You conversations</p>
                            <Button variant="link" className="text-purple-800 font-bold">Clear All</Button>
                        </div>

                        <ScrollArea className="h-full flex flex-col overflow-auto">
                            {
                                chats.map((entry) => {
                                    return <ChatEntry chatTitle={entry.name} />                     
                                })
                            }
                        </ScrollArea>
                    </div>
                </div>


                <div className="w-4/5 min-h-[80%] items-center flex flex-col m-5 relative rounded-2xl text-white">
                    <div className="w-full h-5/6 flex flex-col p-4 ml-[300px]">
                        {isChatEmpty && <div className="absolute top-[30%] text-center  text-4xl font-bold left-[50%] translate-x-[-50%] translate-y-[-50%]">
                            <h1>Good day! How may I assist you today?</h1>
                        </div>}
                        <img className="absolute top-[50%] left-[50%] translate-x-[-50%] translate-y-[-50%] mix-blend-overlay select-none" draggable="false" src={abolifyBotBig} alt="" />
                    </div>

                    <form className="w-[70%] h-[12%] text-black rounded-[36px] flex gap-5 p-6 bg-white items-center">
                        <Textarea className="resize-none" /> 
                        <Button size="icon" className="rounded-full w-14 h-14 bg-[#5661F6] hover:bg-[#5331F3]"><img src={planeIcon} alt="" /></Button>
                    </form>

                </div>

            </div>
        </>
    )
}
