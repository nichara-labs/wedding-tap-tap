import { Suspense } from "react";
import { ChatView } from "@/components/game/play/ChatView";

export default function PlayPage() {
  return (
    <Suspense>
      <ChatView />
    </Suspense>
  );
}
