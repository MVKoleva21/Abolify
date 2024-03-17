import abolifyBot from '/public/abolify-bot.png'
import abolifyFull from '/public/abolify-full.png'
import abolify from '/public/abolify.png'
import circles from '/public/circles.png'
import nameLine from '/public/name-line.png'
import squiglyLine from '/public/not-straith-line.png'
import { Button } from '@/components/ui/button'
import { useNavigate } from 'react-router-dom'

export default function Home() {
    const navigator = useNavigate();

    return (
        <>
            <div className="min-w-screen min-h-screen relative flex flex-col bg-radial-gradient-home before:content-[''] before:w-full before:h-full before:bg-[#FFFFFF40] before:absolute before:top-0 before:left-0 before:backdrop-blur-[128px]">
                <img className='fixed left-[-80px] bottom-[-80px]' draggable={false} src={circles} alt="" />
                <img className='absolute right-4 top-4' draggable={false} src={abolifyBot} alt="" />

                <div className='mt-[190px] ml-[220px] z-20 max-lg:ml-4'>
                    <div className='relative'>
                        <img className='absolute top-[-50px] left-[-20px]' src={nameLine} alt="" />
                        <img className='relative top-0 left-14' src={abolify} alt="" />
                        <img className='absolute top-0 left-0' src={abolifyFull} alt="" />
                    </div>
                </div>

                <div className='ml-[240px] mt-[40px] max-w-[90ch] max-lg:ml-4 font-bold relative z-20 text-white justify-center items-center'>
                    <p>Welcome to Abilify AI, your ultimate guide to navigating the path  from secondary education to university specialization. 
Our mission is to  simplify the journey for prospective students by providing tailored  guidance towards their desired field of study.
By making hard to search in outdated site of the most popular university in Bulgaria into easy accessible chatbot - the Abolify AI , we streamline the application process and make accessing files easier, ensuring a  smoother transition into higher education. 
Let us help you unlock your  potential and embark on your academic journey with ease and confidence.</p>

                    <div className='flex flex-col gap-10 mt-[80px] justify-center items-center'>
                        <Button onClick={() => navigator('/signup')} className='z-20 hover:bg-gradient-to-r from-[#FFAE63] via-[#FC76C6] to-[#7367FF] px-8 py-6 bg-[#ffffff00] border-2 border-white'>Create Account/ Sign in</Button>
                        <img className='relative top-[-30px]' src={squiglyLine} alt="" />
                    </div>
                </div>

            </div>
        </>
    )
}
