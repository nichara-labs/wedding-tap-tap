import { AlertCircleIcon } from "lucide-react";
import { Skeleton } from "@/components/ui/skeleton";
import { api } from "@/lib/client";

export const LorestoneBalance = () => {
  const { data, isPending, error } = api.useQuery("get", "/v1/lorestones");

  if (isPending) {
    return <Skeleton className="h-4 w-full" />;
  }

  if (error) {
    return (
      <div className="flex items-center text-xs text-destructive">
        <AlertCircleIcon className="mr-1 h-[1em] w-[1em] shrink-0" />
        <span className="truncate">Error fetching balance</span>
      </div>
    );
  }

  return (
    <div className="truncate text-xs text-sidebar-foreground/70">
      Lorestones: {data.balance}
    </div>
  );
};
