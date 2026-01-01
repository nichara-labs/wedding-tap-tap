import { useMutation, useQueryClient } from "@tanstack/react-query";
import { useCallback, useEffect, useRef, useState } from "react";
import { toast } from "sonner";
import * as z from "zod";
import { Shimmer } from "@/components/ai-elements/shimmer";
import { api } from "@/lib/client";
import type { components } from "@/types/schema";
import { ChatMessageBubble } from "./ChatMessageBubble";
import { Composer } from "./Composer";
import { generateMessageMutationFn } from "./generateMessageMutationFn";
import { ScrollUntilElement } from "./ScrollUntilElement";
import { useGenerateChatTitle } from "./useGenerateChatTitle";

interface Props {
  chat: components["schemas"]["ChatModel"];
  messages: components["schemas"]["MessageModel"][];
}

const ErrorDetail = z.object({
  status_code: z.number(),
  detail: z.string(),
}) satisfies z.ZodType<components["schemas"]["ErrorDetail"]>;

export const Messages = ({ chat, messages }: Props) => {
  const scrollBottomRef = useRef<HTMLDivElement>(null);
  const messageAbortRef = useRef<AbortController>(null);
  const [composeText, setComposeText] = useState<string>("");
  const [userPrompt, setUserPrompt] = useState<string>();
  const [llmResponse, setLlmResponse] = useState<string[]>([]);
  const client = useQueryClient();

  const { mutate: generateTitle } = useGenerateChatTitle(chat.id);
  const { mutate: generateMessage, isPending: isGeneratingMessage } =
    useMutation({
      mutationFn: generateMessageMutationFn,
      /* Making this async causes the dispatch operation not to be called until refetching is complete. Without it, isGeneratingMessage is set to false BEFORE the new messages are fetched, causing a premature re-render where the messages[] does not have the new messages, but the assistant message is removed, causing a loss of scroll position.
      https://github.com/TanStack/query/blob/a5fca0e541c0782a8b19754e2f3d7d08fcc737cd/packages/query-core/src/mutation.ts#L244
      */
      onSuccess: async () => {
        client.invalidateQueries({
          queryKey: api.queryOptions("get", "/v1/lorestones").queryKey,
        });

        await client.invalidateQueries({
          queryKey: api.queryOptions("get", "/v1/chats/{chat_id}/messages", {
            params: { path: { chat_id: chat.id } },
          }).queryKey,
        });

        /* We don't want these hooks to run BEFORE the new messages are fetched (otherwise scroll position will be lost in the brief instant they are empty), so we await invalidateQueries. */
        setLlmResponse([]);
        setUserPrompt(undefined);
      },
      onError: (err: string) => {
        try {
          const parsed = ErrorDetail.parse(JSON.parse(err));
          toast.error(parsed.detail);
        } catch {
          toast.error("Failed to generate message");
        }
        setComposeText(userPrompt || "");
        setLlmResponse([]);
        setUserPrompt(undefined);
      },
    });

  const onDelta = useCallback(
    (delta: string) => setLlmResponse((v) => [...v, delta]),
    [],
  );

  // Generate a chat title if there are messages
  useEffect(() => {
    if (messages.length !== 0 && !chat.title) {
      generateTitle({ params: { query: { chat_id: chat.id } } });
    }
  }, [chat, generateTitle, messages]);

  // Generate the first message if there are none
  useEffect(() => {
    if (messages.length) return;
    messageAbortRef.current = new AbortController();
    generateMessage({
      request: { type_: "new", chat_id: chat.id },
      onDelta,
      signal: messageAbortRef.current.signal,
    });
    return () => void messageAbortRef.current?.abort();
  }, [messages, chat, generateMessage, onDelta]);

  // Clear state and abort when unmounting
  useEffect(
    () => () => {
      messageAbortRef.current?.abort();
      setLlmResponse([]);
      setUserPrompt(undefined);
    },
    [],
  );

  const onSubmit = (content: string) => {
    const parentMessageId = messages.at(-1)?.id;
    if (!parentMessageId) {
      toast.error("Invalid parent message");
      return;
    }

    // Clear existing generations (if any)
    messageAbortRef.current?.abort();

    messageAbortRef.current = new AbortController();
    setUserPrompt(content);
    generateMessage({
      request: {
        type_: "existing",
        chat_id: chat.id,
        content,
        parent_message_id: parentMessageId,
      },
      onDelta,
      signal: messageAbortRef.current.signal,
    });
  };

  const handleAbort = () => {
    messageAbortRef.current?.abort();
    setLlmResponse([]);
    setComposeText(userPrompt || "");
    setUserPrompt(undefined);
  };

  const llmResponseJoined = llmResponse.join("");

  return (
    <div className="flex flex-col max-w-3xl mx-auto w-full min-h-[calc(100dvh-var(--header-height))]">
      {messages.map((m) => (
        <ChatMessageBubble
          key={m.id}
          messageRole={m.role}
          content={m.content}
        />
      ))}
      {userPrompt && (
        <ChatMessageBubble messageRole={"user"} content={userPrompt} />
      )}
      {isGeneratingMessage && (
        <div
          className="min-h-[calc(100dvh-var(--header-height))] scroll-m-[calc(var(--header-height)+6rem)]"
          ref={(el) => {
            if (!el) return;
            el.scrollIntoView();
          }}
        >
          {llmResponse.length === 0 || llmResponseJoined.trim() === "" ? (
            <Shimmer className="my-2">Planning the adventure</Shimmer>
          ) : (
            <ChatMessageBubble
              messageRole="assistant"
              content={llmResponseJoined}
            />
          )}
        </div>
      )}

      {/* Spacer */}
      <div className="flex-1 min-h-32" />

      <div ref={scrollBottomRef} />

      <div className="sticky bottom-0 flex flex-col pointer-events-none">
        <ScrollUntilElement
          targetRef={scrollBottomRef}
          className="self-center mb-4 rounded-full opacity-70 bg-accent text-accent-foreground pointer-events-auto"
        />
        <div className="pb-4 lg:pb-8 bg-background pointer-events-auto">
          <Composer
            placeholder={
              isGeneratingMessage
                ? "Planning the story..."
                : "What will you do?"
            }
            state={isGeneratingMessage ? "streaming" : "ready"}
            onSubmit={onSubmit}
            handleAbort={handleAbort}
            text={composeText}
            setText={setComposeText}
          />
        </div>
      </div>
    </div>
  );
};
