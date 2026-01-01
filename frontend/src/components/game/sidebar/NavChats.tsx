"use client";

import { useQueryClient } from "@tanstack/react-query";
import { useRouter } from "next/navigation";
import { toast } from "sonner";
import {
  SidebarGroup,
  SidebarGroupLabel,
  SidebarMenu,
  SidebarMenuItem,
  SidebarMenuSkeleton,
} from "@/components/ui/sidebar";
import { useSelectedChat } from "@/hooks/useSelectedChat";
import { useUserData } from "@/hooks/useUserData";
import { api } from "@/lib/client";
import { NavChatItem } from "./NavChatItem";

export const NavChats = () => {
  const { data: userData } = useUserData();
  const isLoggedIn = !!userData;
  return (
    <SidebarGroup className="group-data-[collapsible=icon]:hidden">
      {isLoggedIn && (
        <>
          <SidebarGroupLabel>Chats</SidebarGroupLabel>
          <SidebarMenu>
            <Content />
          </SidebarMenu>
        </>
      )}
    </SidebarGroup>
  );
};

const Content = () => {
  const selectedChatId = useSelectedChat();
  const router = useRouter();
  const {
    data: chats,
    isPending: chatsIsPending,
    isError: chatsIsError,
  } = api.useQuery("get", "/v1/chats");
  const client = useQueryClient();
  const { mutate: deleteChat } = api.useMutation(
    "delete",
    "/v1/chats/{chat_id}",
    {
      onSuccess: async () => {
        client.invalidateQueries({
          queryKey: api.queryOptions("get", "/v1/chats").queryKey,
        });
        router.replace("/game");
      },
      onError: async () => toast("Failed to delete chat"),
    },
  );

  if (chatsIsPending) {
    return Array.from(Array(10).keys()).map((i) => (
      <SidebarMenuSkeleton key={i} showIcon />
    ));
  }

  if (chatsIsError) {
    return <SidebarMenuItem>Error loading chats.</SidebarMenuItem>;
  }

  if (chats.length === 0) {
    return (
      <SidebarMenuItem>No chats yet. Start a new adventure!</SidebarMenuItem>
    );
  }
  return chats.map((chat) => (
    <NavChatItem
      chat={chat}
      deleteChat={() => deleteChat({ params: { path: { chat_id: chat.id } } })}
      selected={selectedChatId === chat.id}
      key={chat.id}
    />
  ));
};
