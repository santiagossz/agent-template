import { CopilotChat } from "@copilotkit/react-ui";

export function Chat() {
    return (
        <CopilotChat
            className="h-screen p-20"
            instructions={"You are assisting the user as best as you can. Answer in the best way possible given the data you have."}
            labels={{
                title: "Your Assistant",
                initial: "Hi! 👋 How can I assist you today?",
            }}
        />
    );
}