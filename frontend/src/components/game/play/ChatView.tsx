"use client";
import { Info } from "lucide-react";
import { useRouter } from "next/navigation";
import { useEffect } from "react";
import { toast } from "sonner";
import { ErrorItem } from "@/components/common/ErrorItem";
import { HeaderTitle } from "@/components/common/HeaderTitle";
import { Button } from "@/components/ui/button";
import { Spinner } from "@/components/ui/spinner";
import { useSelectedChat } from "@/hooks/useSelectedChat";
import { api } from "@/lib/client";
import { useStore } from "@/lib/store";
import { MessagesWrapper } from "./MessagesWrapper";
import { StoryInfoDialog } from "./StoryInfoDialog";

interface Props {
  chatId: string;
}

export const ChatView = () => {
  const chatId = useSelectedChat();
  const router = useRouter();

  useEffect(() => {
    if (!chatId) {
      const timeout = setTimeout(() => toast.error("No chat selected"));
      router.replace("/game");
      return () => clearTimeout(timeout);
    }
  }, [chatId, router]);

  if (!chatId) {
    return;
  }

  return <Content chatId={chatId} />;
};

const Content = ({ chatId }: Props) => {
  const {
    data: chat,
    isPending: chatIsPending,
    isFetching: chatIsFetching,
    error: chatError,
    refetch: refetchChat,
  } = api.useQuery("get", "/v1/chats/{chat_id}", {
    params: { path: { chat_id: chatId } },
  });

  const setHeader = useStore((s) => s.setHeader);
  const setHeaderText = useStore((s) => s.setHeaderText);

  // Update header
  useEffect(() => {
    if (chatIsPending)
      setHeader(
        <>
          <HeaderTitle>Loading</HeaderTitle>
          <Spinner />
        </>,
      );
    else if (chatError) setHeaderText("Error");
    else {
      setHeader(
        <>
          <HeaderTitle>{chat.title ?? chat.story_title}</HeaderTitle>
          <StoryInfoDialog storyId={chat.story_id}>
            <Button variant="ghost" size="icon" className="opacity-50" asChild>
              <div>
                <Info />
              </div>
            </Button>
          </StoryInfoDialog>
        </>,
      );
    }
  }, [chat, chatIsPending, chatError, setHeaderText, setHeader]);

  if (chatIsPending)
    return (
      <div className="flex items-center justify-center w-full h-full">
        <Spinner className="size-auto" />
      </div>
    );

  if (chatError)
    return (
      <div className="flex items-center justify-center w-full h-full">
        {"status_code" in chatError && chatError.status_code === 404 ? (
          <ErrorItem message="Chat not found" />
        ) : (
          <ErrorItem
            message="Failed to load chat"
            isFetching={chatIsFetching}
            refetch={refetchChat}
          />
        )}
      </div>
    );

  return <MessagesWrapper chat={chat} />;
};
