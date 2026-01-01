import { sendGTMEvent } from "@next/third-parties/google";
import { api } from "@/lib/client";

export const useSubscribe = () => {
  const mutation = api.useMutation("post", "/v1/stripe/checkout", {
    onSuccess: (data: { session_id: string; url: string }) => {
      sendGTMEvent({ event: "clicked_checkout" });
      window.location.href = data.url;
    },
  });
  return () => mutation.mutate({});
};
