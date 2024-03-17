import chatIcon from "/public/message-icon.png"

export default function ChatEntry ({ chatTitle, onclick }: any) {
    return (
        <>
            <div onClick={onclick} className="flex items-center gap-4 p-4 hover:bg-[#999] cursor-pointer rounded-xl">
                <img src={chatIcon} alt="" />
                <h2>{chatTitle}</h2>
            </div>
        </>
    )
}
