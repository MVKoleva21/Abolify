import abolifyBot from '/public/abolify-bot.png'
import sofiaUni from '/public/sofia-university.png'
import colorElementTop from '/public/colory-thing-top.png'
import colorElementBot from '/public/colory-thing-bot.png'
import { useState } from 'react'
import { Input } from '@/components/ui/input'
import { Button } from '@/components/ui/button'
import { useNavigate } from 'react-router-dom'

export default function SignIn() {
    let [userName, setUserName] = useState<string>('')
    let [password, setPassword] = useState<string>('')

    const navigator = useNavigate();

    return (
        <>
            <div className="min-w-screen min-h-screen flex">
                <div className="w-1/2 min-h-full pt-36 pl-24 bg-radial-gradient-home before:content-[''] before:w-full before:h-full before:bg-[#FFFFFF40] before:absolute before:top-0 before:left-0 before:backdrop-blur-[128px]">
                    <img className='absolute top-4 left-4' src={abolifyBot} alt="" />
                    <div className='flex flex-col text-white z-2 relative gap-4 justify-center items-center font-black w-fit'>
                        <h1 className='text-4xl'>Learn & Discover</h1>
                        <h1 className='text-2xl'>about</h1>
                    </div>
                    <div className='flex flex-col relative z-20 justify-center items-end'>
                        <img src={sofiaUni} alt="" />
                    </div>
                    <div className='mt-16 flex font-bold relative z-20 text-white flex-col gap-8'>
                       <h1 className='text-2xl'>Welcome to Abolify!</h1> 
                       <p className='max-w-[70ch]'>
                            Our aim is to facilitate the orientation of a future student, after completing secondary education, towards a given specialty at the university where they intend to apply.  We will include information provided by the candidate student (their interests, grades, the specialty they want to apply for, and others), and such related to the university’s requirements (necessary grades, required state exams from 12th grade, and other data that are key to the application process).
                       </p>
                    </div>
                </div>

                <div className='w-1/2 bg-[#1E1E1E] overflow-x-hidden relative z-20 flex flex-col justify-start items-center'>
                    <img className='top-0 right-0 absolute select-none' draggable="false" src={colorElementTop} alt="" />
                    <img className='bottom-0 left-0 absolute translate-x-[-25%] select-none' draggable="false" src={colorElementBot} alt="" />

                    <div className='mt-[25%] flex flex-col justify-center items-center text-white gap-14'>
                        <h1 className='text-6xl'>Sign In</h1> 

                        <form className='flex flex-col gap-5 w-[380px]'>
                            <div className="relative after:content-[''] after:w-full after:absolute after:bg-[#333] after:h-[1px] after:bottom-0 after:left-0">
                                <Input className="p-6 text-xl border-none" onChange={(e) => setUserName(e.target.value)} placeholder='Username' />
                            </div>

                            <div className="relative after:content-[''] after:w-full after:absolute after:bg-[#333] after:h-[1px] after:bottom-0 after:left-0">
                                <Input className="p-6 text-xl border-none" type="password" onChange={(e) => setPassword(e.target.value)} placeholder='Password' />
                            </div>

                            <Button type="submit" className='mt-4 p-6 rounded-2xl text-xl bg-gradient-to-r from-[#6952F7] to-[#C11DA4]'>Sign Up</Button>          
                        </form>

                        <div className='flex justify-center items-center gap-14'>
                            <p className='text-[#888]'>Don't have an account?</p>
                            <Button onClick={() => navigator("/signup")} className='p-6 bg-[#333]'>Sign Up</Button>
                        </div>
                    </div>
                </div>
            </div>
        </>
    )
}
