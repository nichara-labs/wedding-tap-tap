import { useQueryClient } from "@tanstack/react-query";
import { toast } from "sonner";
import { api } from "@/lib/client";

export const useGenerateChatTitle = (chatId: string) => {
  const client = useQueryClient();
  return api.useMutation("post", "/v1/generate/title", {
    onSuccess: async () => {
      client.invalidateQueries({
        queryKey: api.queryOptions("get", "/v1/chats").queryKey,
      });
      client.invalidateQueries({
        queryKey: api.queryOptions("get", "/v1/chats/{chat_id}", {
          params: { path: { chat_id: chatId } },
        }).queryKey,
      });
    },
    retry: 3,
    onError: (err) => {
      toast.error(
        typeof err.detail === "string"
          ? err.detail
          : "Failed to generate title",
      );
    },
  });
};
