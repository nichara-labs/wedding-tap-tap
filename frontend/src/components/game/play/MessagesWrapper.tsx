import { ErrorItem } from "@/components/common/ErrorItem";
import { Skeleton } from "@/components/ui/skeleton";
import { api } from "@/lib/client";
import type { components } from "@/types/schema";
import { Messages } from "./Messages";

export const MessagesWrapper = ({
  chat,
}: {
  chat: components["schemas"]["ChatModel"];
}) => {
  const {
    data: messages,
    isPending: messagesIsPending,
    isFetching: messagesIsFetching,
    error: messagesError,
    refetch: refetchMessages,
  } = api.useQuery("get", "/v1/chats/{chat_id}/messages", {
    params: { path: { chat_id: chat.id } },
  });

  if (messagesIsPending)
    return (
      <div className="space-y-4">
        <Skeleton className="h-16 w-3/4 rounded-2xl" />
        <Skeleton className="ml-auto h-16 w-2/3 rounded-2xl" />
        <Skeleton className="h-20 w-4/5 rounded-2xl" />
      </div>
    );

  if (messagesError)
    return (
      <div className="h-full w-full flex items-center justify-center px-4">
        <ErrorItem
          message="Failed to load messages"
          isFetching={messagesIsFetching}
          refetch={refetchMessages}
        />
      </div>
    );
  return (
    <Messages
      // Force remount when switching chats (e.g. clear Composer)
      key={chat.id}
      chat={chat}
      messages={messages}
    />
  );
};
