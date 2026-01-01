import { useQueryClient } from "@tanstack/react-query";
import { Ellipsis, Pencil, Share2, Trash } from "lucide-react";
import Link from "next/link";
import type React from "react";
import { useEffect, useRef, useState } from "react";
import { toast } from "sonner";
import { Button } from "@/components/ui/button";
import {
  Dialog,
  DialogClose,
  DialogContent,
  DialogDescription,
  DialogFooter,
  DialogHeader,
  DialogTitle,
  DialogTrigger,
} from "@/components/ui/dialog";
import {
  DropdownMenu,
  DropdownMenuContent,
  DropdownMenuItem,
  DropdownMenuSeparator,
  DropdownMenuTrigger,
} from "@/components/ui/dropdown-menu";
import { Input } from "@/components/ui/input";
import {
  SidebarMenuAction,
  SidebarMenuButton,
  SidebarMenuItem,
  useSidebar,
} from "@/components/ui/sidebar";
import { Spinner } from "@/components/ui/spinner";
import { api } from "@/lib/client";
import { CHAT_PARAM } from "@/lib/constants";
import { cn } from "@/lib/utils";
import type { components } from "@/types/schema";

interface Props {
  chat: components["schemas"]["ChatWithStoryModel"];
  selected: boolean;
  deleteChat: () => unknown;
}

export const NavChatItem = ({ chat, deleteChat, selected }: Props) => {
  const { isMobile, setOpenMobile } = useSidebar();
  const client = useQueryClient();
  const inputRef = useRef<HTMLInputElement>(null);
  const [renameValue, setRenameValue] = useState<string>("");
  const [renaming, setIsRenaming] = useState(false);

  const { mutate: renameChat, isPending } = api.useMutation(
    "put",
    "/v1/chats/{chat_id}",
    {
      onSuccess: async () => {
        setIsRenaming(false);
        return Promise.all([
          client.invalidateQueries({
            queryKey: api.queryOptions("get", "/v1/chats/{chat_id}", {
              params: { path: { chat_id: chat.id } },
            }).queryKey,
          }),

          // Wait until the invalidated query has been fetched to avoid a flash of the old title
          client.invalidateQueries({
            queryKey: api.queryOptions("get", "/v1/chats").queryKey,
          }),
        ]);
      },
      onError: async () => toast.error("Failed to rename chat"),
    },
  );

  const onChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    setRenameValue(e.target.value);
  };

  const handleStartRename = () => {
    setRenameValue(chat.title || "");
    setIsRenaming(true);
  };

  const handleRename = () => {
    if (!inputRef.current) return;
    if (renameValue !== chat.title) {
      renameChat({
        body: { title: renameValue },
        params: { path: { chat_id: chat.id } },
      });
    }
    setIsRenaming(false);
  };

  const handleInputKeyDown = (e: React.KeyboardEvent<HTMLInputElement>) => {
    if (e.key === "Enter") {
      e.preventDefault();
      handleRename();
    }
    if (e.key === "Escape") setIsRenaming(false);
  };

  // Focus the rename input when it becomes visible.
  useEffect(() => {
    if (renaming && inputRef.current) {
      inputRef.current.focus();
      inputRef.current.select();
    }
  }, [renaming]);

  return (
    <SidebarMenuItem>
      <SidebarMenuButton
        className={cn(
          "hover:bg-sidebar-accent",
          selected && "bg-sidebar-accent/70 font-bold",
        )}
        asChild
      >
        {renaming ? (
          <Input
            ref={inputRef}
            value={renameValue}
            onBlur={handleRename}
            onKeyDown={handleInputKeyDown}
            disabled={isPending}
            onChange={onChange}
          />
        ) : isPending ? (
          <div className="opacity-50 flex items-center">
            <Spinner />
            <div className="truncate">{renameValue}</div>
          </div>
        ) : (
          <Link
            href={`/game/play?${CHAT_PARAM}=${chat.id}`}
            onClick={() => setOpenMobile(false)}
            title={chat.title ?? undefined}
          >
            <div className="truncate">{chat.title ?? chat.story_title}</div>
          </Link>
        )}
      </SidebarMenuButton>

      <Dialog>
        {!renaming && (
          <DropdownMenu>
            <DropdownMenuTrigger asChild>
              <SidebarMenuAction
                showOnHover
                className="data-[state=open]:bg-accent rounded-sm"
              >
                <Ellipsis />
                <span className="sr-only">More</span>
              </SidebarMenuAction>
            </DropdownMenuTrigger>
            <DropdownMenuContent
              className="w-24 rounded-lg"
              side={isMobile ? "bottom" : "right"}
              align={isMobile ? "end" : "start"}
            >
              <DropdownMenuItem>
                <Share2 />
                <span>Share</span>
              </DropdownMenuItem>
              <DropdownMenuItem onClick={handleStartRename}>
                <Pencil />
                <span>Rename</span>
              </DropdownMenuItem>
              <DropdownMenuSeparator />
              <DialogTrigger asChild>
                <DropdownMenuItem variant="destructive">
                  <Trash />
                  <span>Delete</span>
                </DropdownMenuItem>
              </DialogTrigger>
            </DropdownMenuContent>
          </DropdownMenu>
        )}

        <DialogContent>
          <DialogHeader>
            <DialogTitle>Delete chat?</DialogTitle>
            <DialogDescription>
              This will delete{" "}
              <span className="font-bold">{chat.title ?? "Untitled Chat"}</span>
              .
            </DialogDescription>
          </DialogHeader>
          <DialogFooter>
            <DialogClose asChild>
              <Button variant={"secondary"}>Close</Button>
            </DialogClose>
            <DialogClose asChild>
              <Button onClick={deleteChat} variant="destructive">
                Delete
              </Button>
            </DialogClose>
          </DialogFooter>
        </DialogContent>
      </Dialog>
    </SidebarMenuItem>
  );
};
