"use client";
import { useQueryClient } from "@tanstack/react-query";
import { Pencil } from "lucide-react";
import Link from "next/link";
import { useRouter } from "next/navigation";
import { useEffect } from "react";
import { toast } from "sonner";
import { ErrorItem } from "@/components/common/ErrorItem";
import { Button } from "@/components/ui/button";
import {
  Card,
  CardAction,
  CardContent,
  CardDescription,
  CardHeader,
  CardTitle,
} from "@/components/ui/card";
import { Spinner } from "@/components/ui/spinner";
import { useUserData } from "@/hooks/useUserData";
import { api } from "@/lib/client";
import { CHAT_PARAM, GOOGLE_AUTH_PATH, STORY_PARAM } from "@/lib/constants";
import { useStore } from "@/lib/store";
import { cn, formatTimestamp } from "@/lib/utils";
import type { components } from "@/types/schema";

export default function GamePage() {
  const setHeaderText = useStore((s) => s.setHeaderText);

  const {
    data: stories,
    isPending: storiesIsPending,
    error: storiesError,
    isFetching,
    refetch,
  } = api.useQuery("get", "/v1/stories");

  useEffect(() => setHeaderText("Browse Stories"), [setHeaderText]);

  if (storiesIsPending)
    return (
      <div className="flex items-center justify-center w-full h-full">
        <Spinner className="size-auto" />
      </div>
    );

  if (storiesError)
    return (
      <div className="flex items-center justify-center w-full h-full center">
        <ErrorItem
          message="Error loading stories"
          isFetching={isFetching}
          refetch={refetch}
        />
      </div>
    );

  return <Content stories={stories} />;
}

interface Props {
  stories: components["schemas"]["StoryModel"][];
}

const Content = ({ stories }: Props) => {
  const client = useQueryClient();
  const router = useRouter();
  const user = useUserData();

  const { mutate: createChat, isPending: createChatIsPending } =
    api.useMutation("post", "/v1/chats", {
      onSuccess: async (chat) => {
        client.invalidateQueries({
          queryKey: api.queryOptions("get", "/v1/chats").queryKey,
        });
        router.push(`/game/play?${CHAT_PARAM}=${chat.id}`);
      },
      onError: () => toast.error("Failed to create chat"),
    });

  const handleStoryClick = (storyId: string) => {
    if (user.data) {
      createChat({ body: { story_id: storyId } });
    } else {
      window.location.href = GOOGLE_AUTH_PATH;
    }
  };

  return (
    <div>
      <div className="grid justify-center grid-cols-[repeat(auto-fit,minmax(200px,400px))] gap-4">
        {user.data && (
          <Button asChild>
            <Link href="/game/create">Write Your Own</Link>
          </Button>
        )}
        {stories.map((story) => (
          <Card
            key={story.id}
            className="items-stretch cursor-pointer hover:bg-accent"
            onClick={() => handleStoryClick(story.id)}
          >
            <CardHeader>
              <CardTitle className="truncate">
                {story.title}
                <Spinner
                  className={cn(
                    "inline-block ml-2",
                    !createChatIsPending && "hidden",
                  )}
                />
              </CardTitle>
              <CardDescription>
                Created on {formatTimestamp(story.created_at)} by{" "}
                {story.is_self ? (
                  <span className="font-bold">You</span>
                ) : (
                  (story.user_name ?? (
                    <span className="italic">deleted user</span>
                  ))
                )}
              </CardDescription>
              {story.is_self && (
                <CardAction>
                  <Button
                    onClick={(e) => {
                      e.stopPropagation();
                      router.push(`/game/create?${STORY_PARAM}=${story.id}`);
                    }}
                    variant={"outline"}
                    size="icon"
                  >
                    <Pencil />
                  </Button>
                </CardAction>
              )}
            </CardHeader>
            <CardContent className="line-clamp-2">
              {story.description}
            </CardContent>
          </Card>
        ))}
      </div>
    </div>
  );
};
