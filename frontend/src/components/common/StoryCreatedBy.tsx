import { cn, formatTimestamp } from "@/lib/utils";
import type { components } from "@/types/schema";
export const StoryCreatedBy = ({
  story,
  className,
}: {
  story: components["schemas"]["StoryModel"];
  className?: string;
}) => {
  return (
    <p className={cn("opacity-50", className)}>
      Created on {formatTimestamp(story.created_at)} by{" "}
      {story.is_self ? (
        <span className="font-bold">You</span>
      ) : (
        (story.user_name ?? <span className="italic">deleted user</span>)
      )}
    </p>
  );
};
