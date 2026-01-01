import type { ReadyStateEvent, SSEvent } from "sse.js";
import { SSE } from "sse.js";
import * as z from "zod";
import { api } from "@/lib/client";
import { settings } from "@/lib/settings";
import type { components } from "@/types/schema";

type GenerateNewChatRequest = components["schemas"]["GenerateNewChatRequest"];
type GenerateExistingChatRequest =
  components["schemas"]["GenerateExistingChatRequest"];

type MutationFnProps = {
  request: GenerateExistingChatRequest | GenerateNewChatRequest;
  onDelta: (delta: string) => unknown;
  signal: AbortSignal;
};

// TODO this is not type-safe yet until we figure out OAI 3.2 generation
const DeltaEvent = z.object({
  type_: z.literal("delta"),
  v: z.string(),
});

export const generateMessageMutationFn = async ({
  request,
  onDelta,
  signal,
}: MutationFnProps) => {
  const [method, url, body] = api.queryOptions("post", "/v1/generate/message", {
    body: request,
  }).queryKey;

  return new Promise<void>((resolve, reject) => {
    const es = new SSE(`${settings.api_base_url}${url}`, {
      method,
      payload: JSON.stringify(body.body),
      withCredentials: true,
      headers: {
        "Content-Type": "application/json",
        Accept: "text/event-stream",
      },
    });

    const cleanup = () => {
      es.removeEventListener("message", handleMessage);
      es.removeEventListener("error", handleError);
      es.removeEventListener("readystatechange", handleReadyState);
      signal.removeEventListener("abort", handleAbort);
      es.close();
    };

    const handleMessage = (e: SSEvent) => {
      const data = DeltaEvent.parse(JSON.parse(e.data));
      onDelta(data.v);
    };

    const handleReadyState = (event: ReadyStateEvent) => {
      // https://github.com/mpetazzoni/sse.js?files=1#event-stream-order
      if (event.readyState === SSE.CLOSED) {
        cleanup();
        resolve();
      }
    };

    const handleError = (error: { responseCode: number; data: string }) => {
      cleanup();
      reject(error.data);
    };

    const handleAbort = () => {
      cleanup();
      reject();
    };

    // This stops the double requests during development
    if (signal.aborted) {
      handleAbort();
      return;
    }

    signal.addEventListener("abort", handleAbort);

    es.addEventListener("message", handleMessage);
    es.addEventListener("error", handleError);
    es.addEventListener("readystatechange", handleReadyState);
  });
};
