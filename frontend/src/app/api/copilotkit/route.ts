import {
    CopilotRuntime,
    ExperimentalEmptyAdapter,
    copilotRuntimeNextJSAppRouterEndpoint,
    langGraphPlatformEndpoint
} from "@copilotkit/runtime";;
import { NextRequest } from "next/server";

// You can use any service adapter here for multi-agent support.
const serviceAdapter = new ExperimentalEmptyAdapter();
const AGENT_HOST = process.env.AGENT_HOST;
const AGENT_PORT = process.env.AGENT_PORT;
const runtime = new CopilotRuntime({
    remoteEndpoints: [
        { url: `http://${AGENT_HOST}:${AGENT_PORT}/copilotkit` },
        // added in next step...
    ],
});

export const POST = async (req: NextRequest) => {
    const { handleRequest } = copilotRuntimeNextJSAppRouterEndpoint({
        runtime,
        serviceAdapter,
        endpoint: "/api/copilotkit",
    });

    return handleRequest(req);
};