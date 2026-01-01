import type { PropsWithChildren } from "react";
import { ErrorItem } from "@/components/common/ErrorItem";
import {
  Dialog,
  DialogContent,
  DialogDescription,
  DialogHeader,
  DialogTitle,
  DialogTrigger,
} from "@/components/ui/dialog";
import { Skeleton } from "@/components/ui/skeleton";
import { api } from "@/lib/client";
import { StoryCreatedBy } from "../../common/StoryCreatedBy";

export const StoryInfoDialog = ({
  storyId,
  children,
}: {
  storyId: string;
} & PropsWithChildren) => {
  return (
    <Dialog>
      <DialogTrigger>{children}</DialogTrigger>
      <Content storyId={storyId} />
    </Dialog>
  );
};

const Content = ({ storyId }: { storyId: string }) => {
  const story = api.useQuery("get", "/v1/stories/{story_id}", {
    params: { path: { story_id: storyId } },
  });

  if (story.isPending)
    return (
      <DialogContent>
        <DialogHeader>
          <DialogTitle className="sr-only">Loading...</DialogTitle>
          <Skeleton className="h-4 w-1/2" />
          <Skeleton className="h-20 w-full" />
        </DialogHeader>
      </DialogContent>
    );
  if (story.isError)
    return (
      <DialogContent>
        <DialogHeader>
          <DialogTitle>Error</DialogTitle>
          <ErrorItem
            message="Failed to load story info"
            refetch={story.refetch}
            isFetching={story.isFetching}
          />
        </DialogHeader>
      </DialogContent>
    );
  return (
    <DialogContent>
      <DialogHeader>
        <DialogTitle>{story.data.title}</DialogTitle>
        <DialogDescription className="text-start">
          {story.data.description}
        </DialogDescription>

        <StoryCreatedBy story={story.data} className="text-end" />
      </DialogHeader>
    </DialogContent>
  );
};
