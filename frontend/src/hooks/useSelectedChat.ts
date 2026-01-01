import { useSearchParams } from "next/navigation";
import { CHAT_PARAM } from "@/lib/constants";

export const useSelectedChat = () => {
  const searchParams = useSearchParams();
  const chatId = searchParams.get(CHAT_PARAM);
  return chatId;
};
