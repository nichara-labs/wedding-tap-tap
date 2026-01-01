import { useQueryClient } from "@tanstack/react-query";
import { Sparkles } from "lucide-react";
import { toast } from "sonner";
import { ErrorItem } from "@/components/common/ErrorItem";
import {
  SidebarMenu,
  SidebarMenuButton,
  SidebarMenuItem,
  SidebarMenuSkeleton,
  useSidebar,
} from "@/components/ui/sidebar";
import { useUserData } from "@/hooks/useUserData";
import { api } from "@/lib/client";

export const ClaimDailyLorestones = () => {
  return (
    <SidebarMenu>
      <SidebarMenuItem>
        <Content />
      </SidebarMenuItem>
    </SidebarMenu>
  );
};

const Content = () => {
  const { data: userData } = useUserData();
  const { open } = useSidebar();
  const client = useQueryClient();
  const claim = api.useMutation("post", "/v1/lorestones/daily", {
    onSuccess: () => {
      client.invalidateQueries({
        queryKey: api.queryOptions("get", "/v1/lorestones").queryKey,
      });
      client.invalidateQueries({
        queryKey: api.queryOptions("get", "/v1/lorestones/daily").queryKey,
      });
    },
    onError: () => toast.error("Failed to claim lorestones"),
  });
  const dailyLorestones = api.useQuery(
    "get",
    "/v1/lorestones/daily",
    {},
    { enabled: !!userData },
  );

  if (!userData) return;

  if (dailyLorestones.isPending) return <SidebarMenuSkeleton />;

  if (dailyLorestones.error)
    return (
      <ErrorItem
        message="Error loading lorestone balance"
        isFetching={dailyLorestones.isFetching}
        refetch={dailyLorestones.refetch}
      />
    );

  if (dailyLorestones.data.claimed) {
    return open ? (
      <span className="p-2 text-sm opacity-50">Daily lorestones claimed</span>
    ) : null;
  }

  return (
    <SidebarMenuButton
      onClick={() => claim.mutate({})}
      tooltip="Claim your free daily 100 Lorestones"
      className="bg-primary text-primary-foreground"
    >
      <Sparkles />
      Claim 100 Lorestones
    </SidebarMenuButton>
  );
};
